init -1 python:
    # Структура: (Имя, Код языка, Путь к флагу)
    # Код None = Язык по умолчанию (обычно тот, на котором написан скрипт)
    
    # Рекомендую скачать иконки флагов (например, 64x64) и положить в game/gui/flags/
    
    LANGUAGE_LIST = [
        {
            "name": "Русский 🇷🇺", 
            "code": None, 
            "flag": "gui/flags/ru.png", 
            "font": "fonts/WDXLLubrifontTC-Regular.ttf"
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
    # Обновлять вручную перед релизом!!
    TRANSLATION_STATUS = {
    None: 100,
    "english_us": 95,
}

    def get_lang_progress(code):
        return TRANSLATION_STATUS.get(code, 0)