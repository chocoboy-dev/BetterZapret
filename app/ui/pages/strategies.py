from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QScrollArea

from app.widgets import MD3ElevatedCard, MD3FilledButton, MD3OutlinedButton, MD3FilterChip


class StrategiesPage(QWidget):
    def __init__(self, core, parent=None):
        super().__init__(parent)
        self.core = core
        self._current_filter = "all"
        self._setup_ui()
        self._load_strategies()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 16, 28, 28)
        layout.setSpacing(16)

        header = QLabel("Стратегии обхода")
        header.setStyleSheet("font-family: 'Outfit'; font-size: 28px; font-weight: 700; color: white;")
        layout.addWidget(header)

        sub = QLabel("Выберите подходящую стратегию для вашего провайдера")
        sub.setStyleSheet("font-family: 'Inter'; font-size: 14px; color: rgba(255,255,255,0.45);")
        layout.addWidget(sub)

        # Filter chips
        fl = QHBoxLayout()
        fl.setSpacing(8)
        self.chips = []
        for label, key in [("Все", "all"), ("General", "general"), ("ALT", "alt"),
                           ("Fake TLS", "fake_tls"), ("Simple", "simple_fake")]:
            chip = MD3FilterChip(label)
            chip.setProperty("filter", key)
            chip.setChecked(key == "all")
            chip.clicked.connect(self._on_filter_changed)
            fl.addWidget(chip)
            self.chips.append(chip)
        fl.addStretch()
        layout.addLayout(fl)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 6, 0)
        self.scroll_layout.setSpacing(14)
        self.scroll_layout.setColumnStretch(0, 1)
        self.scroll_layout.setColumnStretch(1, 1)
        self.scroll_layout.setColumnStretch(2, 1)

        scroll.setWidget(self.scroll_content)
        layout.addWidget(scroll)

    def _on_filter_changed(self):
        sender = self.sender()
        if not sender:
            return
        for chip in self.chips:
            chip.setChecked(chip == sender)
        self._current_filter = sender.property("filter")
        self._load_strategies()

    def _load_strategies(self):
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        cfg = self.core['config']
        bats = cfg.get_strategy_files()
        infos = [cfg.parse_strategy_info(b) for b in bats]
        if self._current_filter != "all":
            infos = [i for i in infos if i['category'] == self._current_filter]

        current = self.core['service'].get_current_strategy()

        for i, info in enumerate(infos):
            card = self._create_card(info, current)
            row = i // 3
            col = i % 3
            self.scroll_layout.addWidget(card, row, col)

        self.scroll_layout.setRowStretch(self.scroll_layout.rowCount(), 1)

    def _create_card(self, info, current_strategy):
        card = MD3ElevatedCard()
        cl = card.layout()

        cat_map = {
            'general': ('General', '#60A5FA'),
            'alt': ('ALT', '#34D399'),
            'fake_tls': ('Fake TLS', '#FBBF24'),
            'simple_fake': ('Simple', '#A78BFA'),
        }
        cat_name, cat_color = cat_map.get(info['category'], ('Other', '#9CA3AF'))

        badge = QLabel(cat_name)
        badge.setStyleSheet(f"color: {cat_color}; font-family: 'Inter'; font-size: 10px; font-weight: 700; background: {cat_color}15; border-radius: 5px; padding: 2px 8px;")
        cl.addWidget(badge)

        name = QLabel(info['name'])
        name.setStyleSheet("font-family: 'Outfit'; font-size: 15px; font-weight: 600; color: white;")
        cl.addWidget(name)

        desc = QLabel(info['description'])
        desc.setWordWrap(True)
        desc.setStyleSheet("font-family: 'Inter'; font-size: 12px; color: rgba(255,255,255,0.45);")
        cl.addWidget(desc)
        cl.addStretch()

        is_active = current_strategy and info['name'] == current_strategy
        if is_active:
            active = QLabel("● Активна")
            active.setStyleSheet("color: #34D399; font-family: 'Inter'; font-size: 12px; font-weight: 600;")
            cl.addWidget(active)

        btn = MD3FilledButton("Остановить" if is_active else "Запустить")
        btn.clicked.connect(lambda _, f=info['file']: self._launch(f))
        cl.addWidget(btn)
        return card

    def _launch(self, filename: str):
        self.core['runner'].run_bat_detached(filename)
