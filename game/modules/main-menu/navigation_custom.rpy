init offset = 1 # Force this to load after standard screens

# Переопределяем экран, вызываемый по ESC (game_menu)
# Обычно это "save", но мы меняем на наше новое "pause_menu"
define _game_menu_screen = "pause_menu"

screen pause_menu():
    tag menu
    modal True # Блокируем ввод в игру

    # Затемнение фона
    add Solid("#000000b3")

    # Кнопка возврата по ESC
    key "game_menu" action Return()

    frame:
        style "modern_panel"
        
        vbox:
            style "modern_vbox"

            label _("ПАУЗА") style "modern_title_label"

            textbutton _("Продолжить") action Return() style "modern_button"
            textbutton _("Сохранить") action ShowMenu("save") style "modern_button"
            textbutton _("Загрузить") action ShowMenu("load") style "modern_button"
            textbutton _("Настройки") action ShowMenu("settings_menu") style "modern_button"
            textbutton _("Главное меню") action MainMenu() style "modern_button"
            textbutton _("Выход") action Quit() style "modern_button"
