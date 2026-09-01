#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ren'Py Script & Dialogue Stats Auto-Linter
==========================================
Scans Ren'Py script files, computes lines and word statistics for each character
and chapter, and generates badges and statistics tables in README.md and README.ru.md.

Usage:
    python tools/script_stats_linter.py [options]

Options:
    --update        Update README.md and README.ru.md (default)
    --check         Linter / CI mode: check if README files are up to date
    --json          Output results as JSON to stdout
    --silent        Do not print report to console
    --help, -h      Show this help message
"""

import os
import sys
import re
import json
import argparse
from collections import defaultdict

# Root directory of the repository
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, "game", "game-scripts")
README_EN_PATH = os.path.join(BASE_DIR, "README.md")
README_RU_PATH = os.path.join(BASE_DIR, "README.ru.md")

# Character definitions metadata (ID -> Russian name, English name, Color, Role)
CHARACTERS_DB = {
    # Main Cast
    "neon": {"ru": "Неон", "en": "Neon", "color": "1f4bc4", "role": "main"},
    "argon": {"ru": "Аргон", "en": "Argon", "color": "457632", "role": "main"},
    "oganesson": {"ru": "Оганессон (Опекунша)", "en": "Oganesson (Guardian)", "color": "663399", "role": "main"},
    "seraphina": {"ru": "Серафина", "en": "Seraphina", "color": "f2dbbb", "role": "main"},
    "lily": {"ru": "Лили", "en": "Lily", "color": "c16a19", "role": "main"},
    "alex": {"ru": "Алекс", "en": "Alex", "color": "b41f5d", "role": "main"},
    "celeste": {"ru": "Селестия", "en": "Celeste", "color": "7f9ae4", "role": "main"},

    # Supporting Cast
    "marcus": {"ru": "Маркус", "en": "Marcus", "color": "967230", "role": "supporting"},
    "nari": {"ru": "Нари", "en": "Nari", "color": "863b97", "role": "supporting"},
    "radon": {"ru": "Радон", "en": "Radon", "color": "c04547", "role": "supporting"},
    "helium": {"ru": "Гелий", "en": "Helium", "color": "e6af2e", "role": "supporting"},
    "krypton": {"ru": "Криптон", "en": "Krypton", "color": "b41f1f", "role": "supporting"},
    "xenon": {"ru": "Ксенон", "en": "Xenon", "color": "1f90c4", "role": "supporting"},
    "akane": {"ru": "Аканэ (Мама)", "en": "Akane (Mother)", "color": "e87a90", "role": "supporting"},
    "anna": {"ru": "Анна", "en": "Anna", "color": "d96411", "role": "supporting"},
    "sophie": {"ru": "Софи", "en": "Sophie", "color": "d1c682", "role": "supporting"},
    "meryl": {"ru": "Мэрил Кендрик", "en": "Meryl Kendrick", "color": "e87a90", "role": "supporting"},
    "akari": {"ru": "Учительница Акари", "en": "Teacher Akari", "color": "1885c8", "role": "supporting"},
    "sibyl": {"ru": "СИВИЛЛА", "en": "Sibyl", "color": "663399", "role": "supporting"},

    # Special / System Cast
    "oganesson_young": {"ru": "Оганессон (в молодости)", "en": "Young Oganesson", "color": "390482", "role": "special"},
    "celeste_ghost": {"ru": "Селестия (Призрак)", "en": "Celeste (Phantom)", "color": "7f9ae4", "role": "special"},
    "absolute_silence": {"ru": "Абсолютная Тишина", "en": "Absolute Silence", "color": "5c6bc0", "role": "special"},
    "fcs": {"ru": "АБСУ", "en": "ABSU / FCS", "color": "a30e0e", "role": "special"},
    "unknown": {"ru": "Неизвестный", "en": "Unknown", "color": "9e9e9e", "role": "special"},
    "unknown_f": {"ru": "Неизвестная", "en": "Unknown Female", "color": "9e9e9e", "role": "special"},
    "unknown_char": {"ru": "???", "en": "???", "color": "9e9e9e", "role": "special"},
    "Девушка": {"ru": "Девушка (Неон)", "en": "Girl (Neon)", "color": "1f4bc4", "role": "special"},
    "Голос": {"ru": "Голос", "en": "Voice", "color": "9e9e9e", "role": "special"},
    "Мужчина": {"ru": "Мужчина", "en": "Man", "color": "9e9e9e", "role": "special"},
    "Толпа": {"ru": "Толпа", "en": "Crowd", "color": "9e9e9e", "role": "special"},
    "Система": {"ru": "Система", "en": "System", "color": "9e9e9e", "role": "special"},

    # Narrator
    "narrator": {"ru": "Рассказчик (Описания)", "en": "Narrator / Description", "color": "708090", "role": "narrator"},
    "narrator_nvl": {"ru": "Рассказчик (NVL)", "en": "Narrator (NVL)", "color": "708090", "role": "narrator"},

    # Episodic / Minor Characters
    "father": {"ru": "Папа", "en": "Father", "color": "5a7a8d", "role": "episodic"},
    "hans": {"ru": "Ханс", "en": "Hans", "color": "7a7a7a", "role": "episodic"},
    "ceo": {"ru": "Г-н Бауманн (CEO)", "en": "Mr. Baumann (CEO)", "color": "305a96", "role": "episodic"},
    "cro": {"ru": "Д-р Грубенманн (CRO)", "en": "Dr. Grubenmann (CRO)", "color": "753636", "role": "episodic"},
    "headteacher": {"ru": "Завуч", "en": "Headteacher", "color": "808080", "role": "episodic"},
    "kai": {"ru": "Кай Ито", "en": "Kai Ito", "color": "5d19c9", "role": "episodic"},
    "illusion": {"ru": "Сущность", "en": "Entity / Illusion", "color": "863b97", "role": "episodic"},
    "student1": {"ru": "Студентка 1 (Эми)", "en": "Student 1 (Amy)", "color": "d4ad4b", "role": "episodic"},
    "amy": {"ru": "Эми", "en": "Amy", "color": "d4ad4b", "role": "episodic"},
    "student2": {"ru": "Студентка 2 (Кэрол)", "en": "Student 2 (Carol)", "color": "33dad4", "role": "episodic"},
    "carol": {"ru": "Кэрол", "en": "Carol", "color": "33dad4", "role": "episodic"},
    "clara": {"ru": "Клара", "en": "Clara", "color": "bc040d", "role": "episodic"},
    "mika": {"ru": "Мика Китамура", "en": "Mika Kitamura", "color": "d1289e", "role": "episodic"},
    "guts": {"ru": "Гатс", "en": "Guts", "color": "8b4513", "role": "episodic"},
    "rico": {"ru": "Рико", "en": "Rico", "color": "a56a44", "role": "episodic"},
    "boss": {"ru": "Босс", "en": "Boss", "color": "b22222", "role": "episodic"},
    "Священник": {"ru": "Священник", "en": "Priest", "color": "9e9e9e", "role": "episodic"},
    "Сотрудник Сада": {"ru": "Сотрудник Сада", "en": "Garden Staff", "color": "9e9e9e", "role": "episodic"},
    "Охранник": {"ru": "Охранник", "en": "Guard", "color": "9e9e9e", "role": "episodic"},
    "Продавец": {"ru": "Продавец", "en": "Vendor", "color": "9e9e9e", "role": "episodic"},
    "Консьерж": {"ru": "Консьерж", "en": "Concierge", "color": "9e9e9e", "role": "episodic"},
    "Консьержка": {"ru": "Консьержка", "en": "Concierge (Female)", "color": "9e9e9e", "role": "episodic"},
    "Официантка": {"ru": "Официантка", "en": "Waitress", "color": "9e9e9e", "role": "episodic"},
    "Бандит 2": {"ru": "Бандит 2", "en": "Bandit 2", "color": "9e9e9e", "role": "episodic"},
    "Работник бара": {"ru": "Работник бара", "en": "Bartender Staff", "color": "9e9e9e", "role": "episodic"},
    "Маленькая Хошико": {"ru": "Маленькая Хошико", "en": "Young Hoshiko", "color": "9e9e9e", "role": "episodic"},
    "Автоматон": {"ru": "Автоматон", "en": "Automaton", "color": "9e9e9e", "role": "episodic"},
    "Старик": {"ru": "Старик", "en": "Old Man", "color": "9e9e9e", "role": "episodic"},
    "Вышибала": {"ru": "Вышибала", "en": "Bouncer", "color": "9e9e9e", "role": "episodic"},
    "Бандит 1": {"ru": "Бандит 1", "en": "Bandit 1", "color": "9e9e9e", "role": "episodic"},
    "Бармен": {"ru": "Бармен", "en": "Bartender", "color": "9e9e9e", "role": "episodic"},
    "Диктор": {"ru": "Диктор", "en": "Anchorman", "color": "9e9e9e", "role": "episodic"},
    "Физручка": {"ru": "Физручка", "en": "P.E. Teacher", "color": "9e9e9e", "role": "episodic"},
    "Мама Алекс": {"ru": "Мама Алекс", "en": "Alex's Mom", "color": "9e9e9e", "role": "episodic"},
    "Ода": {"ru": "Ода", "en": "Oda", "color": "9e9e9e", "role": "episodic"},
    "Ведущая Новостей": {"ru": "Ведущая Новостей", "en": "News Anchor", "color": "9e9e9e", "role": "episodic"},
    "Маленькая Алекс": {"ru": "Маленькая Алекс", "en": "Young Alex", "color": "9e9e9e", "role": "episodic"},
    "Рабочий 1": {"ru": "Рабочий 1", "en": "Worker 1", "color": "9e9e9e", "role": "episodic"},
    "Рабочий 2": {"ru": "Рабочий 2", "en": "Worker 2", "color": "9e9e9e", "role": "episodic"},
    "Женщина": {"ru": "Женщина", "en": "Woman", "color": "9e9e9e", "role": "episodic"},
    "Исикава-сенсей": {"ru": "Исикава-сенсей", "en": "Ishikawa-sensei", "color": "9e9e9e", "role": "episodic"},
    "Директор": {"ru": "Директор Академии", "en": "Academy Director", "color": "9e9e9e", "role": "episodic"},
    "Капитан Охраны": {"ru": "Капитан Охраны", "en": "Security Captain", "color": "9e9e9e", "role": "episodic"},
    "Командир Охраны": {"ru": "Командир Охраны", "en": "Security Commander", "color": "9e9e9e", "role": "episodic"},
    "Командир Наёмников": {"ru": "Командир Наёмников", "en": "Mercenary Commander", "color": "9e9e9e", "role": "episodic"},
    "Командир": {"ru": "Командир", "en": "Commander", "color": "9e9e9e", "role": "episodic"},
    "Студентка А": {"ru": "Студентка А", "en": "Student A", "color": "9e9e9e", "role": "episodic"},
    "Студентка Б": {"ru": "Студентка Б", "en": "Student B", "color": "9e9e9e", "role": "episodic"},
    "Студентка В": {"ru": "Студентка В", "en": "Student C", "color": "9e9e9e", "role": "episodic"},
    "Студент 1": {"ru": "Студент 1", "en": "Student 1", "color": "9e9e9e", "role": "episodic"},
    "Студентка 1": {"ru": "Студентка 1", "en": "Student 1 (Girl)", "color": "9e9e9e", "role": "episodic"},
    "Студенты": {"ru": "Студенты", "en": "Students", "color": "9e9e9e", "role": "episodic"},
    "Соседка по парте": {"ru": "Соседка по парте", "en": "Desk Neighbor", "color": "9e9e9e", "role": "episodic"},
    "Фанатка 1": {"ru": "Фанатка 1", "en": "Fan 1", "color": "9e9e9e", "role": "episodic"},
    "Фанатка 2": {"ru": "Фанатка 2", "en": "Fan 2", "color": "9e9e9e", "role": "episodic"},
    "Фанатка 3": {"ru": "Фанатка 3", "en": "Fan 3", "color": "9e9e9e", "role": "episodic"},
    "Фанатка 4": {"ru": "Фанатка 4", "en": "Fan 4", "color": "9e9e9e", "role": "episodic"},
    "Фанатка 5": {"ru": "Фанатка 5", "en": "Fan 5", "color": "9e9e9e", "role": "episodic"},
    "Офицер контроля": {"ru": "Офицер контроля", "en": "Control Officer", "color": "9e9e9e", "role": "episodic"},
    "Офицер СБ": {"ru": "Офицер СБ", "en": "Security Officer", "color": "9e9e9e", "role": "episodic"},
    "Консультант": {"ru": "Консультант", "en": "Consultant", "color": "9e9e9e", "role": "episodic"},
    "Навигатор": {"ru": "Навигатор", "en": "Navigator", "color": "9e9e9e", "role": "episodic"},
    "Водитель": {"ru": "Водитель", "en": "Driver", "color": "9e9e9e", "role": "episodic"},
    "Голос CEO": {"ru": "Голос CEO", "en": "CEO's Voice", "color": "9e9e9e", "role": "episodic"},
    "Медробот": {"ru": "Медробот", "en": "Medrobot", "color": "9e9e9e", "role": "episodic"},
    "Голос Акционера 1": {"ru": "Голос Акционера 1", "en": "Shareholder 1's Voice", "color": "9e9e9e", "role": "episodic"},
    "Голос Акционера 2": {"ru": "Голос Акционера 2", "en": "Shareholder 2's Voice", "color": "9e9e9e", "role": "episodic"},
    "Акционер 1": {"ru": "Акционер 1", "en": "Shareholder 1", "color": "9e9e9e", "role": "episodic"},
    "Пассажир": {"ru": "Пассажир", "en": "Passenger", "color": "9e9e9e", "role": "episodic"},
    "Задира 1": {"ru": "Задира 1", "en": "Bully 1", "color": "9e9e9e", "role": "episodic"},
    "Задира 2": {"ru": "Задира 2", "en": "Bully 2", "color": "9e9e9e", "role": "episodic"},
    "Мальчик": {"ru": "Мальчик", "en": "Boy", "color": "9e9e9e", "role": "episodic"},
    "Голос Охранника": {"ru": "Голос Охранника", "en": "Guard's Voice", "color": "9e9e9e", "role": "episodic"},
    "Телохранитель": {"ru": "Телохранитель", "en": "Bodyguard", "color": "9e9e9e", "role": "episodic"},
    "Прохожий": {"ru": "Прохожий", "en": "Passerby", "color": "9e9e9e", "role": "episodic"},
    "Курьер": {"ru": "Курьер", "en": "Courier", "color": "9e9e9e", "role": "episodic"},
}

# Speaker alias mapping (e.g. Russian display names or alternate keys -> canonical DB IDs)
SPEAKER_ALIASES = {
    "Нари": "nari",
    "Селестия": "celeste",
    "Клара": "clara",
    "CEO": "ceo",
    "???": "unknown_char",
    "ОФициантка": "Официантка",
    "Ведущая новостей": "Ведущая Новостей",
    "Директор Акад.": "Директор",
    "Командир Наемников": "Командир Наёмников",
}

# Chapter display names
CHAPTERS_METADATA = {
    "chapter1": {"ru": "Глава 1: Синяя Ворона", "en": "Chapter 1: The Blue Sheep", "order": 1},
    "chapter2": {"ru": "Глава 2: В Поисках Подруги", "en": "Chapter 2: In Search of A Friend", "order": 2},
    "chapter3": {"ru": "Глава 3: Эскапизм", "en": "Chapter 3: Escapism", "order": 3},
    "chapter4.0": {"ru": "Глава 4.0: Ковчег на мели", "en": "Chapter 4.0: Ark Aground", "order": 4},
    "chapter4.5": {"ru": "Глава 4.5: Из Изгнанницы в Созвездие", "en": "Chapter 4.5: From Exile to Constellation", "order": 5},
    "chapter5": {"ru": "Глава 5: Предложение, от которого нельзя отказаться", "en": "Chapter 5: An Offer You Can’t Refuse", "order": 6},
    "chapter6": {"ru": "Глава 6: Первый ряд, Пятое место", "en": "Chapter 6: First row. Fifth seat.", "order": 7},
    "chapter7": {"ru": "Глава 7: Туман Войны", "en": "Chapter 7: Fog of War", "order": 8},
    "chapter8": {"ru": "Глава 8: Школьные… дни?", "en": "Chapter 8: School Days...?", "order": 9},
    "chapter9": {"ru": "Глава 9: Резонирующий Диссонанс", "en": "Chapter 9: Resonating Dissonance", "order": 10},
    "flashbacks": {"ru": "Воспоминания и Фрагменты", "en": "Flashbacks & Memory Fragments", "order": 11},
}

# Non-dialogue property names often found in Ren'Py style / screen definitions
STYLE_PROPERTIES = {
    'color', 'hover_color', 'background', 'hover_background', 'selected_color',
    'insensitive_color', 'idle_color', 'font', 'size', 'align', 'xalign', 'yalign',
    'pos', 'xpos', 'ypos', 'anchor', 'xanchor', 'yanchor', 'padding', 'margin',
    'spacing', 'outlines', 'text_color', 'sound', 'music', 'voice', 'hover_sound',
    'activate_sound', 'selected_idle_color', 'selected_hover_color', 'thumb', 'hover_thumb',
    'idle_thumb', 'bar_invert', 'bar_vertical', 'unscrollable'
}

# Ren'Py statement keywords to ignore when identifying speakers
RENPY_KEYWORDS = {
    'scene', 'show', 'hide', 'play', 'stop', 'queue', 'voice', 'sound', 
    'label', 'call', 'jump', 'return', 'if', 'elif', 'else', 'while', 
    'python', 'init', 'transform', 'image', 'screen', 'style', 'default', 
    'define', 'window', 'pause', 'with', 'camera', 'menu', 'pass', 'translate',
    'renpy', 'nvl', 'extend', 'set', 'text', 'hbox', 'vbox', 'frame', 'button',
    'textbutton', 'imagebutton', 'action', 'timer', 'key', 'null', 'has', 'use',
    'drag', 'draggroup', 'viewport', 'vpgrid', 'side', 'grid', 'fixed', 'add',
    'on', 'hotspot', 'hotbar', 'bar', 'vbar', 'input', 'dismiss', 'mousearea'
}

FILE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.webp', '.opus', '.mp3', '.ogg', '.wav', '.ttf', '.otf', '.woff')

TAG_REGEX = re.compile(r'\{[^\}]*\}')
WORD_REGEX = re.compile(r"[\wА-Яа-яЁё\-]+", re.UNICODE)

def is_dialogue_text(text: str) -> bool:
    """Checks whether string content is meaningful dialogue or code artifact."""
    text = text.strip()
    if not text:
        return False
    # Check if text is a hex color code
    if re.match(r'^#[0-9a-fA-F]{3,8}$', text):
        return False
    # Check if text is a file path
    if any(text.lower().endswith(ext) for ext in FILE_EXTENSIONS) or text.startswith(('audio/', 'music/', 'sfx/', 'ambient/', 'images/', 'gui/')):
        return False
    return True

def clean_dialogue_text(text: str) -> str:
    """Removes Ren'Py tags, markup and unescapes text."""
    text = TAG_REGEX.sub('', text)
    text = text.replace('\\"', '"').replace("\\'", "'").replace('\\n', ' ').replace('\t', ' ')
    return text.strip()

def count_words_in_text(text: str) -> int:
    """Counts words in a cleaned dialogue string."""
    cleaned = clean_dialogue_text(text)
    words = WORD_REGEX.findall(cleaned)
    return len(words)

def parse_rpy_file(filepath: str):
    """
    Parses an .rpy file extracting (speaker, text) tuples for dialogue and narration.
    Handles single-line and multi-line strings (triple quotes) accurately.
    """
    results = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"[Warning] Failed to read {filepath}: {e}", file=sys.stderr)
        return results

    i = 0
    in_multiline = False
    multiline_speaker = None
    multiline_buffer = []

    while i < len(lines):
        raw_line = lines[i]
        line = raw_line.strip()
        i += 1

        if in_multiline:
            if '"""' in line or "'''" in line:
                quote_delim = '"""' if '"""' in line else "'''"
                idx = line.find(quote_delim)
                multiline_buffer.append(line[:idx])
                full_text = "\n".join(multiline_buffer)
                if is_dialogue_text(full_text):
                    results.append((multiline_speaker, full_text))
                in_multiline = False
                multiline_speaker = None
                multiline_buffer = []
            else:
                multiline_buffer.append(line)
            continue

        if not line or line.startswith('#'):
            continue

        first_word = line.split()[0].rstrip(':') if line.split() else ''
        if line.startswith('$') or first_word in RENPY_KEYWORDS or first_word in STYLE_PROPERTIES:
            continue

        # Triple-quoted multi-line or single-line
        if '"""' in line or "'''" in line:
            quote_delim = '"""' if '"""' in line else "'''"
            before_quote, _, rest = line.partition(quote_delim)
            speaker_str = before_quote.strip()

            if not speaker_str:
                speaker = "narrator"
            else:
                if speaker_str.startswith('"') and speaker_str.endswith('"'):
                    speaker = speaker_str[1:-1]
                else:
                    speaker = speaker_str.split()[0]

            if quote_delim in rest:
                content = rest[:rest.find(quote_delim)]
                if is_dialogue_text(content):
                    results.append((speaker, content))
            else:
                in_multiline = True
                multiline_speaker = speaker
                multiline_buffer = [rest]
            continue

        # Pattern 1: "Speaker Name" "Dialogue text"
        m1 = re.match(r'^"([^"\\]*(?:\\.[^"\\]*)*)"\s+"((?:[^"\\]|\\.)*)"', line)
        if m1:
            speaker, text = m1.group(1), m1.group(2)
            if is_dialogue_text(text):
                results.append((speaker, text))
            continue

        # Pattern 2: "Dialogue text" (narration)
        m2 = re.match(r'^"((?:[^"\\]|\\.)*)"', line)
        if m2:
            text = m2.group(1)
            if is_dialogue_text(text):
                results.append(("narrator", text))
            continue

        # Pattern 3: speaker_id [attributes] "Dialogue text"
        m3 = re.match(r'^([a-zA-Z0-9_]+)(?:\s+[^"]*)?\s+"((?:[^"\\]|\\.)*)"', line)
        if m3:
            spk = m3.group(1)
            text = m3.group(2)
            if spk not in RENPY_KEYWORDS and spk not in STYLE_PROPERTIES:
                if is_dialogue_text(text):
                    results.append((spk, text))
                continue

    return results

def get_chapter_key(rel_path: str) -> str:
    """Classifies a relative file path to its corresponding chapter key."""
    rel_norm = rel_path.replace("\\", "/")
    if rel_norm.startswith("chapters/"):
        parts = rel_norm.split("/")
        return parts[1]  # e.g., chapter1, chapter2, chapter4.5, etc.
    elif rel_norm.startswith("flashbacks/"):
        return "flashbacks"
    return "other"

def analyze_project_scripts(scripts_dir: str = SCRIPTS_DIR):
    """
    Scans and analyzes all .rpy files under game-scripts.
    Returns aggregated stats per character, per chapter, and totals.
    """
    if not os.path.exists(scripts_dir):
        raise FileNotFoundError(f"Scripts directory not found: {scripts_dir}")

    total_stats = {
        "total_lines": 0,
        "total_words": 0,
        "narration_lines": 0,
        "narration_words": 0,
        "dialogue_lines": 0,
        "dialogue_words": 0,
        "total_files": 0,
    }

    chapter_stats = defaultdict(lambda: {
        "lines": 0,
        "words": 0,
        "narration_lines": 0,
        "narration_words": 0,
        "dialogue_lines": 0,
        "dialogue_words": 0,
        "files_count": 0,
        "characters": defaultdict(lambda: {"lines": 0, "words": 0})
    })

    character_stats = defaultdict(lambda: {
        "lines": 0,
        "words": 0,
        "chapters": set()
    })

    for root, _, files in os.walk(scripts_dir):
        for file in files:
            if not file.endswith(".rpy"):
                continue

            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, scripts_dir)
            chap_key = get_chapter_key(rel_path)

            dialogues = parse_rpy_file(full_path)
            total_stats["total_files"] += 1
            chapter_stats[chap_key]["files_count"] += 1

            for speaker, text in dialogues:
                speaker = SPEAKER_ALIASES.get(speaker, speaker)
                words = count_words_in_text(text)
                total_stats["total_lines"] += 1
                total_stats["total_words"] += words

                is_narration = (speaker in ("narrator", "narrator_nvl"))
                if is_narration:
                    total_stats["narration_lines"] += 1
                    total_stats["narration_words"] += words
                    chapter_stats[chap_key]["narration_lines"] += 1
                    chapter_stats[chap_key]["narration_words"] += words
                else:
                    total_stats["dialogue_lines"] += 1
                    total_stats["dialogue_words"] += words
                    chapter_stats[chap_key]["dialogue_lines"] += 1
                    chapter_stats[chap_key]["dialogue_words"] += words

                chapter_stats[chap_key]["lines"] += 1
                chapter_stats[chap_key]["words"] += words
                chapter_stats[chap_key]["characters"][speaker]["lines"] += 1
                chapter_stats[chap_key]["characters"][speaker]["words"] += words

                character_stats[speaker]["lines"] += 1
                character_stats[speaker]["words"] += words
                character_stats[speaker]["chapters"].add(chap_key)

    # Convert sets to serializable lists
    for spk in character_stats:
        character_stats[spk]["chapters"] = sorted(list(character_stats[spk]["chapters"]))

    return {
        "totals": total_stats,
        "chapters": dict(chapter_stats),
        "characters": dict(character_stats)
    }

def format_number(n: int) -> str:
    """Formats numbers with space separation for readability."""
    return f"{n:,}".replace(",", " ")

def generate_progress_bar(percentage: float, length: int = 10) -> str:
    """Generates an ASCII progress bar."""
    filled = int(round(length * (percentage / 100.0)))
    filled = min(max(filled, 0), length)
    return "█" * filled + "░" * (length - filled)

def get_character_role(speaker_id: str) -> str:
    """Gets character role ('main', 'supporting', 'episodic', 'special', etc.)."""
    spk_key = SPEAKER_ALIASES.get(speaker_id, speaker_id)
    if spk_key in CHARACTERS_DB:
        return CHARACTERS_DB[spk_key].get("role", "episodic")
    return "episodic"

def get_character_display_name(speaker_id: str, lang: str = "ru") -> str:
    """Gets character localized name."""
    spk_key = SPEAKER_ALIASES.get(speaker_id, speaker_id)
    if spk_key in CHARACTERS_DB:
        return CHARACTERS_DB[spk_key].get(lang, speaker_id)
    return speaker_id

def generate_badges_md(data: dict, lang: str = "ru") -> str:
    """Generates shields.io badges for the top of the README."""
    totals = data["totals"]
    words_k = f"{totals['total_words'] / 1000.0:.1f}k"
    lines_formatted = format_number(totals["total_lines"]).replace(" ", "%20")
    
    dialogue_pct = (totals["dialogue_words"] / totals["total_words"] * 100) if totals["total_words"] else 0

    if lang == "ru":
        badge_words = f"![Слов](https://img.shields.io/badge/Слов-{words_k}-blue?style=flat-square&logo=gitbook&logoColor=white)"
        badge_lines = f"![Реплик](https://img.shields.io/badge/Реплик-{lines_formatted}-4c1?style=flat-square)"
        badge_chapters = f"![Глав](https://img.shields.io/badge/Глав-10%20-8a2be2?style=flat-square)"
        badge_ratio = f"![Диалоги](https://img.shields.io/badge/Диалоги-{dialogue_pct:.0f}%25-informational?style=flat-square)"
    else:
        badge_words = f"![Words](https://img.shields.io/badge/Words-{words_k}-blue?style=flat-square&logo=gitbook&logoColor=white)"
        badge_lines = f"![Lines](https://img.shields.io/badge/Lines-{lines_formatted}-4c1?style=flat-square)"
        badge_chapters = f"![Chapters](https://img.shields.io/badge/Chapters-10%20-8a2be2?style=flat-square)"
        badge_ratio = f"![Dialogue](https://img.shields.io/badge/Dialogue-{dialogue_pct:.0f}%25-informational?style=flat-square)"

    return f"{badge_words}\n{badge_lines}\n{badge_chapters}\n{badge_ratio}"

def generate_statistics_section(data: dict, lang: str = "ru") -> str:
    """Generates the full Markdown Statistics section with tables and metrics."""
    totals = data["totals"]
    chapters = data["chapters"]
    characters = data["characters"]

    if lang == "ru":
        title = "## Статистика сценария"
        summary_title = "### Общие показатели"
        chap_title = "### Детализация по главам"
        char_title = "### Реплики персонажей"
        
        col_chapter = "Глава"
        col_files = "Файлов"
        col_lines = "Реплик"
        col_words = "Слов"
        col_dialogue_share = "Доля диалогов"
        col_char_name = "Персонаж"
        col_share = "Доля слов"
        
        lbl_total_words = "Всего слов"
        lbl_total_lines = "Всего строк сценария"
        lbl_narration = "Текст описания (Рассказчик)"
        lbl_dialogue = "Прямая речь (Персонажи)"
        lbl_active_chars = "Уникальных говорящих"
        lbl_script_files = "Скриптовых файлов (.rpy)"
        lbl_all = "ИТОГО"
        unit_w = "сл."
        unit_l = "репл."
        extra_chars_title = "Дополнительные и эпизодические персонажи"
    else:
        title = "## Story & Script Statistics"
        summary_title = "### General Metrics"
        chap_title = "### Chapter Breakdown"
        char_title = "### Character Dialogue Distribution"
        
        col_chapter = "Chapter"
        col_files = "Files"
        col_lines = "Lines"
        col_words = "Words"
        col_dialogue_share = "Dialogue Share"
        col_char_name = "Character"
        col_share = "Word Share"
        
        lbl_total_words = "Total Words"
        lbl_total_lines = "Total Script Lines"
        lbl_narration = "Narration / Description"
        lbl_dialogue = "Spoken Dialogue (Characters)"
        lbl_active_chars = "Unique Speakers"
        lbl_script_files = "Script Files (.rpy)"
        lbl_all = "TOTAL"
        unit_w = "words"
        unit_l = "lines"
        extra_chars_title = "Additional and episodic characters"

    total_words = totals["total_words"]
    total_lines = totals["total_lines"]
    narr_pct = (totals["narration_words"] / total_words * 100) if total_words else 0
    dial_pct = (totals["dialogue_words"] / total_words * 100) if total_words else 0

    spoken_chars_count = len([c for c in characters.keys() if c not in ("narrator", "narrator_nvl")])

    # 1. Summary Block
    summary_md = f"""{title}

{summary_title}

| {('Метрика' if lang == 'ru' else 'Metric')} | {('Значение' if lang == 'ru' else 'Value')} | {('Соотношение' if lang == 'ru' else 'Ratio')} |
| :--- | :---: | :--- |
| **{lbl_total_words}** | **{format_number(total_words)}** | `100%` |
| **{lbl_total_lines}** | **{format_number(total_lines)}** | `100%` |
| {lbl_narration} | {format_number(totals['narration_words'])} {unit_w} / {format_number(totals['narration_lines'])} {unit_l} | `{narr_pct:.1f}%` {generate_progress_bar(narr_pct)} |
| {lbl_dialogue} | {format_number(totals['dialogue_words'])} {unit_w} / {format_number(totals['dialogue_lines'])} {unit_l} | `{dial_pct:.1f}%` {generate_progress_bar(dial_pct)} |
| {lbl_active_chars} | {spoken_chars_count} | — |
| {lbl_script_files} | {totals['total_files']} | — |
"""

    # 2. Chapter Breakdown Table
    sorted_chap_keys = sorted(
        chapters.keys(),
        key=lambda k: CHAPTERS_METADATA.get(k, {}).get("order", 99)
    )

    chap_rows = []
    for k in sorted_chap_keys:
        cdata = chapters[k]
        name = CHAPTERS_METADATA.get(k, {}).get(lang, k.capitalize())
        c_lines = cdata["lines"]
        c_words = cdata["words"]
        c_files = cdata["files_count"]
        c_dial_pct = (cdata["dialogue_words"] / c_words * 100) if c_words else 0
        chap_rows.append(
            f"| **{name}** | {c_files} | {format_number(c_lines)} | {format_number(c_words)} | `{c_dial_pct:.1f}%` {generate_progress_bar(c_dial_pct, 8)} |"
        )

    chap_table_md = f"""{chap_title}

| {col_chapter} | {col_files} | {col_lines} | {col_words} | {col_dialogue_share} |
| :--- | :---: | :---: | :---: | :--- |
{chr(10).join(chap_rows)}
| **{lbl_all}** | **{totals['total_files']}** | **{format_number(total_lines)}** | **{format_number(total_words)}** | `{dial_pct:.1f}%` |
"""

    # 3. Character Table (Separating main/supporting cast from episodic/additional characters into collapsible details)
    char_list = []
    for spk, sdata in characters.items():
        if spk in ("narrator", "narrator_nvl"):
            continue
        disp_name = get_character_display_name(spk, lang)
        role = get_character_role(spk)
        char_list.append((disp_name, sdata["lines"], sdata["words"], role))

    char_list.sort(key=lambda x: x[2], reverse=True)

    main_char_rows = []
    minor_char_rows = []
    dialogue_words_total = totals["dialogue_words"] if totals["dialogue_words"] else 1

    for name, c_lines, c_words, role in char_list:
        share = (c_words / dialogue_words_total) * 100
        bar = generate_progress_bar(share, 8)
        row_str = f"| **{name}** | {format_number(c_lines)} | {format_number(c_words)} | `{share:.1f}%` {bar} |"
        
        # Display main and supporting cast in the primary table; episodic / special in collapsible details
        if role in ("main", "supporting"):
            main_char_rows.append(row_str)
        else:
            minor_char_rows.append(row_str)

    char_table_md = f"""{char_title}

| {col_char_name} | {col_lines} | {col_words} | {col_share} ({'от всей речи' if lang == 'ru' else 'of dialogue'}) |
| :--- | :---: | :---: | :--- |
{chr(10).join(main_char_rows)}
"""

    if minor_char_rows:
        char_table_md += f"""
<details>
<summary><b>{extra_chars_title} ({len(minor_char_rows)})</b></summary>

| {col_char_name} | {col_lines} | {col_words} | {col_share} |
| :--- | :---: | :---: | :--- |
{chr(10).join(minor_char_rows)}

</details>
"""

    return f"{summary_md}\n{chap_table_md}\n{char_table_md}"

def update_readme_file(filepath: str, data: dict, lang: str = "ru", check_only: bool = False) -> bool:
    """
    Injects badges and statistics into a README file using standard HTML markers.
    Returns True if file was up to date / successfully updated, False if diff found in check_only mode.
    """
    if not os.path.exists(filepath):
        print(f"[Error] File not found: {filepath}", file=sys.stderr)
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update badges section
    badges_md = generate_badges_md(data, lang)
    badges_marker_start = "<!-- STATS_BADGES:START -->"
    badges_marker_end = "<!-- STATS_BADGES:END -->"

    if badges_marker_start in content and badges_marker_end in content:
        badge_pattern = re.compile(
            rf"{re.escape(badges_marker_start)}.*?{re.escape(badges_marker_end)}",
            re.DOTALL
        )
        new_badges_block = f"{badges_marker_start}\n{badges_md}\n{badges_marker_end}"
        content = badge_pattern.sub(new_badges_block, content)
    else:
        legacy_badge_marker = "<!-- БЕЙДЖИ -->" if lang == "ru" else "<!-- BADGES -->"
        if legacy_badge_marker in content:
            new_badges_block = f"{legacy_badge_marker}\n{badges_marker_start}\n{badges_md}\n{badges_marker_end}"
            content = content.replace(legacy_badge_marker, new_badges_block)
        else:
            lines = content.splitlines()
            new_lines = []
            inserted = False
            for line in lines:
                new_lines.append(line)
                if line.startswith("# ") and not inserted:
                    new_lines.append("")
                    new_lines.append(f"{badges_marker_start}\n{badges_md}\n{badges_marker_end}")
                    inserted = True
            content = "\n".join(new_lines)

    # 2. Update Statistics section
    stats_md = generate_statistics_section(data, lang)
    stats_marker_start = "<!-- SCRIPT_STATS:START -->"
    stats_marker_end = "<!-- SCRIPT_STATS:END -->"

    if stats_marker_start in content and stats_marker_end in content:
        stats_pattern = re.compile(
            rf"{re.escape(stats_marker_start)}.*?{re.escape(stats_marker_end)}",
            re.DOTALL
        )
        new_stats_block = f"{stats_marker_start}\n{stats_md}\n{stats_marker_end}"
        content = stats_pattern.sub(new_stats_block, content)
    else:
        license_header = "## 📜 Лицензия" if "## 📜 Лицензия" in content else ("## License" if "## License" in content else "## Структура" if "## Структура" in content else "## Project Structure")
        new_stats_block = f"\n---\n\n{stats_marker_start}\n{stats_md}\n{stats_marker_end}\n\n"
        if license_header in content:
            content = content.replace(license_header, f"{new_stats_block}{license_header}")
        else:
            content += f"\n{new_stats_block}\n"

    # Compare with existing file
    with open(filepath, 'r', encoding='utf-8') as f:
        old_content = f.read()

    if old_content.strip() == content.strip():
        return True

    if check_only:
        return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

def print_cli_summary(data: dict):
    """Prints a friendly summary report to console."""
    totals = data["totals"]
    print("=" * 60)
    print("  THE BRIGHTEST NEON - SCRIPT & DIALOGUE STATS")
    print("=" * 60)
    print(f"Total Words:        {format_number(totals['total_words'])}")
    print(f"Total Script Lines: {format_number(totals['total_lines'])}")
    print(f"Narration Words:    {format_number(totals['narration_words'])} ({totals['narration_words']/totals['total_words']*100:.1f}%)")
    print(f"Dialogue Words:     {format_number(totals['dialogue_words'])} ({totals['dialogue_words']/totals['total_words']*100:.1f}%)")
    print(f"Total .rpy Files:   {totals['total_files']}")
    print("-" * 60)
    print("Top Speakers by Spoken Words:")
    chars = [
        (get_character_display_name(k, "en"), v["lines"], v["words"])
        for k, v in data["characters"].items()
        if k not in ("narrator", "narrator_nvl")
    ]
    chars.sort(key=lambda x: x[2], reverse=True)
    for name, lines, words in chars[:12]:
        pct = words / totals['dialogue_words'] * 100 if totals['dialogue_words'] else 0
        print(f"  {name:25s} | {lines:5d} lines | {words:6d} words | {pct:4.1f}%")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="Ren'Py Script & Dialogue Stats Auto-Linter")
    parser.add_argument("--update", action="store_true", default=True, help="Update README files (default)")
    parser.add_argument("--check", action="store_true", help="Check if READMEs are up to date (returns exit code 1 if diff)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON data")
    parser.add_argument("--silent", action="store_true", help="Suppress console summary output")

    args = parser.parse_args()

    data = analyze_project_scripts(SCRIPTS_DIR)

    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return 0

    if not args.silent:
        print_cli_summary(data)

    if args.check:
        ru_ok = update_readme_file(README_RU_PATH, data, lang="ru", check_only=True)
        en_ok = update_readme_file(README_EN_PATH, data, lang="en", check_only=True)
        if ru_ok and en_ok:
            print("\n[OK] README.md and README.ru.md are up-to-date!")
            return 0
        else:
            print("\n[FAIL] README files are out-of-date! Run `python tools/script_stats_linter.py` to update.", file=sys.stderr)
            return 1
    else:
        ru_updated = update_readme_file(README_RU_PATH, data, lang="ru", check_only=False)
        en_updated = update_readme_file(README_EN_PATH, data, lang="en", check_only=False)
        print(f"\n[Updated] README.ru.md: {'Success' if ru_updated else 'Failed'}")
        print(f"[Updated] README.md:    {'Success' if en_updated else 'Failed'}")
        return 0

if __name__ == "__main__":
    sys.exit(main())
