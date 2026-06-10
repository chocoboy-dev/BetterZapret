from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QGridLayout, QProgressBar
)
from PyQt6.QtCore import QThread, pyqtSignal

from app.widgets import MD3ElevatedCard, MD3FilledButton


class ToolWorker(QThread):
    line_received = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, runner, bat_name=None, ps1_path=None, args=None):
        super().__init__()
        self.runner = runner
        self.bat_name = bat_name
        self.ps1_path = ps1_path
        self.args = args or []

    def run(self):
        if self.ps1_path:
            proc = self.runner.run_ps1(self.ps1_path, self.args)
        elif self.bat_name:
            proc = self.runner.run_bat(self.bat_name, self.args)
        else:
            self.line_received.emit("[Ошибка] Не указана команда")
            self.finished.emit()
            return

        if proc is None:
            self.line_received.emit("[Ошибка] Не удалось запустить процесс")
            self.finished.emit()
            return

        for line in proc.stdout:
            self.line_received.emit(line.rstrip())
        proc.wait()
        self.finished.emit()


class ToolsPage(QWidget):
    def __init__(self, core, parent=None):
        super().__init__(parent)
        self.core = core
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 16, 28, 28)
        layout.setSpacing(16)

        header = QLabel("Инструменты")
        header.setStyleSheet("font-family: 'Outfit'; font-size: 28px; font-weight: 700; color: white;")
        layout.addWidget(header)

        sub = QLabel("Диагностика, тестирование и обновление компонентов")
        sub.setStyleSheet("font-family: 'Inter'; font-size: 14px; color: rgba(255,255,255,0.45);")
        layout.addWidget(sub)

        grid = QGridLayout()
        grid.setSpacing(16)

        tools = [
            ("Диагностика", "Проверка конфликтов и состояния системы", self._run_diagnostics),
            ("Тесты", "Автоматическое тестирование стратегий", self._run_tests),
            ("Обновить IPSet", "Загрузка актуального списка IP", self._update_ipset),
            ("Обновить Hosts", "Обновление hosts файла", self._update_hosts),
            ("Проверить обновления", "Проверка версии с GitHub", self._check_updates),
        ]

        for i, (title, desc, callback) in enumerate(tools):
            card = MD3ElevatedCard()
            cl = card.layout()
            cl.setContentsMargins(20, 18, 20, 18)
            cl.setSpacing(10)

            lbl_title = QLabel(title)
            lbl_title.setStyleSheet("font-family: 'Outfit'; font-size: 16px; font-weight: 600; color: white;")
            cl.addWidget(lbl_title)

            lbl_desc = QLabel(desc)
            lbl_desc.setWordWrap(True)
            lbl_desc.setStyleSheet("font-family: 'Inter'; font-size: 12px; color: rgba(255,255,255,0.45);")
            cl.addWidget(lbl_desc)
            cl.addStretch()

            btn = MD3FilledButton("Запустить")
            btn.clicked.connect(callback)
            cl.addWidget(btn)

            row = i // 2
            col = i % 2
            grid.addWidget(card, row, col)

        layout.addLayout(grid)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(4)
        self.progress.setStyleSheet("""
            QProgressBar { background: rgba(255,255,255,0.05); border-radius: 2px; }
            QProgressBar::chunk { background: #3B82F6; border-radius: 2px; }
        """)
        self.progress.hide()
        layout.addWidget(self.progress)

        log_card = MD3ElevatedCard()
        ll = log_card.layout()
        ll.setContentsMargins(16, 12, 16, 12)
        ll.setSpacing(8)

        lh = QLabel("Вывод")
        lh.setStyleSheet("font-family: 'Inter'; font-size: 13px; color: rgba(255,255,255,0.40);")
        ll.addWidget(lh)

        self.log_edit = QTextEdit()
        self.log_edit.setReadOnly(True)
        self.log_edit.setStyleSheet("""
            QTextEdit {
                background: rgba(0, 0, 0, 0.20);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 10px;
                color: rgba(255,255,255,0.75);
                font-family: 'Consolas', monospace;
                font-size: 12px;
                padding: 12px;
            }
        """)
        ll.addWidget(self.log_edit)
        layout.addWidget(log_card)
        layout.addStretch()

    def _append_log(self, text: str):
        self.log_edit.append(text)
        sb = self.log_edit.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _clear_log(self):
        self.log_edit.clear()

    def _run_worker(self, bat_name=None, ps1_path=None):
        self._clear_log()
        self.progress.show()
        self.worker = ToolWorker(self.core['runner'], bat_name=bat_name, ps1_path=ps1_path)
        self.worker.line_received.connect(self._append_log)
        self.worker.finished.connect(lambda: self.progress.hide())
        self.worker.start()

    def _run_diagnostics(self):
        self._append_log("[Запуск] Диагностика...")
        self._run_worker(bat_name="service.bat")

    def _run_tests(self):
        self._append_log("[Запуск] Тесты...")
        ps1 = self.core['base_dir'] / "utils" / "test zapret.ps1"
        self._run_worker(ps1_path=ps1)

    def _update_ipset(self):
        self._append_log("[Запуск] Обновление IPSet...")
        self._run_worker(bat_name="service.bat")

    def _update_hosts(self):
        self._append_log("[Запуск] Обновление Hosts...")
        self._run_worker(bat_name="service.bat")

    def _check_updates(self):
        self._append_log("[Запуск] Проверка обновлений...")
        self._run_worker(bat_name="service.bat")
