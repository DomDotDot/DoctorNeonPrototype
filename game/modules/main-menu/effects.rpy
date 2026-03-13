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

    def parallax_func(speed):
        def _updater(d, st, at):
            return 0
        return _updater


transform mouse_parallax(amount=20):

    align (0.5, 0.5)
    xysize (int(config.screen_width * 1.05), int(config.screen_height * 1.05))
    function mouse_parallax_func(amount)

init python:
    def mouse_parallax_func(amount):
        def _func(trans, st, at):
            x, y = renpy.get_mouse_pos()

            norm_x = (x / float(config.screen_width)) - 0.5
            norm_y = (y / float(config.screen_height)) - 0.5
            
            trans.xoffset = norm_x * amount * -1
            trans.yoffset = norm_y * amount * -1
            return 0
        return _func


image particles_winter = SnowBlossom("gui/particle.png", count=120, border=50, xspeed=(20, 50), yspeed=(20, 50), start=10)

image particles_dust:
    "gui/main_menu/particle.png"
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