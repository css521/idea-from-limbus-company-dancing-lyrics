import random
import sys
import time
from PySide6.QtCore import Qt, QTimer, QEvent, QPointF, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QLinearGradient, QFont, QFontMetrics
from PySide6.QtWidgets import QApplication, QWidget
try:
    from PySide6.QtSvg import QSvgRenderer
except ImportError:
    QSvgRenderer = None
from animation import build_layout, display_regions
from lrc import LyricTimeline, LyricDocument, display_document
from settings import Preferences, resource_path
from text_effects import TEXT_EFFECTS
from glyph_motion import glyph_states
from app_info import APP_NAME


class LyricsOverlay(QWidget):
    def __init__(self, player, prefs: Preferences):
        flags = (Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
                 | Qt.WindowType.Tool | Qt.WindowType.WindowTransparentForInput
                 | Qt.WindowType.WindowDoesNotAcceptFocus)
        super().__init__(None, flags)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        if sys.platform == "darwin":
            # Qt's native NSPanel stays visible when another application is active.
            # Keep Tool on Windows: removing it exposes the overlay in the taskbar.
            self.setAttribute(Qt.WidgetAttribute.WA_MacAlwaysShowToolWindow)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setWindowTitle(f"{APP_NAME} · 悬浮层")
        self.player = player
        self.prefs = prefs
        self.document = None
        self.display_document = None
        self.timeline = None
        self.layouts = {}
        self.seed = random.randrange(1_000_000)
        self._screen = None
        self._bind_screen(self._resolve_screen())
        app = QApplication.instance()
        if app:
            app.primaryScreenChanged.connect(self._on_screens_changed)
            app.screenAdded.connect(self._on_screens_changed)
            app.screenRemoved.connect(self._on_screens_changed)
        player.discontinuity.connect(self.clear_layouts)
        self._current_track = ("", "")
        self._pda_start = 0.0
        self._pda_title = ""
        self._pda_artist = ""
        self._dante_svg = None
        if QSvgRenderer is not None:
            svg_path = resource_path("assets/dante-clock.svg")
            if svg_path.is_file():
                try:
                    renderer = QSvgRenderer(str(svg_path))
                    if renderer.isValid():
                        self._dante_svg = renderer
                except Exception:
                    self._dante_svg = None
        self.timer = QTimer(self)
        self.timer.setTimerType(Qt.TimerType.PreciseTimer)
        self.timer.setInterval(33)
        self.timer.timeout.connect(self.update)
        player.changed.connect(self._sync_timer)

    def _resolve_screen(self):
        target = getattr(self.prefs, "target_screen", "").strip()
        app = QApplication.instance()
        if not app:
            return None
        if target:
            for screen in app.screens():
                if screen.name() == target:
                    return screen
        return app.primaryScreen()

    def _on_screens_changed(self, *_):
        self._bind_screen(self._resolve_screen())

    def _bind_screen(self, screen):
        if self._screen:
            try:
                self._screen.availableGeometryChanged.disconnect(self._screen_changed)
            except (RuntimeError, TypeError):
                pass
        self._screen = screen
        if screen:
            screen.availableGeometryChanged.connect(self._screen_changed)
            self._screen_changed()

    def _screen_changed(self, *_):
        if not self._screen:
            return
        handle = self.windowHandle()
        if handle and handle.screen() != self._screen:
            handle.setScreen(self._screen)
        self.setGeometry(self._screen.availableGeometry())
        TEXT_EFFECTS.clear()
        self.clear_layouts()

    def set_document(self, document: LyricDocument | None):
        displayed = display_document(document, self.prefs.prefer_translation)
        same_text = bool(displayed and self.display_document and [(line.start_ms, line.text) for line in displayed.lines]
                         == [(line.start_ms, line.text) for line in self.display_document.lines])
        self.document = document
        self.display_document = displayed
        self.timeline = self._timeline(displayed) if displayed else None
        if not same_text:
            self.seed = random.randrange(1_000_000)
            self.clear_layouts()
        self._sync_timer()

    def refresh_preferences(self):
        self._bind_screen(self._resolve_screen())
        self.display_document = display_document(self.document, self.prefs.prefer_translation)
        if self.document:
            self.timeline = self._timeline(self.display_document)
        self.clear_layouts()

    def _timeline(self, document):
        delay = self.prefs.delay_ms - getattr(self.player, "lyric_offset_ms", 0)
        return LyricTimeline(document, delay, self.prefs.animation_style,
                             self.prefs.entry_speed, self.prefs.exit_speed)

    def clear_layouts(self):
        self.layouts.clear()
        self.update()

    def showEvent(self, event):
        super().showEvent(event)
        self._protect_native_focus()
        self._sync_timer()

    def _get_player_track(self):
        title = getattr(self.player, "title", None)
        artist = getattr(self.player, "artist", None)
        if not title and getattr(self.player, "path", None):
            title = self.player.path.stem
        return (title or "").strip(), (artist or "").strip()

    def _check_track_change(self):
        if not getattr(self.prefs, "pda_banner", True):
            return
        title, artist = self._get_player_track()
        if title and (title, artist) != self._current_track:
            self._current_track = (title, artist)
            self._pda_title = title
            self._pda_artist = artist
            self._pda_start = time.monotonic() if (getattr(self.player, "playing", False) and not getattr(self.player, "ended", False)) else 0.0

    def _is_pda_active(self):
        if not getattr(self.prefs, "pda_banner", True) or not self._pda_title:
            return False
        if not getattr(self.player, "playing", False) or getattr(self.player, "ended", False):
            return False
        if self._pda_start == 0.0:
            return False
        return (time.monotonic() - self._pda_start) < 4.0

    def _sync_timer(self):
        self._check_track_change()
        if getattr(self.player, "playing", False) and not getattr(self.player, "ended", False) and self._pda_title and self._pda_start == 0.0:
            self._pda_start = time.monotonic()
        pda_active = self._is_pda_active()
        music_active = bool(getattr(self.player, "playing", False) and not getattr(self.player, "ended", False))
        has_content = bool(self.timeline or pda_active)
        if self.isVisible() and music_active and has_content:
            if not self.timer.isActive():
                self.timer.start()
        else:
            if self.timer.isActive():
                self.timer.stop()
        self.update()

    def _protect_native_focus(self):
        # Qt handles focus messages, but 6.8 does not add WS_EX_NOACTIVATE itself.
        # Only alter our own HWND, including after it is shown again from the tray.
        if sys.platform != "win32" or QApplication.instance().platformName() != "windows":
            return
        import ctypes
        from ctypes import wintypes
        user32 = ctypes.windll.user32
        user32.GetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int]
        user32.GetWindowLongW.restype = ctypes.c_long
        user32.SetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_long]
        user32.SetWindowLongW.restype = ctypes.c_long
        user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, ctypes.c_int,
                                      ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.UINT]
        user32.SetWindowPos.restype = wintypes.BOOL
        hwnd = int(self.winId())
        style = user32.GetWindowLongW(hwnd, -20)
        user32.SetWindowLongW(hwnd, -20, style | 0x08000000)
        # SWP_NOSIZE | SWP_NOMOVE | SWP_NOZORDER | SWP_NOACTIVATE | SWP_FRAMECHANGED
        user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, 0x37)

    def hideEvent(self, event):
        self.timer.stop()
        super().hideEvent(event)

    def event(self, event):
        if event.type() == QEvent.Type.DevicePixelRatioChange and hasattr(self, "layouts"):
            TEXT_EFFECTS.clear()
            self.clear_layouts()
        return super().event(event)

    def _draw_pda_banner(self, painter: QPainter):
        if not self._is_pda_active():
            return
        elapsed = time.monotonic() - self._pda_start
        if elapsed >= 4.0:
            self._pda_title = ""
            if self.timer.isActive() and not (self.timeline and self.player.playing and not self.player.ended):
                self.timer.stop()
            return

        if elapsed < 0.35:
            t = elapsed / 0.35
            slide = 1.0 - (1.0 - t) ** 3
            alpha = min(1.0, elapsed / 0.25)
        elif elapsed < 3.2:
            slide = 1.0
            alpha = 1.0
        else:
            t = (elapsed - 3.2) / 0.8
            slide = max(0.0, 1.0 - t * t)
            alpha = max(0.0, 1.0 - t)

        if alpha <= 0.0:
            return

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setOpacity(alpha)

        banner_w = 420.0
        banner_h = 68.0
        target_y = 22.0
        current_y = (target_y + banner_h + 10.0) * slide - (banner_h + 10.0)
        center_x = (self.width() - banner_w) / 2.0
        banner_rect = QRectF(center_x, current_y, banner_w, banner_h)

        bg_gradient = QLinearGradient(banner_rect.topLeft(), banner_rect.bottomLeft())
        bg_gradient.setColorAt(0.0, QColor(24, 18, 22, 245))
        bg_gradient.setColorAt(1.0, QColor(12, 10, 14, 248))
        painter.setBrush(bg_gradient)
        border_pen = QPen(QColor(220, 38, 48, 220), 1.5)
        painter.setPen(border_pen)
        painter.drawRoundedRect(banner_rect, 10.0, 10.0)

        gold_pen = QPen(QColor(245, 185, 55, 230), 2.0)
        painter.setPen(gold_pen)
        gold_inset = 40.0
        painter.drawLine(QPointF(banner_rect.left() + gold_inset, banner_rect.top() + 1.0),
                         QPointF(banner_rect.right() - gold_inset, banner_rect.top() + 1.0))

        icon_size = 46.0
        icon_rect = QRectF(banner_rect.left() + 12.0, banner_rect.top() + 11.0, icon_size, icon_size)
        painter.setPen(QPen(QColor(180, 25, 35, 140), 1.0))
        painter.setBrush(QColor(32, 10, 14, 220))
        painter.drawEllipse(icon_rect)
        if self._dante_svg:
            self._dante_svg.render(painter, icon_rect)
        else:
            painter.setPen(QPen(QColor(245, 185, 55), 1.5))
            painter.drawText(icon_rect, Qt.AlignmentFlag.AlignCenter, "XII")

        text_x = banner_rect.left() + 68.0
        text_w = banner_w - 78.0

        tag_font = QFont("Arial", 8)
        tag_font.setBold(True)
        tag_font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 1.2)
        painter.setFont(tag_font)
        painter.setPen(QColor(235, 65, 75, 235))
        painter.drawText(QRectF(text_x, banner_rect.top() + 10.0, text_w, 14.0),
                         Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                         "LCB // DANTE PDA · NOW PLAYING")

        title_font = QFont("Helvetica Neue", 12)
        title_font.setBold(True)
        painter.setFont(title_font)
        painter.setPen(QColor(255, 255, 255, 255))
        metrics_title = QFontMetrics(title_font)
        elided_title = metrics_title.elidedText(self._pda_title, Qt.TextElideMode.ElideRight, int(text_w))
        painter.drawText(QRectF(text_x, banner_rect.top() + 26.0, text_w, 20.0),
                         Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                         elided_title)

        artist_text = self._pda_artist if self._pda_artist else "Limbus Company"
        artist_font = QFont("Helvetica Neue", 9)
        painter.setFont(artist_font)
        painter.setPen(QColor(240, 185, 95, 220))
        metrics_artist = QFontMetrics(artist_font)
        elided_artist = metrics_artist.elidedText(artist_text, Qt.TextElideMode.ElideRight, int(text_w))
        painter.drawText(QRectF(text_x, banner_rect.top() + 47.0, text_w, 15.0),
                         Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                         elided_artist)

        painter.restore()

    def paintEvent(self, _event):
        painter = QPainter(self)
        # Explicitly erase the previous frame in the alpha surface.
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
        painter.fillRect(self.rect(), Qt.GlobalColor.transparent)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        if not self.timeline or self.player.ended:
            if self._is_pda_active():
                self._draw_pda_banner(painter)
            return
        position = self.player.position()
        active = self.timeline.visible(position, self.player.duration)
        wanted = {item.index for item in active}
        self.layouts = {key: value for key, value in self.layouts.items() if key in wanted}
        regions = display_regions(self.width(), self.height(), self.prefs.region)
        for item in active:
            if item.index in self.layouts:
                continue
            occupied = [layout.bounds for layout in self.layouts.values()]
            layout = build_layout(item.text, self.seed + item.index * 7919, regions, occupied, self.prefs)
            if layout:
                self.layouts[item.index] = layout
        energy = self.player.energy_at(position)
        if self.prefs.motion == "wave":
            energy = 0.32
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        seconds = position / 1000.0
        for item in active:
            layout = self.layouts.get(item.index)
            if not layout:
                continue
            # A constrained screen may only have room for the newer sentence.
            if any(layout.bounds.intersects(self.layouts[new.index].bounds)
                   for new in active if new.index > item.index and new.index in self.layouts):
                continue
            age = position - item.start_ms
            remaining = item.end_ms - position
            drift = (8 * (1 - min(1, remaining / (600 * 100 / self.prefs.exit_speed)))
                     - 5 * (1 - min(1, age / (300 * 100 / self.prefs.entry_speed))))
            if self.prefs.animation_style != "classic":
                drift = 0
            painter.save()
            painter.setOpacity(item.opacity * self.prefs.opacity / 100)
            painter.translate(layout.center)
            painter.rotate(layout.angle)
            painter.translate(0, drift)
            if layout.surface is None:
                layout.surface = TEXT_EFFECTS.prepare(layout.glyphs, layout.font_size, self.prefs,
                                                      self.devicePixelRatioF(), self.prefs.jump, layout.angle)
            states = (glyph_states(layout.glyphs, self.prefs, item, position, energy, layout.font_size,
                                   self.seed + item.index * 7919, layout.angle)
                      if self.prefs.animation_style != "classic" or self.prefs.singing_sync else None)
            image = TEXT_EFFECTS.render(layout.surface, self.prefs, seconds, energy, moving=True, states=states)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            painter.drawImage(layout.surface.origin, image)
            painter.restore()
        if self._is_pda_active():
            self._draw_pda_banner(painter)
