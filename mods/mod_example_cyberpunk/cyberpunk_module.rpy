# ==============================================================================
# Cyberpunk Modular Mod - Script & Hooks Implementation
# ==============================================================================
# Демонстрационный модуль:
# 1. Хукается в game/modules/mods/ во время работы игры.
# 2. Регистрирует HUD-оверлей через Mod Overlay API.
# 3. Регистрирует и обрабатывает события через Mod Hook API.
# 4. Читает настройки из settings.json в реальном времени через get_mod_setting().
# ==============================================================================

init 50 python:
    # 1. Регистрация оверлея в Главном Меню
    register_mod_overlay(
        screen_name="cyberpunk_hud_overlay",
        mod_id="mod_example_cyberpunk",
        category="main_menu",
        order=10
    )

    # 2. Регистрация кастомного хука на событие импульса
    def _cyberpunk_pulse_event_logger(*args, **kwargs):
        callsign = kwargs.get("callsign", "UNKNOWN")
        print(f"[CyberpunkMod Hook] Сработал хук 'on_cyber_pulse'! Оператор: {callsign}")

    register_mod_hook("on_cyber_pulse", _cyberpunk_pulse_event_logger)

    # 3. Функция воспроизведения кибер-звука с учетом настроек
    def cyberpunk_play_sfx_test():
        # Чтение параметров из settings.json
        vol_pct = get_mod_setting("mod_example_cyberpunk", "sfx_volume_multiplier", 80)
        try:
            vol_multiplier = max(0.0, min(1.0, float(vol_pct) / 100.0))
        except:
            vol_multiplier = 0.8

        is_bass_boost = bool(get_mod_setting("mod_example_cyberpunk", "enable_bass_boost", True))
        is_glitch = bool(get_mod_setting("mod_example_cyberpunk", "enable_screen_glitch", False))
        callsign = str(get_mod_setting("mod_example_cyberpunk", "operator_callsign", "NEON-77"))

        # Выбор звукового файла в зависимости от настройки Bass Boost
        if is_bass_boost:
            sfx_file = "audio/sfx/sfx_zap-hard1.opus"
        else:
            sfx_file = "audio/sfx/sfx_zap.opus"

        # Воспроизведение звука с кастомной громкостью
        try:
            renpy.sound.play(sfx_file, channel="audio", relative_volume=vol_multiplier)
        except Exception as e:
            print(f"[CyberpunkMod] Ошибка воспроизведения звука: {e}")

        # Вызов зарегистрированных хуков
        trigger_mod_hooks("on_cyber_pulse", callsign=callsign, bass=is_bass_boost, glitch=is_glitch)

        # Визуальный глитч-эффект, если опция включена
        if is_glitch:
            renpy.show_screen("cyberpunk_glitch_flash")

        renpy.restart_interaction()


################################################################################
## Экран кратковременного глитч-эффекта
################################################################################

screen cyberpunk_glitch_flash():
    zorder 300
    timer 0.12 action Hide("cyberpunk_glitch_flash")

    # Вспышка и полоса искажения
    add Solid("#00f0ff22")
    frame:
        ypos 450
        xfill True
        ysize 4
        background Solid("#ffffff88")


################################################################################
## Экран кибер-виджета (Cyber-Terminal HUD Overlay)
################################################################################

screen cyberpunk_hud_overlay():
    zorder 48

    # Защита: виджет отображается только если коммьюнити контент включен и данный мод активен
    if getattr(persistent, "community_content_enabled", False) and is_mod_enabled("mod_example_cyberpunk"):

        # Динамическое чтение настроек из settings.json с защитой от структур словарей
        python:
            raw_callsign = get_mod_setting("mod_example_cyberpunk", "operator_callsign", "NEON-77")
            if isinstance(raw_callsign, dict):
                cur_callsign = str(raw_callsign.get("value", raw_callsign.get("label", "NEON-77")))
            else:
                cur_callsign = str(raw_callsign)

            raw_palette = get_mod_setting("mod_example_cyberpunk", "hud_color_palette", "cyan")
            if isinstance(raw_palette, dict):
                cur_palette = str(raw_palette.get("value", raw_palette.get("label", "cyan")))
            else:
                cur_palette = str(raw_palette)
                if cur_palette.startswith("{") and ("value" in cur_palette or "label" in cur_palette):
                    import ast
                    try:
                        parsed = ast.literal_eval(cur_palette)
                        if isinstance(parsed, dict):
                            cur_palette = str(parsed.get("value", "cyan"))
                    except:
                        cur_palette = "cyan"

            cur_bass = bool(get_mod_setting("mod_example_cyberpunk", "enable_bass_boost", True))
            cur_glitch = bool(get_mod_setting("mod_example_cyberpunk", "enable_screen_glitch", False))
            cur_vol = str(get_mod_setting("mod_example_cyberpunk", "sfx_volume_multiplier", 80))

            # Безопасные строки для текста в Ren'Py (экранирование тегов)
            safe_callsign = cur_callsign.replace("{", "{{").replace("}", "}}").replace("[", "[[").replace("]", "]]")
            safe_vol = cur_vol.replace("{", "{{").replace("}", "}}").replace("[", "[[").replace("]", "]]")

            # Выбор цветов палитры и безопасного имени
            p_lower = str(cur_palette).lower()
            if "magenta" in p_lower:
                accent_color = "#ff007f"
                border_color = "#99004d"
                bg_color = "#150510dd"
                palette_name = "MAGENTA"
            elif "matrix" in p_lower:
                accent_color = "#00ff66"
                border_color = "#008833"
                bg_color = "#05150add"
                palette_name = "MATRIX"
            elif "amber" in p_lower:
                accent_color = "#ffaa00"
                border_color = "#996600"
                bg_color = "#151005dd"
                palette_name = "AMBER"
            else: # "cyan" default
                accent_color = "#00f0ff"
                border_color = "#0088aa"
                bg_color = "#05121cdd"
                palette_name = "CYAN"

        frame:
            xalign 0.985
            ypos 20
            xsize 360
            padding (14, 12)
            background Solid(bg_color)

            vbox:
                spacing 6
                xfill True

                # Шапка виджета
                hbox:
                    spacing 8
                    yalign 0.5
                    text "⚡" size 16 color accent_color yalign 0.5
                    text _("CYBER-NET LINK: ONLINE") substitute False size 13 bold True color accent_color yalign 0.5
                    null width 5
                    text "●" size 11 color "#39ff14" yalign 0.5

                # Линия разделителя
                frame:
                    xfill True
                    ysize 1
                    background Solid(border_color)

                # Информация об операторе и теме
                hbox:
                    xfill True
                    text (_("ОПЕРАТОР: ") + safe_callsign) substitute False size 14 bold True color "#ffffff"
                    text palette_name substitute False size 12 color accent_color xalign 1.0 yalign 0.5

                # Статус настроек (бейджы Bass Boost и Glitch)
                hbox:
                    spacing 6
                    yalign 0.5

                    text ("VOL: " + safe_vol + "%") substitute False size 12 color "#aaaaaa" yalign 0.5

                    if cur_bass:
                        frame:
                            background Solid("#00aa4444")
                            padding (5, 2)
                            text "BASS+" substitute False size 11 bold True color "#39ff14"
                    else:
                        frame:
                            background Solid("#33333344")
                            padding (5, 2)
                            text "BASS" substitute False size 11 color "#666666"

                    if cur_glitch:
                        frame:
                            background Solid("#aa004444")
                            padding (5, 2)
                            text "GLITCH" substitute False size 11 bold True color "#ff5599"

                # Кнопка тестирования SFX и вызова хука
                textbutton _("🔊 ТЕСТ КИБЕР-ИМПУЛЬСА"):
                    action Function(cyberpunk_play_sfx_test)
                    text_size 13
                    text_bold True
                    text_color "#000000"
                    background Solid(accent_color)
                    hover_background Solid("#ffffff")
                    xfill True
                    padding (8, 6)
                    xalign 0.5
