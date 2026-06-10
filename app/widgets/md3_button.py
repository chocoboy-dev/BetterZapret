from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt


class MD3FilledButton(QPushButton):
    """Material Design 3 Filled Button."""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3B82F6, stop:1 #2563EB);
                border: none;
                border-radius: 20px;
                padding: 10px 24px;
                font-family: 'Outfit', 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #60A5FA, stop:1 #2563EB);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1D4ED8, stop:1 #1E40AF);
            }
        """)


class MD3OutlinedButton(QPushButton):
    """Material Design 3 Outlined Button."""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                color: rgba(255,255,255,0.85);
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.20);
                border-radius: 20px;
                padding: 10px 24px;
                font-family: 'Outfit', 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.10);
                border: 1px solid rgba(255, 255, 255, 0.35);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.03);
            }
        """)
