# === ИЗОБРАЖЕНИЯ И ТРАНСФОРМАЦИИ ПРИ ЗАПУСКЕ ===

# Логотип 'студии'
image studio_logo_img = "gui/studio-logo.png"

# Логотип Ren'Py
image renpy_logo_img = "gui/renpy-logo.png"

# Трансформация для объединенного логотипа
transform splash_zoom_fade_combined:
    alpha 0.0 zoom 0.95
    ease 1.5 alpha 1.0 zoom 1.0
    pause 2.5
    ease 1.0 alpha 0.0 zoom 1.05

# Переменные для отслеживания запуска
default persistent.firstlaunch = True
default persistent.last_run_version = None 
default persistent.seen_splash = False

# Экран, на котором отображаются оба логотипа
screen combined_splash_screen():
    zorder 100
    
    frame at splash_zoom_fade_combined:
        background None
        align (0.5, 0.5)
        
        hbox:
            align (0.5, 0.5)
            spacing 150
            
            # Блок Студии
            vbox:
                align (0.5, 0.5)
                spacing 30
                add "studio_logo_img" xalign 0.5 zoom 0.8
                text "Made by DomDot":
                    xalign 0.5
                    size 30
                    color "#e8e8e8"
                    # Использование дефолтного системного шрифта для надежности
                    font "DejaVuSans.ttf" 
                    
            # Блок Ren'Py
            vbox:
                align (0.5, 0.5)
                spacing 30
                add "renpy_logo_img" xalign 0.5 zoom 0.8
                text "Made with Ren'Py [renpy.version_only]":
                    xalign 0.5
                    size 30
                    color "#e8e8e8"
                    font "DejaVuSans.ttf"

# Лейбл, который запускает показ заставки
label _intro_splash_sequence:
    scene black
    
    # Звук заставки
    play sound "audio/sfx/short-logo.opus" volume 0.25

    # Показываем объединенный экран логотипов
    show screen combined_splash_screen
    
    # Логика пропуска:
    # 1.5 сек появление + 2.5 сек показ + 1.0 сек исчезновение = 5.0 сек общего времени
    if persistent.seen_splash:
        $ renpy.pause(5.0) # Можно кликнуть чтобы пропустить
    else:
        $ renpy.pause(5.0, hard=True) # Нельзя пропустить

    hide screen combined_splash_screen with dissolve
    
    $ persistent.seen_splash = True
    scene black with fade
    return
