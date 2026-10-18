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
        sample = str(_("Привет. Это Доктор Неон и вы играете в Semitone Resonance - игру от DomDot."))

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
    key "K_e" action SetScreenVariable("active_tab", get_next_settings_tab(active_tab))
    key "e" action SetScreenVariable("active_tab", get_next_settings_tab(active_tab))
    key "E" action SetScreenVariable("active_tab", get_next_settings_tab(active_tab))
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

                text _("[[ ESC ]] — Выйти") substitute False size 12 color "#64748b" yalign 0.5

                textbutton _("← Назад"):
                    action Return()
                    style "modern_back_button"
                    ysize 40
                    xsize 170
                    text_size 16
                    xalign 1.0



################################################################################
## Модульные экраны вкладок настроек (вынесены в settings/):
## - settings/tab_display.rpy   (screen settings_tab_display)
## - settings/tab_sound.rpy     (screen settings_tab_sound)
## - settings/tab_content.rpy   (screen settings_tab_content)
## - settings/tab_language.rpy  (screen settings_tab_language)
## - settings/tab_data.rpy      (screen settings_tab_data)
################################################################################

################################################################################
## Обратная совместимость для старых вызовов саб-меню
################################################################################

screen graphics_settings_screen():
    use settings_menu(current_tab="display")

screen sound_settings_screen():
    use settings_menu(current_tab="sound")

screen language_selection_screen():
    use settings_menu(current_tab="language")
