import winreg
import sys
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QScrollArea
)

from app.widgets import MD3ElevatedCard, MD3FilledButton, MD3OutlinedButton, MD3Switch


def _get_autostart() -> bool:
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
        winreg.QueryValueEx(key, "BetterZAPRET")
        winreg.CloseKey(key)
        return True
    except Exception:
        return False


def _set_autostart(enabled: bool):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        if enabled:
            exe = Path(sys.executable).resolve()
            script = Path(__file__).resolve().parent.parent.parent.parent / "main.py"
            winreg.SetValueEx(key, "BetterZAPRET", 0, winreg.REG_SZ, f'"{exe}" "{script}"')
        else:
            try:
                winreg.DeleteValue(key, "BetterZAPRET")
            except FileNotFoundError:
                pass
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Autostart error: {e}")


class SettingsPage(QWidget):
    def __init__(self, core, parent=None):
        super().__init__(parent)
        self.core = core
        self._setup_ui()
        self._load_settings()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 16, 28, 28)
        layout.setSpacing(16)

        header = QLabel("Настройки")
        header.setStyleSheet("font-family: 'Outfit'; font-size: 28px; font-weight: 700; color: white;")
        layout.addWidget(header)

        sub = QLabel("Конфигурация фильтров и поведения zapret")
        sub.setStyleSheet("font-family: 'Inter'; font-size: 14px; color: rgba(255,255,255,0.45);")
        layout.addWidget(sub)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        cl = QVBoxLayout(content)
        cl.setContentsMargins(0, 0, 6, 0)
        cl.setSpacing(16)

        # Game Filter
        game_card = MD3ElevatedCard()
        gl = game_card.layout()
        gf_title = QLabel("Game Filter")
        gf_title.setStyleSheet("font-family: 'Outfit'; font-size: 16px; font-weight: 600; color: white;")
        gl.addWidget(gf_title)
        gf_sub = QLabel("Режим фильтрации игрового трафика")
        gf_sub.setStyleSheet("font-family: 'Inter'; font-size: 12px; color: rgba(255,255,255,0.45);")
        gl.addWidget(gf_sub)

        self.game_group = []
        gbl = QHBoxLayout()
        gbl.setSpacing(8)
        for label, key in [("Отключён", "disabled"), ("TCP + UDP", "all"), ("Только TCP", "tcp"), ("Только UDP", "udp")]:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setProperty("mode", key)
            btn.setStyleSheet("""
                QPushButton {
                    color: rgba(255,255,255,0.55);
                    background: rgba(255,255,255,0.04);
                    border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 8px;
                    padding: 8px 14px;
                    font-family: 'Inter';
                    font-size: 13px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background: rgba(255,255,255,0.08);
                    color: rgba(255,255,255,0.85);
                }
                QPushButton:checked {
                    background: rgba(59, 130, 246, 0.15);
                    border: 1px solid rgba(59, 130, 246, 0.40);
                    color: #60A5FA;
                    font-weight: 600;
                }
            """)
            btn.clicked.connect(self._on_game_changed)
            self.game_group.append(btn)
            gbl.addWidget(btn)
        gbl.addStretch()
        gl.addLayout(gbl)
        cl.addWidget(game_card)

        # IPSet
        ipset_card = MD3ElevatedCard()
        il = ipset_card.layout()
        ip_title = QLabel("IPSet Filter")
        ip_title.setStyleSheet("font-family: 'Outfit'; font-size: 16px; font-weight: 600; color: white;")
        il.addWidget(ip_title)
        ip_sub = QLabel("Режим фильтрации по IP-адресам")
        ip_sub.setStyleSheet("font-family: 'Inter'; font-size: 12px; color: rgba(255,255,255,0.45);")
        il.addWidget(ip_sub)

        self.ipset_group = []
        ibl = QHBoxLayout()
        ibl.setSpacing(8)
        for label, key in [("Загружен", "loaded"), ("Любой", "any"), ("Отключён", "none")]:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setProperty("mode", key)
            btn.setStyleSheet("""
                QPushButton {
                    color: rgba(255,255,255,0.55);
                    background: rgba(255,255,255,0.04);
                    border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 8px;
                    padding: 8px 14px;
                    font-family: 'Inter';
                    font-size: 13px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background: rgba(255,255,255,0.08);
                    color: rgba(255,255,255,0.85);
                }
                QPushButton:checked {
                    background: rgba(59, 130, 246, 0.15);
                    border: 1px solid rgba(59, 130, 246, 0.40);
                    color: #60A5FA;
                    font-weight: 600;
                }
            """)
            btn.clicked.connect(self._on_ipset_changed)
            self.ipset_group.append(btn)
            ibl.addWidget(btn)
        ibl.addStretch()
        il.addLayout(ibl)
        cl.addWidget(ipset_card)

        # Toggles
        toggle_card = MD3ElevatedCard()
        tl = toggle_card.layout()
        for text, toggle in [("Автопроверка обновлений", "update"), ("Запускать при старте Windows", "autostart")]:
            row = QHBoxLayout()
            lbl = QLabel(text)
            lbl.setStyleSheet("font-family: 'Outfit'; font-size: 15px; font-weight: 600; color: white;")
            row.addWidget(lbl)
            row.addStretch()
            if toggle == "update":
                self.toggle_update = MD3Switch()
                self.toggle_update.toggled.connect(self._on_update_toggled)
                row.addWidget(self.toggle_update)
            else:
                self.toggle_autostart = MD3Switch()
                self.toggle_autostart.toggled.connect(self._on_autostart_toggled)
                row.addWidget(self.toggle_autostart)
            tl.addLayout(row)
        cl.addWidget(toggle_card)

        # Lists
        lists_card = MD3ElevatedCard()
        ll = lists_card.layout()
        ul_title = QLabel("Пользовательские списки")
        ul_title.setStyleSheet("font-family: 'Outfit'; font-size: 16px; font-weight: 600; color: white;")
        ll.addWidget(ul_title)
        ul_sub = QLabel("Редактируйте домены и исключения. Каждый домен — на новой строке.")
        ul_sub.setStyleSheet("font-family: 'Inter'; font-size: 12px; color: rgba(255,255,255,0.45);")
        ll.addWidget(ul_sub)

        el = QHBoxLayout()
        el.setSpacing(14)
        self.editor_general = QTextEdit()
        self.editor_general.setPlaceholderText("Добавьте домены (list-general-user.txt)")
        self.editor_general.setStyleSheet(self._editor_style())
        self.editor_general.setMaximumHeight(140)
        el.addWidget(self.editor_general)

        self.editor_exclude = QTextEdit()
        self.editor_exclude.setPlaceholderText("Исключения (list-exclude-user.txt)")
        self.editor_exclude.setStyleSheet(self._editor_style())
        self.editor_exclude.setMaximumHeight(140)
        el.addWidget(self.editor_exclude)
        ll.addLayout(el)

        self.btn_save_lists = MD3FilledButton("Сохранить списки")
        self.btn_save_lists.clicked.connect(self._save_lists)
        ll.addWidget(self.btn_save_lists)
        cl.addWidget(lists_card)
        cl.addStretch()

        scroll.setWidget(content)
        layout.addWidget(scroll)

    def _editor_style(self):
        return """
            QTextEdit {
                background: rgba(0, 0, 0, 0.20);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 10px;
                color: rgba(255,255,255,0.75);
                font-family: 'Consolas', monospace;
                font-size: 12px;
                padding: 10px;
            }
        """

    def _load_settings(self):
        cfg = self.core['config']
        mode = cfg.get_game_filter()
        for btn in self.game_group:
            if btn.property("mode") == mode:
                btn.setChecked(True)
                break
        ipset = cfg.get_ipset_status()
        for btn in self.ipset_group:
            if btn.property("mode") == ipset:
                btn.setChecked(True)
                break
        self.toggle_update.setChecked(cfg.get_check_updates())
        self.toggle_autostart.setChecked(_get_autostart())
        self.editor_general.setPlainText(cfg.read_user_list("list-general-user.txt"))
        self.editor_exclude.setPlainText(cfg.read_user_list("list-exclude-user.txt"))

    def _on_game_changed(self):
        sender = self.sender()
        for btn in self.game_group:
            btn.setChecked(btn == sender)
        self.core['config'].set_game_filter(sender.property("mode"))

    def _on_ipset_changed(self):
        sender = self.sender()
        for btn in self.ipset_group:
            btn.setChecked(btn == sender)

    def _on_update_toggled(self, checked: bool):
        self.core['config'].set_check_updates(checked)

    def _on_autostart_toggled(self, checked: bool):
        _set_autostart(checked)

    def _save_lists(self):
        cfg = self.core['config']
        cfg.write_user_list("list-general-user.txt", self.editor_general.toPlainText())
        cfg.write_user_list("list-exclude-user.txt", self.editor_exclude.toPlainText())
