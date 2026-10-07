################################################################################
## Система гипноза Серафины: CRT Шум-шейдер, Монохромность и Аудио-приглушение
## Doctor Neon Prototype - Seraphina Siren / Hypnosis Command FX System
################################################################################

init 5 python:
    # =========================================================================
    # GPU Шейдер гипноза Серафины (Dynamic Breathing Vignette & CRT Static)
    # Вместо плоской десатурации:
    # 1. Глубокая кинематографичная виньетка с мягким спадом и гипнотическим "дыханием"
    # 2. Драматичное изменение контраста: фокусный центр чистый, а периферия погружается в глубокую тень
    # 3. Высокочастотный аналоговый CRT-шум/зерно, усиливающийся в тенях виньетки
    # 4. Тонкие строчные микро-полосы CRT развёртки
    # =========================================================================
    renpy.register_shader("custom.seraphina_hypnosis",
        variables="""
            uniform sampler2D tex0;
            uniform float u_time;
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

            // 1. Аспектно-корректное радиальное расстояние от центра экрана (16:9)
            vec2 centered = (uv - vec2(0.5, 0.5)) * vec2(1.7778, 1.0);
            float dist = length(centered);

            // 2. Медленное гипнотическое "дыхание" виньетки
            float breath = sin(u_time * 1.6) * 0.035;
            float inner_r = u_vig_radius + breath;
            float outer_r = 1.18 + breath;

            // 3. Плавный S-образный спад виньетки: центр остаётся чистым, края глубоко темнеют
            float vig = smoothstep(inner_r, outer_r, dist);

            // 4. Кинематографичный контраст: глубокое затемнение периферии (crushed darks)
            float vig_darkness = pow(vig, 1.35) * u_vig_strength;

            // 5. Высокочастотный аналоговый шум CRT / зерно
            vec2 noise_seed = uv * vec2(960.0, 540.0) + fract(u_time * 31.4159);
            float grain = fract(sin(dot(noise_seed, vec2(12.9898, 78.233))) * 43758.5453);
            float noise = (grain - 0.5) * u_noise_strength;

            // 6. Тонкие строчные микро-линии CRT в зоне периферийного затенения
            float scanline = sin(uv.y * 540.0 * 3.14159) * u_scanline_strength * vig;

            // 7. Сэмплирование базового цвета Solid (глубокий тёмный тон)
            vec4 base = texture2D(tex0, uv);
            vec3 col = base.rgb + vec3(noise - scanline);

            // 8. Итоговая альфа-маска оверлея:
            // В центре: alpha близка к нулю (персонажи и сцена остаются чёткими и яркими)
            // По краям: альфа нарастает до ~85%, сгущая контрастную виньетку с живым CRT-зерном
            float alpha = clamp(vig_darkness + noise * (0.25 + vig * 0.75), 0.0, 0.95);

            gl_FragColor = vec4(col * alpha, alpha);
        """
    )


init -1 python:
    import re

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
                # Мягкий Lowpass (1250 Гц) — деликатное приглушение без глухоты
                renpy.music.set_audio_filter(ch, [renpy.audio.filter.Lowpass(1250)], replace=True)
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

    def seraphina_hypnosis_update_state(who, what):
        if renpy.predicting():
            return
        is_hyp = is_seraphina_hypnosis(who, what)
        if is_hyp:
            if not renpy.is_skipping():
                apply_hypnosis_audio()
        else:
            restore_hypnosis_audio()

    def seraphina_hypnosis_on_say_end():
        restore_hypnosis_audio()

    # Контроллер обновления времени шейдера (ATL Updater)
    class SeraphinaHypnosisUpdater(object):
        def __call__(self, trans, st, at):
            if getattr(persistent, "disable_gpu_animations", False):
                trans.u_time = 0.0
                return 0.2
            trans.u_time = st
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
    alpha 0.0
    easein 0.35 alpha 1.0

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
