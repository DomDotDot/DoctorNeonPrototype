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
    # Лавовая лампа / Дымка — анимированный градиент по буквам
    # =========================================================
    class LavaLampName(renpy.Displayable):
        """
        Каждая буква имени плавно меняет цвет между color1 и color2.
        Фаза зависит от позиции буквы → волна цвета 'течёт' по имени.
        """

        def __init__(self, name, color1, color2, speed=1.0, **kwargs):
            super(LavaLampName, self).__init__(**kwargs)
            self.name = name
            self.color1 = color1
            self.color2 = color2
            self.speed = speed

        def render(self, width, height, st, at):
            chars = list(self.name)
            if not chars:
                return renpy.Render(1, 1)

            renders = []
            max_h = 0

            for i, ch in enumerate(chars):
                # Нормализованная позиция буквы [0..1]
                t = float(i) / max(1.0, len(chars) - 1.0)
                # Абсолютное время — анимация не сбрасывается при {w} и обновлении экрана
                phase = (_time.time() % 10000.0) * self.speed

                # Несколько синусоид для органичного 'лавового' движения
                wave1 = math.sin(t * math.pi * 3.0 + phase * 1.2)
                wave2 = math.sin(t * math.pi * 5.0 + phase * 0.7 + 0.5)
                factor = (wave1 + wave2 * 0.5) / 3.0 + 0.5
                factor = max(0.0, min(1.0, factor))

                c1 = renpy.color.Color(self.color1)
                c2 = renpy.color.Color(self.color2)
                blended = c1.interpolate(c2, factor)

                text_d = Text(
                    ch,
                    color=blended.hexcode,
                    font=gui.name_text_font,
                    size=gui.name_text_size
                )
                r = renpy.render(text_d, width, height, st, at)
                rw, rh = r.get_size()
                renders.append((r, rw, rh))
                if rh > max_h:
                    max_h = rh

            total_w = sum(rw for _, rw, _ in renders)
            result = renpy.Render(int(total_w), int(max_h))

            x = 0
            for r, rw, rh in renders:
                result.blit(r, (int(x), 0))
                x += rw

            renpy.redraw(self, 0.04)  # ~25 fps
            return result

        def visit(self):
            return []

    # =========================================================
    # Градиент — плавный переход цвета слева направо
    # =========================================================
    class GradientName(renpy.Displayable):
        """
        Имя плавно меняет цвет от color1 (слева) к color2 (справа).
        Каждая буква получает интерполированный цвет по позиции.
        """

        def __init__(self, name, color1, color2, **kwargs):
            super(GradientName, self).__init__(**kwargs)
            self.name = name
            self.color1 = color1
            self.color2 = color2

        def render(self, width, height, st, at):
            chars = list(self.name)
            if not chars:
                return renpy.Render(1, 1)

            renders = []
            max_h = 0

            c1 = renpy.color.Color(self.color1)
            c2 = renpy.color.Color(self.color2)

            for i, ch in enumerate(chars):
                t = float(i) / max(1.0, len(chars) - 1.0)
                blended = c1.interpolate(c2, t)

                text_d = Text(
                    ch,
                    color=blended.hexcode,
                    font=gui.name_text_font,
                    size=gui.name_text_size
                )
                r = renpy.render(text_d, width, height, st, at)
                rw, rh = r.get_size()
                renders.append((r, rw, rh))
                if rh > max_h:
                    max_h = rh

            total_w = sum(rw for _, rw, _ in renders)
            result = renpy.Render(int(total_w), int(max_h))

            x = 0
            for r, rw, rh in renders:
                result.blit(r, (int(x), 0))
                x += rw

            return result

        def visit(self):
            return []

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

