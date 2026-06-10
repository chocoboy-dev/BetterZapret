from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices

from app.widgets import MD3ElevatedCard, MD3FilledButton


class InfoPage(QWidget):
    def __init__(self, core, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 16, 28, 28)
        layout.setSpacing(18)

        header = QLabel("Информация")
        header.setStyleSheet("font-family: 'Outfit'; font-size: 28px; font-weight: 700; color: white;")
        layout.addWidget(header)

        sub = QLabel("Версия, безопасность и ссылки")
        sub.setStyleSheet("font-family: 'Inter'; font-size: 14px; color: rgba(255,255,255,0.45);")
        layout.addWidget(sub)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        cl = QVBoxLayout(content)
        cl.setContentsMargins(0, 0, 8, 0)
        cl.setSpacing(18)

        # Version
        version_card = MD3ElevatedCard()
        vl = version_card.layout()
        v_title = QLabel("Версия")
        v_title.setStyleSheet("font-family: 'Outfit'; font-size: 18px; font-weight: 600; color: white;")
        vl.addWidget(v_title)
        v_text = QLabel("BetterZAPRET GUI v1.0.0\nБазируется на zapret-discord-youtube v1.9.9a")
        v_text.setStyleSheet("font-family: 'Inter'; font-size: 14px; color: rgba(255,255,255,0.70);")
        v_text.setWordWrap(True)
        vl.addWidget(v_text)
        cl.addWidget(version_card)

        # Security warning
        warn_card = MD3ElevatedCard()
        wl = warn_card.layout()
        w_title = QLabel("⚠️  Внимание — стиллеры в репозиториях")
        w_title.setStyleSheet("font-family: 'Outfit'; font-size: 18px; font-weight: 700; color: #FBBF24;")
        wl.addWidget(w_title)
        w_text = QLabel(
            "В последнее время появилось очень много поддельных репозиториев zapret, "
            "которые содержат стиллеры (вредоносное ПО, крадущее пароли, куки и токены).\n\n"
            "Признаки подделки:\n"
            "  • Ссылка на Discord/Telegram для скачивания\n"
            "  • Файлы .exe вместо .bat внутри архива\n"
            "  • Просьба отключить антивирус\n"
            "  • Неизвестные бинарники (winws.exe подменён)\n\n"
            "Скачивайте zapret только из официальных источников."
        )
        w_text.setStyleSheet("font-family: 'Inter'; font-size: 14px; color: rgba(255,255,255,0.75);")
        w_text.setWordWrap(True)
        wl.addWidget(w_text)
        cl.addWidget(warn_card)

        # Original repo (Flowseal)
        repo_card = MD3ElevatedCard()
        rl = repo_card.layout()
        r_title = QLabel("Оригинальный репозиторий")
        r_title.setStyleSheet("font-family: 'Outfit'; font-size: 18px; font-weight: 600; color: white;")
        rl.addWidget(r_title)
        r_text = QLabel(
            "Оригинальная сборка zapret-discord-youtube от Flowseal:\n"
            "https://github.com/Flowseal/zapret-discord-youtube"
        )
        r_text.setStyleSheet("font-family: 'Inter'; font-size: 14px; color: rgba(255,255,255,0.70);")
        r_text.setWordWrap(True)
        rl.addWidget(r_text)

        btn_repo = MD3FilledButton("Открыть оригинальный репозиторий")
        btn_repo.clicked.connect(self._open_repo)
        rl.addWidget(btn_repo)
        cl.addWidget(repo_card)

        # Upstream
        flow_card = MD3ElevatedCard()
        fl = flow_card.layout()
        f_title = QLabel("Апстрим (bol-van/zapret)")
        f_title.setStyleSheet("font-family: 'Outfit'; font-size: 18px; font-weight: 600; color: white;")
        fl.addWidget(f_title)
        f_text = QLabel(
            "Базовый zapret от bol-van (без готовых стратегий):\n"
            "https://github.com/bol-van/zapret"
        )
        f_text.setStyleSheet("font-family: 'Inter'; font-size: 14px; color: rgba(255,255,255,0.70);")
        f_text.setWordWrap(True)
        fl.addWidget(f_text)

        btn_flow = MD3FilledButton("Открыть апстрим zapret")
        btn_flow.clicked.connect(self._open_flow_repo)
        fl.addWidget(btn_flow)
        cl.addWidget(flow_card)

        cl.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)

    def _open_repo(self):
        QDesktopServices.openUrl(QUrl("https://github.com/Flowseal/zapret-discord-youtube"))

    def _open_flow_repo(self):
        QDesktopServices.openUrl(QUrl("https://github.com/bol-van/zapret"))
