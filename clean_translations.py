import os
import re

# Настройки путей
GAME_DIR = os.path.join(os.getcwd(), "game")
TL_DIR = os.path.join(GAME_DIR, "tl")

# Регулярные выражения
# 1. Ищет ID в оригинальных скриптах (формат: ... id <смесь_цифр_и_букв>)
SOURCE_ID_REGEX = re.compile(r'[\s\t]+id[\s\t]+([a-zA-Z0-9_]+)\s*$')

# 2. Ищет начало блока перевода (формат: translate <язык> <id>:)
TL_BLOCK_REGEX = re.compile(r'^translate\s+[\w_]+\s+([a-zA-Z0-9_]+):')

def get_active_ids(game_dir):
    """Сканирует папку game (кроме tl) и собирает все активные ID диалогов."""
    active_ids = set()
    print("Сканирование оригинальных скриптов...")
    
    for root, dirs, files in os.walk(game_dir):
        # Исключаем папку переводов из поиска ID
        if "tl" in dirs:
            dirs.remove("tl")
            
        for file in files:
            if file.endswith(".rpy"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        # Ищем явные ID в конце строк диалогов
                        match = SOURCE_ID_REGEX.search(line)
                        if match:
                            active_ids.add(match.group(1))
                            
    print(f"Найдено активных ID: {len(active_ids)}")
    return active_ids

def clean_translation_files(tl_dir, active_ids):
    """Проходит по файлам переводов и удаляет неиспользуемые блоки."""
    print("Очистка файлов перевода...")
    deleted_count = 0
    
    for root, dirs, files in os.walk(tl_dir):
        for file in files:
            if file.endswith(".rpy"):
                file_path = os.path.join(root, file)
                
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                new_lines = []
                skip_block = False
                
                for line in lines:
                    # Проверяем, не начинается ли новый блок перевода
                    block_match = TL_BLOCK_REGEX.match(line)
                    
                    if block_match:
                        tl_id = block_match.group(1)
                        # Если ID нет в списке активных - включаем режим пропуска
                        if tl_id not in active_ids:
                            skip_block = True
                            deleted_count += 1
                            # print(f"Удаляю мусор: {tl_id} в файле {file}") # Раскомментируйте для подробностей
                        else:
                            skip_block = False
                            new_lines.append(line)
                    else:
                        # Логика пропуска строк внутри блока
                        if skip_block:
                            # Если строка пустая или начинается с пробела/комментария - это всё ещё часть блока
                            # Блок заканчивается, когда встречаем строку без отступа, которая не является комментарием/пустой
                            stripped = line.strip()
                            if not line.startswith(" ") and not line.startswith("\t") and stripped and not stripped.startswith("#"):
                                # Это уже не часть блока перевода, перестаем пропускать
                                skip_block = False
                                new_lines.append(line)
                            else:
                                # Пропускаем строку (она часть мусорного блока)
                                continue
                        else:
                            new_lines.append(line)
                
                # Перезаписываем файл только если были изменения (опционально)
                if len(lines) != len(new_lines):
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.writelines(new_lines)

    print(f"Готово! Удалено 'мусорных' блоков: {deleted_count}")

if __name__ == "__main__":
    if not os.path.exists(GAME_DIR):
        print("Ошибка: Не найдена папка 'game'. Запустите скрипт из корня проекта.")
        input("\nНажмите Enter, чтобы выйти...")
    else:
        active_ids = get_active_ids(GAME_DIR)
        clean_translation_files(TL_DIR, active_ids)
        input("\nНажмите Enter, чтобы выйти...")