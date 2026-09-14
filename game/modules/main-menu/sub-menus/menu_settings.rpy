################################################################################
## Unified Settings System (Doctor Neon Prototype)
## Сквозное переключение вкладок: Экран, Звук, Доступность, Язык, Данные + DLC/Моды
################################################################################

init -1 python:
    import time
    import os
    import sys

    SETTINGS_TABS = ["display", "sound", "content", "language", "data"]

    def get_prev_settings_tab(cur):
        if cur not in SETTINGS_TABS:
            return SETTINGS_TABS[0]
        idx = SETTINGS_TABS.index(cur)
        return SETTINGS_TABS[(idx - 1) % len(SETTINGS_TABS)]

    def get_next_settings_tab(cur):
        if cur not in SETTINGS_TABS:
            return SETTINGS_TABS[0]
        idx = SETTINGS_TABS.index(cur)
        return SETTINGS_TABS[(idx + 1) % len(SETTINGS_TABS)]

    preview_text_start_time = time.time()
    preview_text_last_cps = -1

    def restart_text_preview():
        store.preview_text_start_time = time.time()
        renpy.restart_interaction()

    def text_preview_dynamic(st, at):
        cps = int(getattr(preferences, "text_cps", 0))
        sample = str(_("«Доктор Неон: сканирование нейросети завершено. Все протоколы стабильны.»"))

        last_cps = getattr(store, "preview_text_last_cps", -1)
        if cps != last_cps:
            store.preview_text_last_cps = cps
            store.preview_text_start_time = time.time()

        if cps <= 0:
            return Text(sample, size=13, color="#cbd5e1"), None

        now = time.time()
        start = getattr(store, "preview_text_start_time", now)
        elapsed = now - start
        if elapsed < 0:
            elapsed = 0.0

        chars = int(elapsed * cps)
        if chars < len(sample):
            partial = sample[:chars] + " |"
            delay = min(0.04, 1.0 / max(1, cps))
            return Text(partial, size=13, color="#cbd5e1"), delay
        else:
            return Text(sample, size=13, color="#cbd5e1"), None

    def get_game_display_mode():
        saved = getattr(persistent, "custom_display_mode", None)
        if saved in ("window", "borderless", "fullscreen"):
            return saved
        if getattr(_preferences, "fullscreen", False):
            return "fullscreen"
        return "window"

    def set_game_display_mode(mode):
        lib = None
        win_ptr = None
        try:
            import ctypes
            win_ptr = renpy.get_sdl_window_pointer()
            lib_path = os.path.join(config.renpy_base, "lib", "py3-windows-x86_64", "librenpython.dll")
            if not os.path.exists(lib_path):
                lib_path = os.path.join(os.path.dirname(sys.executable), "librenpython.dll")
            if os.path.exists(lib_path):
                lib = ctypes.cdll.LoadLibrary(lib_path)
                lib.SDL_SetWindowBordered.argtypes = [ctypes.c_void_p, ctypes.c_int]
                lib.SDL_SetWindowFullscreen.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
                lib.SDL_SetWindowPosition.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
                lib.SDL_SetWindowSize.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
        except Exception:
            lib = None
            win_ptr = None

        if mode == "fullscreen":
            persistent.custom_display_mode = "fullscreen"
            if win_ptr and lib:
                try:
                    lib.SDL_SetWindowFullscreen(win_ptr, 0)
                    lib.SDL_SetWindowBordered(win_ptr, 1)
                except Exception:
                    pass
            renpy.run(Preference("display", "fullscreen"))
            renpy.save_persistent()

        elif mode == "borderless":
            persistent.custom_display_mode = "borderless"
            if getattr(_preferences, "fullscreen", False):
                renpy.run(Preference("display", "window"))
            if win_ptr and lib:
                try:
                    lib.SDL_SetWindowFullscreen(win_ptr, 0x00001001)
                except Exception:
                    try:
                        import ctypes
                        lib.SDL_SetWindowBordered(win_ptr, 0)
                        class SDL_Rect(ctypes.Structure):
                            _fields_ = [('x', ctypes.c_int), ('y', ctypes.c_int), ('w', ctypes.c_int), ('h', ctypes.c_int)]
                        rect = SDL_Rect()
                        lib.SDL_GetDisplayBounds(0, ctypes.byref(rect))
                        lib.SDL_SetWindowPosition(win_ptr, rect.x, rect.y)
                        lib.SDL_SetWindowSize(win_ptr, rect.w, rect.h)
                        renpy.set_physical_size((rect.w, rect.h))
                    except Exception:
                        pass
            renpy.save_persistent()

        else: # "window"
            persistent.custom_display_mode = "window"
            if win_ptr and lib:
                try:
                    lib.SDL_SetWindowFullscreen(win_ptr, 0)
                    lib.SDL_SetWindowBordered(win_ptr, 1)
                except Exception:
                    pass
            renpy.run(Preference("display", "window"))
            renpy.save_persistent()

        renpy.restart_interaction()

    def get_playing_track_info():
        track = renpy.music.get_playing(channel="music")
        if not track:
            return None, None

        clean = str(track)
        if clean.startswith("<"):
            idx = clean.find(">")
            if idx != -1:
                clean = clean[idx+1:]

        filename = os.path.basename(clean.replace("\\", "/"))
        return filename, clean

    def toggle_main_menu_music():
        cur = getattr(persistent, "main_menu_music_enabled", True)
        new_val = not cur
        persistent.main_menu_music_enabled = new_val
        renpy.save_persistent()

        if getattr(store, "main_menu", False):
            if not new_val:
                renpy.music.stop(channel="music", fadeout=0.8)
            else:
                if hasattr(store, "play_main_menu_music"):
                    store.play_main_menu_music()
        renpy.restart_interaction()

    def toggle_sensitive_mode_with_check():
        persistent.sensitive_mode = not getattr(persistent, "sensitive_mode", False)
        renpy.save_persistent()
        renpy.restart_interaction()

    def toggle_ai_sensitive_with_check():
        persistent.ai_sensitive_mode = not getattr(persistent, "ai_sensitive_mode", False)
        renpy.save_persistent()
        renpy.restart_interaction()

    def get_music_sample():
        return getattr(store, "sample_music", "audio/music/BGM/Commuting.opus")

    def get_sound_sample():
        if hasattr(store, "sample_sound"):
            return store.sample_sound
        try:
            return config.sample_sound
        except Exception:
            return "audio/sfx/sound_sample.opus"

    def get_voice_sample():
        if hasattr(store, "sample_voice"):
            return store.sample_voice
        try:
            return config.sample_voice
        except Exception:
            return "audio/voice/voice_sample.ogg"


################################################################################
## Главный экран настроек со сквозными вкладками и быстрым доступом
################################################################################

screen settings_menu(current_tab="display"):
    tag menu
    zorder 25
    modal True

    default active_tab = current_tab

    if main_menu:
        use main_menu_background
    else:
        add Solid("#000000b3")

    # Горячие клавиши навигации: Q / E переключение разделов (с поддержкой русской раскладки), ESC возврат
    key "K_q" action SetScreenVariable("active_tab", get_prev_settings_tab(active_tab))
    key "q" action SetScreenVariable("active_tab", get_prev_settings_tab(active_tab))
    key "Q" action SetScreenVariable("active_tab", get_prev_settings_tab(active_tab))
    key "й" action SetScreenVariable("active_tab", get_prev_settings_tab(active_tab))
    key "Й" action SetScreenVariable("active_tab", get_prev_settings_tab(active_tab))
    key "K_e" action SetScreenVariable("active_tab", get_next_settings_tab(active_tab))
    key "e" action SetScreenVariable("active_tab", get_next_settings_tab(active_tab))
    key "E" action SetScreenVariable("active_tab", get_next_settings_tab(active_tab))
    key "у" action SetScreenVariable("active_tab", get_next_settings_tab(active_tab))
    key "У" action SetScreenVariable("active_tab", get_next_settings_tab(active_tab))
    key "game_menu" action Return()

    use global_tooltip_display

    frame:
        style "modern_panel_wide"
        xsize 1220
        padding (30, 18)

        vbox:
            spacing 12
            xfill True

            # -----------------------------------------------------------------
            # Верхняя панель: Вкладки + Быстрый доступ к DLC и Модам
            # -----------------------------------------------------------------
            hbox:
                xfill True
                yalign 0.5

                # Блок навигации по основным вкладкам
                hbox:
                    yalign 0.5
                    spacing 6

                    textbutton "◀ Q":
                        style "settings_tab_nav_arrow"
                        action SetScreenVariable("active_tab", get_prev_settings_tab(active_tab))
                        tooltip _("Предыдущий раздел [[Клавиша Q]]")

                    button:
                        style "settings_tab_btn"
                        selected (active_tab == "display")
                        action SetScreenVariable("active_tab", "display")
                        text _("🖥️ Текст и Графика") style "settings_tab_text"

                    button:
                        style "settings_tab_btn"
                        selected (active_tab == "sound")
                        action SetScreenVariable("active_tab", "sound")
                        text _("🔊 Звук") style "settings_tab_text"

                    button:
                        style "settings_tab_btn"
                        selected (active_tab == "content")
                        action SetScreenVariable("active_tab", "content")
                        text _("♿ Доступность") style "settings_tab_text"

                    button:
                        style "settings_tab_btn"
                        selected (active_tab == "language")
                        action SetScreenVariable("active_tab", "language")
                        text _("🌐 Язык") style "settings_tab_text"

                    button:
                        style "settings_tab_btn"
                        selected (active_tab == "data")
                        action SetScreenVariable("active_tab", "data")
                        text _("💾 Данные") style "settings_tab_text"

                    textbutton "E ▶":
                        style "settings_tab_nav_arrow"
                        action SetScreenVariable("active_tab", get_next_settings_tab(active_tab))
                        tooltip _("Следующий раздел [[Клавиша E]]")

            # -----------------------------------------------------------------
            # Контентная область активного раздела
            # -----------------------------------------------------------------
            fixed:
                xfill True
                ysize 575

                if active_tab == "display":
                    use settings_tab_display
                elif active_tab == "sound":
                    use settings_tab_sound
                elif active_tab == "content":
                    use settings_tab_content
                elif active_tab == "language":
                    use settings_tab_language
                elif active_tab == "data":
                    use settings_tab_data

            # -----------------------------------------------------------------
            # Нижняя строка состояния и кнопка "Назад"
            # -----------------------------------------------------------------
            hbox:
                xfill True
                yalign 0.5

                text _("[[ Q / E ]] — Переключение разделов  •  [[ ESC ]] — Назад") substitute False size 12 color "#64748b" yalign 0.5

                textbutton _("← Назад"):
                    action Return()
                    style "modern_back_button"
                    ysize 40
                    xsize 170
                    text_size 16
                    xalign 1.0


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


################################################################################
## Раздел 3: Доступность, Моды и DLC (Accessibility & Extensibility)
################################################################################

screen settings_tab_content():
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

                text "♿" size 24 yalign 0.5
                vbox:
                    yalign 0.5
                    text _("Специальные возможности, Моды и Дополнения:") size 17 bold True color "#ffffff"
                    text _("Управление аппаратными шейдерами, загрузкой модификаций и DLC контентом.") size 13 color "#aaaaaa"

        # Две колонки по 535px
        hbox:
            spacing 20
            xalign 0.5

            # ==================================================================
            # ЛЕВАЯ КОЛОНКА: Доступность и Оптимизация (535px)
            # ==================================================================
            vbox:
                xsize 535
                spacing 10

                # Карточка 1: Производительность и отображение
                frame:
                    style "settings_card"
                    vbox:
                        spacing 8
                        xfill True

                        text _("ОПТИМИЗАЦИЯ И ИНТЕРФЕЙС") size 15 bold True color "#00d4ff"

                        # GPU-анимации
                        button:
                            xfill True
                            ysize 38
                            style "settings_chip_btn"
                            action ToggleField(persistent, "disable_gpu_animations")
                            tooltip _("Выключение тяжелых аппаратных GLSL-шейдеров, шторма лепестков и динамического параллакса.")
                            hbox:
                                xfill True
                                yalign 0.5
                                text _("⚡ GPU-анимации и шейдеры") size 13 color "#e2e8f0" yalign 0.5
                                $ is_no_gpu = bool(getattr(persistent, "disable_gpu_animations", False))
                                frame:
                                    xalign 1.0
                                    yalign 0.5
                                    background (Solid("#ef4444") if is_no_gpu else Solid("#16a34a"))
                                    padding (8, 3)
                                    text (_("✕ ВЫКЛ") if is_no_gpu else _("✓ ВКЛ")):
                                        size 11
                                        bold True
                                        color "#ffffff"

                        # Крупный шрифт
                        button:
                            xfill True
                            ysize 38
                            style "settings_chip_btn"
                            action ToggleField(persistent, "font_size_large")
                            tooltip _("Увеличивает базовый кегль шрифта диалогов для комфортного чтения.")
                            hbox:
                                xfill True
                                yalign 0.5
                                text _("🔍 Крупный шрифт интерфейса") size 13 color "#e2e8f0" yalign 0.5
                                $ is_large_font = bool(getattr(persistent, "font_size_large", False))
                                frame:
                                    xalign 1.0
                                    yalign 0.5
                                    background (Solid("#39ff14") if is_large_font else Solid("#222230"))
                                    padding (8, 3)
                                    text (_("✓ ВКЛ") if is_large_font else _("✕ ВЫКЛ")) size 11 bold True color ("#000000" if is_large_font else "#888888")

                        # Скрыть ачивки
                        button:
                            xfill True
                            ysize 38
                            style "settings_chip_btn"
                            action ToggleField(persistent, "hide_achievement_notifications")
                            tooltip _("Отключает всплывающие уведомления о получении достижений во время игры.")
                            hbox:
                                xfill True
                                yalign 0.5
                                text _("🏆 Скрыть всплывающие ачивки") size 13 color "#e2e8f0" yalign 0.5
                                $ is_hide_ach = bool(getattr(persistent, "hide_achievement_notifications", False))
                                frame:
                                    xalign 1.0
                                    yalign 0.5
                                    background (Solid("#f59e0b") if is_hide_ach else Solid("#222230"))
                                    padding (8, 3)
                                    text (_("СКРЫТЫ") if is_hide_ach else _("ВИДНЫ")) size 11 bold True color ("#000000" if is_hide_ach else "#888888")

                # Карточка 2: Чувствительный контент
                frame:
                    style "settings_card"
                    vbox:
                        spacing 8
                        xfill True

                        text _("ФИЛЬТРЫ КОНТЕНТА") size 15 bold True color "#00d4ff"

                        button:
                            xfill True
                            ysize 38
                            style "settings_chip_btn"
                            action Function(toggle_sensitive_mode_with_check)
                            tooltip _("Включает отображение откровенных и взрослых сцен новеллы.")
                            hbox:
                                xfill True
                                yalign 0.5
                                text _("🔞 Взрослый контент (18+)") size 13 color "#e2e8f0" yalign 0.5
                                frame:
                                    xalign 1.0
                                    yalign 0.5
                                    background (Solid("#f43f5e") if persistent.sensitive_mode else Solid("#222230"))
                                    padding (8, 3)
                                    text (_("ВКЛЮЧЕН") if persistent.sensitive_mode else _("ВЫКЛ")) size 11 bold True color ("#ffffff" if persistent.sensitive_mode else "#888888")

                        button:
                            xfill True
                            ysize 38
                            style "settings_chip_btn"
                            action Function(toggle_ai_sensitive_with_check)
                            tooltip _("Выключение всех изображений с участием ИИ-генерации.")
                            hbox:
                                xfill True
                                yalign 0.5
                                text _("🤖 ИИ-чувствительность") size 13 color "#e2e8f0" yalign 0.5
                                frame:
                                    xalign 1.0
                                    yalign 0.5
                                    background (Solid("#39ff14") if persistent.ai_sensitive_mode else Solid("#222230"))
                                    padding (8, 3)
                                    text (_("✓ ВКЛ") if persistent.ai_sensitive_mode else _("✕ ВЫКЛ")) size 11 bold True color ("#000000" if persistent.ai_sensitive_mode else "#888888")

            # ==================================================================
            # ПРАВАЯ КОЛОНКА: Моды и DLC (535px)
            # ==================================================================
            vbox:
                xsize 535
                spacing 10

                # Карточка 3: Моды и коммьюнити контент
                frame:
                    style "settings_card"
                    vbox:
                        spacing 8
                        xfill True

                        hbox:
                            xfill True
                            yalign 0.5
                            text _("МОДЫ И КОММЬЮНИТИ") size 15 bold True color "#00d4ff"
                            if persistent.community_content_enabled:
                                text _("● Моды активны") size 12 bold True color "#39ff14" yalign 0.5
                            else:
                                text _("○ Моды выключены") size 12 color "#888888" yalign 0.5

                        text _("Включение поддержки пользовательских модификаций, кастомных скриптов и переводов:") size 12 color "#94a3b8"

                        # Тумблер включения/выключения модов
                        button:
                            xfill True
                            ysize 38
                            style "settings_chip_btn"
                            action ToggleField(persistent, "community_content_enabled")
                            tooltip _("Включить или отключить поддержку модов. При включении в главном меню появится значок 🧩.")
                            hbox:
                                xfill True
                                yalign 0.5
                                hbox:
                                    spacing 6
                                    yalign 0.5
                                    text "🧩" size 15 yalign 0.5
                                    text _("Поддержка коммьюнити контента:"):
                                        style "settings_chip_text"
                                        size 12
                                        color ("#39ff14" if persistent.community_content_enabled else "#cbd5e1")
                                frame:
                                    xalign 1.0
                                    yalign 0.5
                                    background (Solid("#39ff14") if persistent.community_content_enabled else Solid("#222230"))
                                    padding (8, 3)
                                    text (_("✓ ВКЛ") if persistent.community_content_enabled else _("✕ ВЫКЛ")):
                                        size 11
                                        bold True
                                        color ("#000000" if persistent.community_content_enabled else "#888888")

                        # Кнопка прямого входа в менеджер модов
                        button:
                            xfill True
                            ysize 44
                            style "settings_chip_btn"
                            background Solid("#1e293b")
                            hover_background Solid("#334155")
                            action ShowMenu("mod_manager_screen")
                            tooltip _("Открыть полноценный менеджер модификаций для установки и настройки модов")
                            hbox:
                                align (0.5, 0.5)
                                spacing 8
                                text "🧩" size 16 yalign 0.5
                                text _("Открыть Менеджер Модов ▶"):
                                    style "settings_chip_text"
                                    size 13
                                    bold True
                                    color "#38bdf8"
                                    yalign 0.5

                # Карточка 4: Менеджер DLC
                frame:
                    style "settings_card"
                    vbox:
                        spacing 8
                        xfill True

                        hbox:
                            xfill True
                            yalign 0.5
                            text _("DLC И ДОПОЛНЕНИЯ") size 15 bold True color "#00d4ff"
                            text _("Официальный контент") size 12 color "#b87107" yalign 0.5

                        text _("Загрузка сюжетных дополнений, артбуков, саундтрека и дополнительных материалов:") size 12 color "#94a3b8"

                        if not renpy.variant("web"):
                            button:
                                xfill True
                                ysize 44
                                style "settings_chip_btn"
                                background Solid("#2a1f14")
                                hover_background Solid("#3d2c1c")
                                action Function(renpy.call_in_new_context, "dlc_manager_main", is_in_game=not main_menu)
                                tooltip _("Запустить официальный менеджер DLC для проверки и загрузки контента")
                                hbox:
                                    align (0.5, 0.5)
                                    spacing 8
                                    text "📦" size 16 yalign 0.5
                                    text _("Открыть Менеджер DLC ▶"):
                                        style "settings_chip_text"
                                        size 13
                                        bold True
                                        color "#fbbf24"
                                        yalign 0.5
                        else:
                            frame:
                                xfill True
                                ysize 40
                                background Solid("#1a1a24")
                                text _("📦 DLC доступны только в версии для ПК") align (0.5, 0.5) size 12 color "#888888"


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


################################################################################
## Обратная совместимость для старых вызовов саб-меню
################################################################################

screen graphics_settings_screen():
    use settings_menu(current_tab="display")

screen sound_settings_screen():
    use settings_menu(current_tab="sound")

screen language_selection_screen():
    use settings_menu(current_tab="language")
