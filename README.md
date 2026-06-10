# BetterZAPRET GUI

Неофициальная графическая оболочка для [zapret](https://github.com/bol-vet/zapret) — утилиты для обхода DPI.

**Внимание:** Это неофициальный проект, созданный для удобства использования. Оригинальный проект: [github.com/bol-vet/zapret](https://github.com/bol-vet/zapret)

## Возможности

- Управление сервисом zapret
- Выбор стратегий обхода (fake, multisplit, multidisorder и др.)
- Мониторинг статуса в реальном времени
- Управление фильтрами (WinDivert, TCP timestamps, Game filter)
- Material Design 3 интерфейс с glassmorphism

## Требования

- Windows 10/11
- Python 3.10+
- [zapret](https://github.com/bol-vet/zapret) (установленный рядом с папкой `betterzapret-gui`)

## Установка

```bash
pip install -r requirements.txt
python main.py
```

## Сборка EXE

```bash
python build_exe.py
```

Готовый exe появится в папке `dist/BetterZAPRET/`.
