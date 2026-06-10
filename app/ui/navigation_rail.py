from pathlib import Path
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QRect, QEasingCurve, QSize
from PyQt6.QtGui import QIcon


class NavigationRail(QWidget):
    """Material Design 3 Navigation Rail (sidebar)."""

    page_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(80)
        self._setup_ui()
        self._current_index = 0

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 16, 12, 12)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.nav_items = []
        items = [
            ("home", 0),
            ("list", 1),
            ("settings", 2),
            ("sliders", 3),
            ("tool", 4),
            ("info", 5),
        ]
        icons_dir = Path(__file__).resolve().parent.parent.parent / "assets" / "icons"

        for icon_name, idx in items:
            btn = QPushButton()
            btn.setCheckable(True)
            btn.setProperty("index", idx)
            btn.setFixedSize(56, 56)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                    border-radius: 16px;
                    color: rgba(255,255,255,0.55);
                }
                QPushButton:hover {
                    background: rgba(255,255,255,0.06);
                    color: rgba(255,255,255,0.85);
                }
                QPushButton:checked {
                    background: rgba(59, 130, 246, 0.15);
                    color: #60A5FA;
                }
            """)
            ip = icons_dir / f"{icon_name}.svg"
            if ip.exists():
                btn.setIcon(QIcon(str(ip)))
                btn.setIconSize(QSize(24, 24))
            btn.clicked.connect(lambda _, i=idx: self._on_nav_clicked(i))
            layout.addWidget(btn)
            self.nav_items.append(btn)

        layout.addStretch()

        self.indicator = QWidget(self)
        self.indicator.setFixedWidth(3)
        self.indicator.setStyleSheet("background-color: #3B82F6; border-radius: 2px;")
        self.indicator.hide()

        self._anim = QPropertyAnimation(self.indicator, b"geometry")
        self._anim.setDuration(250)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.nav_items[0].setChecked(True)
        self._update_indicator(0)

    def _on_nav_clicked(self, index: int):
        if index == self._current_index:
            return
        for i, btn in enumerate(self.nav_items):
            btn.setChecked(i == index)
        self._current_index = index
        self._update_indicator(index)
        self.page_changed.emit(index)

    def _update_indicator(self, index: int):
        btn = self.nav_items[index]
        y = btn.mapTo(self, btn.rect().topLeft()).y() + 8
        h = btn.height() - 16
        target = QRect(4, y, 3, h)

        if self.indicator.isVisible():
            self._anim.setStartValue(self.indicator.geometry())
            self._anim.setEndValue(target)
            self._anim.start()
        else:
            self.indicator.setGeometry(target)
        self.indicator.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_indicator(self._current_index)
