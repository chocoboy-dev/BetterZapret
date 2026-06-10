import sys
import ctypes
import os
from pathlib import Path

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontDatabase

# Добавляем путь к app
sys.path.insert(0, str(Path(__file__).parent))

from app.core import ProcessRunner, ServiceManager, StatusMonitor, ConfigManager
from app.ui.main_window import MainWindow
from app.ui.disclaimer_dialog import DisclaimerDialog


def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def run_as_admin():
    """Перезапускает приложение с правами администратора через UAC."""
    exe = Path(sys.executable).resolve()
    script = Path(__file__).resolve()
    params = f'"{script}"'
    
    result = ctypes.windll.shell32.ShellExecuteW(
        None, "runas", str(exe), params, None, 1
    )
    # result <= 32 means error
    if result <= 32:
        print(f"Failed to elevate privileges. Error code: {result}")
        sys.exit(1)


def main():
    # Проверка прав администратора
    if not is_admin():
        print("Запрашиваем права администратора...")
        run_as_admin()
        sys.exit(0)

    # Определяем директории
    gui_dir = Path(__file__).parent.resolve()
    base_dir = gui_dir.parent

    try:
        # PyQt6 приложение
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
        app = QApplication(sys.argv)
        app.setStyle("Fusion")

        # Загрузка шрифтов
        fonts_dir = gui_dir / "assets" / "fonts"
        for font_file in fonts_dir.glob("*.ttf"):
            QFontDatabase.addApplicationFont(str(font_file))

        # Инициализация core
        runner = ProcessRunner(base_dir)
        service = ServiceManager(base_dir)
        config = ConfigManager(base_dir)
        monitor = StatusMonitor(service)

        core = {
            'base_dir': base_dir,
            'gui_dir': gui_dir,
            'runner': runner,
            'service': service,
            'config': config,
            'monitor': monitor,
        }

        # Предупреждение при первом запуске
        if not config.get_warning_accepted():
            dialog = DisclaimerDialog(gui_dir)
            dialog.exec()
            config.set_warning_accepted(True)

        # Создание окна
        window = MainWindow(core)
        window.show()

        # Запуск мониторинга
        monitor.start(2000)

        sys.exit(app.exec())
    except Exception as e:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("BetterZAPRET — Ошибка")
        msg.setText(f"Не удалось запустить GUI:\n{str(e)}")
        msg.exec()
        raise


if __name__ == "__main__":
    main()
