from PyQt6.QtCore import QTimer, QObject, pyqtSignal


class StatusMonitor(QObject):
    """Живой мониторинг статусов zapret через QTimer."""

    status_changed = pyqtSignal(dict)

    def __init__(self, service_manager):
        super().__init__()
        self.sm = service_manager
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._check)
        self._running = False

    def start(self, interval_ms: int = 2000):
        self._running = True
        self._check()
        self.timer.start(interval_ms)

    def stop(self):
        self._running = False
        self.timer.stop()

    def _check(self):
        if not self._running:
            return
        data = {
            'winws_running': self.sm.check_winws_running(),
            'zapret_service': self.sm.query_service('zapret'),
            'windivert_service': self.sm.query_service('WinDivert'),
            'tcp_timestamps': self.sm.check_tcp_timestamps(),
            'current_strategy': self.sm.get_current_strategy(),
        }
        self.status_changed.emit(data)

    def force_check(self):
        self._check()
