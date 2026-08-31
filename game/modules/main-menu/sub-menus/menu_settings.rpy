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

            use icon_button("🖥️", _("Текст/Графика"), action=ShowMenu("graphics_settings_screen"), btn_style="modern_button")
            use icon_button("🔊", _("Звук"), action=ShowMenu("sound_settings_screen"), btn_style="modern_button")
            
            # Если есть экран языка
            use icon_button("🌐", _("Язык"), action=ShowMenu("language_selection_screen"), btn_style="modern_button")
            
            if not renpy.variant("web"):
                use icon_button("📦", _("DLC Контент"), action=Function(renpy.call_in_new_context, "dlc_manager_main", is_in_game=not main_menu), btn_style="modern_button")
            else:
                use icon_button("📦", _("DLC Контент (Только ПК)"), action=None, btn_style="modern_button", txt_color="#888")

            use icon_button("💾", _("Управление данными"), action=ShowMenu("data_settings_screen"), btn_style="modern_button", txt_color="#a11919")

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
                        hbox:
                            spacing 10
                            textbutton "↺":
                                action Preference("text speed", getattr(config, "default_text_cps", 0))
                                style "settings_test_button"
                                xsize 45
                                left_margin 0
                                tooltip _("Сбросить")
                            bar value Preference("text speed") xsize 345 yalign 0.5

                    null height 15

                    vbox:
                        style_prefix "settings_slider"
                        spacing 5
                        xsize 400
                        
                        $ afm_val = int(preferences.afm_time) if getattr(preferences, "afm_time", 0) > 0 else 0
                        $ afm_text = str(afm_val) if afm_val > 0 else _("Выкл")
                        
                        label _("Скорость авточтения: ") + afm_text
                        hbox:
                            spacing 10
                            textbutton "↺":
                                action Preference("auto-forward time", getattr(config, "default_afm_time", 15))
                                style "settings_test_button"
                                xsize 45
                                left_margin 0
                                tooltip _("Сбросить")
                            bar value Preference("auto-forward time") xsize 345 yalign 0.5

                    null height 15

                    vbox:
                        style_prefix "settings_check"
                        spacing 15

                        label _("Доступность")
                        textbutton _("Включение Чувствительнного контента (18+)"):
                            action Function(toggle_sensitive_mode_with_check)
                            tooltip _("Включает отображение откровенных сцен.")
                        
                        textbutton _("ИИ Чувствительность"):
                            action Function(toggle_ai_sensitive_with_check)

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
                    $ mus_vol = int(preferences.volumes["music"] * 100)
                    label _("Громкость музыки: ") + str(mus_vol) + "%"
                    hbox:
                        spacing 10
                        textbutton "↺":
                            action Preference("music volume", 1.0)
                            style "settings_test_button"
                            xsize 45
                            left_margin 0
                            tooltip _("Сбросить")
                        bar value Preference("music volume") xsize 345 yalign 0.5
                        textbutton _("Тест") action Play("music", sample_music) style "settings_test_button"

                if config.has_sound:
                    $ sfx_vol = int(preferences.volumes["sfx"] * 100)
                    label _("Громкость звуков: ") + str(sfx_vol) + "%"
                    hbox:
                        spacing 10
                        textbutton "↺":
                            action Preference("sound volume", 1.0)
                            style "settings_test_button"
                            xsize 45
                            left_margin 0
                            tooltip _("Сбросить")
                        bar value Preference("sound volume") xsize 345 yalign 0.5
                        if config.sample_sound:
                            textbutton _("Тест") action Play("sound", config.sample_sound) style "settings_test_button"

                if config.has_voice:
                    $ voi_vol = int(preferences.volumes["voice"] * 100)
                    label _("Громкость голоса: ") + str(voi_vol) + "%"
                    hbox:
                        spacing 10
                        textbutton "↺":
                            action Preference("voice volume", 1.0)
                            style "settings_test_button"
                            xsize 45
                            left_margin 0
                            tooltip _("Сбросить")
                        bar value Preference("voice volume") xsize 345 yalign 0.5
                        if config.sample_voice:
                            textbutton _("Тест") action Play("voice", config.sample_voice) style "settings_test_button"
            
                null height 15

                textbutton _("Без звука"):
                    action Preference("all mute", "toggle")
                    style "settings_check_button"

            null height 30
            textbutton _("Назад") action ShowMenu("settings_menu") style "modern_back_button"