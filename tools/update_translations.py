# update_translations.py (Запускать через Python на компьютере разработчика)
import requests
import re

# --- НАСТРОЙКИ ---
PROJECT_ID = "853084"
API_TOKEN = "HIDDEN"
FILE_TO_UPDATE = "game/modules/language/language_setup.rpy"

# Маппинг: Код Crowdin -> Код RenPy
# (В Crowdin часто коды типа 'en', 'ru', а в RenPy 'english_us')
CODE_MAP = {
    "ru": None,         # Исходный язык
    "en": "english_us",
}

def get_crowdin_stats():
    url = f"https://api.crowdin.com/api/v2/projects/{PROJECT_ID}/languages/progress"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    
    print("Запрос к Crowdin...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Ошибка API: {response.status_code} - {response.text}")
            return None
        
        data = response.json().get('data', [])
        stats = {}
        
        for item in data:
            c_code = item['data']['languageId']
            percent = item['data']['translationProgress']
            
            # Соответствие в карте, иначе оставляем код как есть
            renpy_code = CODE_MAP.get(c_code, c_code)
            stats[renpy_code] = percent
            
        # Родной язык всегда 100%
        stats[None] = 100
        return stats

    except Exception as e:
            print(f"Ошибка соединения: {e}")
            return None

def format_for_renpy(stats):
    """
    Превращает словарь в строку валидного Python-кода для RenPy.
    JSON тут не подходит, так как None должен быть без кавычек.
    """
    lines = []
    lines.append("TRANSLATION_STATUS = {")
    
    # None (родной язык), чтобы был сверху
    if None in stats:
        lines.append(f"    None: {stats[None]},")
        
    # Сортируем остальные ключи для красоты
    sorted_keys = sorted([k for k in stats.keys() if k is not None])
    
    for key in sorted_keys:
        value = stats[key]
        # Ключи-строки оборачиваем в кавычки
        lines.append(f'    "{key}": {value},')
        
    lines.append("}")
    return "\n".join(lines)

def update_renpy_file(stats):
    try:
        with open(FILE_TO_UPDATE, "r", encoding="utf-8") as f:
            content = f.read()
            

        # Формируем новую строку словаря
        # Выглядеть будет так: TRANSLATION_STATUS = { None: 100, "english_us": 45, ... }
        new_dict_str = format_for_renpy(stats)
        
        # Ищем старый словарь и заменяем его (используем RegEx)
        # Ищем от 'TRANSLATION_STATUS =' до закрывающей скобки '}'
        pattern = r"TRANSLATION_STATUS\s*=\s*\{.*?\}"

        if not re.search(pattern, content, flags=re.DOTALL):
                print("ОШИБКА: Не найдена переменная TRANSLATION_STATUS в файле!")
                return
        
        new_content = re.sub(pattern, new_dict_str, content, flags=re.DOTALL)
        
        with open(FILE_TO_UPDATE, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        print(f"УСПЕХ! Файл {FILE_TO_UPDATE} обновлен.")
        print("-" * 20)
        print(new_dict_str)
        print("-" * 20)
            
    except FileNotFoundError:
        print(f"ОШИБКА: Файл {FILE_TO_UPDATE} не найден.")


if __name__ == "__main__":
    print("--- Start Update ---")
    stats = get_crowdin_stats()
    if stats:
        print(f"Получены данные: {stats}")
        update_renpy_file(stats)
    else:
        print("Не удалось получить данные.")