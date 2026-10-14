"""Control-panel themes. Lyric materials and preview backgrounds are independent."""
from string import Template
from functools import lru_cache
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QColor, QPalette, QPainter, QPainterPath, QPen, QPixmap, QLinearGradient
from PySide6.QtWidgets import QFrame, QWidget
from settings import resource_path, DEFAULT_FONT_FAMILY

THEMES = {
    "light": dict(background="#f7f8fa", text="#293449", sidebar="#f0f3f6", border="#e0e5ed",
                  surface="#ffffff", muted="#7b8597", hover="#f0f2f6", pressed="#e8ecf2",
                  disabled="#a5acb9", disabled_surface="#f0f2f5", nav="#626d80", nav_hover="#e7ecf2",
                  track="#e4e8ee", scroll="#cfd6e1", selection="#ffe6eb", selection_text="#b7213c",
                  notice="#fff3e8", notice_text="#955224", notice_border="#f2dcc4"),
    "dark": dict(background="#171b24", text="#edf1f7", sidebar="#202632", border="#394354",
                 surface="#252d3a", muted="#acb7c9", hover="#303b4c", pressed="#39465b",
                 disabled="#798599", disabled_surface="#222936", nav="#c2ccdc", nav_hover="#303b4c",
                 track="#414d60", scroll="#58667e", selection="#542c3c", selection_text="#ff94a7",
                 notice="#3c2d22", notice_text="#ffd3a8", notice_border="#755038"),
    "special": dict(background="#0e0c0a", text="#f3ebdc", sidebar="#15120e", border="#4a3c2a",
                    surface="#1a1511", muted="#9b856b", hover="#251e18", pressed="#33291f",
                    disabled="#605240", disabled_surface="#14110e", nav="#dfd0b5", nav_hover="#261e16",
                    track="#382e21", scroll="#6d583b", selection="#3e2a14", selection_text="#ffdf99",
                    notice="#261b11", notice_text="#ffcc7a", notice_border="#5c4125", accent="#e5a93b"),
}

STYLE = Template("""
QWidget { background: $background; color: $text; font-family: '$ui_font'; font-size: 13px; }
QLabel, QCheckBox { background: transparent; }
QCheckBox { spacing: 8px; }
QCheckBox::indicator { width: 16px; height: 16px; border: 1.5px solid $muted; border-radius: 4px; background: $surface; }
QCheckBox::indicator:checked { background: #ff3656; border-color: #ff3656; image: url("$checkmark"); }
QCheckBox::indicator:hover { border-color: $text; }
QFrame#sidebar { background: $sidebar; border-right: 1px solid $border; }
QLabel#brand { font-size: 22px; font-weight: 700; letter-spacing: 1px; }
QLabel#heading { font-size: 28px; font-weight: 700; }
QLabel#muted, QLabel#eyebrow, QLabel#creator, QLabel#version, QLabel#motto { color: $muted; }
QLabel#creator, QLabel#version { font-size: 11px; }
QLabel#motto { font-size: 11px; letter-spacing: 1px; }
QLabel#eyebrow { font-size: 11px; letter-spacing: 3px; font-weight: 600; }
QLabel#section { font-size: 15px; font-weight: 700; letter-spacing: 0.5px; }
QLabel#song { font-size: 18px; font-weight: 600; }
QLabel#footerSong { font-size: 15px; font-weight: 500; }
QLabel#badge { background: $sidebar; color: $muted; border-radius: 12px; padding: 5px 14px; font-size: 12px; }
QLabel#notice { background: $notice; color: $notice_text; border: 1px solid $notice_border; border-radius: 10px; padding: 12px 16px; font-size: 13px; }
QFrame#card, QFrame#songRow { background: $surface; border: 1px solid $border; border-radius: 12px; }
QPushButton { background: $surface; border: 1px solid $border; border-radius: 8px; padding: 9px 16px; outline: none; font-size: 13px; }
QPushButton:hover { background: $hover; border-color: $muted; }
QPushButton:pressed { background: $pressed; }
QPushButton:focus { outline: none; }
QPushButton:disabled { color: $disabled; background: $disabled_surface; border-color: $border; }
QPushButton#primary { background: #ff3656; color: #ffffff; border: 1px solid #ff3656; font-weight: 600; border-radius: 8px; }
QPushButton#primary:hover { background: #f42648; }
QPushButton#primary:pressed { background: #de2342; }
QPushButton#nav { background: transparent; color: $nav; border: 1px solid transparent; text-align: left; padding: 11px 16px; font-size: 14px; font-weight: 500; border-radius: 8px; }
QPushButton#nav:hover { background: $nav_hover; }
QPushButton#nav:checked { background: #ff3656; color: #ffffff; font-weight: 600; }
QPushButton#nav:checked:hover { background: #f42648; }
QPushButton#nav:focus { border-color: #c62845; }
QPushButton#quiet { background: transparent; color: $muted; border: 1px solid transparent; text-align: left; font-size: 13px; padding: 8px 12px; border-radius: 6px; }
QPushButton#quiet:hover { background: $nav_hover; }
QPushButton#quiet:focus { border-color: #ff3656; }
QFrame#playerBar { background: $surface; border-top: 1px solid $border; }
QWidget#footerGroup { background: transparent; }
QPushButton#playRound { background: #ff3656; border: 1px solid #ff3656; border-radius: 24px; padding: 0; }
QPushButton#playRound:hover { background: #f42648; }
QPushButton#playRound:pressed { background: #de2342; }
QPushButton#playRound:focus { border: 2px solid #ad1833; }
QPushButton#playRound:disabled { background: $disabled_surface; border-color: $border; }
QPushButton#visibility { background: $surface; border: 1px solid $border; padding: 7px 12px; font-size: 12px; border-radius: 6px; }
QPushButton#visibility:hover { background: $hover; }
QComboBox, QSpinBox { background: $surface; border: 1px solid $border; border-radius: 8px; padding: 8px 12px; min-height: 20px; font-size: 13px; }
QComboBox:focus, QSpinBox:focus { border-color: #ff3656; }
QComboBox:disabled, QSpinBox:disabled { color: $disabled; background: $disabled_surface; }
QComboBox::drop-down { border: none; width: 26px; }
QComboBox QAbstractItemView { background: $surface; color: $text; selection-background-color: $selection; selection-color: $selection_text; border: 1px solid $border; border-radius: 6px; padding: 4px; }
QSpinBox::up-button, QSpinBox::down-button { width: 22px; }
QSlider { background: transparent; }
QSlider::groove:horizontal, QSlider::add-page:horizontal { height: 5px; background: $track; border: none; border-radius: 2px; }
QSlider::sub-page:horizontal { background: #ff3656; border: none; border-radius: 2px; }
QSlider::handle:horizontal { background: #ff3656; width: 14px; margin: -5px 0; border-radius: 7px; }
QSlider:disabled::sub-page:horizontal { background: $track; }
QSlider#progress::groove:horizontal { height: 3px; }
QSlider#progress::handle:horizontal { width: 8px; margin: -3px 0; border-radius: 4px; }
QScrollArea { border: none; background: transparent; }
QScrollBar:vertical { background: $background; width: 7px; }
QScrollBar::handle:vertical { background: $scroll; border-radius: 3px; min-height: 36px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QMenu { background: $surface; color: $text; border: 1px solid $border; border-radius: 8px; padding: 6px; }
QMenu::item { padding: 8px 20px; border-radius: 4px; }
QMenu::item:selected { background: $selection; color: $selection_text; }
QMenu::item:disabled { color: $disabled; }
""")


def theme_colors(name):
    return THEMES.get(name, THEMES["light"])


def theme_stylesheet(name):
    style = STYLE.substitute(theme_colors(name), ui_font=DEFAULT_FONT_FAMILY,
                             checkmark=resource_path("assets/check-white.svg").as_posix())
    if name != "special":
        return style
    style = style.replace("#ff3656", "#ffb526").replace("#f42648", "#ffc24b").replace("#de2342", "#d89619").replace("#c62845", "#c18c32").replace("#ad1833", "#b98731")
    return style + """
    QFrame#sidebar, QFrame#card, QFrame#songRow, QFrame#playerBar { background: transparent; border: none; border-radius: 0; }
    QWidget#themeCanvas { background: transparent; }
    QPushButton, QComboBox, QSpinBox { border-radius: 6px; }
    QPushButton#nav { border-radius: 6px; }
    QPushButton#nav:checked { color: #ffe6a3; border: 1px solid #c89538;
        background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #2f2214,stop:1 #1c140c); }
    QPushButton#nav:checked:hover { background: #3b2c1b; }
    QPushButton#primary { color: #1c140c; font-weight: 700; }
    QCheckBox::indicator { border-radius: 3px; }
    QPushButton:focus { outline: none; }
    """


def theme_accent(name):
    return theme_colors(name).get("accent", "#ff3656")


def accent_text(name):
    return "#21170b" if name == "special" else "#ffffff"


def theme_palette(name):
    colors = theme_colors(name)
    palette = QPalette()
    for role, key in ((QPalette.ColorRole.Window, "background"), (QPalette.ColorRole.WindowText, "text"),
                      (QPalette.ColorRole.Base, "surface"), (QPalette.ColorRole.AlternateBase, "sidebar"),
                      (QPalette.ColorRole.Text, "text"), (QPalette.ColorRole.Button, "surface"),
                      (QPalette.ColorRole.ButtonText, "text"), (QPalette.ColorRole.Mid, "track"),
                      (QPalette.ColorRole.ToolTipBase, "surface"), (QPalette.ColorRole.ToolTipText, "text")):
        palette.setColor(role, QColor(colors[key]))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(theme_accent(name)))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    for role in (QPalette.ColorRole.WindowText, QPalette.ColorRole.Text, QPalette.ColorRole.ButtonText):
        palette.setColor(QPalette.ColorGroup.Disabled, role, QColor(colors["disabled"]))
    return palette


@lru_cache(maxsize=1)
def blueprint_texture():
    return QPixmap(str(resource_path("assets/special-blueprint.svg")))


def _special(widget):
    return widget.window().property("interfaceTheme") == "special"


def _paint_surface(painter, rectangle, base, opacity=.24):
    gradient = QLinearGradient(rectangle.topLeft(), rectangle.bottomRight())
    gradient.setColorAt(0, QColor(base))
    gradient.setColorAt(1, QColor("#100d09"))
    painter.fillRect(rectangle, gradient)
    painter.save()
    painter.setOpacity(opacity)
    painter.drawPixmap(rectangle, blueprint_texture(), QRectF(blueprint_texture().rect()))
    painter.restore()


class ThemeCanvas(QWidget):
    """Paint decorative margins only for the special skin; normal QSS stays intact."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("themeCanvas")

    def paintEvent(self, event):
        super().paintEvent(event)
        if _special(self):
            painter = QPainter(self)
            _paint_surface(painter, QRectF(self.rect()), "#15110c", .5)
            painter.end()


class ThemeFrame(QFrame):
    def paintEvent(self, event):
        super().paintEvent(event)
        if not _special(self):
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rectangle = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        corner = 6.0
        path = QPainterPath()
        x, y, w, h = rectangle.x(), rectangle.y(), rectangle.width(), rectangle.height()
        path.moveTo(x + corner, y)
        for point in ((x + w - corner, y), (x + w, y + corner), (x + w, y + h - corner), (x + w - corner, y + h),
                      (x + corner, y + h), (x, y + h - corner), (x, y + corner)):
            path.lineTo(*point)
        path.closeSubpath()
        painter.setClipPath(path)
        _paint_surface(painter, rectangle, "#1c1712", 0.18)
        painter.setClipping(False)
        # Refined single gold accent border
        painter.setPen(QPen(QColor("#7d6542"), 1))
        painter.drawPath(path)
        # Subtle top-edge accent highlight
        painter.setPen(QPen(QColor("#e8c076"), 1.2))
        painter.drawLine(QPointF(x + corner + 2, y + 0.5), QPointF(x + w - corner - 2, y + 0.5))
        painter.end()
