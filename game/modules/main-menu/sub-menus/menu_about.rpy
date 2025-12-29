# Файл: menu_about.rpy

################################################################################
## Саб-меню "Об игре"
################################################################################

screen about_menu():
    tag menu
    zorder 25
    modal True

    use main_menu_background
    key "game_menu" action ShowMenu("main_menu") 

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
## Экраны информации
################################################################################

screen license_screen():
    tag menu
    zorder 25
    use game_menu(_("Лицензия"), scroll="viewport"):
        vbox:
            style_prefix "about"
            spacing 20

            label _("Музыка")
            text "ksho - Purge Protocol\n{a=https://www.youtube.com/watch?v=BecKecHBOdc}Источник{/a}"
            text "Factorio - Swell Pad\n{a=https://www.youtube.com/watch?v=2C8-u0IkQVk}Источник{/a}\n"
            text "Rewrite - Potted One\n{a=https://www.youtube.com/watch?v=2C8-u0IkQVk}Источник{/a}\n"
            text "Rewrite - Sorrowless\n{a=https://www.youtube.com/watch?v=rIwl2cDwStw}Источник{/a}\n"
            text "Rewrite - Rememberance\n{a=}Источник{/a}\n"
            text "Rewrite - Reply\n{a=}Источник{/a}\n"
            text "PRESSURE - One Way Trip\n{a=https://www.youtube.com/watch?v=8yFUzUmWe4M}Источник{/a}\n"
            text "PRESSURE - First Theme\n{a=}Источник{/a}\n"
            text "Steins;Gate - Self Affirmation\n{a=}Источник{/a}\n"
            text "Steins;Gate - Quiet Air\n{a=}Источник{/a}\n"
            text "Occultic;Nine - OVERCAST-EYES\n{a=}Источник{/a}\n"
            text "CHAOS;HEAD - Colors\n{a=}Источник{/a}\n"
            text "Shadows of Doubt - Revpad\n{a=}Источник{/a}\n"
            text "Shadows of Doubt - LD Celts\n{a=}Источник{/a}\n"
            text "Shadows of Doubt - FM Modul\n{a=}Источник{/a}\n"
            text "Intravenous - Initiation (Inactive)\n{a=}Источник{/a}\n"
            text "Avery Alexander - HRT\n{a=https://www.youtube.com/watch?v=7OpLRMyiueY}Источник{/a}\n"



            label _("Музыка в меню")
            text "1 - NightMare\n"
            text "2 - FearForUnreal\n"
            text "3 - Sorrowless\n"
            text "4 - BuzzingGoodbye\n"

screen credits_screen():
    tag menu
    use game_menu(_("Титры"), scroll="viewport"):
        vbox:
            style_prefix "about"
            spacing 15
            
            text "Спасибо за игру в этот прототип..."
            text "Автор и Разработчик: {a=https://dotprod.itch.io/}Dot{/a}\n"
            text "Тестировщик и Вдохновитель: Overhappy_Avali\n"

screen update_screen():
    tag menu
    use game_menu(_("Обновление")):
        vbox:
            style_prefix "about"
            xalign 0.5
            yalign 0.5

            text _("Текущая версия: [config.version]\n")
            text _("\nСписок изменений:\n- Оптимизация и DLC Контент")