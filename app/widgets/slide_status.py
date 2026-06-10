from PyQt6.QtWidgets import QWidget, QLabel, QSizePolicy
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtGui import QFont


class SlideStatusLabel(QWidget):
    """Статус-лейбл с анимацией slide-down при смене текста."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(42)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._font = QFont("Outfit", 26, QFont.Weight.Bold)
        self._current_label = None
        self._anim = None
        self._label = QLabel("Остановлен", self)
        self._label.setFont(self._font)
        self._label.setStyleSheet("color: #F87171; font-family: 'Outfit'; font-size: 26px; font-weight: 700; padding: 0 8px;")
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.setMinimumWidth(1)
        self._label.setMinimumHeight(42)
        self._label.move(0, 0)
        self._label.show()
        self._current_label = self._label

    def setText(self, text: str, color: str = "#F87171"):
        if self._current_label and self._current_label.text() == text:
            return
        self._animate_change(text, color)

    def _create_label(self, text, color, y):
        lbl = QLabel(text, self)
        lbl.setFont(self._font)
        lbl.setStyleSheet(f"color: {color}; font-family: 'Outfit'; font-size: 26px; font-weight: 700; padding: 0 8px;")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setMinimumWidth(1)
        lbl.setMinimumHeight(42)
        lbl.move(0, y)
        lbl.show()
        return lbl

    def _animate_change(self, text: str, color: str):
        if self._anim:
            self._anim.stop()
            self._anim.deleteLater()
            self._anim = None

        old = self._current_label
        if old:
            old.deleteLater()

        new = self._create_label(text, color, -42)

        self._anim = QPropertyAnimation(new, b"pos")
        self._anim.setDuration(300)
        self._anim.setStartValue(QPoint(0, -42))
        self._anim.setEndValue(QPoint(0, 0))
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.finished.connect(self._on_anim_finished)
        self._anim.start()

        self._current_label = new

    def _on_anim_finished(self):
        self._anim = None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._current_label:
            self._current_label.resize(self.width(), 42)
