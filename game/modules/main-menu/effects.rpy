init python:
    class MouseParallax(renpy.Displayable):
        def __init__(self, layer_info):
            super(renpy.Displayable, self).__init__()
            self.xoffset, self.yoffset = 0.0, 0.0
            self.sort_layer = layer_info

        def render(self, width, height, st, at):
            return renpy.Render(width, height)

        def event(self, ev, x, y, st):
            import pygame
            if ev.type == pygame.MOUSEMOTION:

                mw, mh = renpy.config.screen_width, renpy.config.screen_height
                self.xoffset = (float(x) / mw) - 0.5
                self.yoffset = (float(y) / mh) - 0.5
                renpy.redraw(self, 0)
            return None

    def Parallax(d, speed=-20.0):
        # speed: насколько сильно двигается фон (отрицательное значение - движение против мыши)
        return Transform(d, function=parallax_func(speed))

    class ParallaxUpdater(object):
        def __init__(self, speed):
            self.speed = speed
        def __call__(self, d, st, at):
            return 0

    def parallax_func(speed):
        return ParallaxUpdater(speed)


# --- GPU ШЕЙДЕР ПАРАЛЛАКСА ---
# Сдвигает UV-координаты текстуры аппаратно на видеокарте (вершинный шейдер)
# Без смещения матриц дисплейбла, без пересчетов лейаута, без статтеров.
init 5 python:
    renpy.register_shader("custom.parallax",
        variables="""
            uniform vec2 u_parallax;
            uniform float u_parallax_zoom;
            attribute vec2 a_tex_coord;
            varying vec2 v_tex_coord;
        """,
        vertex_300="""
            v_tex_coord = (a_tex_coord - vec2(0.5, 0.5)) * u_parallax_zoom + vec2(0.5, 0.5) + u_parallax;
        """
    )

init -1 python:
    import math
    import time

    class GPUParallaxUpdater(object):
        def __init__(self, amount=40, speed=0.0):
            self.amount = float(amount)
            self.speed = float(speed)
            self.current_x = None
            self.current_y = None
            self.last_time = None

        def __call__(self, trans, st, at):
            raw_x, raw_y = renpy.get_mouse_pos()
            sw = float(config.screen_width)
            sh = float(config.screen_height)

            mx = max(0.0, min(float(raw_x), sw))
            my = max(0.0, min(float(raw_y), sh))

            nx = (mx / sw) - 0.5
            ny = (my / sh) - 0.5

            target_x = nx * (self.amount / sw) * -1.0
            target_y = ny * (self.amount / sh) * -1.0

            if self.speed <= 0.0:
                # Мгновенный 1:1 трекинг на GPU
                trans.u_parallax = (target_x, target_y)
                return 0

            # Плавная инерция через аппаратный таймер высокого разрешения
            now = time.perf_counter()
            if self.last_time is None or self.current_x is None:
                self.current_x = target_x
                self.current_y = target_y
                dt = 0.016
            else:
                dt = max(0.001, min(now - self.last_time, 0.05))

            self.last_time = now
            factor = 1.0 - math.exp(-self.speed * 14.0 * dt)

            self.current_x += (target_x - self.current_x) * factor
            self.current_y += (target_y - self.current_y) * factor

            trans.u_parallax = (self.current_x, self.current_y)
            return 0

    def gpu_parallax_func(amount=40, speed=0.0):
        return GPUParallaxUpdater(amount, speed)


    class MouseParallaxUpdater(object):
        def __init__(self, amount=20, speed=0.0):
            self.amount = float(amount)
            self.speed = float(speed)
            self.current_x = None
            self.current_y = None
            self.last_time = None

        def __call__(self, trans, st, at):
            raw_x, raw_y = renpy.get_mouse_pos()
            sw = float(config.screen_width)
            sh = float(config.screen_height)

            mx = max(0.0, min(float(raw_x), sw))
            my = max(0.0, min(float(raw_y), sh))

            norm_x = (mx / sw) - 0.5
            norm_y = (my / sh) - 0.5

            target_x = norm_x * self.amount * -1.0
            target_y = norm_y * self.amount * -1.0

            if self.speed <= 0.0:
                # Мгновенный 1:1 отклик без задержек и смазывания
                trans.xoffset = target_x
                trans.yoffset = target_y
                return 0

            # Плавное сглаживание через таймер time.perf_counter (не зависит от Ren'Py st)
            now = time.perf_counter()
            if self.last_time is None or self.current_x is None:
                self.current_x = target_x
                self.current_y = target_y
                dt = 0.016
            else:
                dt = max(0.001, min(now - self.last_time, 0.05))

            self.last_time = now
            factor = 1.0 - math.exp(-self.speed * 14.0 * dt)

            self.current_x += (target_x - self.current_x) * factor
            self.current_y += (target_y - self.current_y) * factor

            trans.xoffset = self.current_x
            trans.yoffset = self.current_y
            return 0

    def mouse_parallax_func(amount=20, speed=0.0):
        return MouseParallaxUpdater(amount, speed)


# Чистый GPU-шейдер параллакса
transform gpu_parallax(amount=40, speed=0.0):
    shader "custom.parallax"
    u_parallax_zoom (1.0 - min(0.2, max(0.05, abs(amount) * 0.0015)))
    u_parallax (0.0, 0.0)
    function gpu_parallax_func(amount, speed)

# Классический трансформ со сглаживанием / без статтеров
transform mouse_parallax(amount=20, speed=0.0):
    align (0.5, 0.5)
    subpixel True
    zoom (1.0 + max(0.06, abs(amount) * 0.0012))
    function mouse_parallax_func(amount, speed)


image particles_winter = SnowBlossom("gui/particle.png", count=120, border=50, xspeed=(20, 50), yspeed=(20, 50), start=10)

image particles_dust:
    "gui/particle.png"
    xalign 0.5 yalign 0.5
    block:

        choice:
            xoffset -600 yoffset 400 alpha 0.0
            ease 4.0 xoffset 600 yoffset -400 alpha 0.5
            ease 1.0 alpha 0.0
        choice:
            xoffset 600 yoffset 400 alpha 0.0
            ease 5.0 xoffset -600 yoffset -400 alpha 0.5
            ease 1.0 alpha 0.0
        repeat