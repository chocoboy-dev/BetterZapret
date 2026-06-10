from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from app.widgets import MD3ElevatedCard, MD3FilledButton, MD3OutlinedButton


class LogWorker(QThread):
    line_received = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, runner, bat_name, args=None):
        super().__init__()
        self.runner = runner
        self.bat_name = bat_name
        self.args = args or []

    def run(self):
        proc = self.runner.run_bat(self.bat_name, self.args)
        if proc is None:
            self.line_received.emit("[Ошибка] Не удалось запустить процесс")
            self.finished.emit()
            return
        for line in proc.stdout:
            self.line_received.emit(line.rstrip())
        proc.wait()
        self.finished.emit()


class ServicePage(QWidget):
    def __init__(self, core, parent=None):
        super().__init__(parent)
        self.core = core
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 16, 28, 28)
        layout.setSpacing(16)

        header = QLabel("Управление сервисом")
        header.setStyleSheet("font-family: 'Outfit'; font-size: 28px; font-weight: 700; color: white;")
        layout.addWidget(header)

        sub = QLabel("Установка, удаление и проверка статуса системного сервиса")
        sub.setStyleSheet("font-family: 'Inter'; font-size: 14px; color: rgba(255,255,255,0.45);")
        layout.addWidget(sub)

        btn_card = MD3ElevatedCard()
        bl = btn_card.layout()
        bl.setContentsMargins(20, 16, 20, 16)
        bl.setSpacing(12)
        bl.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.btn_install = MD3FilledButton("Установить сервис")
        self.btn_install.clicked.connect(self._install_service)
        bl.addWidget(self.btn_install)

        self.btn_remove = MD3OutlinedButton("Удалить сервис")
        self.btn_remove.clicked.connect(self._remove_service)
        bl.addWidget(self.btn_remove)

        self.btn_status = MD3OutlinedButton("Проверить статус")
        self.btn_status.clicked.connect(self._check_status)
        bl.addWidget(self.btn_status)
        layout.addWidget(btn_card)

        log_card = MD3ElevatedCard()
        ll = log_card.layout()
        ll.setContentsMargins(16, 12, 16, 12)
        ll.setSpacing(8)

        lh = QLabel("Вывод консоли")
        lh.setStyleSheet("font-family: 'Inter'; font-size: 12px; color: rgba(255,255,255,0.40);")
        ll.addWidget(lh)

        self.log_edit = QTextEdit()
        self.log_edit.setReadOnly(True)
        self.log_edit.setStyleSheet("""
            QTextEdit {
                background: rgba(0, 0, 0, 0.20);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 8px;
                color: rgba(255,255,255,0.75);
                font-family: 'Consolas', monospace;
                font-size: 12px;
                padding: 10px;
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

    def _install_service(self):
        self._clear_log()
        self._append_log("[Запуск] Установка сервиса...")
        self._run_worker("service.bat")

    def _remove_service(self):
        self._clear_log()
        self._append_log("[Запуск] Удаление сервиса...")
        self.core['service'].stop_and_delete_service('zapret')
        self.core['service'].stop_and_delete_service('WinDivert')
        self._append_log("[Готово] Сервис удалён")

    def _check_status(self):
        self._clear_log()
        self._append_log("[Проверка] Статус сервисов:")
        for name in ['zapret', 'WinDivert']:
            status = self.core['service'].query_service(name)
            self._append_log(f"  {name}: {status}")
        self._append_log(f"[Проверка] winws.exe: {'running' if self.core['service'].check_winws_running() else 'not running'}")

    def _run_worker(self, bat_name: str):
        self.worker = LogWorker(self.core['runner'], bat_name)
        self.worker.line_received.connect(self._append_log)
        self.worker.finished.connect(lambda: self._append_log("[Завершено]"))
        self.worker.start()
