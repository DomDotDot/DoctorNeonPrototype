# ==============================================================================
# Doctor Neon - Language Subsystem
# ==============================================================================

init -1 python:
    # Базовые официальные языки игры
    BASE_LANGUAGE_LIST = [
        {
            "name": "Русский",
            "native_name": "Русский",
            "sub_name": "Russian (Оригинал)",
            "code": None, 
            "flag": "gui/flags/ru.png", 
            "font": "fonts/WDXLLubrifontTC-Regular.ttf",
            "official": True,
            "progress": 100
        },
        {
            "name": "English", 
            "native_name": "English",
            "sub_name": "English (US)",
            "code": "english_us", 
            "flag": "gui/flags/us.png",
            "font": "DejaVuSans.ttf",
            "official": True,
            "progress": 95
        },
    ]

    TRANSLATION_STATUS = {
        None: 100,
        "english_us": 95,
    }

    def select_game_language(code):
        """Переключает язык игры, вызывает проверку достижений и обновляет экран."""
        renpy.change_language(code)
        if hasattr(store, "check_polyglot_on_lang_change"):
            try:
                check_polyglot_on_lang_change()
            except Exception as e:
                print(f"[LanguageSetup] Ошибка check_polyglot_on_lang_change: {e}")
        renpy.restart_interaction()

    def get_active_languages():
        """Возвращает список доступных языков с учетом активных коммьюнити-переводов."""
        langs = list(BASE_LANGUAGE_LIST)
        if hasattr(store, "get_active_community_translations"):
            try:
                comm_langs = get_active_community_translations()
                for cl in comm_langs:
                    if not any(x.get("code") == cl.get("code") for x in langs):
                        langs.append(cl)
            except Exception as e:
                print(f"[LanguageSetup] Ошибка загрузки коммьюнити языков: {e}")
        return langs

    # Для обратной совместимости
    LANGUAGE_LIST = BASE_LANGUAGE_LIST

    def get_lang_progress(code):
        if code in TRANSLATION_STATUS:
            return TRANSLATION_STATUS[code]
        for l in get_active_languages():
            if l.get("code") == code:
                return l.get("progress", 100)
        return 0


