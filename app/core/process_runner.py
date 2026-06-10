import subprocess
import os
from pathlib import Path


class ProcessRunner:
    """Запускает bat/ps1 файлы."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def run_bat(self, bat_name: str, args=None, shell=True):
        bat_path = self.base_dir / bat_name
        if not bat_path.exists():
            return None

        cmd = [str(bat_path)]
        if args:
            cmd.extend(args)

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace',
            cwd=str(self.base_dir),
            shell=shell
        )
        return proc

    def run_bat_detached(self, bat_name: str):
        """Запускает bat в отдельной консоли (не блокирует GUI)."""
        bat_path = self.base_dir / bat_name
        if not bat_path.exists():
            return None

        # CREATE_NEW_CONSOLE создаёт новое окно консоли
        subprocess.Popen(
            [str(bat_path)],
            cwd=str(self.base_dir),
            shell=True,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

    def run_ps1(self, ps1_path: Path, args=None):
        if not ps1_path.exists():
            return None

        cmd = [
            'powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass',
            '-File', str(ps1_path)
        ]
        if args:
            cmd.extend(args)

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace',
            cwd=str(self.base_dir)
        )
        return proc

    def read_output(self, proc, chunk_callback=None):
        """Читает stdout построчно."""
        if proc is None:
            return ""
        lines = []
        for line in proc.stdout:
            line = line.rstrip()
            lines.append(line)
            if chunk_callback:
                chunk_callback(line)
        proc.wait()
        return "\n".join(lines)
