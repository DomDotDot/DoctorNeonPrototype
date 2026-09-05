# ---------------------------------------------------------
# Эффекты имён персонажей (отображение в say screen)
# ---------------------------------------------------------
# Неон   → "лавовая лампа" (два синих переливаются)
# Нари   → "фиолетовая дымка" (два фиолетовых переливаются)
# Селестия → раздельные цвета (белый + чёрный с контуром)
# ---------------------------------------------------------

init python:
    import math
    import time as _time

    # =========================================================
    # Регистрация GPU-шейдеров для имен персонажей
    # =========================================================
    renpy.register_shader("custom.lavalamp_name",
        variables="""
            uniform float u_time;
            uniform float u_speed;
            uniform vec4 u_c1;
            uniform vec4 u_c2;
            varying vec2 v_tex_coord;
            attribute vec2 a_tex_coord;
        """,
        vertex_300="""
            v_tex_coord = a_tex_coord;
        """,
        fragment_300="""
            float phase = u_time * u_speed;
            float wave1 = sin(v_tex_coord.x * 3.14159 * 3.0 + phase * 1.2);
            float wave2 = sin(v_tex_coord.x * 3.14159 * 5.0 + phase * 0.7 + 0.5);
            float factor = clamp((wave1 + wave2 * 0.5) / 3.0 + 0.5, 0.0, 1.0);
            vec4 col = mix(u_c1, u_c2, factor);
            gl_FragColor = vec4(col.rgb * gl_FragColor.a, gl_FragColor.a);
        """
    )

    renpy.register_shader("custom.gradient_name",
        variables="""
            uniform vec4 u_c1;
            uniform vec4 u_c2;
            varying vec2 v_tex_coord;
            attribute vec2 a_tex_coord;
        """,
        vertex_300="""
            v_tex_coord = a_tex_coord;
        """,
        fragment_300="""
            vec4 col = mix(u_c1, u_c2, clamp(v_tex_coord.x, 0.0, 1.0));
            gl_FragColor = vec4(col.rgb * gl_FragColor.a, gl_FragColor.a);
        """
    )

    # =========================================================
    # Лавовая лампа / Дымка — аппаратный GPU-шейдер
    # =========================================================
    class LavaLampName(renpy.Displayable):
        """
        Каждая буква имени плавно меняет цвет между color1 и color2.
        Выполняется на GPU через кастомный шейдер без нагрузки на CPU.
        """

        def __init__(self, name, color1, color2, speed=1.0, **kwargs):
            super(LavaLampName, self).__init__(**kwargs)
            self.name = name
            self.color1 = color1
            self.color2 = color2
            self.speed = speed

            c1 = renpy.color.Color(color1).rgba
            c2 = renpy.color.Color(color2).rgba
            text_d = Text(name, font=gui.name_text_font, size=gui.name_text_size, color="#ffffff")
            self.child = At(text_d, animated_lavalamp_tf(speed, c1, c2))

        def render(self, width, height, st, at):
            return renpy.render(self.child, width, height, st, at)

        def visit(self):
            return [self.child]

    # =========================================================
    # Градиент — плавный переход цвета слева направо (GPU)
    # =========================================================
    class GradientName(renpy.Displayable):
        """
        Имя плавно меняет цвет от color1 (слева) к color2 (справа) на GPU.
        """

        def __init__(self, name, color1, color2, **kwargs):
            super(GradientName, self).__init__(**kwargs)
            self.name = name
            self.color1 = color1
            self.color2 = color2

            c1 = renpy.color.Color(color1).rgba
            c2 = renpy.color.Color(color2).rgba
            text_d = Text(name, font=gui.name_text_font, size=gui.name_text_size, color="#ffffff")
            self.child = At(text_d, gradient_static_tf(c1, c2))

        def render(self, width, height, st, at):
            return renpy.render(self.child, width, height, st, at)

        def visit(self):
            return [self.child]

transform animated_lavalamp_tf(speed, c1, c2):
    mesh True
    shader "custom.lavalamp_name"
    u_speed speed
    u_c1 c1
    u_c2 c2
    pause 0
    repeat

transform gradient_static_tf(c1, c2):
    mesh True
    shader "custom.gradient_name"
    u_c1 c1
    u_c2 c2

init python:

    # =========================================================
    # Маппинг: active_speaker → эффект (с кешированием)
    # =========================================================
    _name_effect_cache = {}

    def get_name_effect(who_text):
        """
        Возвращает кастомный Displayable для имени персонажа,
        или None если эффект не нужен (обычный текст).
        Кеширует экземпляр, чтобы при обновлении экрана ({w}, и т.д.)
        возвращался тот же объект без мерцаний.
        """
        speaker = store.active_speaker
        cache_key = (speaker, who_text)

        cached = _name_effect_cache.get(cache_key)
        if cached is not None:
            return cached

        effect = None

        if speaker == "neon":
            # Лавовая лампа: два синих
            effect = LavaLampName(who_text, "#1f4bc4", "#5b8eef", speed=1.0)

        elif speaker == "nari":
            # Фиолетовая дымка: два фиолетовых
            effect = LavaLampName(who_text, "#863b97", "#c070e0", speed=0.8)

        elif speaker == "celeste":
            # Плавный градиент: белый → тёмный
            effect = GradientName(who_text, "#b4adad", "#6a6a83")

        # Очищаем старый кеш и сохраняем новый
        _name_effect_cache.clear()
        if effect is not None:
            _name_effect_cache[cache_key] = effect

        return effect

