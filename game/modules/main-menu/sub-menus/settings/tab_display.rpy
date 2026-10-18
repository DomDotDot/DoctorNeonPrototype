################################################################################
## Раздел 1: Текст и Графика (Display & Text) - Идеальная симметрия 2 колонок
################################################################################

screen settings_tab_display():
    on "show" action Function(restart_text_preview)
    on "replace" action Function(restart_text_preview)

    $ cur_disp_mode = get_game_display_mode()
    $ cps_val = int(preferences.text_cps)
    $ cps_text = f"{cps_val} зн/с" if cps_val > 0 else _("Мгновенно")
    $ afm_val = int(preferences.afm_time) if getattr(preferences, "afm_time", 0) > 0 else 0
    $ afm_text = f"{afm_val} сек" if afm_val > 0 else _("Выкл")

    vbox:
        spacing 10
        xfill True

        # Информационная плашка сверху
        frame:
            xfill True
            padding (16, 10)
            background Solid("#181824cc")

            hbox:
                spacing 14
                yalign 0.5
                xfill True

                text "🖥️" size 24 yalign 0.5
                vbox:
                    yalign 0.5
                    text _("Настройки экрана и вывода текста:") size 17 bold True color "#ffffff"
                    text _("Регулировка режима окна, скорости вывода реплик и параметров пропуска.") size 13 color "#aaaaaa"

                frame:
                    xalign 1.0
                    yalign 0.5
                    background None
                    if cur_disp_mode == "fullscreen":
                        frame:
                            background Solid("#0284c7")
                            padding (10, 5)
                            text _("🖥️ ПОЛНЫЙ ЭКРАН") size 12 bold True color "#ffffff"
                    elif cur_disp_mode == "borderless":
                        frame:
                            background Solid("#059669")
                            padding (10, 5)
                            text _("🔲 БЕЗ РАМОК") size 12 bold True color "#ffffff"
                    else:
                        frame:
                            background Solid("#1e293b")
                            padding (10, 5)
                            text _("🪟 ОКОННЫЙ РЕЖИМ") size 12 bold True color "#38bdf8"

        # Две колонки по 535px
        hbox:
            spacing 20
            xalign 0.5

            # ==================================================================
            # ЛЕВАЯ КОЛОНКА: Режим экрана + Скорость текста (535px)
            # ==================================================================
            vbox:
                xsize 535
                spacing 10

                # Карточка 1: Режим отображения экрана (3 ровные кнопки в ряд)
                frame:
                    style "settings_card"
                    vbox:
                        spacing 8
                        xfill True

                        hbox:
                            xfill True
                            yalign 0.5
                            text _("РЕЖИМ ЭКРАНА") size 15 bold True color "#00d4ff"
                            text _("Формат окна игры") size 12 color "#888888" yalign 0.5

                        hbox:
                            spacing 8
                            xalign 0.5

                            button:
                                xsize 158
                                ysize 44
                                style "settings_chip_btn"
                                selected (cur_disp_mode == "window")
                                action Function(set_game_display_mode, "window")
                                hbox:
                                    align (0.5, 0.5)
                                    spacing 6
                                    text "🪟" size 15 yalign 0.5
                                    text _("Оконный"):
                                        style "settings_chip_text"
                                        size 13
                                        color ("#39ff14" if cur_disp_mode == "window" else "#cbd5e1")

                            button:
                                xsize 158
                                ysize 44
                                style "settings_chip_btn"
                                selected (cur_disp_mode == "borderless")
                                action Function(set_game_display_mode, "borderless")
                                hbox:
                                    align (0.5, 0.5)
                                    spacing 6
                                    text "🔲" size 15 yalign 0.5
                                    text _("Без рамок"):
                                        style "settings_chip_text"
                                        size 13
                                        color ("#39ff14" if cur_disp_mode == "borderless" else "#cbd5e1")

                            button:
                                xsize 158
                                ysize 44
                                style "settings_chip_btn"
                                selected (cur_disp_mode == "fullscreen")
                                action Function(set_game_display_mode, "fullscreen")
                                hbox:
                                    align (0.5, 0.5)
                                    spacing 6
                                    text "🖥️" size 15 yalign 0.5
                                    text _("Полный"):
                                        style "settings_chip_text"
                                        size 13
                                        color ("#39ff14" if cur_disp_mode == "fullscreen" else "#cbd5e1")

                # Карточка 2: Скорость диалогов и авточтение
                frame:
                    style "settings_card"
                    vbox:
                        spacing 8
                        xfill True

                        hbox:
                            xfill True
                            yalign 0.5
                            text _("СКОРОСТЬ ВЫВОДА ТЕКСТА") size 15 bold True color "#00d4ff"
                            text _("Динамика диалогов") size 12 color "#888888" yalign 0.5

                        # Скорость печати
                        vbox:
                            spacing 2
                            xfill True
                            hbox:
                                xfill True
                                yalign 0.5
                                text _("Скорость печати:") size 13 color "#dddddd"
                                hbox:
                                    xalign 1.0
                                    spacing 8
                                    text cps_text size 13 bold True color ("#39ff14" if cps_val == 0 else "#00d4ff")
                                    button:
                                        style "settings_mini_btn"
                                        action Preference("text speed", 25)
                                        tooltip _("Сбросить скорость текста к значению по умолчанию")
                                        text "↺" style "settings_mini_btn_text"

                            bar value Preference("text speed") style "settings_slider_bar"

                        # Время авточтения
                        vbox:
                            spacing 2
                            xfill True
                            hbox:
                                xfill True
                                yalign 0.5
                                text _("Задержка авточтения:") size 13 color "#dddddd"
                                hbox:
                                    xalign 1.0
                                    spacing 8
                                    text afm_text size 13 bold True color ("#888888" if afm_val == 0 else "#00d4ff")
                                    button:
                                        style "settings_mini_btn"
                                        action Preference("auto-forward time", 15)
                                        tooltip _("Сбросить задержку авточтения к значению по умолчанию")
                                        text "↺" style "settings_mini_btn_text"

                            bar value Preference("auto-forward time") style "settings_slider_bar"

                        # Живой интерактивный предпросмотр вывода текста
                        frame:
                            xfill True
                            background Solid("#0d0d16")
                            padding (10, 8)
                            vbox:
                                spacing 4
                                hbox:
                                    xfill True
                                    yalign 0.5
                                    text _("ПРЕДПРОСМОТР ВЫВОДА РЕПЛИК:") size 10 bold True color "#64748b" yalign 0.5
                                    hbox:
                                        xalign 1.0
                                        spacing 8
                                        if cps_val == 0:
                                            text _("МГНОВЕННО") size 10 bold True color "#39ff14" yalign 0.5
                                        else:
                                            text f"{cps_val} зн/с" size 10 bold True color "#00d4ff" yalign 0.5
                                        button:
                                            style "settings_mini_btn"
                                            action Function(restart_text_preview)
                                            tooltip _("Перезапустить анимацию вывода текста")
                                            text _("↻ Тест") style "settings_mini_btn_text"

                                fixed:
                                    xfill True
                                    ysize 32
                                    add DynamicDisplayable(text_preview_dynamic)

            # ==================================================================
            # ПРАВАЯ КОЛОНКА: Пропуск + Специальные опции (535px)
            # ==================================================================
            vbox:
                xsize 535
                spacing 10

                # Карточка 3: Параметры пропуска
                frame:
                    style "settings_card"
                    vbox:
                        spacing 6
                        xfill True

                        hbox:
                            xfill True
                            yalign 0.5
                            text _("ПАРАМЕТРЫ ПРОПУСКА") size 15 bold True color "#00d4ff"
                            text _("Быстрая перемотка") size 12 color "#888888" yalign 0.5

                        button:
                            xfill True
                            ysize 36
                            style "settings_chip_btn"
                            action Preference("skip", "toggle")
                            tooltip _("Позволяет пропускать новый, ещё не прочитанный текст.")
                            hbox:
                                xfill True
                                yalign 0.5
                                text _("⏩ Непрочитанный текст") size 13 color "#e2e8f0" yalign 0.5
                                $ is_sk_unseen = bool(getattr(_preferences, "skip_unseen", False))
                                frame:
                                    xalign 1.0
                                    yalign 0.5
                                    background (Solid("#39ff14") if is_sk_unseen else Solid("#222230"))
                                    padding (8, 2)
                                    text (_("✓ ВКЛ") if is_sk_unseen else _("✕ ВЫКЛ")) size 11 bold True color ("#000000" if is_sk_unseen else "#888888")

                        button:
                            xfill True
                            ysize 36
                            style "settings_chip_btn"
                            action Preference("after choices", "toggle")
                            tooltip _("Продолжать перемотку после совершения сюжетного выбора.")
                            hbox:
                                xfill True
                                yalign 0.5
                                text _("🔀 После сюжетных выборов") size 13 color "#e2e8f0" yalign 0.5
                                $ is_sk_choices = bool(getattr(_preferences, "skip_after_choices", False))
                                frame:
                                    xalign 1.0
                                    yalign 0.5
                                    background (Solid("#39ff14") if is_sk_choices else Solid("#222230"))
                                    padding (8, 2)
                                    text (_("✓ ВКЛ") if is_sk_choices else _("✕ ВЫКЛ")) size 11 bold True color ("#000000" if is_sk_choices else "#888888")

                        button:
                            xfill True
                            ysize 36
                            style "settings_chip_btn"
                            action InvertSelected(Preference("transitions", "toggle"))
                            tooltip _("Пропускать анимации и графические переходы между сценами.")
                            hbox:
                                xfill True
                                yalign 0.5
                                text _("⚡ Пропуск переходов") size 13 color "#e2e8f0" yalign 0.5
                                $ is_sk_trans = bool(getattr(_preferences, "transitions", 2) == 0)
                                frame:
                                    xalign 1.0
                                    yalign 0.5
                                    background (Solid("#39ff14") if is_sk_trans else Solid("#222230"))
                                    padding (8, 2)
                                    text (_("✓ ВКЛ") if is_sk_trans else _("✕ ВЫКЛ")) size 11 bold True color ("#000000" if is_sk_trans else "#888888")


