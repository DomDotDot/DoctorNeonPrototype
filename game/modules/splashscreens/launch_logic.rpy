# ==============================================================================
# Кинематографичная заставка при запуске (Library of Ruina / Project Moon Style)
# ==============================================================================

define config.end_splash_transition = Dissolve(1.2)

# Логотип студии
image studio_logo_img = "gui/studio-logo.png"

# Логотип игры
image game_title_logo = "gui/main_menu/logo3.png"

# Переменные для отслеживания запуска
default persistent.firstlaunch = True
default persistent.last_run_version = None 
default persistent.seen_splash = False
default persistent.first_game_warning_seen = False


# ------------------------------------------------------------------------------
# 1. Трансформация заставки студии (Fade по центру с легким зумом)
# ------------------------------------------------------------------------------
transform splash_studio_fade:
    xalign 0.5
    yalign 0.5
    alpha 0.0
    zoom 0.43
    easein 1.0 alpha 1.0 zoom 0.46
    pause 1.4
    easeout 0.8 alpha 0.0 zoom 0.48


# ------------------------------------------------------------------------------
# 2. Трансформация логотипа игры (Расширение по центру -> Скольжение наверх)
# ------------------------------------------------------------------------------
transform splash_logo_ruina_full:
    xalign 0.5
    ypos 0.5
    yanchor 0.5
    alpha 0.0
    zoom 0.94
    # Фаза 1: Плавное проявление и медленное кинематографичное расширение
    parallel:
        easein 0.8 alpha 1.0
    parallel:
        ease 2.2 zoom 1.0
    # Фаза 2: Пауза после завершения полосы загрузки
    pause 0.2
    # Фаза 3: Плавное скольжение наверх к позиции логотипа в главном меню (ypos 25, yanchor 0.0)
    easein_cubic 0.85 ypos 25 yanchor 0.0


# Фиксированное положение логотипа на позиции главного меню
transform splash_logo_fixed_top:
    xalign 0.5
    ypos 25
    yanchor 0.0
    alpha 1.0
    zoom 1.0


# ------------------------------------------------------------------------------
# 3. Индикатор загрузки и инициализации в стиле Library of Ruina
# ------------------------------------------------------------------------------
init python:
    def ruina_loader_status(st, at):
        t = max(0.0, st - 0.2)
        if t < 0.5:
            msg = "SYNCHRONIZING NEURAL PROTOCOLS • 18%"
        elif t < 1.1:
            msg = "MOUNTING GAME ARCHIVES & CACHE • 56%"
        elif t < 1.6:
            msg = "VERIFYING DLC INTEGRITY & SHADERS • 88%"
        else:
            msg = "SYSTEM INITIALIZED // READY 100%"
        return Text(msg, substitute=False, size=11, bold=True, color="#94a3b8", font=gui.text_font), 0.05

transform splash_loader_container:
    alpha 0.0
    pause 0.2
    easein 0.35 alpha 1.0
    pause 1.65
    easeout 0.25 alpha 0.0

transform splash_bar_progress:
    xsize 0
    pause 0.2
    easein 0.5 xsize 120
    ease 0.6 xsize 270
    ease 0.4 xsize 380
    easeout 0.3 xsize 440

screen ruina_splash_loader():
    zorder 105
    frame at splash_loader_container:
        background None
        align (0.5, 0.88)
        vbox:
            align (0.5, 0.5)
            spacing 6

            # Кибер-строка статуса
            hbox:
                align (0.5, 0.5)
                spacing 10
                text "SYS.INIT //" size 11 bold True color "#00d4ff" font gui.text_font
                add DynamicDisplayable(ruina_loader_status)

            # Тонкая неоновая полоска прогресса
            frame:
                background Solid("#111827")
                xsize 440
                ysize 3
                padding (0, 0)
                
                frame at splash_bar_progress:
                    background Solid("#00d4ff")
                    ysize 3


# ------------------------------------------------------------------------------
# 4. Основной сценарий заставки
# ------------------------------------------------------------------------------
label _intro_splash_sequence:
    scene black

    # --------------------------------------------------------------------------
    # Сцена 1: Заставка студии (Fade по центру)
    # --------------------------------------------------------------------------
    show studio_logo_img at splash_studio_fade

    if persistent.seen_splash:
        $ renpy.pause(3.2, hard=False)
    else:
        $ renpy.pause(3.2, hard=True)

    hide studio_logo_img
    scene black with Dissolve(0.3)

    # --------------------------------------------------------------------------
    # Сцена 2: Заставка игры (logo3 в центре, расширение) + полоска загрузки
    # Сцена 3: Скольжение логотипа наверх к позиции главного меню
    # --------------------------------------------------------------------------
    play sound "audio/sfx/logo-reveal.mp3" volume 0.5
    show game_title_logo at splash_logo_ruina_full
    show screen ruina_splash_loader

    if persistent.seen_splash:
        $ renpy.pause(3.35, hard=False)
    else:
        $ renpy.pause(3.35, hard=True)

    hide screen ruina_splash_loader
    show game_title_logo at splash_logo_fixed_top

    $ persistent.seen_splash = True
    return


# ------------------------------------------------------------------------------
# 5. Последовательность предупреждений при первом запуске Новой Игры
# ------------------------------------------------------------------------------
label new_game_warning_flow:
    $ _warning_step = 1
    while _warning_step <= 2:
        if _warning_step == 1:
            call screen content_warning_screen with dissolve
            $ _res = _return
            if _res == "cancel":
                $ MainMenu(confirm=False)()
            else:
                $ _warning_step = 2
        elif _warning_step == 2:
            call screen content_warning with dissolve
            $ _res = _return
            if _res == "back":
                $ _warning_step = 1
            else:
                $ _warning_step = 3

    $ persistent.first_game_warning_seen = True
    $ renpy.save_persistent()
    if renpy.has_screen("content_warning") and hasattr(store, "save_ai_disclaimer_notification"):
        $ save_ai_disclaimer_notification()
    return
