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
                use icon_button("📦", _("DLC Контент"), action=Function(renpy.call_in_new_context, "dlc_manager_main", is_in_game=not main_menu), btn_style="modern_button", txt_color="#b87107")
            else:
                use icon_button("📦", _("DLC Контент (Только ПК)"), action=None, btn_style="modern_button", txt_color="#888")

            # Коммьюнити Контент (по умолчанию выключен)
            if not renpy.variant("web"):
                $ comm_status = _("") if persistent.community_content_enabled else _("")
                $ comm_color = "#39ff14" if persistent.community_content_enabled else "#888888"
                use icon_button("🧩", _("Коммьюнити Контент") + comm_status, action=ShowMenu("mod_manager_screen"), btn_style="modern_button", txt_color=comm_color)
            else:
                use icon_button("🧩", _("Коммьюнити Контент (Только ПК)"), action=None, btn_style="modern_button", txt_color="#888")

            use icon_button("💾", _("Управление данными"), action=ShowMenu("data_settings_screen"), btn_style="modern_button", txt_color="#a11919")

            null height 30
            textbutton _("Назад") action Return() style "modern_back_button"


################################################################################
## Логика режимов экрана и предпросмотра (Window / Borderless / Fullscreen)
################################################################################

init -1 python:
    import time
    preview_text_start_time = time.time()
    preview_text_last_cps = -1

    def restart_text_preview():
        import time
        store.preview_text_start_time = time.time()
        renpy.restart_interaction()

    def text_preview_dynamic(st, at):
        import time
        cps = int(getattr(preferences, "text_cps", 0))
        sample = str(_("«Доктор Неон: сканирование нейросети завершено. Все протоколы стабильны.»"))

        # Если скорость изменилась на слайдере — авто-перезапуск тайминга печати
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
        import os
        import sys

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
            # Сначала переключаем ренпай в режим окна если был эксклюзивный фуллскрин
            if getattr(_preferences, "fullscreen", False):
                renpy.run(Preference("display", "window"))
            if win_ptr and lib:
                try:
                    # SDL_WINDOW_FULLSCREEN_DESKTOP (0x00001001) в SDL2 - стандартный borderless fullscreen
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


################################################################################
## Экран настроек Текста и Графики (Cyber-Glassmorphism Redesign)
################################################################################

screen graphics_settings_screen():
    tag menu
    zorder 50
    modal True

    on "show" action Function(restart_text_preview)
    on "replace" action Function(restart_text_preview)

    if main_menu:
        use main_menu_background
    else:
        add Solid("#000000b3")

    key "game_menu" action ShowMenu("settings_menu")

    use global_tooltip_display

    $ cur_disp_mode = get_game_display_mode()
    $ cps_val = int(preferences.text_cps)
    $ cps_text = f"{cps_val} зн/с" if cps_val > 0 else _("Мгновенно")
    $ afm_val = int(preferences.afm_time) if getattr(preferences, "afm_time", 0) > 0 else 0
    $ afm_text = f"{afm_val} сек" if afm_val > 0 else _("Выкл")

    frame:
        style "modern_panel_wide"
        xsize 1180
        padding (35, 24)

        vbox:
            spacing 12
            xfill True

            # Заголовок
            label _("Текст и Графика / Display & Text") style "modern_title_label" bottom_margin 8

            # Информационная плашка
            frame:
                xfill True
                padding (18, 12)
                background Solid("#181824cc")

                hbox:
                    spacing 15
                    yalign 0.5
                    xfill True

                    text "🖥️" size 26 yalign 0.5
                    vbox:
                        yalign 0.5
                        text _("Настройки экрана и вывода текста:") size 18 bold True color "#ffffff"
                        text _("Регулировка режима окна, скорости вывода реплик, параметров пропуска и доступности.") size 14 color "#aaaaaa"

                    frame:
                        xalign 1.0
                        yalign 0.5
                        background None
                        if cur_disp_mode == "fullscreen":
                            frame:
                                background Solid("#0284c7")
                                padding (12, 6)
                                text _("🖥️ ПОЛНЫЙ ЭКРАН") size 13 bold True color "#ffffff"
                        elif cur_disp_mode == "borderless":
                            frame:
                                background Solid("#059669")
                                padding (12, 6)
                                text _("🔲 БЕЗ РАМОК") size 13 bold True color "#ffffff"
                        else:
                            frame:
                                background Solid("#1e293b")
                                padding (12, 6)
                                text _("🪟 ОКОННЫЙ РЕЖИМ") size 13 bold True color "#38bdf8"

            # Рабочая область: две колонки карточек (по 535px каждая)
            hbox:
                spacing 20
                xalign 0.5

                # ==============================================================
                # ЛЕВАЯ КОЛОНКА
                # ==============================================================
                vbox:
                    xsize 535
                    spacing 12

                    # Карточка 1: Режим отображения экрана (3 режима: Окно / Без рамок / Полный)
                    frame:
                        style "settings_card"
                        vbox:
                            spacing 10
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
                            spacing 10
                            xfill True

                            hbox:
                                xfill True
                                yalign 0.5
                                text _("СКОРОСТЬ ВЫВОДА ТЕКСТА") size 15 bold True color "#00d4ff"
                                text _("Динамика диалогов") size 12 color "#888888" yalign 0.5

                            # Регулятор скорости текста
                            vbox:
                                spacing 3
                                xfill True
                                hbox:
                                    xfill True
                                    yalign 0.5
                                    text _("Скорость печати:") size 14 color "#dddddd"
                                    hbox:
                                        xalign 1.0
                                        spacing 8
                                        text cps_text size 14 bold True color ("#39ff14" if cps_val == 0 else "#00d4ff")
                                        button:
                                            style "settings_mini_btn"
                                            action Preference("text speed", getattr(config, "default_text_cps", 0))
                                            tooltip _("Сбросить скорость текста к значению по умолчанию")
                                            text "↺" style "settings_mini_btn_text"

                                bar value Preference("text speed") style "settings_slider_bar"

                            # Регулятор задержки авточтения
                            vbox:
                                spacing 3
                                xfill True
                                hbox:
                                    xfill True
                                    yalign 0.5
                                    text _("Задержка авточтения:") size 14 color "#dddddd"
                                    hbox:
                                        xalign 1.0
                                        spacing 8
                                        text afm_text size 14 bold True color ("#888888" if afm_val == 0 else "#00d4ff")
                                        button:
                                            style "settings_mini_btn"
                                            action Preference("auto-forward time", getattr(config, "default_afm_time", 15))
                                            tooltip _("Сбросить задержку авточтения к значению по умолчанию")
                                            text "↺" style "settings_mini_btn_text"

                                bar value Preference("auto-forward time") style "settings_slider_bar"

                            # Живой интерактивный предпросмотр скорости текста
                            frame:
                                xfill True
                                background Solid("#0d0d16")
                                padding (12, 10)
                                vbox:
                                    spacing 6
                                    hbox:
                                        xfill True
                                        yalign 0.5
                                        text _("ПРЕДПРОСМОТР ВЫВОДА РЕПЛИК:") size 11 bold True color "#64748b" yalign 0.5
                                        hbox:
                                            xalign 1.0
                                            spacing 8
                                            if cps_val == 0:
                                                text _("МГНОВЕННО") size 11 bold True color "#39ff14" yalign 0.5
                                            else:
                                                text f"{cps_val} зн/с" size 11 bold True color "#00d4ff" yalign 0.5
                                            button:
                                                style "settings_mini_btn"
                                                action Function(restart_text_preview)
                                                tooltip _("Перезапустить анимацию вывода текста")
                                                text _("↻ Тест") style "settings_mini_btn_text"

                                    fixed:
                                        xfill True
                                        ysize 38
                                        add DynamicDisplayable(text_preview_dynamic)

                # ==============================================================
                # ПРАВАЯ КОЛОНКА
                # ==============================================================
                vbox:
                    xsize 535
                    spacing 12

                    # Карточка 3: Параметры пропуска
                    frame:
                        style "settings_card"
                        vbox:
                            spacing 8
                            xfill True

                            hbox:
                                xfill True
                                yalign 0.5
                                text _("ПАРАМЕТРЫ ПРОПУСКА") size 15 bold True color "#00d4ff"
                                text _("Быстрая перемотка") size 12 color "#888888" yalign 0.5

                            # 3 чипа пропуска
                            button:
                                xfill True
                                ysize 38
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
                                ysize 38
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
                                ysize 38
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

                    # Карточка 4: Доступность и игровой контент
                    frame:
                        style "settings_card"
                        vbox:
                            spacing 7
                            xfill True

                            hbox:
                                xfill True
                                yalign 0.5
                                text _("ДОСТУПНОСТЬ И КОНТЕНТ") size 15 bold True color "#00d4ff"
                                text _("Специальные опции") size 12 color "#888888" yalign 0.5

                            # Включение 18+ контента
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
                                        padding (8, 2)
                                        text (_("ВКЛЮЧЕН") if persistent.sensitive_mode else _("ВЫКЛ")) size 11 bold True color ("#ffffff" if persistent.sensitive_mode else "#888888")

                            # ИИ Чувствительность
                            button:
                                xfill True
                                ysize 38
                                style "settings_chip_btn"
                                action Function(toggle_ai_sensitive_with_check)
                                tooltip _("Выключение всех изображений с участием ИИ-генерации и контента, связанного с нейросетями.")
                                hbox:
                                    xfill True
                                    yalign 0.5
                                    text _("🤖 ИИ-чувствительность") size 13 color "#e2e8f0" yalign 0.5
                                    frame:
                                        xalign 1.0
                                        yalign 0.5
                                        background (Solid("#39ff14") if persistent.ai_sensitive_mode else Solid("#222230"))
                                        padding (8, 2)
                                        text (_("✓ ВКЛ") if persistent.ai_sensitive_mode else _("✕ ВЫКЛ")) size 11 bold True color ("#000000" if persistent.ai_sensitive_mode else "#888888")

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
                                        padding (8, 2)
                                        text (_("✓ ВКЛ") if is_large_font else _("✕ ВЫКЛ")) size 11 bold True color ("#000000" if is_large_font else "#888888")

                            # Не отображать достижения
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
                                        padding (8, 2)
                                        text (_("СКРЫТЫ") if is_hide_ach else _("ВИДНЫ")) size 11 bold True color ("#000000" if is_hide_ach else "#888888")

            null height 6

            # Нижняя панель действий со сквозной навигацией
            hbox:
                xalign 0.5
                spacing 16

                textbutton _("◀ Назад в меню"):
                    action ShowMenu("settings_menu")
                    style "modern_button"
                    xsize 210
                    ysize 48
                    text_size 16

                textbutton _("🔊 Настройки звука"):
                    action ShowMenu("sound_settings_screen")
                    style "modern_button"
                    xsize 230
                    ysize 48
                    text_size 16

                textbutton _("🌐 Выбор языка"):
                    action ShowMenu("language_selection_screen")
                    style "modern_button"
                    xsize 210
                    ysize 48
                    text_size 16

                if not renpy.variant("web"):
                    textbutton _("🧩 Моды / Коммьюнити"):
                        action ShowMenu("mod_manager_screen")
                        style "modern_button"
                        xsize 240
                        ysize 48
                        text_size 16


################################################################################
## Экран настроек Звука (Cyber-Glassmorphism Redesign)
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

    use global_tooltip_display

    $ is_all_muted = bool(_preferences.get_mute("music") and _preferences.get_mute("sfx"))
    $ mus_vol = int(preferences.volumes["music"] * 100) if config.has_music else 0
    $ sfx_vol = int(preferences.volumes["sfx"] * 100) if config.has_sound else 0
    $ amb_vol = int(preferences.volumes.get("ambient", 1.0) * 100)
    $ voi_vol = int(preferences.volumes["voice"] * 100) if config.has_voice else 0

    frame:
        style "modern_panel_wide"
        xsize 1180
        padding (35, 24)

        vbox:
            spacing 12
            xfill True

            # Заголовок
            label _("Звук / Audio Settings") style "modern_title_label" bottom_margin 8

            # Информационная плашка
            frame:
                xfill True
                padding (18, 12)
                background Solid("#181824cc")

                hbox:
                    spacing 15
                    yalign 0.5
                    xfill True

                    text "🔊" size 26 yalign 0.5
                    vbox:
                        yalign 0.5
                        text _("Аудиосистема и баланс громкости:") size 18 bold True color "#ffffff"
                        text _("Индивидуальная калибровка каналов музыки, спецэффектов, окружения и озвучки.") size 14 color "#aaaaaa"

                    frame:
                        xalign 1.0
                        yalign 0.5
                        background None
                        if is_all_muted:
                            frame:
                                background Solid("#dc2626")
                                padding (12, 6)
                                text _("🔇 ЗВУК ОТКЛЮЧЕН") size 13 bold True color "#ffffff"
                        else:
                            frame:
                                background Solid("#16a34a")
                                padding (12, 6)
                                text _("🔊 АУДИО АКТИВНО") size 13 bold True color "#ffffff"

            # Сетка микшера громкости: 2 колонки по 535px (4 канала)
            hbox:
                spacing 20
                xalign 0.5

                # ==============================================================
                # ЛЕВАЯ КОЛОНКА: Музыка и Звуковые эффекты
                # ==============================================================
                vbox:
                    xsize 535
                    spacing 12

                    # Канал 1: Музыка
                    if config.has_music:
                        frame:
                            style "settings_card"
                            vbox:
                                spacing 8
                                xfill True

                                hbox:
                                    xfill True
                                    yalign 0.5
                                    hbox:
                                        spacing 8
                                        yalign 0.5
                                        text "🎵" size 20 yalign 0.5
                                        vbox:
                                            text _("Музыка") size 16 bold True color "#ffffff"
                                            text _("Саундтрек и фоновые треки") size 12 color "#888888"

                                    hbox:
                                        xalign 1.0
                                        yalign 0.5
                                        spacing 8
                                        text f"{mus_vol}%" size 16 bold True color "#00d4ff" yalign 0.5

                                bar value Preference("music volume") style "settings_slider_bar"

                                hbox:
                                    xalign 1.0
                                    spacing 10
                                    button:
                                        style "settings_mini_btn"
                                        action Preference("music volume", 1.0)
                                        tooltip _("Вернуть громкость музыки на 100%")
                                        text _("↺ Сброс") style "settings_mini_btn_text"

                                    button:
                                        style "settings_mini_btn"
                                        action Play("music", sample_music)
                                        tooltip _("Воспроизвести образец музыки")
                                        text _("▶ Тест музыки") style "settings_mini_btn_text"

                    # Канал 2: SFX
                    if config.has_sound:
                        frame:
                            style "settings_card"
                            vbox:
                                spacing 8
                                xfill True

                                hbox:
                                    xfill True
                                    yalign 0.5
                                    hbox:
                                        spacing 8
                                        yalign 0.5
                                        text "💥" size 20 yalign 0.5
                                        vbox:
                                            text _("Звуковые эффекты") size 16 bold True color "#ffffff"
                                            text _("Интерфейс, шаги, удары, выстрелы") size 12 color "#888888"

                                    hbox:
                                        xalign 1.0
                                        yalign 0.5
                                        spacing 8
                                        text f"{sfx_vol}%" size 16 bold True color "#00d4ff" yalign 0.5

                                bar value Preference("sound volume") style "settings_slider_bar"

                                hbox:
                                    xalign 1.0
                                    spacing 10
                                    button:
                                        style "settings_mini_btn"
                                        action Preference("sound volume", 1.0)
                                        tooltip _("Вернуть громкость звуков на 100%")
                                        text _("↺ Сброс") style "settings_mini_btn_text"

                                    $ sfx_sample = getattr(config, "sample_sound", None) or "audio/sfx/sound_sample.opus"
                                    button:
                                        style "settings_mini_btn"
                                        action Play("sound", sfx_sample)
                                        tooltip _("Воспроизвести тестовый звуковой эффект")
                                        text _("▶ Тест звука") style "settings_mini_btn_text"

                # ==============================================================
                # ПРАВАЯ КОЛОНКА: Эмбиент и Голос
                # ==============================================================
                vbox:
                    xsize 535
                    spacing 12

                    # Канал 3: Фоновый эмбиент
                    frame:
                        style "settings_card"
                        vbox:
                            spacing 8
                            xfill True

                            hbox:
                                xfill True
                                yalign 0.5
                                hbox:
                                    spacing 8
                                    yalign 0.5
                                    text "🍃" size 20 yalign 0.5
                                    vbox:
                                        text _("Фоновый эмбиент") size 16 bold True color "#ffffff"
                                        text _("Атмосфера города, дождь, ветер, гул") size 12 color "#888888"

                                hbox:
                                    xalign 1.0
                                    yalign 0.5
                                    spacing 8
                                    text f"{amb_vol}%" size 16 bold True color "#00d4ff" yalign 0.5

                            bar value Preference("ambient volume") style "settings_slider_bar"

                            hbox:
                                xalign 1.0
                                spacing 10
                                button:
                                    style "settings_mini_btn"
                                    action Preference("ambient volume", 1.0)
                                    tooltip _("Вернуть громкость эмбиента на 100%")
                                    text _("↺ Сброс") style "settings_mini_btn_text"


                    # Канал 4: Голос
                    if config.has_voice:
                        frame:
                            style "settings_card"
                            vbox:
                                spacing 8
                                xfill True

                                hbox:
                                    xfill True
                                    yalign 0.5
                                    hbox:
                                        spacing 8
                                        yalign 0.5
                                        text "🎙️" size 20 yalign 0.5
                                        vbox:
                                            text _("Голос и озвучка") size 16 bold True color "#ffffff"
                                            text _("Реплики и озвучка персонажей") size 12 color "#888888"

                                    hbox:
                                        xalign 1.0
                                        yalign 0.5
                                        spacing 8
                                        text f"{voi_vol}%" size 16 bold True color "#00d4ff" yalign 0.5

                                bar value Preference("voice volume") style "settings_slider_bar"

                                hbox:
                                    xalign 1.0
                                    spacing 10
                                    button:
                                        style "settings_mini_btn"
                                        action Preference("voice volume", 1.0)
                                        tooltip _("Вернуть громкость голоса на 100%")
                                        text _("↺ Сброс") style "settings_mini_btn_text"

                                    if getattr(config, "sample_voice", None):
                                        button:
                                            style "settings_mini_btn"
                                            action Play("voice", config.sample_voice)
                                            tooltip _("Воспроизвести образец голоса")
                                            text _("▶ Тест голоса") style "settings_mini_btn_text"

            # Общее отключение звука (Master Mute Card)
            frame:
                style "settings_card"
                xfill True
                padding (18, 12)
                hbox:
                    xfill True
                    yalign 0.5

                    hbox:
                        spacing 12
                        yalign 0.5
                        text ("🔇" if is_all_muted else "🔊") size 24 yalign 0.5
                        vbox:
                            text _("Мастер-переключатель звука (Mute All)") size 15 bold True color "#ffffff"
                            text _("Мгновенно приглушает все каналы без сброса настроек громкости.") size 13 color "#888888"

                    button:
                        xalign 1.0
                        yalign 0.5
                        xsize 220
                        ysize 40
                        style "settings_chip_btn"
                        selected is_all_muted
                        action Preference("all mute", "toggle")
                        hbox:
                            align (0.5, 0.5)
                            spacing 8
                            if is_all_muted:
                                text "🔊" size 16 yalign 0.5
                                text _("ВКЛЮЧИТЬ ЗВУК") size 13 bold True color "#39ff14" yalign 0.5
                            else:
                                text "🔇" size 16 yalign 0.5
                                text _("БЕЗ ЗВУКА") size 13 bold True color "#ef4444" yalign 0.5

            null height 6

            # Нижняя панель действий со сквозной навигацией
            hbox:
                xalign 0.5
                spacing 16

                textbutton _("◀ Назад в меню"):
                    action ShowMenu("settings_menu")
                    style "modern_button"
                    xsize 210
                    ysize 48
                    text_size 16

                textbutton _("🖥️ Текст и Графика"):
                    action ShowMenu("graphics_settings_screen")
                    style "modern_button"
                    xsize 230
                    ysize 48
                    text_size 16

                textbutton _("🌐 Выбор языка"):
                    action ShowMenu("language_selection_screen")
                    style "modern_button"
                    xsize 210
                    ysize 48
                    text_size 16

                if not renpy.variant("web"):
                    textbutton _("🧩 Моды / Коммьюнити"):
                        action ShowMenu("mod_manager_screen")
                        style "modern_button"
                        xsize 240
                        ysize 48
                        text_size 16