################################################################################
## Саб-меню "Настройки"
################################################################################

screen settings_menu():
    tag menu
    zorder 25
    modal True

    if main_menu:
        use main_menu_background
    else:
        add Solid("#000000b3")
        
    key "game_menu" action Return()

    frame:
        style "modern_panel"
        vbox:
            style "modern_vbox"
            label _("Настройки") style "modern_title_label"

            textbutton _("Текст/Графика") action ShowMenu("graphics_settings_screen") style "modern_button"
            textbutton _("Звук") action ShowMenu("sound_settings_screen") style "modern_button"
            
            # Если есть экран языка
            textbutton _("Язык") action ShowMenu("language_selection_screen") style "modern_button"
            
            if not renpy.variant("web"):
                textbutton _("DLC Контент") action Function(renpy.call_in_new_context, "dlc_manager_main", is_in_game=not main_menu) style "modern_button"
            else:
                textbutton _("DLC Контент (Только ПК)") action None style "modern_button" text_color "#888"

            textbutton _("Управление данными") action ShowMenu("data_settings_screen") style "modern_button" text_color "#a11919"

            null height 30
            textbutton _("Назад") action Return() style "modern_back_button"


################################################################################
## Экран настроек Текста и Графики
################################################################################

screen graphics_settings_screen():
    tag menu
    zorder 50
    modal True

    if main_menu:
        use main_menu_background
    else:
        add Solid("#000000b3")
        
    key "game_menu" action ShowMenu("settings_menu") 

    frame:
        style "modern_panel"
        vbox:
            style "modern_vbox"
            label _("Текст и Графика") style "modern_title_label"

            grid 2 1:
                xalign 0.5
                xsize 900
                spacing 80

                # Левая колонка
                vbox:
                    style_prefix "settings_check"
                    spacing 15
                    
                    label _("Режим экрана")
                    textbutton _("Оконный") action Preference("display", "window")
                    textbutton _("Полный") action Preference("display", "fullscreen")

                    null height 20

                    label _("Пропуск")
                    textbutton _("Непрочитанного текста") action Preference("skip", "toggle")
                    textbutton _("После выборов") action Preference("after choices", "toggle")
                    textbutton _("Переходов") action InvertSelected(Preference("transitions", "toggle"))

                # Правая колонка
                vbox:
                    spacing 15

                    vbox:
                        style_prefix "settings_slider"
                        spacing 5
                        xsize 400
                        
                        $ cps_val = int(preferences.text_cps)
                        $ cps_text = str(cps_val) if cps_val > 0 else _("Мгн.")
                        
                        label _("Скорость текста: ") + cps_text
                        bar value Preference("text speed") xsize 400

                    null height 15

                    vbox:
                        style_prefix "settings_check"
                        spacing 15

                        label _("Доступность")
                        textbutton _("Включение Чувствительнного контента (18+)"):
                            action ToggleField(persistent, "sensitive_mode")
                            tooltip _("Включает отображение откровенных сцен.")
                        
                        textbutton _("ИИ Чувствительность"):
                            action ToggleField(persistent, "ai_sensitive_mode")

                        textbutton _("Крупный шрифт"):
                            action ToggleField(persistent, "font_size_large")

                    

            null yfill True
            textbutton _("Назад") action ShowMenu("settings_menu") style "modern_back_button"


################################################################################
## Экран настроек Звука
################################################################################

screen sound_settings_screen():
    tag menu
    zorder 50
    modal True
    
    if main_menu:
        use main_menu_background
    else:
        add Solid("#000000b3")
        
    key "game_menu" action ShowMenu("settings_menu") 

    frame:
        style "modern_panel"
        vbox:
            style "modern_vbox"
            label _("Звук") style "modern_title_label"
            
            vbox:
                style_prefix "settings_slider"
                xalign 0.5
                spacing 15

                if config.has_music:
                    label _("Громкость музыки")
                    hbox:
                        bar value Preference("music volume")
                        textbutton "Тест" action Play("music", config.sample_sound) style "settings_test_button"

                if config.has_sound:
                    label _("Громкость звуков")
                    hbox:
                        bar value Preference("sound volume")
                        if config.sample_sound:
                            textbutton _("Тест") action Play("sound", config.sample_sound) style "settings_test_button"

                if config.has_voice:
                    label _("Громкость голоса")
                    hbox:
                        bar value Preference("voice volume")
                        if config.sample_voice:
                            textbutton _("Тест") action Play("voice", config.sample_voice) style "settings_test_button"
            
            null height 30

            textbutton _("Без звука"):
                action Preference("all mute", "toggle")
                style "settings_check_button"
                xalign 0.5

            null height 30
            textbutton _("Назад") action ShowMenu("settings_menu") style "modern_back_button"