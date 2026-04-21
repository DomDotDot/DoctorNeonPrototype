# ---------------------------------------------------------
# Эффекты имён персонажей (отображение в say screen)
# ---------------------------------------------------------
# Неон   → "лавовая лампа" (два синих переливаются)
# Нари   → "фиолетовая дымка" (два фиолетовых переливаются)
# Селестия → раздельные цвета (белый + чёрный с контуром)
# ---------------------------------------------------------

init python:
    import math

    # =========================================================
    # Лавовая лампа / Дымка — анимированный градиент по буквам
    # =========================================================
    class LavaLampName(renpy.Displayable):
        """
        Каждая буква имени плавно меняет цвет между color1 и color2.
        Фаза зависит от позиции буквы → волна цвета «течёт» по имени.
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
                phase = st * self.speed

                # Несколько синусоид для органичного «лавового» движения
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
    # Раздельные цвета — первая/вторая половина имени
    # =========================================================
    class SplitColorName(renpy.Displayable):
        """
        Имя делится на две части:
         - part1 отображается цветом color1
         - part2 отображается цветом color2 с обводкой outline_color
        """

        def __init__(self, name, split_at, color1, color2, outline_color, outline_width=2, **kwargs):
            super(SplitColorName, self).__init__(**kwargs)
            self.part1 = name[:split_at]
            self.part2 = name[split_at:]
            self.color1 = color1
            self.color2 = color2
            self.outline_color = outline_color
            self.outline_width = outline_width

        def render(self, width, height, st, at):
            text1 = Text(
                self.part1,
                color=self.color1,
                font=gui.name_text_font,
                size=gui.name_text_size
            )
            text2 = Text(
                self.part2,
                color=self.color2,
                font=gui.name_text_font,
                size=gui.name_text_size,
                outlines=[(self.outline_width, self.outline_color, 0, 0)]
            )

            r1 = renpy.render(text1, width, height, st, at)
            r2 = renpy.render(text2, width, height, st, at)

            w1, h1 = r1.get_size()
            w2, h2 = r2.get_size()
            max_h = max(h1, h2)

            result = renpy.Render(int(w1 + w2), int(max_h))
            result.blit(r1, (0, 0))
            result.blit(r2, (int(w1), 0))

            return result

        def visit(self):
            return []

    # =========================================================
    # Маппинг: active_speaker → эффект
    # =========================================================
    def get_name_effect(who_text):
        """
        Возвращает кастомный Displayable для имени персонажа,
        или None если эффект не нужен (обычный текст).
        """
        speaker = store.active_speaker

        if speaker == "neon":
            # Лавовая лампа: два синих
            return LavaLampName(who_text, "#1f4bc4", "#5b8eef", speed=1.0)

        elif speaker == "nari":
            # Фиолетовая дымка: два фиолетовых
            return LavaLampName(who_text, "#863b97", "#c070e0", speed=0.8)

        elif speaker == "celeste":
            # «Селе» белым, «стия» чёрным с белым контуром
            split = len(who_text) // 2
            return SplitColorName(who_text, split, "#ffffff", "#1a1a1a", "#ffffff")

        return None
