# Данные для Тома 1
define credits_vol1 = [
    (_("Сценарий"), "DomDot"),

    (_("Художник"), "NanoBanana Pro"),

    (_("Тестировщик и Вдохновитель"), "Overhappy_Avali"),

    ("Музыка", ""),
    ("ksho", "Purge Protocol"),
    ("Factorio", "Swell Pad"),
    ("Rewrite", "Potted One"),
    ("Rewrite", "Sorrowless"),
    ("Rewrite", "Rememberance"),
    ("Rewrite", "Reply"),
    ("PRESSURE", "One Way Trip"),
    ("PRESSURE", "First Theme"),
    ("Steins;Gate", "Self Affirmation"),
    ("Steins;Gate", "Quiet Air"),
    ("Steins;Gate", "Chaos Mind"),
    ("Steins;Gate", "SERN"),
    ("Occultic;Nine", "OVERCAST-EYES"),
    ("Occultic;Nine", "GRAY HEARTS"),
    ("Occultic;Nine", "LISTEN"),
    ("CHAOS;HEAD", "Colors"),
    ("Shadows of Doubt", "Revpad"),
    ("Shadows of Doubt", "LD Celts"),
    ("Shadows of Doubt", "FM Modul"),
    ("Intravenous", "Initiation (Inactive)"),
    ("Avery Alexander", "HRT"),
    ("AND ONE", "Angel Eyes"),
    ("Ezio Bosso", "Rain, In Your Black Eyes"),
    ("Ever 17: The Out of Infinity", "Karma"),
    ("Date a Live", "Marionettica"),
    ("Brandon Fiechter", "Eyes of the Forest"),
    ("God Smiles", "Tilman Sillescu"),
    
    (_("Спецэффекты"), "StoryBlocks"),

    (_("Игры, Которые Вдохновили"), ""),
    ("", "Voices of the Void"),
    ("", "Rewrite"),
    ("", "Higurashi"),
    ("", "Date a Live"),
    ("", "ROBLOX - Anomic"),
    ("", "Ever 17"),
    ("", "Library of Ruina"),
    ("", "Space Station 13"),
]

#TODO Данные для Тома 2 (просто заглушка)
define credits_vol2 = [
    (_("Сценарий"), "DomDot"),
    (_("Художник"), "NanoBanana Pro"),
    (_("Тестировщик и Вдохновитель"), "Overhappy_Avali"),
    ("CG Артист", "-"),
    ("Фоны", "-"),
    ("Спецэффекты", "-"),
]


# --- ЛЕЙБЛ-ОБРАБОТЧИК ---

label credits_sequence(volume_id):
    
    window hide dissolve
    
    if volume_id == 1:
        $ audio_file = "audio/music/BGM/Tide.opus"
        $ my_credits = credits_vol1
        $ featured_cg, all_cg = get_images_from_dir("images/cg/vol1", featured_prefix="featured_")  
        $ duration = 303.0 # Длительность музыки в секундах
        $ end_msg_offset = 12.0 # За сколько секунд до конца музыки показать "Спасибо за игру"
        $ cg_time = 3.2 # Каждые сколько секунд менять картинку
        $ fade_time = 1.0 # Время растворения между картинками
    elif volume_id == 2:
        $ audio_file = "audio/music/BGM/CallYou.mp3"
        $ my_credits = credits_vol2
        $ featured_cg, all_cg = get_images_from_dir("images/cg/vol2", featured_prefix="featured_")
        $ duration = 224 #175
        $ end_msg_offset = 13.0
        $ cg_time = 3.0
        $ fade_time = 1.0
    

    $ final_slideshow = create_slideshow(featured_cg, cg_time, fade_time)

    play music audio_file noloop fadeout 1.0

    call screen end_credits(my_credits, final_slideshow, duration, end_msg_offset)

    stop music fadeout 2.0
    scene black with Fade(1.0, 2.0, 5.0)

    if _return == "skipped":
        return # Возвращаемся, секретной сцены не будет (результат по умолчанию None)
    
    elif _return == "finished":
        python:
            # Ачивка "Концерт в одиночестве" (дослушан финальный трек)
            if volume_id == 2 or volume_id == 1:
                grant_achievement("concert_in_solitude")

            # Ачивка "В этом нет ничего такого" (пройдено с включенной ИИ-чувствительностью)
            if getattr(persistent, "ai_mode_full_run_valid", False) and getattr(persistent, "ai_sensitive_mode", False):
                grant_achievement("nothing_wrong_ai")

        return "secret_scene" # Возвращаем флаг секретной сцены