import os
from pathlib import Path


class ConfigManager:
    """Чтение и запись конфигурационных файлов zapret."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.lists_dir = base_dir / "lists"
        self.utils_dir = base_dir / "utils"

    def get_game_filter(self) -> str:
        path = self.utils_dir / "game_filter.enabled"
        if not path.exists():
            return "disabled"
        mode = path.read_text(encoding='utf-8').strip().lower()
        if mode in ("all", "tcp", "udp"):
            return mode
        return "disabled"

    def set_game_filter(self, mode: str):
        path = self.utils_dir / "game_filter.enabled"
        if mode == "disabled":
            if path.exists():
                path.unlink()
        else:
            path.write_text(mode + "\n", encoding='utf-8')

    def get_check_updates(self) -> bool:
        return (self.utils_dir / "check_updates.enabled").exists()

    def set_check_updates(self, enabled: bool):
        path = self.utils_dir / "check_updates.enabled"
        if enabled:
            path.write_text("ENABLED\n", encoding='utf-8')
        else:
            if path.exists():
                path.unlink()

    def get_ipset_status(self) -> str:
        path = self.lists_dir / "ipset-all.txt"
        if not path.exists():
            return "none"
        lines = [l.strip() for l in path.read_text(encoding='utf-8').splitlines() if l.strip()]
        if not lines:
            return "any"
        # Проверяем, есть ли реальные IP (строки с цифрами и точками, не комментарии)
        real_ips = [l for l in lines if not l.startswith('#') and any(c.isdigit() for c in l)]
        if not real_ips:
            return "none"
        return "loaded"

    def read_user_list(self, name: str) -> str:
        path = self.lists_dir / name
        if not path.exists():
            return ""
        return path.read_text(encoding='utf-8')

    def write_user_list(self, name: str, content: str):
        path = self.lists_dir / name
        path.write_text(content, encoding='utf-8')

    def get_warning_accepted(self) -> bool:
        path = self.utils_dir / ".betterzapret_warning_accepted"
        return path.exists()

    def set_warning_accepted(self, accepted: bool):
        path = self.utils_dir / ".betterzapret_warning_accepted"
        if accepted:
            path.write_text("1\n", encoding='utf-8')
        else:
            if path.exists():
                path.unlink()

    def get_strategy_files(self):
        """Возвращает список .bat файлов (кроме service.bat)."""
        bats = []
        for f in sorted(self.base_dir.glob("*.bat")):
            if f.name.lower() == "service.bat":
                continue
            bats.append(f)
        return bats

    def parse_strategy_info(self, bat_path: Path) -> dict:
        """Извлекает название и описание из bat файла."""
        name = bat_path.stem
        try:
            text = bat_path.read_text(encoding='utf-8')
        except Exception:
            text = ""

        # Определяем категорию по имени
        upper = name.upper()
        if "FAKE TLS" in upper:
            category = "fake_tls"
        elif "SIMPLE FAKE" in upper:
            category = "simple_fake"
        elif "ALT" in upper:
            category = "alt"
        else:
            category = "general"

        # Определяем краткое описание по аргументам
        desc = ""
        if "multisplit" in text:
            desc = "Multisplit стратегия"
        elif "multidisorder" in text:
            desc = "Multidisorder стратегия"
        elif "fakedsplit" in text:
            desc = "Fake + split"
        elif "fake" in text and "fakedsplit" not in text:
            desc = "Fake стратегия"
        else:
            desc = "Стандартная стратегия"

        if "tls_clienthello_www_google_com" in text:
            desc += " (Google TLS)"
        if "tls_clienthello_4pda_to" in text:
            desc += " (4pda TLS)"

        return {
            'file': bat_path.name,
            'name': name,
            'category': category,
            'description': desc,
        }
