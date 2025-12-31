# Данные для Тома 1
define credits_vol1 = [
    ("Сценарий", "DomDot"),

    ("Художник", "NanoBanana Pro"),

    ("Тестировщик и Вдохновитель", "Overhappy_Avali"),

    ("Музыка", ""),
    ("", "ksho - Purge Protocol"),
    ("", "Factorio - Swell Pad"),
    ("", "Rewrite - Potted One"),
    ("", "Rewrite - Sorrowless"),
    ("", "Rewrite - Rememberance"),
    ("", "Rewrite - Reply"),
    ("", "PRESSURE - One Way Trip"),
    ("", "PRESSURE - First Theme"),
    ("", "Steins;Gate - Self Affirmation"),
    ("", "Steins;Gate - Quiet Air"),
    ("", "Occultic;Nine - OVERCAST-EYES"),
    ("", "CHAOS;HEAD - Colors"),
    ("", "Shadows of Doubt - Revpad"),
    ("", "Shadows of Doubt - LD Celts"),
    ("", "Shadows of Doubt - FM Modul"),
    ("", "Intravenous - Initiation (Inactive)"),
    ("", "Avery Alexander - HRT"),

    ("Спецэффекты", "StoryBlocks"),
]

# Данные для Тома 2
define credits_vol2 = [
    ("Главный сценарист", "-"),
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
        $ audio_file = "audio/credits_song2.opus"
        $ my_credits = credits_vol2
        $ featured_cg, all_cg = get_images_from_dir("images/cg/vol2", featured_prefix="featured_")
        $ duration = 120.0
        $ end_msg_offset = 10.0
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

        return "secret_scene" # Возвращаем флаг секретной сцены