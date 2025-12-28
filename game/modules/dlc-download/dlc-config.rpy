init -1 python:
    # Базовая ссылка на релизы
    DLC_REPO_URL = "https://github.com/DomDotDot/DoctorNeonPrototype/releases/download"
    
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
            "version": "v0.6.0",
            "folder": "audio",
            "check_file": "audio/music/BGM/FogHorns.opus",
            "title": _("Фоновая музыка"),
            "desc": _("Атмосферные треки для погружения.\n~120 МБ")
        },
        {
            "id": "ambient",
            "file": "ambient.zip",
            "version": "v0.6.0",
            "folder": "audio",
            "check_file": "audio/ambient/Target.opus",
            "title": _("Эмбиент и Звуки"),
            "desc": _("Звуки дождя, ветра и шагов.\n~15 МБ")
        },
        {
            "id": "voice_ru",
            "file": "voice_ru.zip", 
            "version": "v0.6.0",
            "folder": "audio",
            "check_file": "audio/voice/voice_sample.ogg",
            "title": _("Озвучка персонажей"),
            "desc": _("Частичная озвучка диалогов (Русский) (это тест).\n~250 КБ")
        },
        {
            "id": "voice_en_us",
            "file": "voice_en.zip", 
            "version": "v0.5.3", 
            "folder": "tl/english_us/audio",
            "check_file": "tl/english_us/audio/voice/escaping_facility_grounds_c1f78dab.ogg",
            "title": _("Озвучка персонажей"),
            "desc": _("Частичная озвучка диалогов (Английский) (это тест).\n~250 КБ")
        },
        {
            "id": "sfx",
            "file": "sfx.zip", 
            "version": "v0.6.0", 
            "folder": "audio",
            "check_file": "audio/sfx/Chair_Hit.opus",
            "title": _("SFX-Эффекты"),
            "desc": _("Звуковые эффекты\n~2 МБ")
        }
    ]