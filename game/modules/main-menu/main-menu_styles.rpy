style main_menu_vbox:

    xalign 0.5
    yalign 0.5
    yoffset 150
    spacing 15

style main_menu_button is button:
    xsize 300
    ysize 100
    xalign 0.5
    yalign 0.5

# Стиль текста кнопок
style main_menu_button_text is button_text:
    size 30
    color "#e8e8e8"
    hover_color "#ffffff"
    # idle_color - цвет в обычном состоянии
    # selected_idle_color - цвет выбранной кнопки
    # selected_hover_color - цвет выбранной кнопки при наведении
    xalign 0.5
    yalign 0.5

style main_menu_button:
    background "gui/main_menu/button_idle.avif"
    hover_background "gui/main_menu/button_hover.avif"
    xmargin 0
    ymargin 0

    hover_sound "audio/sfx/cursor-hover.opus" 
    activate_sound "audio/sfx/button-click.opus"

# Стили для саб-меню
style sub_menu_frame:
    background Frame("gui/frame.png", 25, 25, tile=True)
    xalign 0.5
    yalign 0.5
    xsize 600
    padding (40, 40)

style sub_menu_vbox:
    xalign 0.5
    spacing 15

style sub_menu_label is label:
    xalign 0.5
    bottom_margin 20

style sub_menu_label_text is label_text:
    size 40
    color gui.accent_color

style sub_menu_button is main_menu_button:
    xsize 350
    
style sub_menu_button_text is main_menu_button_text:
    size 28


#################################
## Стили для новых экранов настроек
#################################

# Основное окно-рамка
style settings_frame:
    background "#000b"
    xalign 0.5
    yalign 0.5
    xsize 1000
    padding (40, 40)
    modal True

# Заголовок окна ("Текст и Графика", "Звук")
style settings_title is label:
    xalign 0.5
    bottom_margin 30

style settings_title_text is label_text:
    size 45
    color gui.accent_color
    text_align 0.5

# Кнопка "Назад"
style settings_back_button is main_menu_button:

    xsize 300
    ysize 50
    background None 
    hover_background None
    xalign 0.5
    yalign 0.5

# Стили для кнопок-переключателей (Оконный/Полный, Пропуск)
style settings_check_label is label:
    xalign 0

style settings_check_label_text is label_text:
    size 24
    color "#cccccc"
    bottom_margin 5

style settings_check_button is button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"
    xsize 400

style settings_check_button_text is button_text:
    properties gui.text_properties("check_button")
    size 22

# Стили для слайдеров (громкость, скорость текста)
style settings_slider_label is settings_check_label:
    text_align 1
    

style settings_slider_label_text is settings_check_label_text:
    size 24
    color "#ffffff"
    bottom_margin 5

style settings_slider_bar is bar:
    xfill True 
    ysize 12
    left_bar Solid("#08608f")
    right_bar Solid("#333")
    thumb Solid("#0f63c9")
    thumb_shadow None
    thumb_offset 6

# Кнопка "Тест" рядом со слайдером
style settings_test_button is button:
    xsize 100
    ysize 35
    left_margin 15
    
style settings_test_button_text is button_text:
    size 20

style main_menu_button_text is button_text:
    size 30
    color "#e8e8e8"
    hover_color "#ffffff"
    selected_color "#ffffff"
    insensitive_color "#555555"
    
    xalign 0.5
    yalign 0.5

style chapter_button is button:
    background Solid("#00000080")
    hover_background Solid("#ffffff20")
    xsize 335
    ysize 250

style chapter_title_text is text:
    size 22
    bold True
    color "#eba900"
    xalign 0.5
    text_align 0.5
    layout "subtitle"

style chapter_subtitle_text is text:
    size 18
    color "#cccccc"
    xalign 0.5
    text_align 0.5


# Стиль для контейнера одной опции ("Карточка")
style danger_zone_frame:
    background Solid("#00000080") # Полупрозрачный черный фон
    xfill True # Растянуть на всю ширину родителя
    ysize 110  # Фиксированная высота карточки
    padding (20, 15)
    margin (0, 10) # Отступ между карточками

# Стиль для красной рамки (Danger)
style danger_zone_frame_red is danger_zone_frame:
    
    # ВАРИАНТ "GITHUB": Цветная обводка
    # Для этого нам нужен файл рамки. Но мы можем сэмулировать его:
    background Frame(Fixed(Solid("#b60205"), Solid("#000000", xmargin=2, ymargin=2), xysize=(100,100)), 4, 4)

# Стиль для зеленой рамки (Safe/Cheat)
style danger_zone_frame_green is danger_zone_frame:
    background Frame(Fixed(Solid("#2ea043"), Solid("#000000", xmargin=2, ymargin=2), xysize=(100,100)), 4, 4)

# Стиль заголовка внутри карточки
style danger_title_text:
    size 28
    bold True
    color "#ffffff"

# Стиль описания внутри карточки
style danger_desc_text:
    size 18
    color "#aaaaaa"

# Кнопка внутри опасной зоны
style danger_button is button:
    background Solid("#b60205") # Красный фон
    hover_background Solid("#ff4444")
    xsize 200
    ysize 50
    xalign 1.0 # Прижать вправо
    yalign 0.5
    
style danger_button_text:
    color "#fff"
    size 20
    xalign 0.5
    yalign 0.5
    bold True

# Кнопка внутри зеленой зоны
style safe_button is danger_button:
    background Solid("#2ea043") # Зеленый фон
    hover_background Solid("#4ac260")

# Кнопка нейтральная (белая/серая)
style neutral_button is danger_button:
    background Solid("#333")
    hover_background Solid("#555")