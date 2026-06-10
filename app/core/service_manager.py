import subprocess
import re
import winreg


class ServiceManager:
    """Управление Windows сервисами и проверка статусов."""

    def __init__(self, base_dir):
        self.base_dir = base_dir

    def query_service(self, name: str) -> str:
        """Возвращает 'running', 'stopped', 'not_installed' или 'error'."""
        try:
            result = subprocess.run(
                ['sc', 'query', name],
                capture_output=True, text=True, timeout=5,
                encoding='utf-8', errors='replace'
            )
            out = result.stdout
            if 'RUNNING' in out:
                return 'running'
            elif 'STOPPED' in out:
                return 'stopped'
            elif 'STOP_PENDING' in out:
                return 'stop_pending'
            else:
                return 'not_installed'
        except Exception:
            return 'error'

    def stop_and_delete_service(self, name: str):
        subprocess.run(['net', 'stop', name], capture_output=True, timeout=15)
        subprocess.run(['sc', 'delete', name], capture_output=True, timeout=15)

    def start_service(self, name: str):
        subprocess.run(['sc', 'start', name], capture_output=True, timeout=15)

    def get_current_strategy(self) -> str | None:
        """Читает из реестра имя установленной стратегии."""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"System\CurrentControlSet\Services\zapret"
            )
            value, _ = winreg.QueryValueEx(key, "zapret-discord-youtube")
            winreg.CloseKey(key)
            return value
        except Exception:
            return None

    def check_winws_running(self) -> bool:
        result = subprocess.run(
            ['tasklist', '/FI', 'IMAGENAME eq winws.exe'],
            capture_output=True, text=True, timeout=5
        )
        return 'winws.exe' in result.stdout

    def enable_tcp_timestamps(self):
        subprocess.run(
            ['netsh', 'interface', 'tcp', 'set', 'global', 'timestamps=enabled'],
            capture_output=True, timeout=10
        )

    def check_tcp_timestamps(self) -> bool:
        result = subprocess.run(
            ['netsh', 'interface', 'tcp', 'show', 'global'],
            capture_output=True, text=True, timeout=5
        )
        out = result.stdout.lower()
        return 'enabled' in out and 'timestamps' in out

    def kill_winws(self):
        subprocess.run(['taskkill', '/IM', 'winws.exe', '/F'],
                       capture_output=True, timeout=10)

    def check_adguard(self) -> bool:
        result = subprocess.run(
            ['tasklist', '/FI', 'IMAGENAME eq AdguardSvc.exe'],
            capture_output=True, text=True, timeout=5
        )
        return 'AdguardSvc.exe' in result.stdout

    def check_bfe_running(self) -> bool:
        result = subprocess.run(
            ['sc', 'query', 'BFE'],
            capture_output=True, text=True, timeout=5
        )
        return 'RUNNING' in result.stdout
