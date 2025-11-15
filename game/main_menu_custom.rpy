# Файл: main_menu_custom.rpy

init python:
    def play_main_menu_music():
        if persistent.main_menu_level == 0:
            renpy.music.play(main_menu_music_default, fadein=1.0)
        elif persistent.main_menu_level == 1:
            renpy.music.play(main_menu_music_unlocked_1, fadein=1.0)
        elif persistent.main_menu_level == 2:
            renpy.music.play(main_menu_music_unlocked_2, fadein=1.0)

################################################################################
## 1. Главное меню (Полная замена стандартного)
################################################################################

screen main_menu():
    tag menu

    # Логика смены фона и музыки при показе экрана
    on "show" action Function(play_main_menu_music)

    # Отображение фона в зависимости от прогресса
    if persistent.main_menu_level == 0:
        add "main_menu_bg_default"
    elif persistent.main_menu_level == 1:
        add "main_menu_bg_unlocked_1"
    elif persistent.main_menu_level == 2:
        add "main_menu_bg_unlocked_2"
    
    # Баннер-логотип сверху
    add "main_menu_logo" xalign 0.5 ypos 25

    # Основной блок навигации
    vbox:
        style "main_menu_vbox"

        textbutton _("Начать") action Start() style "main_menu_button"
        textbutton _("Продолжить") action ShowMenu("load") style "main_menu_button"
        textbutton _("Настройки") action ShowMenu("settings_menu") style "main_menu_button"
        
        # Показываем галерею, только если она доступна
        if renpy.has_screen("gallery"):
            textbutton _("Галерея CG") action ShowMenu("gallery") style "main_menu_button"

        textbutton _("Об игре") action ShowMenu("about_menu") style "main_menu_button"
        textbutton _("Выход") action Quit(confirm=True) style "main_menu_button"


################################################################################
## 2. Саб-меню "Настройки"
################################################################################

screen settings_menu():
    tag menu
    modal True # Делает фон неактивным

    # Используем экран main_menu как фон, чтобы не было "скачка"
    use main_menu

    # Затемняющая рамка для фокуса на саб-меню
    frame:
        style "sub_menu_frame"

        vbox:
            style "sub_menu_vbox"
            label _("Настройки") style "sub_menu_label"

            textbutton _("Текст/Графика") action ShowMenu("preferences") style "sub_menu_button"
            textbutton _("Звук") action ShowMenu("preferences") style "sub_menu_button"
            textbutton _("Язык") action ShowMenu("language_selection_screen") style "sub_menu_button"
            
            null height 30 # Отступ

            textbutton _("Назад") action ShowMenu("main_menu") style "sub_menu_button"

# Экран выбора языка (если у вас его еще нет)
screen language_selection_screen():
    modal True
    tag menu
    
    use game_menu(_("Выбор языка")):
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 15

            # Пример:
            textbutton "Русский" action [Language(None), Return()]
            textbutton "English" action [Language("english_us"), Return()]


################################################################################
## 3. Саб-меню "Об игре"
################################################################################

screen about_menu():
    tag menu
    modal True

    use main_menu

    frame:
        style "sub_menu_frame"

        vbox:
            style "sub_menu_vbox"
            label _("Об игре") style "sub_menu_label"

            textbutton _("Управление") action ShowMenu("help") style "sub_menu_button"
            textbutton _("Лицензия") action ShowMenu("license_screen") style "sub_menu_button"
            textbutton _("Титры") action ShowMenu("credits_screen") style "sub_menu_button"
            textbutton _("Обновление") action ShowMenu("update_screen") style "sub_menu_button"

            null height 30

            textbutton _("Назад") action ShowMenu("main_menu") style "sub_menu_button"


################################################################################
## 4. Конечные экраны для раздела "Об игре"
## Они используют стандартный фрейм `game_menu` для единообразия
################################################################################

screen license_screen():
    tag menu
    use game_menu(_("Лицензия"), scroll="viewport"):
        vbox:
            style_prefix "about" # Используем стили от стандартного экрана about
            spacing 20

            label _("Музыка")
            text "Artist Name - Track Title 1\n{a=https://example.com}Источник{/a}"
            text "Artist Name - Track Title 2\n{a=https://example.com}Источник{/a}\n"

            label _("Графика")
            text "Имя художника - Тип ресурса\n"
            
            # ... и так далее

screen credits_screen():
    tag menu
    use game_menu(_("Титры"), scroll="viewport"):
        vbox:
            style_prefix "about"
            spacing 15
            
            text "Иван Иванов - Сценарист, Режиссер"
            text "Пётр Петров - Программист"
            text "Мария Сидорова - Художник персонажей"
            text "Елена Кузнецова - Художник фонов"
            # ... и так далее

screen update_screen():
    tag menu
    use game_menu(_("Обновление")):
        vbox:
            style_prefix "about"
            xalign 0.5
            yalign 0.5

            text "Текущая версия: [config.version]\n"
            text "\nСписок изменений:\n- Добавлена новая система меню.\n- Исправлены опечатки в 1 главе."