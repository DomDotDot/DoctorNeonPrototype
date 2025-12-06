init -1 python:
    # Базовая ссылка на релизы
    DLC_REPO_URL = "https://github.com/DomDotDot/DoctorNeonPrototype/releases/download"
    
    # Версии (можно вынести в options.rpy, но можно и тут)
    # Важно: имя файла в версии должно совпадать с тем, что в URL
    
    # СПИСОК ВСЕХ DLC
    # file: имя архива на сервере
    # version: папка версии на гитхабе (тэги)
    # folder: куда распаковать (внутри game/)
    # check_file: файл-маркер (если он есть, значит DLC установлено)
    # title: Заголовок для игрока
    # desc: Описание (что это и какой размер)
    
    available_dlcs = [
        {
            "id": "music",
            "file": "music.zip",
            "version": "v0.5.3",
            "folder": "audio",
            "check_file": "audio/music/BGM/FogHorns.opus",
            "title": "Фоновая музыка",
            "desc": "Атмосферные треки для погружения.\n~120 Мб"
        },
        {
            "id": "ambient",
            "file": "ambient.zip",
            "version": "v0.5.3",
            "folder": "audio",
            "check_file": "audio/ambient/Target.opus",
            "title": "Эмбиент и Звуки",
            "desc": "Звуки дождя, ветра и шагов.\n~15 Мб"
        },
        {
            "id": "voice_ru",
            "file": "voice_ru.zip", 
            "version": "v0.5.3",
            "folder": "audio",
            "check_file": "audio/voice/voice_sample.ogg",
            "title": "Озвучка персонажей",
            "desc": "Полная озвучка диалогов (Русский).\n~250 КБ"
        },
        {
            "id": "voice_en_us",
            "file": "voice_en.zip", 
            "version": "v0.5.3", 
            "folder": "tl/english_us/audio",
            "check_file": "tl/english_us/audio/escaping_facility_grounds_c1f78dab.ogg",
            "title": "Озвучка персонажей",
            "desc": "Полная озвучка диалогов (Английский).\n~250 КБ"
        },
        {
            "id": "sfx",
            "file": "sfx.zip", 
            "version": "v0.5.3", 
            "folder": "audio",
            "check_file": "audio/sfx/Chair_Hit.opus",
            "title": "SFX-Эффекты",
            "desc": "Звуковые эффекты\n~2 Мб"
        }
    ]