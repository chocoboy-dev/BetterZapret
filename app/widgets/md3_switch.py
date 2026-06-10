from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen


class MD3Switch(QWidget):
    """Material Design 3 Switch."""

    toggled = pyqtSignal(bool)

    def __init__(self, checked=False, parent=None):
        super().__init__(parent)
        self.setFixedSize(52, 32)
        self._checked = checked
        self._circle_x = 28 if checked else 4
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def isChecked(self):
        return self._checked

    def setChecked(self, checked: bool):
        if self._checked == checked:
            return
        self._checked = checked
        self._circle_x = 28 if checked else 4
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self._checked:
            bg = QColor(59, 130, 246)
        else:
            bg = QColor(255, 255, 255, 50)
        painter.setBrush(QBrush(bg))
        painter.setPen(QPen(QColor(255, 255, 255, 30), 1))
        painter.drawRoundedRect(0, 0, 52, 32, 16, 16)

        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(self._circle_x, 4, 24, 24)
        painter.end()

    def mousePressEvent(self, event):
        self._checked = not self._checked
        self._circle_x = 28 if self._checked else 4
        self.toggled.emit(self._checked)
        self.update()
