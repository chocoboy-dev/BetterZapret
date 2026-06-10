"""
Сборка BetterZAPRET GUI в единый exe через PyInstaller.
Запуск: python build_exe.py
"""
import sys
import subprocess
from pathlib import Path


def main():
    # Определяем папки
    here = Path(__file__).parent.resolve()
    assets_dir = here / "assets"
    dist_dir = here / "dist" / "BetterZAPRET"
    icon_path = next(assets_dir.rglob("*.ico"), None)

    # Проверяем установку PyInstaller
    try:
        import PyInstaller  # noqa
    except ImportError:
        print("Устанавливаем PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Формируем команду
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "BetterZAPRET",
        "--distpath", str(dist_dir.parent),
        "--workpath", str(here / "build"),
        "--specpath", str(here),
        "--add-data", f"{assets_dir}{'/' if sys.platform != 'win32' else ';'}.assets",
        "--hidden-import", "PyQt6.QtMultimedia",
        "--hidden-import", "app.core",
        "--hidden-import", "app.ui",
        "--hidden-import", "app.widgets",
        "--collect-all", "app",
        str(here / "main.py"),
    ]

    if sys.platform == "win32" and icon_path:
        cmd.insert(1, f"--icon={icon_path}")

    subprocess.check_call(cmd)

    # Копируем assets в dist
    print(f"Готово: {dist_dir / 'BetterZAPRET.exe'}")


if __name__ == "__main__":
    main()
