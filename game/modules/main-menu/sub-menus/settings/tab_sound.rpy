################################################################################
## Раздел 2: Звук (Audio Settings) - С Мастером, UI-звуками и музыкой меню
################################################################################

screen settings_tab_sound():
    timer 0.8 action NullAction() repeat True

    $ is_all_muted = bool(_preferences.get_mute("music") and _preferences.get_mute("sfx"))
    $ mus_vol = int(preferences.volumes["music"] * 100) if config.has_music else 0
    $ sfx_vol = int(preferences.volumes["sfx"] * 100) if config.has_sound else 0
    $ amb_vol = int(preferences.volumes.get("ambient", 1.0) * 100)
    $ voi_vol = int(preferences.volumes["voice"] * 100) if config.has_voice else 0
    $ menu_sfx_vol = int(preferences.volumes.get("menu_sfx", 0.8) * 100)
    $ main_vol = int(preferences.volumes.get("main", 1.0) * 100)
    $ menu_music_on = getattr(persistent, "main_menu_music_enabled", True)
    $ cur_track_filename, cur_track_path = get_playing_track_info()

    viewport:
        mousewheel True
        draggable True
        scrollbars "vertical"
        xfill True
        ysize 570

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

                    text "🔊" size 24 yalign 0.5
                    vbox:
                        yalign 0.5
                        text _("Аудиосистема и баланс громкости:") size 17 bold True color "#ffffff"
                        text _("Индивидуальная калибровка каналов музыки, спецэффектов, интерфейса, окружения и озвучки.") size 13 color "#aaaaaa"

                    frame:
                        xalign 1.0
                        yalign 0.5
                        background None
                        if is_all_muted:
                            frame:
                                background Solid("#dc2626")
                                padding (10, 5)
                                text _("🔇 ЗВУК ОТКЛЮЧЕН") size 12 bold True color "#ffffff"
                        else:
                            frame:
                                background Solid("#16a34a")
                                padding (10, 5)
                                text _("🔊 АУДИО АКТИВНО") size 12 bold True color "#ffffff"

            # Сетка микшера: 2 колонки по 535px
            hbox:
                spacing 20
                xalign 0.5

                # --------------------------------------------------------------
                # ЛЕВАЯ КОЛОНКА (535px): Мастер, Музыка, SFX
                # --------------------------------------------------------------
                vbox:
                    xsize 535
                    spacing 10

                    # Канал 0: Мастер-громкость
                    frame:
                        style "settings_card"
                        vbox:
                            spacing 6
                            xfill True

                            hbox:
                                xfill True
                                yalign 0.5
                                hbox:
                                    spacing 8
                                    yalign 0.5
                                    text "🎛️" size 18 yalign 0.5
                                    vbox:
                                        text _("Мастер-громкость (Основная)") size 15 bold True color "#ffffff"
                                        text _("Общий уровень всех аудиосистем") size 11 color "#888888"

                                hbox:
                                    xalign 1.0
                                    yalign 0.5
                                    spacing 8
                                    text f"{main_vol}%" size 15 bold True color "#38bdf8" yalign 0.5

                            bar value Preference("main volume") style "settings_slider_bar"

                            hbox:
                                xalign 1.0
                                spacing 8
                                button:
                                    style "settings_mini_btn"
                                    action Preference("main volume", 1.0)
                                    tooltip _("Вернуть общую громкость на 100%")
                                    text _("↺ 100%") style "settings_mini_btn_text"

                                button:
                                    style "settings_mini_btn"
                                    action Preference("all mute", "toggle")
                                    tooltip _("Заглушить все звуки / Возобновить")
                                    text (_("🔇 Без звука") if is_all_muted else _("🔊 Заглушить всё")) style "settings_mini_btn_text"

                    # Канал 1: Музыка
                    if config.has_music:
                        frame:
                            style "settings_card"
                            vbox:
                                spacing 6
                                xfill True

                                hbox:
                                    xfill True
                                    yalign 0.5
                                    hbox:
                                        spacing 8
                                        yalign 0.5
                                        text "🎵" size 18 yalign 0.5
                                        vbox:
                                            text _("Музыка") size 15 bold True color "#ffffff"
                                            text _("Саундтрек и фоновые композиции") size 11 color "#888888"

                                    hbox:
                                        xalign 1.0
                                        yalign 0.5
                                        spacing 8
                                        text f"{mus_vol}%" size 15 bold True color "#00d4ff" yalign 0.5

                                bar value Preference("music volume") style "settings_slider_bar"

                                hbox:
                                    xalign 1.0
                                    spacing 8
                                    button:
                                        style "settings_mini_btn"
                                        action Preference("music volume", 1.0)
                                        tooltip _("Вернуть громкость музыки на 100%")
                                        text _("↺ Сброс") style "settings_mini_btn_text"

                                    $ cur_sample_music = get_music_sample()
                                    button:
                                        style "settings_mini_btn"
                                        action Play("music", cur_sample_music)
                                        tooltip _("Воспроизвести образец музыки")
                                        text _("▶ Тест") style "settings_mini_btn_text"

                                    if cur_track_filename:
                                        button:
                                            style "settings_mini_btn"
                                            action Stop("music", fadeout=0.5)
                                            tooltip _("Остановить воспроизведение музыки")
                                            text _("⏹ Стоп") style "settings_mini_btn_text"

                    # Канал 2: Звуковые эффекты (SFX)
                    if config.has_sound:
                        frame:
                            style "settings_card"
                            vbox:
                                spacing 6
                                xfill True

                                hbox:
                                    xfill True
                                    yalign 0.5
                                    hbox:
                                        spacing 8
                                        yalign 0.5
                                        text "💥" size 18 yalign 0.5
                                        vbox:
                                            text _("Звуковые эффекты (SFX)") size 15 bold True color "#ffffff"
                                            text _("Шаги, выстрелы, окружение, удары") size 11 color "#888888"

                                    hbox:
                                        xalign 1.0
                                        yalign 0.5
                                        spacing 8
                                        text f"{sfx_vol}%" size 15 bold True color "#00d4ff" yalign 0.5

                                bar value Preference("sound volume") style "settings_slider_bar"

                                hbox:
                                    xalign 1.0
                                    spacing 8
                                    button:
                                        style "settings_mini_btn"
                                        action Preference("sound volume", 1.0)
                                        tooltip _("Вернуть громкость эффектов на 100%")
                                        text _("↺ Сброс") style "settings_mini_btn_text"

                                    $ sfx_sample = get_sound_sample()
                                    button:
                                        style "settings_mini_btn"
                                        action Play("sound", sfx_sample)
                                        tooltip _("Воспроизвести тестовый звуковой эффект")
                                        text _("▶ Тест SFX") style "settings_mini_btn_text"

                # --------------------------------------------------------------
                # ПРАВАЯ КОЛОНКА (535px): Звуки интерфейса, Эмбиент, Голос
                # --------------------------------------------------------------
                vbox:
                    xsize 535
                    spacing 10

                    # Канал 3: Звуки интерфейса (menu_sfx)
                    frame:
                        style "settings_card"
                        vbox:
                            spacing 6
                            xfill True

                            hbox:
                                xfill True
                                yalign 0.5
                                hbox:
                                    spacing 8
                                    yalign 0.5
                                    text "🔔" size 18 yalign 0.5
                                    vbox:
                                        text _("Звуки интерфейса (UI)") size 15 bold True color "#ffffff"
                                        text _("Наведение курсора, клики, переходы") size 11 color "#888888"

                                hbox:
                                    xalign 1.0
                                    yalign 0.5
                                    spacing 8
                                    text f"{menu_sfx_vol}%" size 15 bold True color "#00d4ff" yalign 0.5

                            bar value Preference("menu_sfx volume") style "settings_slider_bar"

                            hbox:
                                xalign 1.0
                                spacing 8
                                button:
                                    style "settings_mini_btn"
                                    action Preference("menu_sfx volume", 1.0)
                                    tooltip _("Вернуть громкость интерфейса на 100%")
                                    text _("↺ Сброс") style "settings_mini_btn_text"

                                button:
                                    style "settings_mini_btn"
                                    action Play("menu_sfx", "audio/sfx/button-click.opus")
                                    tooltip _("Протестировать звук нажатия кнопки")
                                    text _("▶ Тест клика") style "settings_mini_btn_text"

                    # Канал 4: Фоновый эмбиент
                    frame:
                        style "settings_card"
                        vbox:
                            spacing 6
                            xfill True

                            hbox:
                                xfill True
                                yalign 0.5
                                hbox:
                                    spacing 8
                                    yalign 0.5
                                    text "🍃" size 18 yalign 0.5
                                    vbox:
                                        text _("Фоновый эмбиент") size 15 bold True color "#ffffff"
                                        text _("Атмосфера города, дождь, ветер, гул") size 11 color "#888888"

                                hbox:
                                    xalign 1.0
                                    yalign 0.5
                                    spacing 8
                                    text f"{amb_vol}%" size 15 bold True color "#00d4ff" yalign 0.5

                            bar value Preference("ambient volume") style "settings_slider_bar"

                            hbox:
                                xalign 1.0
                                spacing 8
                                button:
                                    style "settings_mini_btn"
                                    action Preference("ambient volume", 1.0)
                                    tooltip _("Вернуть громкость эмбиента на 100%")
                                    text _("↺ Сброс") style "settings_mini_btn_text"

                    # Канал 5: Голос и озвучка
                    if config.has_voice:
                        frame:
                            style "settings_card"
                            vbox:
                                spacing 6
                                xfill True

                                hbox:
                                    xfill True
                                    yalign 0.5
                                    hbox:
                                        spacing 8
                                        yalign 0.5
                                        text "🎙️" size 18 yalign 0.5
                                        vbox:
                                            text _("Голос и озвучка") size 15 bold True color "#ffffff"
                                            text _("Реплики и озвучка персонажей") size 11 color "#888888"

                                    hbox:
                                        xalign 1.0
                                        yalign 0.5
                                        spacing 8
                                        text f"{voi_vol}%" size 15 bold True color "#00d4ff" yalign 0.5

                                bar value Preference("voice volume") style "settings_slider_bar"

                                hbox:
                                    xalign 1.0
                                    spacing 8
                                    button:
                                        style "settings_mini_btn"
                                        action Preference("voice volume", 1.0)
                                        tooltip _("Вернуть громкость голоса на 100%")
                                        text _("↺ Сброс") style "settings_mini_btn_text"

                                    $ cur_voice_sample = get_voice_sample()
                                    if cur_voice_sample:
                                        button:
                                            style "settings_mini_btn"
                                            action Play("voice", cur_voice_sample)
                                            tooltip _("Воспроизвести образец голоса")
                                            text _("▶ Тест") style "settings_mini_btn_text"

            # ------------------------------------------------------------------
            # Нижний ряд: Музыка главного меню + Мастер сброс (535px x 2)
            # ------------------------------------------------------------------
            hbox:
                spacing 20
                xalign 0.5

                # Карточка 7: Музыка главного меню и текущий трек
                frame:
                    style "settings_card"
                    xsize 535
                    vbox:
                        spacing 6
                        xfill True

                        hbox:
                            xfill True
                            yalign 0.5
                            text _("МУЗЫКА ГЛАВНОГО МЕНЮ") size 14 bold True color "#00d4ff"
                            if menu_music_on:
                                text _("● Музыка включена") size 11 bold True color "#39ff14" yalign 0.5
                            else:
                                text _("○ Музыка отключена") size 11 color "#ef4444" yalign 0.5

                        button:
                            xfill True
                            ysize 36
                            style "settings_chip_btn"
                            selected menu_music_on
                            action Function(toggle_main_menu_music)
                            tooltip _("Включает или отключает воспроизведение музыки на экранах главного меню.")
                            hbox:
                                xfill True
                                yalign 0.5
                                hbox:
                                    spacing 6
                                    yalign 0.5
                                    text "🏛️" size 14 yalign 0.5
                                    text _("Музыка в главном меню:"):
                                        style "settings_chip_text"
                                        size 12
                                        color ("#39ff14" if menu_music_on else "#cbd5e1")
                                frame:
                                    xalign 1.0
                                    yalign 0.5
                                    background (Solid("#39ff14") if menu_music_on else Solid("#222230"))
                                    padding (8, 2)
                                    text (_("✓ ВКЛЮЧЕНА") if menu_music_on else _("✕ ОТКЛЮЧЕНА")):
                                        size 10
                                        bold True
                                        color ("#000000" if menu_music_on else "#94a3b8")

                        # Текущий трек
                        frame:
                            xfill True
                            background Solid("#0d0d16")
                            padding (8, 6)
                            vbox:
                                spacing 2
                                hbox:
                                    xfill True
                                    yalign 0.5
                                    text _("СЕЙЧАС ИГРАЕТ:") size 10 bold True color "#64748b" yalign 0.5
                                    if cur_track_filename:
                                        text _("МУЗЫКАЛЬНЫЙ ТРЕК") size 10 bold True color "#00d4ff" yalign 0.5
                                    else:
                                        text _("ТИШИНА") size 10 bold True color "#64748b" yalign 0.5

                                hbox:
                                    spacing 6
                                    yalign 0.5
                                    text ("🎶" if cur_track_filename else "⏹️") size 12 yalign 0.5
                                    if cur_track_filename:
                                        text cur_track_filename:
                                            size 11
                                            bold True
                                            color "#38bdf8"
                                            yalign 0.5
                                    else:
                                        text _("Фоновая музыка не воспроизводится"):
                                            size 11
                                            color "#64748b"
                                            yalign 0.5

                                if cur_track_path:
                                    text cur_track_path size 9 color "#475569"

                # Карточка 8: Мастер-сброс всех каналов микшера
                frame:
                    style "settings_card"
                    xsize 535
                    vbox:
                        spacing 8
                        xfill True

                        hbox:
                            xfill True
                            yalign 0.5
                            text _("ОБЩИЙ РЕЖИМ АУДИО") size 14 bold True color "#00d4ff"
                            if is_all_muted:
                                text _("● Без звука") size 11 bold True color "#ef4444" yalign 0.5
                            else:
                                text _("● Звук активен") size 11 bold True color "#39ff14" yalign 0.5

                        button:
                            xfill True
                            ysize 36
                            style "settings_mini_btn"
                            action [
                                Preference("main volume", 1.0),
                                Preference("music volume", 1.0),
                                Preference("sound volume", 1.0),
                                Preference("ambient volume", 1.0),
                                Preference("voice volume", 1.0),
                                Preference("menu_sfx volume", 1.0)
                            ]
                            tooltip _("Сбросить все 6 каналов микшера на 100% громкости")
                            hbox:
                                align (0.5, 0.5)
                                spacing 8
                                text "↺" style "settings_mini_btn_text" size 13 yalign 0.5
                                text _("Сбросить все каналы микшера на 100%") style "settings_mini_btn_text" size 12 yalign 0.5

                        hbox:
                            xfill True
                            yalign 0.5
                            text _("Статус звуковой подсистемы:") size 10 color "#64748b"
                            text _("OK • 6 каналов (Мастер, Музыка, SFX, UI, Эмбиент, Голос)") size 10 bold True color "#39ff14" xalign 1.0


