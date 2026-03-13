import os
import re

# ================= НАСТРОЙКИ =================

# 1. Какую главу собираем?
TARGET_CHAPTER = "chapter6" 

# 2. Имя выходного файла
OUTPUT_FILENAME = f"Full_{TARGET_CHAPTER}.txt"

# 3. Список "Корневых" файлов главы.
# ВАЖНО: Сюда пишем только те файлы, которые идут ПО ПОРЯДКУ в основной линии.
# Если файлы типа "slice-of-life" вызываются через call внутри других файлов, 
# их СЮДА ПИСАТЬ НЕ НАДО (скрипт сам их найдет и вставит).
CHAPTERS_DB = {
    "chapter1": [
        "chapters/chapter1/1-lab-night.rpy",
        "chapters/chapter1/2-lab-morning.rpy",
        "chapters/chapter1/3-lab-noon.rpy",
        "chapters/chapter1/3.1-library.rpy",
        "chapters/chapter1/3.2-library-desk.rpy",
        "chapters/chapter1/4-meeting-start.rpy",
        "chapters/chapter1/5-meeting-end.rpy",
        "chapters/chapter1/6-security-post.rpy",
        "chapters/chapter1/7-confrontation.rpy",
        "chapters/chapter1/8-attack-scene.rpy",
        "chapters/chapter1/9-escape-start.rpy",
        "chapters/chapter1/10-escape-mid.rpy",
        "chapters/chapter1/11-escape-end.rpy",
        "chapters/chapter1/11-escape-end.rpy",
    ],

    "chapter2": [
        "flashbacks/krypton/krypton_flashbacks.rpy",
        "chapters/chapter2/1-false-memories.rpy",
        "chapters/chapter2/2-long-night.rpy",
        "chapters/chapter2/3-nightmare.rpy",
        "chapters/chapter2/4-facing-reality.rpy",
        "chapters/chapter2/5-desperate-measures.rpy",
        "chapters/chapter2/6-anomic.rpy",
        "flashbacks/neon/childhood/1-dream-fragment.rpy",
        "chapters/chapter2/7-arrival.rpy",
    ],

    "chapter3": [
        "chapters/chapter3/1-start.rpy",
        "chapters/chapter3/2.1-main-hall.rpy",
        "chapters/chapter3/2.1.1-bouncer-actions.rpy",
        "chapters/chapter3/2.2-left-wing.rpy",
        "chapters/chapter3/2.3-gate.rpy",
        "chapters/chapter3/2.4-cabinet.rpy",
        "chapters/chapter3/2.5-stairs.rpy",
        "chapters/chapter3/2.6-long-hall.rpy",
        "chapters/chapter3/2.7-post-office.rpy",
        "chapters/chapter3/3-chase.rpy",
        "chapters/chapter3/4-argon.rpy",
        "chapters/chapter3/5-distillation.rpy",
        "chapters/chapter3/6-briefing.rpy",
        "chapters/chapter3/7-path-sorting-station.rpy",
        "chapters/chapter3/8-sorting-station.rpy",
        "chapters/chapter3/9-argon-apartment-old.rpy",
        "chapters/chapter3/10-end.rpy",
    ],

    "chapter4.0": [
        "flashbacks/neon/childhood/2-dream-fragment.rpy",
        "chapters/chapter4.0/1-train-dream.rpy",
        "chapters/chapter4.0/2-ark-aground.rpy",
        "chapters/chapter4.0/3-academy.rpy",
        "chapters/chapter4.0/4-24_syndromechapter.rpy",
        "chapters/chapter4.0/5-garden.rpy",
    ],

    "chapter4.5": [
        "chapters/chapter4.5/1-garden-aftermath.rpy",
        "chapters/chapter4.5/2-cafe.rpy",
        "chapters/chapter4.5/3-1-concert.rpy",
        "chapters/chapter4.5/3-2-fan-meeting.rpy",
        "chapters/chapter4.5/3-3-seraphina-meeting.rpy",
        "chapters/chapter4.5/slice-of-life/1-nari.rpy",
        "chapters/chapter4.5/4-base.rpy",
        "chapters/chapter4.5/slice-of-life/2-kai.rpy",
        "chapters/chapter4.5/5-dormitory-nest.rpy",
        "chapters/chapter4.5/6-boulevard-fair.rpy",
        "chapters/chapter4.5/7-academic.rpy",
        "chapters/chapter4.5/8-busted-enemy.rpy",
        "chapters/chapter4.5/slice-of-life/4-penthouse.rpy",
        "chapters/chapter4.5/9-lily-rescue.rpy",
        "flashbacks/neon/childhood/4-dream-fragment.rpy",
        "chapters/chapter4.5/10-hostage.rpy",
        "chapters/chapter4.5/11-deadwall.rpy",
        "chapters/chapter4.5/12-epilogue.rpy",
    ],

    "chapter5": [
        "chapters/chapter5/1-arrival.rpy",
        "chapters/chapter5/2-start.rpy",
        "chapters/chapter5/3-station-hub.rpy",
        "chapters/chapter5/3.0-quest-hub-level2.rpy",
        "chapters/chapter5/3.0-quest-hub-level3.rpy",
        "chapters/chapter5/3.1-bar.rpy",
        "chapters/chapter5/3.2-chapel.rpy",
        "chapters/chapter5/3.3-library.rpy",
        "chapters/chapter5/3.4-server.rpy",
        "chapters/chapter5/4-brig.rpy",
        "chapters/chapter5/5-permabrig.rpy",
        "chapters/chapter5/6-erebus.rpy",
        "chapters/chapter5/7-bridge.rpy",
        "chapters/chapter5/8-father.rpy",
        "chapters/chapter5/9-epilogue.rpy",
    ],

    "chapter6": [
        "chapters/chapter6/1-alley-valley.rpy",
        "chapters/chapter6/2-spire.rpy",
        "chapters/chapter6/3-elision.rpy",
        "chapters/chapter6/4-encounter.rpy",
        "chapters/chapter6/5-beautiful-night.rpy",
    ]
}

# Путь к папке со всеми скриптами (относительно devtools)
PATH_TO_GAME_SCRIPTS = os.path.join("..", "game/game-scripts")

# ================= ЛОГИКА =================

# Словарь: "label_name" -> "full_path_to_file"
label_map = {}

def get_abs_path(rel_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, PATH_TO_GAME_SCRIPTS, rel_path))

def scan_all_scripts():
    """
    Сканирует ВСЮ папку game-scripts рекурсивно.
    Находит все 'label xxx:' и запоминает, в каких они файлах.
    """
    root_dir = get_abs_path("") # Получаем полный путь к game-scripts
    print(f"--- 1. Глобальное сканирование всех скриптов в: {root_dir} ---")
    
    if not os.path.exists(root_dir):
        print(f"!!! ОШИБКА: Папка не найдена: {root_dir}")
        return

    regex_label = re.compile(r'^\s*label\s+([a-zA-Z0-9_]+)\s*:')
    count = 0

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".rpy"):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            match = regex_label.search(line)
                            if match:
                                label_name = match.group(1)
                                # Если такой лейбл уже был, не перезаписываем (или можно вывести ворнинг)
                                if label_name not in label_map:
                                    label_map[label_name] = full_path
                                    count += 1
                except Exception as e:
                    print(f"Ошибка чтения {file}: {e}")
    
    print(f"Сканирование завершено. Найдено меток (labels): {count}\n")

def process_file(filepath, outfile, depth=0):
    """
    Читает файл строку за строкой.
    Если находит call -> ищет файл -> вставляет его содержимое.
    """
    # Защита от бесконечной рекурсии
    if depth > 10:
        outfile.write(f"\n[!!! ПРЕДУПРЕЖДЕНИЕ: Слишком глубокая вложенность (LOOP?) !!!]\n")
        return

    if not os.path.exists(filepath):
        outfile.write(f"\n[!!! ОШИБКА: Файл не найден: {filepath} !!!]\n")
        print(f"Не найден: {filepath}")
        return

    # Регулярка для call (исключая call screen)
    regex_call = re.compile(r'^\s*call\s+(?!screen\b)([a-zA-Z0-9_]+)')

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        outfile.write(f"\n[!!! ОШИБКА ЧТЕНИЯ: {e} !!!]\n")
        return

    indent = "    " * depth
    short_name = os.path.basename(filepath)
    
    # Заголовок
    outfile.write(f"\n{indent}{'='*15} [{short_name}] {'='*15}\n")

    for line in lines:
        match_call = regex_call.search(line)
        
        # Если нашли call
        if match_call:
            called_label = match_call.group(1)
            
            # Проверяем, есть ли такой лейбл в нашей базе
            if called_label in label_map:
                target_file = label_map[called_label]
                
                # ВАЖНО: Не вставлять файл в самого себя (рекурсия внутри файла)
                if os.path.abspath(target_file) == os.path.abspath(filepath):
                     outfile.write(line) # Просто пишем call как есть
                else:
                    outfile.write(f"\n{indent}>>> CALL: {called_label} (Файл: {os.path.basename(target_file)}) >>>\n")
                    # РЕКУРСИЯ: вставляем содержимое вызываемого файла
                    process_file(target_file, outfile, depth + 1)
                    outfile.write(f"{indent}<<< RETURN: {called_label} <<<\n\n")
            else:
                # Лейбл не найден (возможно, системный или из движка)
                outfile.write(line)
        else:
            # Обычная строка
            outfile.write(line)

    outfile.write(f"\n{indent}{'='*15} [КОНЕЦ: {short_name}] {'='*15}\n")

def main():
    # 1. Сканируем ВСЕ файлы проекта
    scan_all_scripts()

    # 2. Проверяем настройки
    if TARGET_CHAPTER not in CHAPTERS_DB:
        print(f"Глава '{TARGET_CHAPTER}' не найдена в настройках.")
        return

    file_list = CHAPTERS_DB[TARGET_CHAPTER]
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), OUTPUT_FILENAME)
    
    print(f"--- 2. Сборка главы {TARGET_CHAPTER} ---")

    try:
        with open(output_path, 'w', encoding='utf-8') as outfile:
            outfile.write(f"СБОРКА: {TARGET_CHAPTER}\n\n")
            
            for rel_path in file_list:
                full_path = get_abs_path(rel_path)
                print(f"Обработка корневого файла: {rel_path}")
                process_file(full_path, outfile)
                outfile.write("\n\n") 
        
        print(f"\nУСПЕШНО! Файл сохранен: {OUTPUT_FILENAME}")
        
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")

if __name__ == "__main__":
    main()