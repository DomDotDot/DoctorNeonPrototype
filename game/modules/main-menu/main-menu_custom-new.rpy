init python:
    import datetime
    def play_main_menu_music():
        if not getattr(persistent, "main_menu_music_enabled", True):
            renpy.music.stop(channel="music", fadeout=0.5)
            return

        music_map = {
            0: main_menu_music_default,
            1: main_menu_music_unlocked_1,
            2: main_menu_music_unlocked_2,
            3: main_menu_music_unlocked_3,
            4: main_menu_music_unlocked_4
        }
        track = music_map.get(persistent.main_menu_level, main_menu_music_default)
        renpy.music.play(track, fadein=1.0, if_changed=True)

    # -------------------------------------------------------------------------
    # КОД КОНАМИ (СЕКРЕТНЫЙ РЕТРО-КОД В ГЛАВНОМ МЕНЮ)
    # -------------------------------------------------------------------------
    _konami_state = {
        "step": 0,
        "last_time": 0.0
    }

    def execute_konami_code():
        _safe_init_achievements_persistent()

        # 1. Разблокировка раздела читов в Управлении данными вне дев-режима
        persistent.cheats_unlocked = True

        # 2. Выдача скрытого достижения "Код"
        grant_achievement("konami_code", notify=True)

        renpy.save_persistent()

        # 3. Звуковой отклик
        try:
            sound_file = "audio/sfx/keycard-accepted.opus"
            if renpy.loadable(sound_file):
                renpy.sound.play(sound_file, channel="sfx")
        except Exception:
            pass

        # 4. Всплывающее уведомление
        renpy.notify(_("Код Konami принят! Читы в управлении данными разблокированы."))
        _safe_restart_interaction()

    class KonamiCodeListener(renpy.Displayable):
        def __init__(self, **properties):
            super(KonamiCodeListener, self).__init__(**properties)

        def render(self, width, height, st, at):
            return renpy.Render(0, 0)

        def event(self, ev, x, y, st):
            import pygame
            import time

            # Обрабатываем только нажатия клавиш и геймпада
            is_key_down = (ev.type == pygame.KEYDOWN)
            is_joy = False

            joy_btn_type = getattr(pygame, "JOYBUTTONDOWN", None)
            joy_hat_type = getattr(pygame, "JOYHATMOTION", None)
            if joy_btn_type and ev.type == joy_btn_type:
                is_joy = True
            elif joy_hat_type and ev.type == joy_hat_type:
                is_joy = True
            elif hasattr(renpy.display, "core") and ev.type == renpy.display.core.EVENTNAME and not getattr(ev, "up", False):
                is_joy = True

            if not (is_key_down or is_joy):
                return None

            now = time.time()
            if _konami_state["last_time"] > 0 and (now - _konami_state["last_time"] > 4.0):
                _konami_state["step"] = 0

            tokens = set()
            try:
                # ВВЕРХ: Стрелка вверх, Numpad 8, W, D-pad вверх
                if renpy.map_event(ev, ["K_UP", "K_KP8", "w", "W", "ц", "Ц", "pad_dpup_press"]):
                    tokens.add("up")

                # ВНИЗ: Стрелка вниз, Numpad 2, S, D-pad вниз
                if renpy.map_event(ev, ["K_DOWN", "K_KP2", "s", "S", "ы", "Ы", "pad_dpdown_press"]):
                    tokens.add("down")

                # ВЛЕВО: Стрелка влево, Numpad 4, A, D-pad влево
                if renpy.map_event(ev, ["K_LEFT", "K_KP4", "a", "A", "ф", "Ф", "pad_dpleft_press"]):
                    tokens.add("left")

                # ВПРАВО: Стрелка вправо, Numpad 6, D, D-pad вправо
                if renpy.map_event(ev, ["K_RIGHT", "K_KP6", "d", "D", "в", "В", "pad_dpright_press"]):
                    tokens.add("right")

                # B: Клавиша B, D-pad/Геймпад B
                if renpy.map_event(ev, ["K_b", "b", "B", "и", "И", "pad_b_press"]):
                    tokens.add("b")

                # A: Клавиша A, D-pad/Геймпад A
                if renpy.map_event(ev, ["K_a", "a", "A", "ф", "Ф", "pad_a_press"]):
                    tokens.add("a")
            except Exception:
                pass

            if not tokens:
                _konami_state["step"] = 0
                _konami_state["last_time"] = now
                return None

            sequence = ["up", "up", "down", "down", "left", "right", "left", "right", "b", "a"]
            expected = sequence[_konami_state["step"]]

            if expected in tokens:
                _konami_state["step"] += 1
                _konami_state["last_time"] = now
                if _konami_state["step"] >= len(sequence):
                    _konami_state["step"] = 0
                    execute_konami_code()
                    raise renpy.IgnoreEvent()
            else:
                if "up" in tokens:
                    _konami_state["step"] = 2 if _konami_state["step"] >= 2 else 1
                else:
                    _konami_state["step"] = 0
                _konami_state["last_time"] = now

            return None


################################################################################
## Главное меню (HUB)
################################################################################

screen main_menu_background():

    on "show" action [Function(play_main_menu_music), Function(check_midnight_shift)]
    on "replace" action [Function(play_main_menu_music), Function(check_midnight_shift)]

    # Фон с параллаксом
    if persistent.disable_gpu_animations:
        add "main_menu_bg_dynamic"
    else:
        add "main_menu_bg_dynamic":
            at mouse_parallax(30)

    # Динамическая анимация сакуры (схема волны и лепестков по аналогии с chapter-title.rpy)
    if not persistent.disable_gpu_animations:
        if persistent.main_menu_level == 3:
            use sakura_menu_breeze
        elif persistent.main_menu_level == 4:
            use sakura_menu_storm

        # Частицы (для зимнего сезона на других фонах)
        if datetime.datetime.now().month in (12, 1, 2) and persistent.main_menu_level not in (3, 4):
            add SnowBlossom("gui/particle.png", count=120, border=50, xspeed=(20, 50), yspeed=(20, 50), start=10) id "main_menu_effect"

    # Виньетка
    add "gui/main_menu/vignette.png" alpha 0.4

    # Логотип (интерактивный с реакцией на клик)
    imagebutton:
        idle "main_menu_logo"
        hover "main_menu_logo"
        xalign 0.5
        ypos 25
        action Function(add_achievement_progress, "dont_touch_logo", 1)
        hover_sound "audio/sfx/cursor-hover.opus"
        activate_sound "audio/sfx/button-click.opus"

screen main_menu():
    tag menu
    zorder 10
    
    use main_menu_background 

    # Слушатель секретного кода Конами
    add KonamiCodeListener()

    # Анимация раскрытия главного меню через улетающий вихрь сакуры
    if getattr(persistent, "_sakura_wipe_active", False):
        $ persistent._sakura_wipe_active = False
        use sakura_wipe_out_screen

    # Модульные оверлеи модов (Mod API Hooks)
    if renpy.has_screen("mod_main_menu_overlays"):
        use mod_main_menu_overlays

    # Основной блок навигации
    vbox:
        style "main_menu_vbox"

        use icon_button("▶️", _("Играть"), action=ShowMenu("play_menu"), btn_style="main_menu_button")
        fixed:
            xsize 450
            ysize 75
            xalign 0.5

            use icon_button("⚙️", _("Настройки"), action=ShowMenu("settings_menu"), btn_style="main_menu_button")

            if getattr(persistent, "community_content_enabled", False):
                button:
                    style "main_menu_button"
                    xsize 75
                    ysize 75
                    xpos 500
                    yalign 0.5
                    action ShowMenu("mod_manager_screen")
                    tooltip _("Менеджер модов")
                    text "🧩" size 30 align (0.5, 0.5)

        fixed:
            xsize 450
            ysize 75
            xalign 0.5
        
            if renpy.has_screen("memory_recollection"):
                use icon_button("💡", _("Воспоминания"), action=ShowMenu("memory_recollection"), btn_style="main_menu_button")

                button:
                    style "main_menu_button"
                    xsize 75
                    ysize 75
                    xpos 500
                    yalign 0.5
                    action ShowMenu("achievements_screen")
                    tooltip _("Достижения")
                    text "🏆" size 30 align (0.5, 0.5)


        python:
            try:
                unread = get_unread_count()
            except:
                unread = 0

        if unread > 0:
            $ notif_text = _("Уведомления ({0})").format(unread)
            use icon_button("📧", notif_text, action=ShowMenu("notification_center"), btn_style="main_menu_button", txt_color="#a11919")
        else:
            use icon_button("📧", _("Уведомления"), action=ShowMenu("notification_center"), btn_style="main_menu_button")

        use icon_button("ℹ️", _("Об игре"), action=ShowMenu("about_menu"), btn_style="main_menu_button")
        use icon_button(None, _("Выход"), action=Quit(confirm=True), btn_style="main_menu_button")