################################################################################
## Раздел 4: Язык (Language Selection)
################################################################################

screen settings_tab_language():
    $ active_langs = get_active_languages()

    vbox:
        spacing 10
        xfill True

        frame:
            xfill True
            padding (16, 10)
            background Solid("#181824cc")

            hbox:
                spacing 14
                yalign 0.5
                xfill True

                text "🌐" size 24 yalign 0.5
                vbox:
                    yalign 0.5
                    text _("Язык интерфейса и субтитров / Language Selection:") size 17 bold True color "#ffffff"
                    text _("Выбор языка мгновенно обновляет диалоги, интерфейс и субтитры.") size 13 color "#aaaaaa"

                frame:
                    xalign 1.0
                    yalign 0.5
                    background None
                    if getattr(persistent, "community_content_enabled", False):
                        text _("🟢 КОММЬЮНИТИ КОНТЕНТ ВКЛЮЧЕН") size 12 bold True color "#39ff14" yalign 0.5
                    else:
                        text _("⚪ ОФИЦИАЛЬНЫЕ ЯЗЫКИ") size 12 bold True color "#888888" yalign 0.5

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            xsize 1100
            ysize 470
            xalign 0.5

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
                        ysize 100
                        padding (14, 10)
                        background (Solid("#00ffcc18") if is_active else Solid("#141420cc"))
                        hover_background (Solid("#00ffcc33") if is_active else Solid("#202032cc"))
                        hover_sound "audio/sfx/cursor-hover.opus"
                        activate_sound "audio/sfx/button-click.opus"
                        action Function(select_game_language, code)

                        hbox:
                            spacing 14
                            yalign 0.5
                            xfill True

                            frame:
                                xsize 68
                                ysize 68
                                padding (2, 2)
                                background (Solid("#39ff1444") if is_active else Solid("#222230"))
                                yalign 0.5

                                if renpy.loadable(flag_path):
                                    add flag_path xsize 64 ysize 64 fit "contain" xalign 0.5 yalign 0.5
                                else:
                                    text ("🌐" if not is_official else "🏳️") size 30 xalign 0.5 yalign 0.5

                            vbox:
                                spacing 2
                                yalign 0.5
                                xsize 280

                                hbox:
                                    spacing 8
                                    text native_title size 18 bold True color ("#39ff14" if is_active else "#ffffff")
                                    if is_official:
                                        text _("[[ОФИЦИАЛЬНЫЙ]]") substitute False size 10 bold True color "#00d4ff" yalign 0.5
                                    else:
                                        text _("[[КОММЬЮНИТИ]]") substitute False size 10 bold True color "#ffaa00" yalign 0.5

                                text sub_title size 12 color "#aaaaaa"

                                if percent >= 100:
                                    text _("✓ 100% Завершено") size 12 color "#39ff14"
                                else:
                                    text f"{percent}% Завершено" size 12 color "#00d4ff"

                            frame:
                                xalign 1.0
                                yalign 0.5
                                background None

                                if is_active:
                                    frame:
                                        background Solid("#39ff14")
                                        padding (10, 5)
                                        text _("● АКТИВЕН") size 12 bold True color "#000000"
                                else:
                                    frame:
                                        background Solid("#252538")
                                        padding (10, 5)
                                        text _("ВЫБРАТЬ") size 12 bold True color "#aaaaaa"


