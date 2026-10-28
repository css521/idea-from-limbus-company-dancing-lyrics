import sys
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication, QWidget

import hotkey


class HotkeyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_default_shortcuts_and_display(self):
        shortcuts = hotkey.default_visibility_shortcuts()
        self.assertIn("Ctrl+Alt+D", shortcuts)
        self.assertIn("Ctrl+Alt+L", shortcuts)

        with patch("hotkey.sys", SimpleNamespace(platform="darwin")):
            self.assertEqual(hotkey.default_shortcut_display(), "⌥⌘D / ⌥⌘L")

        with patch("hotkey.sys", SimpleNamespace(platform="win32")):
            self.assertEqual(hotkey.default_shortcut_display(), "Ctrl+Alt+D / Ctrl+Alt+L")

    def test_global_hotkey_lifecycle_and_callback(self):
        widget = QWidget()
        calls = []

        hk = hotkey.GlobalHotKey(widget, callback=lambda: calls.append(True))
        try:
            self.assertTrue(hk.register("Ctrl+Alt+D"))
            self.assertTrue(hk.register("Ctrl+Alt+L"))

            # Activating the signal triggers callback
            hk.activated.emit()
            self.assertEqual(len(calls), 1)

            hk.activated.emit()
            self.assertEqual(len(calls), 2)
        finally:
            hk.close()
            self.assertTrue(hk._closed)
            # Repeated close is safe
            hk.close()

    def test_setup_lyrics_visibility_hotkey_binds_panel_and_tooltips(self):
        panel = QWidget()
        button = QWidget(panel)
        tray_action = SimpleNamespace(tooltip="")
        panel.visibility_button = button
        panel.tray_visibility = SimpleNamespace(setToolTip=lambda text: setattr(tray_action, "tooltip", text))

        toggled = []
        panel.toggle_overlay = lambda: toggled.append(True)

        hk = hotkey.setup_lyrics_visibility_hotkey(panel)
        try:
            self.assertIn("快捷键", panel.visibility_button.toolTip())
            self.assertIn("快捷键", tray_action.tooltip)

            hk.activated.emit()
            self.assertEqual(len(toggled), 1)
        finally:
            hk.close()

    def test_mac_carbon_registration_and_cleanup(self):
        with patch("hotkey.sys", SimpleNamespace(platform="darwin")):
            mock_carbon = MagicMock()
            mock_carbon.GetEventDispatcherTarget.return_value = 12345
            mock_carbon.InstallEventHandler.return_value = 0
            mock_carbon.RegisterEventHotKey.return_value = 0
            mock_carbon.UnregisterEventHotKey.return_value = 0
            mock_carbon.RemoveEventHandler.return_value = 0

            with patch("hotkey.ctypes.CDLL", return_value=mock_carbon):
                hk = hotkey.GlobalHotKey()
                try:
                    self.assertIsNotNone(hk._mac_carbon)
                    ok = hk.register("Ctrl+Alt+D")
                    self.assertTrue(ok)
                    self.assertEqual(len(hk._mac_hotkey_refs), 1)
                finally:
                    hk.close()
                    mock_carbon.UnregisterEventHotKey.assert_called()
                    mock_carbon.RemoveEventHandler.assert_called()

    def test_windows_registration_and_cleanup(self):
        with patch("hotkey.sys", SimpleNamespace(platform="win32")):
            mock_user32 = MagicMock()
            mock_user32.RegisterHotKey.return_value = True
            mock_user32.UnregisterHotKey.return_value = True

            with patch.object(hotkey.ctypes, "windll", SimpleNamespace(user32=mock_user32), create=True):
                hk = hotkey.GlobalHotKey()
                try:
                    self.assertIsNotNone(hk._win_user32)
                    ok = hk.register("Ctrl+Alt+D")
                    self.assertTrue(ok)
                    self.assertEqual(len(hk._win_hotkey_ids), 1)
                finally:
                    hk.close()
                    mock_user32.UnregisterHotKey.assert_called()


if __name__ == "__main__":
    unittest.main()
