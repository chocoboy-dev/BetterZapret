from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget,
    QPushButton, QLabel, QSystemTrayIcon, QMenu
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontDatabase

from .glass_effects import enable_acrylic, enable_rounded_corners
from .navigation_rail import NavigationRail
from .title_bar import TitleBar
from .pages import DashboardPage, StrategiesPage, ServicePage, SettingsPage, ToolsPage, InfoPage


class MainWindow(QMainWindow):
    def __init__(self, core, parent=None):
        super().__init__(parent)
        self.core = core
        self.setWindowTitle("BetterZAPRET")
        self.setMinimumSize(900, 600)
        self.resize(1100, 760)
        self.setWindowFlags(
            Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowMinimizeButtonHint
        )
        self._load_fonts()
        self._setup_ui()
        self._setup_tray()

    def _load_fonts(self):
        fonts_dir = self.core['gui_dir'] / "assets" / "fonts"
        for f in fonts_dir.glob("*.ttf"):
            QFontDatabase.addApplicationFont(str(f))

    def showEvent(self, event):
        super().showEvent(event)
        hwnd = int(self.winId())
        enable_acrylic(hwnd)
        enable_rounded_corners(hwnd)

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.rail = NavigationRail()
        self.rail.page_changed.connect(self._on_page_changed)
        layout.addWidget(self.rail)

        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(0)

        self.title_bar = TitleBar(self)
        rl.addWidget(self.title_bar)

        self.stack = QStackedWidget()
        self.pages = [
            DashboardPage(self.core),
            StrategiesPage(self.core),
            ServicePage(self.core),
            SettingsPage(self.core),
            ToolsPage(self.core),
            InfoPage(self.core),
        ]
        for p in self.pages:
            self.stack.addWidget(p)
        rl.addWidget(self.stack, 1)

        layout.addWidget(right, 1)

    def _setup_tray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setToolTip("BetterZAPRET")
        menu = QMenu()
        a1 = menu.addAction("Открыть")
        a1.triggered.connect(self._show_window)
        a2 = menu.addAction("Выход")
        a2.triggered.connect(self._quit_app)
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self._tray_activated)
        self.tray.show()

    def _tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self._show_window()

    def _show_window(self):
        if self.isMinimized():
            self.showNormal()
        self.show()
        self.raise_()
        self.activateWindow()

    def _quit_app(self):
        self.tray.hide()
        self.close()

    def closeEvent(self, event):
        self.tray.hide()
        event.accept()

    def _on_page_changed(self, index: int):
        self.stack.setCurrentIndex(index)
