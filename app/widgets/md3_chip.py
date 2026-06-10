from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt


class MD3FilterChip(QPushButton):
    """Material Design 3 Filter Chip."""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                color: rgba(255,255,255,0.65);
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 8px;
                padding: 6px 14px;
                font-family: 'Inter', 'Segoe UI', sans-serif;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.08);
                color: rgba(255,255,255,0.90);
            }
            QPushButton:checked {
                background: rgba(59, 130, 246, 0.18);
                border: 1px solid rgba(59, 130, 246, 0.45);
                color: #60A5FA;
                font-weight: 600;
            }
        """)
