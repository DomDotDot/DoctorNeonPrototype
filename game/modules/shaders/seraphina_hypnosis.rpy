################################################################################
## Система гипноза Серафины: CRT Шум-шейдер, Монохромность и Аудио-приглушение
## Doctor Neon Prototype - Seraphina Siren / Hypnosis Command FX System
################################################################################

init 5 python:
    # =========================================================================
    # GPU Шейдер гипноза Серафины (Start Glitch Distortion Transition + Breathing Vignette)
    # 1. Стартовый transition-дисторшен (первые ~0.28 сек):
    #    - Яркий первоначальный шоковый всплеск (initial flash)
    #    - Горизонтальные блоки срыва развёртки (Horizontal Slice Tears)
    #    - Хроматические полосы расслоения (Neon Cyan, Hot Magenta, Pure White, Dark)
    #    - Волновой аналоговый дисторшен (Analog Sync Wave)
    #    - Высокочастотный цифровой шум/снег внутри глитч-полос
    # 2. Мгновенная нормализация ровно через 0.28 сек: глитч резко спадает в 0
    # 3. Глубокая кинематографичная виньетка с мягким спадом и гипнотическим "дыханием"
    # 4. Высокочастотный аналоговый CRT-шум/зерно в тенях
    # 5. Тонкие строчные микро-полосы CRT развёртки
    # =========================================================================
    renpy.register_shader("custom.seraphina_hypnosis",
        variables="""
            uniform sampler2D tex0;
            uniform float u_time;
            uniform float u_glitch_progress;
            uniform float u_noise_strength;
            uniform float u_scanline_strength;
            uniform float u_vig_strength;
            uniform float u_vig_radius;
            attribute vec2 a_tex_coord;
            varying vec2 v_tex_coord;
        """,
        vertex_300="""
            v_tex_coord = a_tex_coord;
        """,
        fragment_300="""
            vec2 uv = v_tex_coord;

            // =================================================================
            // 1. СТАРТОВЫЙ GLITCH-ДИСТОРШЕН TRANSITION (~0.28 сек)
            // =================================================================
            float glitch_intensity = (1.0 - u_glitch_progress) * step(u_glitch_progress, 0.999);
            glitch_intensity = pow(glitch_intensity, 1.25);

            vec3 glitch_color = vec3(0.0);
            float glitch_alpha = 0.0;

            if (glitch_intensity > 0.001) {
                // Быстро меняющийся временной шаг для резких цифровых сдвигов
                float glitch_seed = floor(u_time * 24.0);

                // Горизонтальные блоки срыва развёртки (Slice Tears)
                float slice_y = floor(uv.y * 32.0);
                float slice_rand = fract(sin(slice_y * 127.1 + glitch_seed * 43.17) * 43758.5453);
                float is_slice = step(0.68, slice_rand);

                // Вторичные узкие полосы срыва (Micro tearing lines)
                float micro_y = floor(uv.y * 160.0);
                float micro_rand = fract(sin(micro_y * 311.7 + glitch_seed * 19.3) * 26143.123);
                float is_micro = step(0.82, micro_rand);

                // Волновое искажение (Analog Sync Wave)
                float is_wave = step(0.70, sin(uv.y * 12.0 + u_time * 40.0));

                // Хроматические цвета глитча (Cyberpunk Cyan, Hot Magenta, Pure White, Dark)
                vec3 col_cyan = vec3(0.0, 0.92, 1.0);
                vec3 col_magenta = vec3(1.0, 0.08, 0.65);
                vec3 col_white = vec3(0.95, 0.98, 1.0);
                vec3 col_dark = vec3(0.01, 0.02, 0.04);

                vec3 slice_col = mix(col_cyan, col_magenta, step(0.5, fract(slice_rand * 7.3)));
                if (slice_rand > 0.88) {
                    slice_col = col_white;
                } else if (slice_rand < 0.74) {
                    slice_col = col_dark;
                }

                // Сила проявления глитч-полос
                float slice_power = is_slice * 0.75 + is_micro * 0.60 + is_wave * 0.40;
                slice_power = clamp(slice_power, 0.0, 1.0);

                // Высокочастотный снег/шум внутри глитч-полос
                float static_noise = fract(sin(dot(uv * vec2(480.0, 960.0) + glitch_seed, vec2(12.9898, 78.233))) * 43758.5453);
                slice_col += vec3((static_noise - 0.5) * 0.35);

                glitch_color = slice_col;
                glitch_alpha = slice_power * glitch_intensity * 0.85;

                // Начальный шоковый импульс в первые 0.06 сек
                if (u_time < 0.06) {
                    float initial_flash = (1.0 - (u_time / 0.06)) * 0.35;
                    glitch_color = mix(glitch_color, col_white, initial_flash);
                    glitch_alpha = max(glitch_alpha, initial_flash);
                }
            }

            // =================================================================
            // 2. ДЫШАЩАЯ ВИНЬЕТКА И CRT-ШУМ (Стабильное состояние)
            // =================================================================
            vec2 centered = (uv - vec2(0.5, 0.5)) * vec2(1.7778, 1.0);
            float dist = length(centered);

            // Медленное гипнотическое "дыхание" виньетки
            float breath = sin(u_time * 1.6) * 0.035;
            float inner_r = u_vig_radius + breath;
            float outer_r = 1.18 + breath;
            float vig = smoothstep(inner_r, outer_r, dist);

            // Затемнение периферии
            float vig_darkness = pow(vig, 1.35) * u_vig_strength;

            // Аналоговый высокочастотный CRT-шум / зерно
            vec2 noise_seed = uv * vec2(960.0, 540.0) + fract(u_time * 31.4159);
            float grain = fract(sin(dot(noise_seed, vec2(12.9898, 78.233))) * 43758.5453);
            float noise = (grain - 0.5) * u_noise_strength;

            // Микро-строки развёртки CRT в зоне затенения
            float scanline = sin(uv.y * 540.0 * 3.14159) * u_scanline_strength * vig;

            // Базовый цвет тени виньетки (глубокий полуночный тон)
            vec3 vig_color = vec3(0.015, 0.018, 0.028) + vec3(noise - scanline);
            float vig_alpha = clamp(vig_darkness + noise * (0.25 + vig * 0.75), 0.0, 0.95);

            // =================================================================
            // 3. КОМПОЗИЦИЯ: СТАРТОВЫЙ ГЛИТЧ + ВИНЬЕТКА
            // =================================================================
            vec3 final_color = mix(vig_color, glitch_color, glitch_alpha / max(glitch_alpha + vig_alpha, 0.001));
            float final_alpha = clamp(vig_alpha + glitch_alpha, 0.0, 1.0);

            gl_FragColor = vec4(final_color * final_alpha, final_alpha);
        """
    )


init -1 python:
    import re
    import time as _time

    # =========================================================================
    # Детекция гипнотических команд Серафины
    # (реплики Серафины, оканчивающиеся на тильду '~', '~?', '~!', и т.п.)
    # =========================================================================
    def is_seraphina_speaker(who):
        if getattr(store, "active_speaker", None) == "seraphina":
            return True
        if who is None:
            return False
        if who is getattr(store, "seraphina", None):
            return True
        try:
            ser_char = getattr(store, "seraphina", None)
            if ser_char and getattr(ser_char, "name", None) == who:
                return True
        except:
            pass
        w = str(who).strip()
        return w in ("Серафина", "Seraphina", _("Серафина"))

    def is_seraphina_hypnosis(who, what):
        if not is_seraphina_speaker(who):
            return False
        if not what:
            return False
        # Удаляем служебные теги Ren'Py (например, {cps}, {b}, {color})
        clean = re.sub(r'\{[^}]*\}', '', str(what)).strip()
        if '~' not in clean:
            return False
        # Проверяем окончание на тильду (с возможной пунктуацией: ~, ~?, ~!, ~..., ~.)
        if re.search(r'~[\s?!.…"\'”’)]*$', clean):
            return True
        # Или тильда в конце предложения/клаузы внутри строки
        if re.search(r'~[?!.…"\'”’)]*(?:\s|$)', clean):
            return True
        return False

    # =========================================================================
    # Управление аудио-фильтрами (Приглушение звука при гипнозе)
    # =========================================================================
    _seraphina_audio_hypnosis_active = False
    _seraphina_saved_audio_filters = {}

    def apply_hypnosis_audio():
        global _seraphina_audio_hypnosis_active, _seraphina_saved_audio_filters
        if _seraphina_audio_hypnosis_active:
            return
        _seraphina_audio_hypnosis_active = True

        channels = ["music", "ambient", "ambient1"]
        for ch in channels:
            try:
                # Сохраняем исходный фильтр канала, если он был задан
                getter = getattr(renpy.music, "get_audio_filter", None)
                orig = getter(ch) if getter else None
                _seraphina_saved_audio_filters[ch] = orig
            except:
                _seraphina_saved_audio_filters[ch] = None

            try:
                # Мягкий Lowpass (850 Гц) — деликатное приглушение без глухоты
                renpy.music.set_audio_filter(ch, [renpy.audio.filter.Lowpass(850)], replace=True)
            except Exception:
                pass

    def restore_hypnosis_audio():
        global _seraphina_audio_hypnosis_active, _seraphina_saved_audio_filters
        if not _seraphina_audio_hypnosis_active:
            return
        _seraphina_audio_hypnosis_active = False

        for ch in ("music", "ambient", "ambient1"):
            orig = _seraphina_saved_audio_filters.get(ch, None)
            try:
                renpy.music.set_audio_filter(ch, orig, replace=True)
            except Exception:
                pass
        _seraphina_saved_audio_filters.clear()

    # =========================================================================
    # Комплексный контроллер состояния гипноза (Шейдер + Аудио)
    # =========================================================================
    _seraphina_hypnosis_active = False
    _hypnosis_start_time = 0.0

    def apply_hypnosis():
        global _seraphina_hypnosis_active, _hypnosis_start_time
        if _seraphina_hypnosis_active:
            return
        _seraphina_hypnosis_active = True
        # Фиксируем точное время старта реплики для глитч-перехода
        _hypnosis_start_time = _time.perf_counter()

        # Приглушение звука
        apply_hypnosis_audio()

    def restore_hypnosis():
        global _seraphina_hypnosis_active
        if not _seraphina_hypnosis_active:
            return
        _seraphina_hypnosis_active = False

        # Возврат звука в норму
        restore_hypnosis_audio()

    def seraphina_hypnosis_update_state(who, what):
        if renpy.predicting():
            return
        is_hyp = is_seraphina_hypnosis(who, what)
        if is_hyp:
            if not renpy.is_skipping():
                apply_hypnosis()
        else:
            restore_hypnosis()

    def seraphina_hypnosis_on_say_end():
        restore_hypnosis()

    # Контроллер обновления времени и прогресса глитча (ATL Updater)
    class SeraphinaHypnosisUpdater(object):
        def __call__(self, trans, st, at):
            if getattr(persistent, "disable_gpu_animations", False):
                trans.u_time = 0.0
                trans.u_glitch_progress = 1.0
                return 0.2

            # Точное физическое время с момента старта реплики
            now = _time.perf_counter()
            elapsed = max(0.0, now - _hypnosis_start_time)

            # Длительность стартового глитч-перехода: ровно 0.28 сек
            glitch_dur = 0.28
            progress = min(1.0, elapsed / glitch_dur)

            trans.u_time = elapsed
            trans.u_glitch_progress = progress
            return 0

    def seraphina_hypnosis_time_func():
        return SeraphinaHypnosisUpdater()


# =============================================================================
# ATL-трансформы экрана гипноза и мерцания текста
# =============================================================================

transform seraphina_hypnosis_screen_tf:
    mesh True
    shader "custom.seraphina_hypnosis"
    u_noise_strength 0.055
    u_scanline_strength 0.022
    u_vig_strength 0.85
    u_vig_radius 0.36
    function seraphina_hypnosis_time_func()

# Статический фолбэк (для устройств с отключенными GPU-анимациями)
transform seraphina_hypnosis_static_tf:
    alpha 0.0
    easein 0.35 alpha 0.45

# Тонкое, едва заметное гипнотическое мерцание текста диалога
transform seraphina_hypnosis_text_flicker:
    subpixel True
    block:
        easein 0.08 alpha 0.93
        easeout 0.06 alpha 1.0
        easein 0.11 alpha 0.96
        easeout 0.07 alpha 1.0
        easein 0.05 alpha 0.91
        easeout 0.08 alpha 1.0
        pause 0.06
        easein 0.09 alpha 0.94
        easeout 0.05 alpha 1.0
        pause 0.10
        repeat

transform default_dialogue_tf:
    alpha 1.0
