from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
from PyQt6.QtCore import Qt

from app.widgets import MD3ElevatedCard, MD3FilledButton, MD3OutlinedButton, SlideStatusLabel


class DashboardPage(QWidget):
    def __init__(self, core, parent=None):
        super().__init__(parent)
        self.core = core
        self._setup_ui()
        self.core['monitor'].status_changed.connect(self._update_status)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 16, 28, 28)
        layout.setSpacing(20)

        header = QLabel("Панель управления")
        header.setStyleSheet("font-family: 'Outfit'; font-size: 28px; font-weight: 700; color: white;")
        layout.addWidget(header)

        sub = QLabel("Быстрый доступ к основным функциям zapret")
        sub.setStyleSheet("font-family: 'Inter'; font-size: 14px; color: rgba(255,255,255,0.45);")
        layout.addWidget(sub)

        # Status card
        status_card = MD3ElevatedCard()
        scl = status_card.layout()
        scl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.slide_status = SlideStatusLabel()
        self.slide_status.setText("Остановлен", "#F87171")
        scl.addWidget(self.slide_status)

        self.status_strategy = QLabel("Стратегия не выбрана")
        self.status_strategy.setStyleSheet("font-family: 'Inter'; font-size: 13px; color: rgba(255,255,255,0.50);")
        self.status_strategy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scl.addWidget(self.status_strategy)
        layout.addWidget(status_card)

        # Buttons
        bl = QHBoxLayout()
        bl.setSpacing(12)
        self.btn_start = MD3FilledButton("Запустить обход")
        self.btn_start.clicked.connect(self._start_bypass)
        bl.addWidget(self.btn_start)
        self.btn_stop = MD3OutlinedButton("Остановить")
        self.btn_stop.clicked.connect(self._stop_bypass)
        bl.addWidget(self.btn_stop)
        bl.addStretch()
        layout.addLayout(bl)

        # Status grid
        grid = QGridLayout()
        grid.setSpacing(12)

        self._add_status_card(grid, 0, 0, "Zapret сервис", "stopped")
        self._add_status_card(grid, 0, 1, "WinDivert", "stopped")
        self._add_status_card(grid, 1, 0, "TCP timestamps", "stopped")
        self._add_status_card(grid, 1, 1, "Game filter", "stopped")

        layout.addLayout(grid)
        layout.addStretch()

    def _add_status_card(self, grid, row, col, title, status):
        card = MD3ElevatedCard()
        cl = card.layout()
        lbl = QLabel(title)
        lbl.setStyleSheet("font-family: 'Inter'; font-size: 12px; color: rgba(255,255,255,0.40);")
        cl.addWidget(lbl)
        status_lbl = QLabel(status)
        status_lbl.setStyleSheet("font-family: 'Inter'; font-size: 14px; color: #F87171;")
        cl.addWidget(status_lbl)
        grid.addWidget(card, row, col)
        return status_lbl

    def _update_status(self, data: dict):
        winws = data.get('winws_running', False)
        strategy = data.get('current_strategy')

        if winws:
            self.slide_status.setText("Обход активен", "#34D399")
        else:
            self.slide_status.setText("Обход остановлен", "#F87171")

        if strategy:
            self.status_strategy.setText(f"Текущая стратегия: {strategy}")
        else:
            self.status_strategy.setText("Стратегия не выбрана")

    def _start_bypass(self):
        self.core['runner'].run_bat_detached("general.bat")

    def _stop_bypass(self):
        self.core['service'].kill_winws()
