################################################################################
## Раздел 5: Управление данными (Data Management) - Все опции и разблокировка
################################################################################

screen settings_tab_data():
    viewport:
        mousewheel True
        draggable True
        scrollbars "vertical"
        xsize 1100
        ysize 570
        xalign 0.5

        vbox:
            spacing 10
            xfill True

            # Плашка сверху
            frame:
                xfill True
                padding (16, 10)
                background Solid("#181824cc")

                hbox:
                    spacing 14
                    yalign 0.5
                    xfill True

                    text "💾" size 24 yalign 0.5
                    vbox:
                        yalign 0.5
                        text _("Управление данными, прогрессом и сохранениями:") size 17 bold True color "#ffffff"
                        text _("Сброс настроек, удаление сохранений, обнуление прогресса и разблокировка контента.") size 13 color "#aaaaaa"

            # --- СЕКЦИЯ: НАСТРОЙКИ ---
            label _("Общие настройки") text_size 16 text_color "#94a3b8" xoffset 5

            frame:
                style "danger_zone_frame"
                background Frame(Fixed(Solid("#555"), Solid("#000000", xmargin=2, ymargin=2), xysize=(100,100)), 4, 4)

                hbox:
                    yalign 0.5
                    xfill True

                    vbox:
                        yalign 0.5
                        text _("Сброс настроек") style "danger_title_text" size 16
                        text _("Вернуть громкость, скорость текста и параметры пропуска к значениям по умолчанию.") style "danger_desc_text" size 12

                    button:
                        style "neutral_button"
                        text _("Сбросить") style "danger_button_text" size 15
                        action Confirm(_("Сбросить все настройки звука и текста по умолчанию?"), yes=Function(reset_preferences_to_default))

            null height 4

            # --- СЕКЦИЯ: ОПАСНАЯ ЗОНА ---
            label _("Опасная зона (Danger Zone)") text_size 16 text_color "#ef4444" xoffset 5

            # Карточка: Сброс сюжета
            frame:
                style "danger_zone_frame_red"
                hbox:
                    yalign 0.5
                    xfill True

                    vbox:
                        yalign 0.5
                        text _("Сбросить прогресс сюжета") style "danger_title_text" size 16 color "#ffaaaa"
                        text _("Закроет все главы и вернет главное меню в исходное начальное состояние.") style "danger_desc_text" size 12

                    button:
                        style "danger_button"
                        text _("Сбросить") style "danger_button_text" size 15
                        action Confirm(_("Вы уверены? Это действие обнулит сюжетный прогресс."), yes=Function(hard_reset_progress))

            # Карточка: Удаление сейвов
            frame:
                style "danger_zone_frame_red"
                hbox:
                    yalign 0.5
                    xfill True

                    vbox:
                        yalign 0.5
                        text _("Удалить ВСЕ сохранения") style "danger_title_text" size 16 color "#ffaaaa"
                        text _("Безвозвратно удаляет абсолютно все файлы сохранений с диска.") style "danger_desc_text" size 12

                    button:
                        style "danger_button"
                        text _("Удалить всё") style "danger_button_text" size 15
                        action Confirm(_("Это действие нельзя отменить. Удалить ВСЕ сохранения?"), yes=Function(delete_all_saves))

            # Карточка: Сброс достижений
            frame:
                style "danger_zone_frame_red"
                hbox:
                    yalign 0.5
                    xfill True

                    vbox:
                        yalign 0.5
                        text _("Сбросить все достижения") style "danger_title_text" size 16 color "#ffaaaa"
                        text _("Обнуляет список всех полученных игровых достижений.") style "danger_desc_text" size 12

                    button:
                        style "danger_button"
                        text _("Сбросить") style "danger_button_text" size 15
                        action Confirm(_("Обнулить все открытые достижения?"), yes=Function(reset_all_achievements))

            # --- СЕКЦИЯ: РАЗБЛОКИРОВКА КОНТЕНТА (ЧИТЫ / ТЕСТЫ) ---
            if config.developer or getattr(persistent, "cheats_unlocked", False):
                null height 4
                label _("Разблокировка контента (Чит-коды / Тестирование)") text_size 16 text_color "#22c55e" xoffset 5

                # Unlock All
                frame:
                    style "danger_zone_frame_green"
                    hbox:
                        yalign 0.5
                        xfill True

                        vbox:
                            yalign 0.5
                            text _("Разблокировать сюжетный контент") style "danger_title_text" size 16 color "#aaffaa"
                            text _("Открывает все главы, музыку, воспоминания и фоны меню.") style "danger_desc_text" size 12

                        button:
                            style "safe_button"
                            text _("Открыть всё") style "danger_button_text" size 15
                            action Confirm(_("Открыть весь сюжетный контент и главы?"), yes=Function(unlock_everything))

                # Unlock Characters
                frame:
                    style "danger_zone_frame_green"
                    hbox:
                        yalign 0.5
                        xfill True

                        vbox:
                            yalign 0.5
                            text _("Разблокировать всех персонажей") style "danger_title_text" size 16 color "#aaffaa"
                            text _("Открывает полные досье всех персонажей в Глоссарии.") style "danger_desc_text" size 12

                        button:
                            style "safe_button"
                            text _("Открыть всех") style "danger_button_text" size 15
                            action Confirm(_("Открыть всех персонажей в Глоссарии?"), yes=Function(unlock_all_chars_full))

                # Unlock Achievements
                frame:
                    style "danger_zone_frame_green"
                    hbox:
                        yalign 0.5
                        xfill True

                        vbox:
                            yalign 0.5
                            text _("Разблокировать все достижения") style "danger_title_text" size 16 color "#aaffaa"
                            text _("Мгновенно выдает все достижения новеллы.") style "danger_desc_text" size 12

                        button:
                            style "safe_button"
                            text _("Открыть все ачивки") style "danger_button_text" size 15
                            action Confirm(_("Разблокировать все достижения?"), yes=Function(unlock_all_achievements))


