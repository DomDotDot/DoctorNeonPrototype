init python:
    # Класс для движения фона за мышкой
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
                # Вычисляем смещение от центра (-1.0 до 1.0)
                mw, mh = renpy.config.screen_width, renpy.config.screen_height
                self.xoffset = (float(x) / mw) - 0.5
                self.yoffset = (float(y) / mh) - 0.5
                renpy.redraw(self, 0)
            return None

    # Функция для трансформации, которую будем применять к фону
    def Parallax(d, speed=-20.0):
        # speed: насколько сильно двигается фон (отрицательное значение - движение против мыши)
        return Transform(d, function=parallax_func(speed))

    def parallax_func(speed):
        def _updater(d, st, at):
            # Получаем текущее смещение мыши (нужен экземпляр MouseParallax на экране)
            # Но для простоты используем упрощенный ATL вариант ниже, он стабильнее
            return 0
        return _updater

# --- ПРОСТОЙ ВАРИАНТ ПАРАЛЛАКСА ЧЕРЕЗ ATL (Рекомендую этот) ---
transform mouse_parallax(amount=20):
    # Центрируем изображение
    align (0.5, 0.5)
    # Делаем его чуть больше экрана, чтобы не было черных краев при движении
    xysize (int(config.screen_width * 1.05), int(config.screen_height * 1.05))
    # Магия движения
    function mouse_parallax_func(amount)

init python:
    def mouse_parallax_func(amount):
        def _func(trans, st, at):
            # Получаем координаты мыши
            x, y = renpy.get_mouse_pos()
            # Нормализуем от -0.5 до 0.5
            norm_x = (x / float(config.screen_width)) - 0.5
            norm_y = (y / float(config.screen_height)) - 0.5
            
            # Смещаем
            trans.xoffset = norm_x * amount * -1
            trans.yoffset = norm_y * amount * -1
            return 0
        return _func


image particles_dust:
    "gui/main_menu/particle.png" # Нужна маленькая белая точка/кружок с размытыми краями
    xalign 0.5 yalign 0.5
    block:
        # Случайное появление и движение
        choice:
            xoffset -600 yoffset 400 alpha 0.0
            ease 4.0 xoffset 600 yoffset -400 alpha 0.5
            ease 1.0 alpha 0.0
        choice:
            xoffset 600 yoffset 400 alpha 0.0
            ease 5.0 xoffset -600 yoffset -400 alpha 0.5
            ease 1.0 alpha 0.0
        repeat