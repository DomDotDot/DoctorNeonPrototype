# === ИЗОБРАЖЕНИЯ И ТРАНСФОРМАЦИИ ===

# Логотип вашей студии (замените путь на свой файл)
image studio_logo_img = "gui/studio-logo.png"

# Логотип Ren'Py (стандартный или свой)
image renpy_logo_img = "gui/renpy-logo.png"

# Красивая анимация появления (зум + прозрачность)
transform splash_zoom_fade:
    xalign 0.5 yalign 0.5
    alpha 0.0 zoom 0.8
    ease 1.5 alpha 1.0 zoom 1.0 # Появление
    pause 2.0                    # Пауза пока видно
    ease 1.0 alpha 0.0 zoom 1.1  # Исчезновение

# Переменная для отслеживания первого запуска
default persistent.firstlaunch = True
# Переменная, видели ли мы уже интро (чтобы можно было пропускать)
default persistent.seen_splash = False


label splashscreen:

    # -----------------------------------------------------------
    # 1. ТЕХНИЧЕСКИЕ ПРОВЕРКИ (На черном фоне)
    # -----------------------------------------------------------
    scene black
    
    # Сначала проверяем обновления (если у вас есть эта функция)
    if hasattr(store, 'start_update_check'):
        $ start_update_check()
    
    # Затем проверяем DLC. 
    # Это самое логичное место: игрок еще не видит логотипов, 
    # и если нужно качать файлы - он увидит меню загрузки здесь.
    call dlc_check_sequence from _call_dlc_check_sequence

    # Небольшая пауза после проверок перед началом шоу (чтобы не было резких скачков)
    $ renpy.pause(0.5, hard=True)


    # -----------------------------------------------------------
    # 2. ЛОГОТИП СТУДИИ
    # -----------------------------------------------------------
    
    # Если у вас есть звук логотипа студии
    # play sound "audio/sfx/studio_intro.opus" 

    show studio_logo_img at splash_zoom_fade

    show text "{size=30}Made by DomDot{/s}":
        xalign 0.5 yalign 0.85 alpha 0.0
        pause 1.0
        ease 1.0 alpha 1.0
        pause 1.5
        ease 1.0 alpha 0.0
    
    # Логика пропуска:
    # Если игрок уже видел интро, клик пропустит паузу.
    # Если нет (hard=True) - обязан досмотреть.
    if persistent.seen_splash:
        $ renpy.pause(4.5) # Можно кликнуть чтобы пропустить
    else:
        $ renpy.pause(4.5, hard=True) # Нельзя пропустить

    scene black with dissolve
    $ renpy.pause(0.5)


    # -----------------------------------------------------------
    # 3. ЛОГОТИП REN'PY / ДВИЖКА
    # -----------------------------------------------------------

    play sound "audio/sfx/short-logo.opus" volume 0.25
    
    show renpy_logo_img at splash_zoom_fade
    
    show text "{size=30}Made with Ren'Py [renpy.version_only]{/s}":
        xalign 0.5 yalign 0.85 alpha 0.0
        pause 1.0
        ease 1.0 alpha 1.0
        pause 1.5
        ease 1.0 alpha 0.0

    if persistent.seen_splash:
        $ renpy.pause(4.5)
    else:
        $ renpy.pause(4.5, hard=True)

    # Отмечаем, что интро просмотрено хотя бы раз
    $ persistent.seen_splash = True

    scene black with fade


    # -----------------------------------------------------------
    # 4. НАСТРОЙКИ ПРИ ПЕРВОМ ЗАПУСКЕ
    # -----------------------------------------------------------
    
    if persistent.firstlaunch:
        
        # 4.1 Выбор языка
        call screen language_selection_screen
        
        # 4.2 Предупреждение о контенте (Оставьте только один вариант, который рабочий)
        # Обычно это экран с кнопкой "Я понял / Продолжить"
        call screen content_warning_screen with dissolve
        
        # 4.3 Настройки доступности (размер текста и т.д., если есть)
        # call screen accessibility_settings 

        # Фиксируем, что первичная настройка завершена
        $ persistent.firstlaunch = False

    return