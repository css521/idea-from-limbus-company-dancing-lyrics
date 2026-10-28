"""Global and application hotkey manager for Desktop Lyrics.

Supports system-wide global hotkeys on:
- macOS via Carbon RegisterEventHotKey (no accessibility permissions required)
- Windows via RegisterHotKey + QAbstractNativeEventFilter
- In-app fallback via QShortcut with ApplicationShortcut context
"""
import ctypes
import logging
import sys
from PySide6.QtCore import QAbstractNativeEventFilter, QCoreApplication, QObject, Qt, Signal
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QWidget

logger = logging.getLogger(__name__)

MAC_KEY_CODES = {
    'A': 0, 'S': 1, 'D': 2, 'F': 3, 'H': 4, 'G': 5, 'Z': 6, 'X': 7,
    'C': 8, 'V': 9, 'B': 11, 'Q': 12, 'W': 13, 'E': 14, 'R': 15,
    'Y': 16, 'T': 17, '1': 18, '2': 19, '3': 20, '4': 21, '6': 22,
    '5': 23, '=': 24, '9': 25, '7': 26, '-': 27, '8': 28, '0': 29,
    ']': 30, 'O': 31, 'U': 32, '[': 33, 'I': 34, 'P': 35, 'L': 37,
    'J': 38, '\'': 39, 'K': 40, ';': 41, '\\': 42, ',': 43, '/': 44,
    'N': 45, 'M': 46, '.': 47, '`': 50,
    'SPACE': 49, 'RETURN': 36, 'TAB': 48, 'ESCAPE': 53,
    'UP': 126, 'DOWN': 125, 'LEFT': 123, 'RIGHT': 124,
    'F1': 122, 'F2': 120, 'F3': 99, 'F4': 118, 'F5': 96, 'F6': 97,
    'F7': 98, 'F8': 100, 'F9': 101, 'F10': 109, 'F11': 103, 'F12': 111,
}

CARBON_MOD_CMD = 0x0100     # 256
CARBON_MOD_SHIFT = 0x0200   # 512
CARBON_MOD_OPT = 0x0800     # 2048
CARBON_MOD_CONTROL = 0x1000 # 4096

WIN_MOD_ALT = 0x0001
WIN_MOD_CONTROL = 0x0002
WIN_MOD_SHIFT = 0x0004
WIN_MOD_WIN = 0x0008
WIN_MOD_NOREPEAT = 0x4000

class EventHotKeyID(ctypes.Structure):
    _fields_ = [('signature', ctypes.c_uint32), ('id', ctypes.c_uint32)]


class EventTypeSpec(ctypes.Structure):
    _fields_ = [('eventClass', ctypes.c_uint32), ('eventKind', ctypes.c_uint32)]


EventHandlerProc = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)

try:
    from ctypes import wintypes
except Exception:  # pragma: no cover
    wintypes = None

if wintypes is not None:
    class MSG(ctypes.Structure):
        _fields_ = [
            ("hwnd", wintypes.HWND),
            ("message", wintypes.UINT),
            ("wParam", wintypes.WPARAM),
            ("lParam", wintypes.LPARAM),
            ("time", wintypes.DWORD),
            ("pt", wintypes.POINT),
        ]
else:  # pragma: no cover
    MSG = None


class _WinNativeHotKeyFilter(QAbstractNativeEventFilter):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner

    def nativeEventFilter(self, eventType, message):
        if eventType in (b"windows_generic_MSG", b"windows_dispatcher_MSG"):
            try:
                msg = MSG.from_address(int(message))
                if msg.message == 0x0312:  # WM_HOTKEY
                    hid = int(msg.wParam)
                    if any(registered_id == hid for _, registered_id in self.owner._win_hotkey_ids):
                        self.owner.activated.emit()
                        return True, 0
            except Exception as error:
                logger.debug("WinNativeHotKeyFilter error: %s", error)
        return False, 0


class GlobalHotKey(QObject):
    activated = Signal()

    def __init__(self, parent=None, callback=None):
        super().__init__(parent)
        if callback:
            self.activated.connect(callback)
        self._parent_widget = parent if isinstance(parent, QWidget) else None
        self._shortcuts = []
        self._hotkey_id_counter = 1000

        # Mac Carbon state
        self._mac_carbon = None
        self._mac_handler_ref = None
        self._mac_c_callback = None
        self._mac_hotkey_refs = []

        # Windows state
        self._win_user32 = None
        self._win_event_filter = None
        self._win_hotkey_ids = set()

        self._closed = False
        self._init_backend()

    def _init_backend(self):
        if sys.platform == "darwin":
            try:
                carbon = ctypes.CDLL("/System/Library/Frameworks/Carbon.framework/Carbon")
                carbon.GetEventDispatcherTarget.restype = ctypes.c_void_p
                carbon.GetEventDispatcherTarget.argtypes = []
                carbon.InstallEventHandler.restype = ctypes.c_int32
                carbon.InstallEventHandler.argtypes = [
                    ctypes.c_void_p,
                    EventHandlerProc,
                    ctypes.c_uint32,
                    ctypes.POINTER(EventTypeSpec),
                    ctypes.c_void_p,
                    ctypes.POINTER(ctypes.c_void_p)
                ]
                carbon.RegisterEventHotKey.restype = ctypes.c_int32
                carbon.RegisterEventHotKey.argtypes = [
                    ctypes.c_uint32,
                    ctypes.c_uint32,
                    EventHotKeyID,
                    ctypes.c_void_p,
                    ctypes.c_uint32,
                    ctypes.POINTER(ctypes.c_void_p)
                ]
                carbon.UnregisterEventHotKey.restype = ctypes.c_int32
                carbon.UnregisterEventHotKey.argtypes = [ctypes.c_void_p]
                carbon.RemoveEventHandler.restype = ctypes.c_int32
                carbon.RemoveEventHandler.argtypes = [ctypes.c_void_p]

                target = carbon.GetEventDispatcherTarget()
                if not target:
                    logger.debug("Carbon GetEventDispatcherTarget returned NULL")
                    return

                def _carbon_cb(handler_call_ref, event_ref, user_data):
                    self.activated.emit()
                    return 0

                self._mac_c_callback = EventHandlerProc(_carbon_cb)
                spec = EventTypeSpec(0x6b657962, 5)  # 'keyb', kEventHotKeyPressed = 5
                handler_ref = ctypes.c_void_p()
                err = carbon.InstallEventHandler(
                    target, self._mac_c_callback, 1, ctypes.byref(spec), None, ctypes.byref(handler_ref)
                )
                if err == 0:
                    self._mac_carbon = carbon
                    self._mac_handler_ref = handler_ref
                else:
                    logger.debug("InstallEventHandler failed with code %d", err)
            except Exception as error:
                logger.debug("Failed to initialize Carbon hotkey backend: %s", error)

        elif sys.platform == "win32":
            try:
                windll = getattr(ctypes, "windll", None)
                if not windll:
                    return
                user32 = windll.user32
                user32.RegisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int, wintypes.UINT, wintypes.UINT]
                user32.RegisterHotKey.restype = wintypes.BOOL
                user32.UnregisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int]
                user32.UnregisterHotKey.restype = wintypes.BOOL
                self._win_user32 = user32

                app = QCoreApplication.instance()
                if app:
                    self._win_event_filter = _WinNativeHotKeyFilter(self)
                    app.installNativeEventFilter(self._win_event_filter)
            except Exception as error:
                logger.debug("Failed to initialize Windows hotkey backend: %s", error)

    def register(self, sequence_str: str) -> bool:
        if self._closed:
            return False

        # In-app QShortcut fallback
        if self._parent_widget is not None:
            try:
                shortcut = QShortcut(QKeySequence(sequence_str), self._parent_widget)
                shortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)
                shortcut.activated.connect(self.activated.emit)
                self._shortcuts.append(shortcut)
            except Exception as error:
                logger.debug("QShortcut registration failed for %s: %s", sequence_str, error)

        # OS-level Global HotKey
        if sys.platform == "darwin" and self._mac_carbon is not None and self._mac_handler_ref is not None:
            try:
                return self._register_mac_carbon(sequence_str)
            except Exception as error:
                logger.debug("Mac global hotkey registration failed for %s: %s", sequence_str, error)

        elif sys.platform == "win32" and self._win_user32 is not None:
            try:
                return self._register_win(sequence_str)
            except Exception as error:
                logger.debug("Windows global hotkey registration failed for %s: %s", sequence_str, error)

        return True

    def _register_mac_carbon(self, sequence_str: str) -> bool:
        parts = [p.strip() for p in sequence_str.split('+')]
        mods = 0
        key_char = None
        for p in parts:
            lower = p.lower()
            if lower in ('ctrl', 'control', 'cmd', 'command', 'meta'):
                mods |= CARBON_MOD_CMD
            elif lower in ('alt', 'opt', 'option'):
                mods |= CARBON_MOD_OPT
            elif lower == 'shift':
                mods |= CARBON_MOD_SHIFT
            else:
                key_char = p.upper()

        if not key_char or key_char not in MAC_KEY_CODES:
            logger.debug("Unsupported key for Mac Carbon: %s", key_char)
            return False

        key_code = MAC_KEY_CODES[key_char]
        self._hotkey_id_counter += 1
        hotkey_id = EventHotKeyID(0x43454348, self._hotkey_id_counter)  # 'CECH'
        target = self._mac_carbon.GetEventDispatcherTarget()
        ref = ctypes.c_void_p()
        err = self._mac_carbon.RegisterEventHotKey(
            key_code, mods, hotkey_id, target, 0, ctypes.byref(ref)
        )
        if err == 0:
            self._mac_hotkey_refs.append(ref)
            return True
        logger.debug("RegisterEventHotKey failed for %s with code %d", sequence_str, err)
        return False

    def _register_win(self, sequence_str: str) -> bool:
        parts = [p.strip() for p in sequence_str.split('+')]
        mods = WIN_MOD_NOREPEAT
        key_char = None
        for p in parts:
            lower = p.lower()
            if lower in ('ctrl', 'control'):
                mods |= WIN_MOD_CONTROL
            elif lower in ('alt', 'opt', 'option'):
                mods |= WIN_MOD_ALT
            elif lower == 'shift':
                mods |= WIN_MOD_SHIFT
            elif lower in ('win', 'meta', 'cmd', 'command'):
                mods |= WIN_MOD_WIN
            else:
                key_char = p.upper()

        if not key_char:
            return False

        vk = ord(key_char[0]) if len(key_char) == 1 else 0
        if not vk:
            return False

        self._hotkey_id_counter += 1
        hid = self._hotkey_id_counter
        hwnd = int(self._parent_widget.winId()) if self._parent_widget else 0
        ok = bool(self._win_user32.RegisterHotKey(hwnd, hid, mods, vk))
        if ok:
            self._win_hotkey_ids.add((hwnd, hid))
            return True
        logger.debug("Win RegisterHotKey failed for %s", sequence_str)
        return False

    def close(self):
        if self._closed:
            return
        self._closed = True

        for sc in self._shortcuts:
            try:
                sc.setEnabled(False)
                sc.deleteLater()
            except Exception:
                pass
        self._shortcuts.clear()

        if sys.platform == "darwin" and self._mac_carbon is not None:
            for ref in self._mac_hotkey_refs:
                try:
                    self._mac_carbon.UnregisterEventHotKey(ref)
                except Exception:
                    pass
            self._mac_hotkey_refs.clear()
            if self._mac_handler_ref is not None:
                try:
                    self._mac_carbon.RemoveEventHandler(self._mac_handler_ref)
                except Exception:
                    pass
                self._mac_handler_ref = None

        elif sys.platform == "win32" and self._win_user32 is not None:
            for hwnd, hid in list(self._win_hotkey_ids):
                try:
                    self._win_user32.UnregisterHotKey(hwnd, hid)
                except Exception:
                    pass
            self._win_hotkey_ids.clear()
            if self._win_event_filter:
                try:
                    app = QCoreApplication.instance()
                    if app:
                        app.removeNativeEventFilter(self._win_event_filter)
                except Exception:
                    pass
                self._win_event_filter = None


def default_visibility_shortcuts():
    return ["Ctrl+Alt+D", "Ctrl+Alt+L"]


def default_shortcut_display():
    return "⌥⌘D / ⌥⌘L" if sys.platform == "darwin" else "Ctrl+Alt+D / Ctrl+Alt+L"


def setup_lyrics_visibility_hotkey(panel, callback=None):
    cb = callback or panel.toggle_overlay
    hotkey = GlobalHotKey(parent=panel, callback=cb)
    for seq in default_visibility_shortcuts():
        hotkey.register(seq)

    hint = default_shortcut_display()
    if hasattr(panel, "visibility_button") and panel.visibility_button:
        panel.visibility_button.setToolTip(f"显示/隐藏桌面歌词（快捷键：{hint}）")
    if hasattr(panel, "tray_visibility") and panel.tray_visibility:
        panel.tray_visibility.setToolTip(f"显示/隐藏桌面歌词（快捷键：{hint}）")

    app = QCoreApplication.instance()
    if app:
        app.aboutToQuit.connect(hotkey.close)
    return hotkey
