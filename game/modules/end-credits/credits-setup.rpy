# Флаги открытия титров для повторного просмотра в меню "Воспоминания"
default persistent.credits_vol1_unlocked = False
default persistent.credits_vol2_unlocked = False

# Формат записей в списках титров:
#   ("---", "")            -> вертикальный разделитель / отступ между секциями
#   (_("Заголовок"), "")   -> заголовок секции с неоновым разделителем
#   ("", "Название")       -> одиночная строка по центру колонки
#   (_("Роль"), "Имя")     -> двухколоночная пара

# Данные для Тома 1
define credits_vol1 = [
    (_("Команда разработки"), ""),
    (_("Сценарий"), "DomDot"),
    (_("Художник"), "NanoBanana Pro"),
    (_("Тестировщик и Вдохновитель"), "Overhappy_Avali"),

    ("---", ""),
    (_("Музыка"), ""),
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

    ("---", ""),
    (_("Аудио"), ""),
    (_("Спецэффекты"), "StoryBlocks"),

    ("---", ""),
    (_("Вдохновление"), ""),
    ("", "Voices of the Void"),
    ("", "Rewrite"),
    ("", "Higurashi"),
    ("", "Date a Live"),
    ("", "ROBLOX - Anomic"),
    ("", "Ever 17"),
    ("", "Library of Ruina"),
    ("", "Space Station 13"),
]

# Данные для Тома 2 (базовый шаблон; секцию музыки можно дополнить позже)
define credits_vol2 = [
    (_("Команда разработки"), ""),
    (_("Сценарий"), "DomDot"),
    (_("Художник"), "NanoBanana Pro"),
    (_("Тестировщик и Вдохновитель"), "Overhappy_Avali"),

    # --- Шаблон под будущие треки Тома 2 ---
    # ("---", ""),
    # (_("Музыка"), ""),
    # ("Исполнитель", "Название трека"),

    ("---", ""),
    (_("Аудио"), ""),
    (_("Спецэффекты"), "StoryBlocks"),

    ("---", ""),
    (_("Вдохновление"), ""),
    ("", "Voices of the Void"),
    ("", "Rewrite"),
    ("", "Higurashi"),
    ("", "Date a Live"),
    ("", "ROBLOX - Anomic"),
    ("", "Ever 17"),
    ("", "Library of Ruina"),
    ("", "Space Station 13"),
    ("", "Subarashiki Hibi"),
    ("", "Saya no Uta"),
    ("", "Perfect Blue"),
    ("", "Perfect Blue"),
    ("", "Kimi no Na wa"),
    ("", "Mahou Shoujo Madoka Magica"),
    ("", "Happy Sugar Life"),
]


# --- ЛЕЙБЛ-ОБРАБОТЧИК ---

label credits_sequence(volume_id, replay_mode=False):

    # Блокируем откат, чтобы игрок не мог откатиться назад в середину слайдшоу
    $ renpy.block_rollback()

    # Сохраняем состояние быстрого меню и скрываем интерфейс на время титров
    $ _credits_prev_quick_menu = quick_menu
    $ quick_menu = False
    window hide dissolve

    if volume_id == 1:
        $ persistent.credits_vol1_unlocked = True
        $ audio_file = "audio/music/BGM/Tide.opus"
        $ my_credits = credits_vol1
        $ featured_cg, all_cg = get_images_from_dir("images/cg/vol1")
        $ duration = 303.0
        $ end_msg_offset = 12.0
        $ fade_time = 1.2
    elif volume_id == 2:
        $ persistent.credits_vol2_unlocked = True
        $ audio_file = "audio/music/BGM/CallYou.mp3"
        $ my_credits = credits_vol2
        $ featured_cg, all_cg = get_images_from_dir("images/cg/vol2")
        $ duration = 224.0
        $ end_msg_offset = 13.0
        $ fade_time = 1.2
    else:
        $ quick_menu = _credits_prev_quick_menu
        return

    $ slides_source = featured_cg if featured_cg else all_cg
    $ cg_time = calculate_credits_slide_timing(len(slides_source), duration, fade_time)
    $ final_slideshow = create_slideshow(slides_source, cg_time, fade_time, total_duration=duration)

    play music audio_file noloop fadeout 1.0

    call screen end_credits(my_credits, final_slideshow, duration, end_msg_offset)
    $ _credits_result = _return

    stop music fadeout 2.0

    if replay_mode:
        $ quick_menu = _credits_prev_quick_menu
        return

    scene black with Fade(1.0, 2.0, 5.0)
    $ quick_menu = _credits_prev_quick_menu

    if _credits_result == "skipped":
        return  # Возвращаемся, секретной сцены не будет (результат по умолчанию None)

    elif _credits_result == "finished":
        python:
            # Ачивка "В этом нет ничего такого" (пройдено с включенной ИИ-чувствительностью)
            if getattr(persistent, "ai_mode_full_run_valid", False) and getattr(persistent, "ai_sensitive_mode", False):
                grant_achievement("nothing_wrong_ai")

        return "secret_scene"  # Возвращаем флаг секретной сцены


# --- ЛЕЙБЛЫ ПОВТОРНОГО ПРОСМОТРА ИЗ МЕНЮ "ВОСПОМИНАНИЯ" ---

label credits_replay_vol1:
    call credits_sequence(1, replay_mode=True) from _call_credits_replay_vol1
    $ renpy.end_replay()
    return

label credits_replay_vol2:
    call credits_sequence(2, replay_mode=True) from _call_credits_replay_vol2
    $ renpy.end_replay()
    return
