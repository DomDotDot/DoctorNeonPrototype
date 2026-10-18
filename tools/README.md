# DoctorNeonPrototype — Справочник инструментов разработки (`tools/`)

В данном каталоге собраны вспомогательные утилиты, скрипты автоматизации и линтеры для проекта **The Brightest Neon: Semitone Resonance**.

---

## 📋 Оглавление

1. [Скрипт статистики и линтер сценария (`script_stats_linter.py`)](#1-script_stats_linterpy)
2. [Конвертер диалогов в текстовый формат (`rpy-to-text-converter.py`)](#2-rpy-to-text-converterpy)
3. [Установка Git Pre-commit хука (`install_git_hook.py`)](#3-install_git_hookpy)
4. [Быстрые скрипты обновления (`update_stats.bat` / `update_stats.ps1`)](#4-быстрые-скрипты-обновления)
5. [CI/CD автоматизация (GitHub Actions)](#5-cicd-автоматизация)

---

## 1. `script_stats_linter.py`

Основной инструмент аудита сценария новеллы. Сканирует все файлы глав в `game/game-scripts/`, вычисляет точный объём текста (диалоги, нарратив, статистика по персонажам) и синхронизирует бейджи и таблицы в `README.md` и `README.ru.md`.

### Основные команды:

```bash
# Вывести подробную статистику в консоль и обновить README файлы:
python tools/script_stats_linter.py

# Только проверка (режим CI, возвращает код 0 если README актуален, 1 если устарел):
python tools/script_stats_linter.py --check

# Тихий режим (для запуска внутри git pre-commit хука):
python tools/script_stats_linter.py --silent

# Генерация отчета в JSON:
python tools/script_stats_linter.py --json stats.json
```

---

## 2. `rpy-to-text-converter.py`

Конвертирует Ren'Py сценарии (`.rpy`) в чистый человекочитаемый текст без управляющих тегов, меток и программного кода. Незаменим для редакторов, корректоров и переводчиков.

### Основные команды:

```bash
# Конвертировать все главы (по умолчанию сохраняет в Downloads):
python tools/rpy-to-text-converter.py

# Конвертировать конкретную главу:
python tools/rpy-to-text-converter.py --chapter chapter1

# Сохранить результат в кастомную папку:
python tools/rpy-to-text-converter.py --chapter chapter5 --output ./exports/chapter5.txt

# Собрать все главы в единый файл Full_all.txt:
python tools/rpy-to-text-converter.py --combine
```

---

## 3. `install_git_hook.py`

Скрипт однократной настройки локального окружения разработчика. Создает `.git/hooks/pre-commit`, который при каждом коммите автоматически пересчитывает статистику слов и добавляет обновленные `README.md` и `README.ru.md` в коммит.

### Установка:

```bash
python tools/install_git_hook.py
```

---

## 4. Быстрые скрипты обновления

Для запуска в один клик без терминала:
- **`update_stats.bat`** — запускает линтер и выводит статистику через стандартный Windows `cmd`.
- **`update_stats.ps1`** — аналогичный запуск для пользователей PowerShell.

---

## 5. CI/CD автоматизация

Проект настроен на непрерывную интеграцию через GitHub Actions:
- **`.github/workflows/stats_lint.yml`**: При каждом пуше или PR проверяет соответствие статистики в README реальному тексту игры. Для экономии квоты GitHub LFS в шаге `actions/checkout` явно задан флаг `lfs: false`.
- **`.github/workflows/update_cdn_hash.yml`**: При выпуске релиза вычисляет контрольные суммы SHA-256 и обновляет манифест CDN-лаунчера.
