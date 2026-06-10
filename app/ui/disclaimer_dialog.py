from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QLinearGradient, QFontDatabase


class DisclaimerDialog(QDialog):
    def __init__(self, gui_dir, parent=None):
        super().__init__(parent)
        self.setWindowTitle("BetterZAPRET — Предупреждение")
        self.setFixedSize(500, 380)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)

        self._load_fonts(gui_dir)
        self._setup_ui()
        self._start_enter_animation()

    def _load_fonts(self, gui_dir):
        fonts_dir = gui_dir / "assets" / "fonts"
        for f in fonts_dir.glob("*.ttf"):
            QFontDatabase.addApplicationFont(str(f))

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 24)
        layout.setSpacing(12)

        icon = QLabel("⚡")
        icon.setStyleSheet("font-size: 36px;")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)

        title = QLabel("Важное предупреждение")
        title.setStyleSheet("font-family: 'Outfit'; font-size: 20px; font-weight: 700; color: #FBBF24;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        msg = QLabel(
            "Вы используете <b>неофициальную</b> графическую оболочку для zapret.\n\n"
            "Данное меню создано исключительно для удобства использования "
            "и не имеет отношения к официальному проекту.\n\n"
            "Оригинальный проект zapret:\n"
            "<a href='https://github.com/Flowseal/zapret-discord-youtube' style='color: #60A5FA; "
            "text-decoration: none; font-weight: 600;'>"
            "github.com/Flowseal/zapret-discord-youtube</a>\n\n"
            "Используйте на свой страх и риск."
        )
        msg.setOpenExternalLinks(True)
        msg.setWordWrap(True)
        msg.setStyleSheet(
            "font-family: 'Inter'; font-size: 13px; color: rgba(255,255,255,0.72); "
            "line-height: 1.55;"
        )
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(msg)

        layout.addStretch()

        self.btn = QPushButton("Понятно")
        self.btn.setFixedHeight(42)
        self.btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn.setStyleSheet("""
            QPushButton {
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3B82F6, stop:1 #2563EB);
                border: none;
                border-radius: 12px;
                font-family: 'Outfit';
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #60A5FA, stop:1 #3B82F6);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1D4ED8, stop:1 #1E40AF);
            }
        """)
        self.btn.clicked.connect(self._on_accept)
        layout.addWidget(self.btn)

    def _start_enter_animation(self):
        self.setWindowOpacity(0.0)
        self._anim_opacity = QPropertyAnimation(self, b"windowOpacity")
        self._anim_opacity.setDuration(350)
        self._anim_opacity.setStartValue(0.0)
        self._anim_opacity.setEndValue(1.0)
        self._anim_opacity.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim_opacity.start()

    def _on_accept(self):
        self.btn.setEnabled(False)
        self._anim_exit = QPropertyAnimation(self, b"windowOpacity")
        self._anim_exit.setDuration(200)
        self._anim_exit.setStartValue(1.0)
        self._anim_exit.setEndValue(0.0)
        self._anim_exit.setEasingCurve(QEasingCurve.Type.InCubic)
        self._anim_exit.finished.connect(self.accept)
        self._anim_exit.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()

        grad = QLinearGradient(0, 0, 0, h)
        grad.setColorAt(0, QColor(22, 24, 36))
        grad.setColorAt(0.5, QColor(18, 20, 32))
        grad.setColorAt(1, QColor(14, 16, 28))

        painter.setBrush(QBrush(grad))
        painter.setPen(QPen(QColor(255, 255, 255, 18), 1))
        painter.drawRoundedRect(1, 1, w - 2, h - 2, 18, 18)

        # Subtle top glow
        glow = QLinearGradient(0, 0, 0, 80)
        glow.setColorAt(0, QColor(59, 130, 246, 30))
        glow.setColorAt(1, QColor(59, 130, 246, 0))
        painter.setBrush(QBrush(glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(1, 1, w - 2, 80, 18, 18)

        painter.end()

    def showEvent(self, event):
        super().showEvent(event)
        screen = self.screen().availableGeometry()
        self.move(
            screen.center().x() - self.width() // 2,
            screen.center().y() - self.height() // 2
        )
