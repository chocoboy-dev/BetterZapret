<p align="center">
  <img src="https://img.shields.io/badge/⚠️%20НЕОФИЦИАЛЬНЫЙ%20ПРОЕКТ-red?style=for-the-badge&logo=github&logoColor=white" alt="Неофициальный проект"/>
  <img src="https://img.shields.io/badge/НИКАК%20НЕ%20СВЯЗАН%20С%20ОРИГИНАЛОМ-orange?style=for-the-badge" alt="Не связан с оригиналом"/>
  <br/>
  <img src="https://img.shields.io/badge/ИСПОЛЬЗУЕТЕ%20НА%20СВОЙ%20СТРАХ%20И%20РИСК-darkred?style=for-the-badge&logo=fire&logoColor=white"/>
</p>

---

# ⚡ BetterZAPRET GUI

Неофициальная графическая оболочка для **zapret** — утилиты для обхода DPI.

---

> [!CAUTION]
> ## 🚨 ВАЖНЕЙШЕЕ ПРЕДУПРЕЖДЕНИЕ
>
> ### Этот проект является **НЕОФИЦИАЛЬНЫМ** и **НЕ ИМЕЕТ НИКАКОГО ОТНОШЕНИЯ** к оригинальному репозиторию.
>
> | ❌ Что это НЕ | ✅ Что это |
> |---|---|
> | Не официальная версия zapret | Просто удобная графическая обёртка |
> | Не связано с разработчиками Flowseal | Сделано сторонним энтузиастом |
> | Не гарантирует работу | Для удобства использования |
>
> **Оригинальный проект (30к+ ★):** [github.com/Flowseal/zapret-discord-youtube](https://github.com/Flowseal/zapret-discord-youtube)
>
> **Всё, что делает эта оболочка — запускает .bat-файлы zapret через кнопки.** Никакой магии.
>
> Любые вопросы по работе обхода DPI — **только в репозиторий Flowseal**.

---

## ✨ Возможности

- 🎛 Управление сервисом zapret
- 📋 Выбор стратегий обхода (fake, multisplit, multidisorder и др.)
- 📊 Мониторинг статуса в реальном времени
- 🔧 Управление фильтрами (WinDivert, TCP timestamps, Game filter)
- 🎨 Material Design 3 интерфейс с glassmorphism

## 📋 Требования

- 🪟 Windows 10/11
- 🐍 Python 3.10+
- 📦 [zapret](https://github.com/Flowseal/zapret-discord-youtube) (установленный рядом с папкой `betterzapret-gui`)

## 🚀 Установка

```bash
pip install -r requirements.txt
python main.py
```

## 📦 Сборка EXE

```bash
python build_exe.py
```

Готовый exe появится в папке `dist/BetterZAPRET/`.
