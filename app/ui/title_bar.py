from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt


class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        self._drag_pos = None
        self.setFixedHeight(40)
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 12, 0)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        title = QLabel("BetterZAPRET")
        title.setStyleSheet("font-family: 'Outfit'; font-size: 14px; font-weight: 700; color: rgba(255,255,255,0.85);")
        layout.addWidget(title)
        layout.addStretch()

        for char, slot in [("–", self._parent.showMinimized),
                           ("□", self._toggle_maximize),
                           ("×", self._parent.close)]:
            btn = QPushButton(char)
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("""
                QPushButton {
                    color: rgba(255,255,255,0.55);
                    background: transparent;
                    border: none;
                    border-radius: 6px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background: rgba(255,255,255,0.10);
                    color: white;
                }
            """)
            btn.clicked.connect(slot)
            layout.addWidget(btn)

    def _toggle_maximize(self):
        if self._parent.isMaximized():
            self._parent.showNormal()
        else:
            self._parent.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() == Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self._drag_pos
            if self._parent.isMaximized():
                self._parent.showNormal()
            self._parent.move(self._parent.x() + delta.x(), self._parent.y() + delta.y())
            self._drag_pos = event.globalPosition().toPoint()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        self._toggle_maximize()
