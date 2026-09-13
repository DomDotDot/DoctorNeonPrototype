# ==============================================================================
# Doctor Neon - Modern Language Selection Screen
# ==============================================================================

screen language_selection_screen():
    tag menu
    zorder 150
    modal True

    if main_menu:
        use main_menu_background
    else:
        add Solid("#000000b3")

    key "game_menu" action Return()

    frame:
        style "modern_panel_wide"
        xsize 1180
        padding (35, 30)

        vbox:
            spacing 12
            xfill True

            # Заголовок
            label _("Выбор языка / Language Selection") style "modern_title_label"

            # Информационная плашка
            frame:
                xfill True
                padding (18, 12)
                background Solid("#181824cc")

                hbox:
                    spacing 15
                    yalign 0.5
                    xfill True

                    text "🌐" size 26 yalign 0.5
                    vbox:
                        yalign 0.5
                        text _("Локализация игры:") size 18 bold True color "#ffffff"
                        text _("Выбор языка мгновенно обновляет диалоги, интерфейс и субтитры.") size 14 color "#aaaaaa"

                    frame:
                        xalign 1.0
                        yalign 0.5
                        background None
                        if getattr(persistent, "community_content_enabled", False):
                            text _("🟢 КОММЬЮНИТИ КОНТЕНТ ВКЛЮЧЕН") size 13 bold True color "#39ff14" yalign 0.5
                        else:
                            text _("⚪ ОФИЦИАЛЬНЫЕ ЯЗЫКИ") size 13 bold True color "#888888" yalign 0.5

            # Список доступных языков в виде интерактивных карточек
            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True
                ysize 380

                $ active_langs = get_active_languages()

                vpgrid:
                    cols 2
                    spacing 16
                    xalign 0.5

                    for lang in active_langs:
                        $ code = lang.get("code")
                        $ is_active = (_preferences.language == code)
                        $ percent = get_lang_progress(code)
                        $ is_official = lang.get("official", True)
                        $ flag_path = lang.get("flag", "")
                        $ native_title = lang.get("native_name") or lang.get("name", "Language")
                        $ sub_title = lang.get("sub_name") or (_("Официальный перевод") if is_official else (f"Автор: {lang.get('author')}" if lang.get("author") else _("Коммьюнити перевод")))

                        button:
                            xsize 530
                            ysize 116
                            padding (14, 12)
                            background (Solid("#00ffcc18") if is_active else Solid("#141420cc"))
                            hover_background (Solid("#00ffcc33") if is_active else Solid("#202032cc"))
                            hover_sound "audio/sfx/cursor-hover.opus"
                            activate_sound "audio/sfx/button-click.opus"
                            action Function(select_game_language, code)

                            hbox:
                                spacing 14
                                yalign 0.5
                                xfill True

                                # Контейнер иконки/флага 1:1
                                frame:
                                    xsize 76
                                    ysize 76
                                    padding (3, 3)
                                    background (Solid("#39ff1444") if is_active else Solid("#222230"))
                                    yalign 0.5

                                    if renpy.loadable(flag_path):
                                        add flag_path xsize 70 ysize 70 fit "contain" xalign 0.5 yalign 0.5
                                    else:
                                        text ("🌐" if not is_official else "🏳️") size 34 xalign 0.5 yalign 0.5

                                # Информация о языке
                                vbox:
                                    spacing 3
                                    yalign 0.5
                                    xsize 280

                                    hbox:
                                        spacing 8
                                        text native_title size 20 bold True color ("#39ff14" if is_active else "#ffffff")
                                        if is_official:
                                            text _("[[ОФИЦИАЛЬНЫЙ]]") substitute False size 11 bold True color "#00d4ff" yalign 0.5
                                        else:
                                            text _("[[КОММЬЮНИТИ]]") substitute False size 11 bold True color "#ffaa00" yalign 0.5

                                    text sub_title size 13 color "#aaaaaa"

                                    # Прогресс перевода
                                    if percent >= 100:
                                        hbox:
                                            spacing 6
                                            yalign 0.5
                                            text "✓" size 13 bold True color "#39ff14"
                                            text _("100% Завершено") size 13 color "#39ff14"
                                    else:
                                        hbox:
                                            spacing 8
                                            yalign 0.5
                                            bar:
                                                value percent
                                                range 100
                                                xsize 120
                                                ysize 8
                                                yalign 0.5
                                                left_bar Solid("#00d4ff")
                                                right_bar Solid("#222233")
                                            text f"{percent}%" size 13 color "#00d4ff" yalign 0.5

                                # Правый индикатор статуса
                                frame:
                                    xalign 1.0
                                    yalign 0.5
                                    background None

                                    if is_active:
                                        frame:
                                            background Solid("#39ff14")
                                            padding (12, 6)
                                            text _("● АКТИВЕН") size 13 bold True color "#000000"
                                    else:
                                        frame:
                                            background Solid("#252538")
                                            hover_background Solid("#3a3a50")
                                            padding (12, 6)
                                            text _("ВЫБРАТЬ") size 13 bold True color "#aaaaaa"

            null height 4

            # Подсказка о коммьюнити контенте
            if not getattr(persistent, "community_content_enabled", False):
                hbox:
                    xalign 0.5
                    spacing 8
                    text "💡" size 16
                    text _("Нужны фанатские переводы? Включите «Коммьюнити Контент» в Менеджере модов.") size 14 color "#888888"

            # Нижняя панель действий
            hbox:
                xalign 0.5
                spacing 25

                textbutton _("🧩 Менеджер модов"):
                    action ShowMenu("mod_manager_screen")
                    style "modern_button"
                    xsize 250
                    ysize 52
                    text_size 17

                textbutton _("Назад"):
                    action Return()
                    style "modern_button"
                    xsize 180
                    ysize 52
                    text_size 17