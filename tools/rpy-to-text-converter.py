import os
import re

# ================= НАСТРОЙКИ =================

# 1. Какую главу собираем?
TARGET_CHAPTER = "chapter8" 

# 2. Имя выходного файла
OUTPUT_FILENAME = f"Full_{TARGET_CHAPTER}.txt"

# 3. Список "Корневых" файлов главы.
# ВАЖНО: Сюда пишем только те файлы, которые идут ПО ПОРЯДКУ в основной линии.
# Если файлы типа "slice-of-life" вызываются через call внутри других файлов, 
# их СЮДА ПИСАТЬ НЕ НАДО (скрипт сам их найдет и вставит).
CHAPTERS_DB = {
    "chapter1": [
        "chapters/chapter1/1-lab-night.rpy",
        "flashbacks/krypton/krypton_baddream.rpy",
        "chapters/chapter1/2-lab-morning.rpy",
        "chapters/chapter1/3-lab-noon.rpy",
        "chapters/chapter1/3.1-library.rpy",
        "flashbacks/neon/1-zurich_flashback.rpy",
        "chapters/chapter1/3.2-library-desk.rpy",
        "chapters/chapter1/4-meeting-start.rpy",
        "flashbacks/oganesson/1-oganesson_flashback.rpy",
        "chapters/chapter1/5-meeting-end.rpy",
        "chapters/chapter1/6-security-post.rpy",
        "chapters/chapter1/7-confrontation.rpy",
        "chapters/chapter1/8-attack-scene.rpy",
        "chapters/chapter1/9-escape.rpy",
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
        "chapters/chapter5/level-1/1-arrival.rpy",
        "chapters/chapter5/level-1/2-start.rpy",
        "chapters/chapter5/level-2/3.0-quest-hub-level2.rpy",
        "chapters/chapter5/level-2/3.1-bar.rpy",
        "chapters/chapter5/level-2/3.2-chapel.rpy",
        "chapters/chapter5/level-2/3.3-library.rpy",
        "chapters/chapter5/level-2/3.4-elevator.rpy",
        "chapters/chapter5/level-2/3.5-cargo.rpy",
        "chapters/chapter5/level-2/3.6-dorms.rpy",
        "chapters/chapter5/level-3/4.0-quest-hub-level3.rpy",
        "chapters/chapter5/level-3/4.1-research-department.rpy",
        "chapters/chapter5/level-3/4.2-trauma.rpy",
        "chapters/chapter5/level-3/4.3.0-medbay.rpy",
        "chapters/chapter5/level-3/4.3.1-genetics.rpy",
        "chapters/chapter5/level-3/4.4-robotics.rpy",
        "chapters/chapter5/level-3/4.5-hop-office.rpy",
        "chapters/chapter5/level-4/5.0-monorail.rpy",
        "chapters/chapter5/level-4/5.1-satellite-reception.rpy",
        "chapters/chapter5/level-4/5.2-corridor-alpha.rpy",
        "chapters/chapter5/level-4/5.3-corridor-beta.rpy",
        "chapters/chapter5/level-4/5.4-corridor-gamma.rpy",
        "chapters/chapter5/level-4/5.5-corridor-core.rpy",
        "chapters/chapter5/level-4/5.6-ai-core.rpy",
        "chapters/chapter5/level-4/5.7-generators-failed.rpy",
        "chapters/chapter5/6-server.rpy",
        "chapters/chapter5/7-brig.rpy",
        "chapters/chapter5/8-permabrig.rpy",
        "chapters/chapter5/9-erebus.rpy",
        "chapters/chapter5/10-bridge.rpy",
        "chapters/chapter5/11-father.rpy",
        "chapters/chapter5/12-epilogue.rpy",
    ],

    "chapter6": [
        "chapters/chapter6/1-alley-valley.rpy",
        "chapters/chapter6/2-spire.rpy",
        "chapters/chapter6/3-elision.rpy",
        "chapters/chapter6/4-encounter.rpy",
        "chapters/chapter6/5-ceo.rpy",
        "chapters/chapter6/6-beautiful-night.rpy",
    ],

    "chapter7": [
        "chapters/chapter7/1-library.rpy",
        "chapters/chapter7/2-family-apartment.rpy",
        "chapters/chapter7/3-decay.rpy",
    ],

    "chapter8": [
        "chapters/chapter8/1-drown.rpy",
        "chapters/chapter8/2-schooldays.rpy",
        "chapters/chapter8/3-lockedroom.rpy",
        "chapters/chapter8/4-basketball.rpy",
        "chapters/chapter8/5-infirmary.rpy",
        "chapters/chapter8/6-search-island.rpy",
        "chapters/chapter8/7-cave.rpy",
        "chapters/chapter8/8-letter.rpy",
        "chapters/chapter8/9-mismatch.rpy",
        "chapters/chapter8/10-morning-incident.rpy",
        "chapters/chapter8/11-club-invitation.rpy",
        "chapters/chapter8/12-classmate.rpy",
        "chapters/chapter8/13-club.rpy",
        "chapters/chapter8/14-lost-key.rpy",
        "chapters/chapter8/15-afternoon-date.rpy",
        "chapters/chapter8/16-martyrdom-tide.rpy",
        "chapters/chapter8/17-ocean-of-loneless.rpy",
        "chapters/chapter8/18-memory-sea.rpy",
        "chapters/chapter8/19-boundless-ocean.rpy",
        "chapters/chapter8/20-helious-helium.rpy",
        "chapters/chapter8/21-dream.rpy",
    ],

    "chapter9": [
        "chapters/chapter9/1-meet-me-there.rpy",
        "chapters/chapter9/2-red-mist.rpy",
        "chapters/chapter9/3-concert-hall.rpy",
        "chapters/chapter9/4-absolute-silence.rpy",
        "chapters/chapter9/5-bell-toll.rpy",
        "chapters/chapter9/6-epilogue.rpy",
    ],
}

# Путь к папке со всеми скриптами (относительно devtools)
PATH_TO_GAME_SCRIPTS = os.path.join("..", "game/game-scripts")

# ================= ЛОГИКА =================

# Словарь: "label_name" -> "full_path_to_file"


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
    root_dir = get_abs_path("")
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

                                if label_name not in label_map:
                                    label_map[label_name] = full_path
                                    count += 1
                except Exception as e:
                    print(f"Ошибка чтения {file}: {e}")
    
    print(f"Сканирование завершено. Найдено меток (labels): {count}\n")

def extract_label_lines(filepath, target_label):
    """
    Извлекает из файла только строки указанной метки (от 'label target_label:' до 'return' или следующей метки).
    Возвращает список строк или None, если метка не найдена.
    """
    regex_label = re.compile(rf'^\s*label\s+{re.escape(target_label)}\s*(\(.*\))?\s*:')
    regex_any_label = re.compile(r'^\s*label\s+[a-zA-Z0-9_]+\s*(\(.*\))?\s*:')
    regex_return = re.compile(r'^\s*return\b')

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
    except Exception:
        return None

    in_label = False
    label_lines = []
    base_indent = 0

    for line in all_lines:
        if not in_label:
            if regex_label.search(line):
                in_label = True
                base_indent = len(line) - len(line.lstrip())
                label_lines.append(line)
        else:
            cur_indent = len(line) - len(line.lstrip())
            # Если встретили новую метку на том же или меньшем уровне отступа - конец текущей метки
            if line.strip() and cur_indent <= base_indent and regex_any_label.search(line):
                break
            label_lines.append(line)
            # Если встретили return на уровне метки
            if regex_return.search(line) and cur_indent <= base_indent + 4:
                break

    return label_lines if in_label else None

def process_lines(lines, filepath, outfile, depth=0):
    """
    Обрабатывает переданные строки файла.
    Если находит call -> ищет метку -> рекурсивно вставляет ее тело до return.
    """
    if depth > 10:
        outfile.write("\n[!!! ПРЕДУПРЕЖДЕНИЕ: Слишком глубокая вложенность (LOOP?) !!!]\n")
        return

    regex_call = re.compile(r'^\s*call\s+(?!screen\b)([a-zA-Z0-9_]+)')
    indent = "    " * depth
    short_name = os.path.basename(filepath)

    outfile.write(f"\n{indent}{'='*15} [{short_name}] {'='*15}\n")

    for line in lines:
        match_call = regex_call.search(line)
        if match_call:
            called_label = match_call.group(1)
            if called_label in label_map:
                target_file = label_map[called_label]
                if os.path.abspath(target_file) == os.path.abspath(filepath):
                    outfile.write(line)
                else:
                    outfile.write(f"\n{indent}>>> CALL: {called_label} (Файл: {os.path.basename(target_file)}) >>>\n")
                    target_lines = extract_label_lines(target_file, called_label)
                    if target_lines:
                        process_lines(target_lines, target_file, outfile, depth + 1)
                    else:
                        process_file(target_file, outfile, depth + 1)
                    outfile.write(f"{indent}<<< RETURN: {called_label} <<<\n\n")
            else:
                outfile.write(line)
        else:
            outfile.write(line)

    outfile.write(f"\n{indent}{'='*15} [КОНЕЦ: {short_name}] {'='*15}\n")

def process_file(filepath, outfile, depth=0):
    """
    Читает файл целиком и передает его строки в process_lines.
    """
    if not os.path.exists(filepath):
        outfile.write(f"\n[!!! ОШИБКА: Файл не найден: {filepath} !!!]\n")
        print(f"Не найден: {filepath}")
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        outfile.write(f"\n[!!! ОШИБКА ЧТЕНИЯ: {e} !!!]\n")
        return

    process_lines(lines, filepath, outfile, depth)

def build_chapter(chapter_name, output_path=None):
    """
    Собирает указанную главу в текстовый файл.
    """
    if chapter_name not in CHAPTERS_DB:
        print(f"[ОШИБКА] Глава '{chapter_name}' не найдена в базе.")
        print(f"Доступные главы: {', '.join(CHAPTERS_DB.keys())}")
        return False

    file_list = CHAPTERS_DB[chapter_name]
    if output_path is None:
        filename = f"Full_{chapter_name}.txt"
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

    print(f"--- Сборка главы {chapter_name} -> {os.path.basename(output_path)} ---")

    try:
        with open(output_path, 'w', encoding='utf-8') as outfile:
            outfile.write(f"СБОРКА: {chapter_name}\n\n")
            for rel_path in file_list:
                full_path = get_abs_path(rel_path)
                print(f"  Обработка: {rel_path}")
                process_file(full_path, outfile)
                outfile.write("\n\n")
        print(f"[УСПЕХ] Файл сохранен: {output_path}\n")
        return True
    except Exception as e:
        print(f"[Критическая ошибка]: {e}\n")
        return False

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Ren'Py Script to Full Text Converter")
    parser.add_argument(
        "--chapter", "-c",
        default="chapter8",
        help="Chapter to convert (e.g. chapter1, chapter8, or 'all'). Default: chapter8"
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Custom output filename or directory"
    )

    args = parser.parse_args()

    # 1. Сканируем все файлы проекта
    scan_all_scripts()

    # 2. Сборка выбранной главы или всех глав
    if args.chapter.lower() == "all":
        print("=== Пакетная сборка всех глав ===")
        for ch in CHAPTERS_DB.keys():
            out = None
            if args.output and os.path.isdir(args.output):
                out = os.path.join(args.output, f"Full_{ch}.txt")
            build_chapter(ch, out)
    else:
        build_chapter(args.chapter, args.output)

if __name__ == "__main__":
    main()