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
        style "modern_panel"
        vbox:
            style "modern_vbox"
            label _("Об игре") style "modern_title_label"

            textbutton _("Управление") action ShowMenu("help") style "modern_button"
            textbutton _("Лицензия") action ShowMenu("license_screen") style "modern_button"
            textbutton _("Титры") action ShowMenu("credits_screen") style "modern_button"
            textbutton _("Обновление") action ShowMenu("update_screen") style "modern_button"

            null height 30
            textbutton _("Назад") action ShowMenu("main_menu") style "modern_back_button"

################################################################################
## Экраны информации
################################################################################

screen license_screen():
    tag menu
    zorder 25
    modal True
    use main_menu_background
    key "game_menu" action ShowMenu("about_menu")

    frame:
        style "modern_panel"
        vbox:
            style "modern_vbox"
            label _("Лицензия") style "modern_title_label"

            viewport:
                mousewheel True
                draggable True
                scrollbars "vertical"
                xsize 900
                ysize 600
                xalign 0.5
                
                vbox:
                    style_prefix "about"
                    spacing 20

                    label _("Музыка")
                    text "ksho - Purge Protocol\n{a=https://www.youtube.com/watch?v=BecKecHBOdc}Источник{/a}"
                    text "Factorio - Swell Pad\n{a=https://www.youtube.com/watch?v=2C8-u0IkQVk}Источник{/a}\n"
                    text "Rewrite - Potted One\n{a=https://www.youtube.com/watch?v=2C8-u0IkQVk}Источник{/a}\n"
                    text "Rewrite - Sorrowless\n{a=https://www.youtube.com/watch?v=rIwl2cDwStw}Источник{/a}\n"
                    text "Rewrite - Rememberance\n"
                    text "Rewrite - Reply\n"
                    text "PRESSURE - One Way Trip\n{a=https://www.youtube.com/watch?v=8yFUzUmWe4M}Источник{/a}\n"
                    text "PRESSURE - First Theme\n"
                    text "Steins;Gate - Self Affirmation\n"
                    text "Steins;Gate - Quiet Air\n"
                    text "Steins;Gate - Chaos Mind\n"
                    text "Steins;Gate - SERN\n"
                    text "Occultic;Nine - OVERCAST-EYES\n"
                    text "Occultic;Nine - GRAY HEARTS\n"
                    text "Occultic;Nine - LISTEN\n"
                    text "CHAOS;HEAD - Colors\n"
                    text "Shadows of Doubt - Revpad\n"
                    text "Shadows of Doubt - LD Celts\n"
                    text "Shadows of Doubt - FM Modul\n"
                    text "Intravenous - Initiation (Inactive)\n"
                    text "Avery Alexander - HRT\n{a=https://www.youtube.com/watch?v=7OpLRMyiueY}Источник{/a}\n"
                    text "AND ONE - Angel Eyes\n"
                    text "Ezio Bosso - Rain, In Your Black Eyes\n"
                    text "Ever 17: The Out of Infinity - Karma\n"
                    text "Date a Live - Marionettica\n"
                    text "Brandon Fiechter - Eyes of the Forest\n"
                    text "God Smiles - Tilman Sillescu\n"

                    label _("Музыка в меню")
                    text "1 - NightMare\n"
                    text "2 - FearForUnreal\n"
                    text "3 - Sorrowless\n"
            null height 20
            textbutton _("Назад") action ShowMenu("about_menu") style "modern_back_button"

screen credits_screen():
    tag menu
    zorder 25
    modal True
    use main_menu_background
    key "game_menu" action ShowMenu("about_menu")

    frame:
        style "modern_panel"
        vbox:
            style "modern_vbox"
            label _("Титры") style "modern_title_label"

            viewport:
                mousewheel True
                draggable True
                scrollbars "vertical"
                xsize 900
                ysize 600
                xalign 0.5
                
                vbox:
                    style_prefix "about"
                    spacing 15
            
                    text _("Спасибо за игру в этот прототип. Это моя первая визуальная новелла, и я многому научился в процессе её создания. Я надеюсь, что вам понравится история и персонажи, и я с нетерпением жду возможности поделиться с вами остальной частью истории в будущем.\n")
                    text _("Автор и Разработчик: {a=https://dotprod.itch.io/}Dot{/a}\n")
                    text _("Тестировщик и Вдохновитель: Overhappy_Avali\n")

            null height 20
            textbutton _("Назад") action ShowMenu("about_menu") style "modern_back_button"

screen update_screen():
    tag menu
    zorder 25
    modal True
    use main_menu_background
    key "game_menu" action ShowMenu("about_menu")

    frame:
        style "modern_panel"
        vbox:
            style "modern_vbox"
            label _("Обновление") style "modern_title_label"

            vbox:
                style_prefix "about"
                xalign 0.5
                yalign 0.5

                text _("Текущая версия: [config.version]\n")
                text _("\nСписок изменений:\n- Оптимизация и DLC Контент")

            null yfill True
            textbutton _("Назад") action ShowMenu("about_menu") style "modern_back_button"