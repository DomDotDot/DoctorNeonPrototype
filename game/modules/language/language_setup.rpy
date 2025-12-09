# Список доступных языков (Имя, Код Языка)
# Имя без _(), чтобы оно всегда отображалось одинаково на первом экране

init python:
    LANGUAGE_LIST = [
        ("Русский 🇷🇺", None), # None - это язык по умолчанию
        ("English 🇺🇸", "english_us")
    ]


init -1 python:
    # Структура: (Имя, Код языка, Путь к флагу)
    # Код None = Язык по умолчанию (обычно тот, на котором написан скрипт)
    
    # Рекомендую скачать иконки флагов (например, 64x64) и положить в game/gui/flags/
    
    LANGUAGE_LIST = [
        {
            "name": "Русский 🇷🇺", 
            "code": None, 
            "flag": "gui/flags/ru.png", 
            "font": "fonts/WDXLLubrifontTC-Regular.ttf
        },
        {
            "name": "English 🇺🇸", 
            "code": "english_us", 
            "flag": "gui/flags/us.png",
            "font": "DejaVuSans.ttf" 
        },
        # Пример будущего языка
        # { "name": "Español", "code": "spanish", "flag": "gui/flags/es.png", "font": "..." },
    ]

    # Словарь процентов готовности. 
    # Обновлять скриптом или вручную перед релизом!!
    TRANSLATION_STATUS = {
        None: 100,          # Родной язык всегда 100%
        "english_us": 45,   # Пример: переведено на 45%
        "spanish": 0
    }

    def get_lang_progress(code):
        return TRANSLATION_STATUS.get(code, 0)