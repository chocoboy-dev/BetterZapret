from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QLinearGradient


class MD3ElevatedCard(QWidget):
    """Material Design 3 Elevated Card с glassmorphism."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._hover = False
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(16, 16, 16, 16)
        self._layout.setSpacing(8)

    def layout(self):
        return self._layout

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        grad = QLinearGradient(0, 0, 0, self.height())
        if self._hover:
            grad.setColorAt(0, QColor(255, 255, 255, 28))
            grad.setColorAt(1, QColor(255, 255, 255, 12))
        else:
            grad.setColorAt(0, QColor(255, 255, 255, 18))
            grad.setColorAt(1, QColor(255, 255, 255, 6))

        painter.setBrush(QBrush(grad))
        painter.setPen(QPen(QColor(255, 255, 255, 20), 1))
        painter.drawRoundedRect(1, 1, self.width() - 2, self.height() - 2, 16, 16)
        painter.end()

    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self.update()
        super().leaveEvent(event)
