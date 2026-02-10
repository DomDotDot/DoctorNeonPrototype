init offset = 1 # Force this to load after standard screens

# Переопределяем экран, вызываемый по ESC (game_menu)
# Обычно это "save", но мы меняем на наше новое "pause_menu"
# Переопределяем экран, вызываемый по ESC (game_menu)
# Обычно это "save", но мы меняем на наше новое "pause_menu"
define _game_menu_screen = "pause_menu"

screen pause_menu():
    tag menu
    modal True # Блокируем ввод в игру

    # Затемнение фона
    add "gui/overlay/game_menu.png" alpha 0.8:
        xalign 0.5
        yalign 0.5

    # Кнопка возврата по ESC
    key "game_menu" action Return()

    vbox:
        style_prefix "navigation" # Используем стили, которые мы унифицировали в main-menu_styles.rpy
        
        xalign 0.5
        yalign 0.5
        spacing 20

        # Заголовок (опционально)
        text _("ПАУЗА"):
            style "main_menu_title"
            xalign 0.5
            yoffset -50
            size 60

        # Кнопки
        textbutton _("Продолжить") action Return()
        
        textbutton _("Сохранить") action ShowMenu("save")
        
        textbutton _("Загрузить") action ShowMenu("load")
        
        textbutton _("Настройки") action ShowMenu("preferences")
        
        textbutton _("Главное меню") action MainMenu()
        
        textbutton _("Выход") action Quit()

# Стили уже определены в main-menu_styles.rpy (style navigation_button is main_menu_button)
# Но если нужно что-то специфичное для паузы:

style pause_menu_vbox is navigation_vbox
