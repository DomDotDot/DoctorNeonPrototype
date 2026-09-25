################################################################################
## Динамические анимации фонов Главного Меню (Doctor Neon Prototype)
## - background-1: медленное изменение контраста + мерцание голубого свечения
## - background-2..5: оптический solar flare с параллаксом мыши
## - background-7: медленное мерцание пожара (контраст/яркость/теплота) + искры
################################################################################

init -1 python:
    import math
    import time

    # =========================================================================
    # Контроллер динамического Solar Flare
    # Реагирует на параллакс мыши:
    # 1. Смещается быстрее заднего фона (parallax_amount 50 против 30), создавая глубину
    # 2. При приближении взгляда/мыши к солнцу (вверху-слева) вспыхивает ярче
    # 3. Плавная физическая инерция и оптическое мерцание лучей
    # =========================================================================
    class SolarFlareUpdater(object):
        def __init__(self, sun_x=320, sun_y=120, base_alpha=0.40, max_alpha=0.85, parallax_amount=50.0):
            self.sun_x = float(sun_x)
            self.sun_y = float(sun_y)
            self.base_alpha = float(base_alpha)
            self.max_alpha = float(max_alpha)
            self.parallax_amount = float(parallax_amount)
            self.current_x = 0.0
            self.current_y = 0.0
            self.current_alpha = base_alpha
            self.current_zoom = 1.0
            self.last_time = None

        def __call__(self, trans, st, at):
            if getattr(persistent, "disable_gpu_animations", False):
                trans.alpha = 0.0
                return 0.1

            raw_x, raw_y = renpy.get_mouse_pos()
            sw = float(config.screen_width)
            sh = float(config.screen_height)

            mx = max(0.0, min(float(raw_x), sw))
            my = max(0.0, min(float(raw_y), sh))

            norm_x = (mx / sw) - 0.5
            norm_y = (my / sh) - 0.5

            # Динамический параллакс солнечного блика (быстрее задника 30px для ощущения объема)
            target_x = norm_x * self.parallax_amount * -1.0
            target_y = norm_y * self.parallax_amount * -1.0

            # Расстояние от курсора мыши до солнца
            sun_nx = self.sun_x / sw
            sun_ny = self.sun_y / sh
            dist = math.hypot((mx / sw) - sun_nx, (my / sh) - sun_ny)

            # Чем ближе курсор к солнцу (взгляд в сторону источника света), тем ярче блик
            proximity = max(0.0, min(1.0, 1.0 - (dist / 1.15)))
            proximity_factor = proximity * proximity

            target_alpha = self.base_alpha + (self.max_alpha - self.base_alpha) * proximity_factor
            target_zoom = 1.0 + 0.14 * proximity_factor

            # Плавная физическая инерция через таймер высокого разрешения
            now = time.perf_counter()
            if self.last_time is None:
                self.current_x = target_x
                self.current_y = target_y
                self.current_alpha = target_alpha
                self.current_zoom = target_zoom
                dt = 0.016
            else:
                dt = max(0.001, min(now - self.last_time, 0.05))
            self.last_time = now

            factor = 1.0 - math.exp(-9.0 * dt)
            self.current_x += (target_x - self.current_x) * factor
            self.current_y += (target_y - self.current_y) * factor
            self.current_alpha += (target_alpha - self.current_alpha) * factor
            self.current_zoom += (target_zoom - self.current_zoom) * factor

            # Живое оптическое дыхание лучей во времени
            shimmer = math.sin(st * 1.6) * 0.05 + math.cos(st * 2.8) * 0.025

            trans.xoffset = self.current_x
            trans.yoffset = self.current_y
            trans.alpha = max(0.0, min(1.0, self.current_alpha + shimmer))
            trans.zoom = self.current_zoom
            return 0

    def solar_flare_func(sun_x=320, sun_y=120, base_alpha=0.40, max_alpha=0.85, parallax_amount=50.0):
        return SolarFlareUpdater(sun_x, sun_y, base_alpha, max_alpha, parallax_amount)


################################################################################
## 1. SOLAR FLARE (Фоны 2 - 5, уровни 1 - 4)
################################################################################

# Дневной солнечный блик (фоны 2, 3, 4)
transform solar_flare_day_transform:
    anchor (0.22, 0.193)
    pos (320, 120)
    subpixel True
    blend "add"
    matrixcolor TintMatrix("#fff6de")
    function solar_flare_func(sun_x=320, sun_y=120, base_alpha=0.38, max_alpha=0.82, parallax_amount=50.0)

# Закатный золотисто-янтарный солнечный блик (фон 5, закат)
transform solar_flare_sunset_transform:
    anchor (0.22, 0.193)
    pos (320, 120)
    subpixel True
    blend "add"
    matrixcolor TintMatrix("#ffb266")
    function solar_flare_func(sun_x=320, sun_y=120, base_alpha=0.45, max_alpha=0.90, parallax_amount=50.0)

screen main_menu_solar_flare():
    if getattr(persistent, "main_menu_level", 0) == 4:
        add "gui/main_menu/solar_flare.png":
            at solar_flare_sunset_transform
    else:
        add "gui/main_menu/solar_flare.png":
            at solar_flare_day_transform


################################################################################
## 2. АНИМАЦИИ ДЛЯ BACKGROUND-1 (Мерцание голубого свечения и затемнение)
################################################################################

# Медленное дыхание контраста и затемнения для базового фона
transform bg1_contrast_anim:
    subpixel True
    matrixcolor ContrastMatrix(1.0) * BrightnessMatrix(0.0)
    block:
        ease 5.0 matrixcolor ContrastMatrix(1.18) * BrightnessMatrix(-0.04)
        ease 4.0 matrixcolor ContrastMatrix(1.02) * BrightnessMatrix(0.00)
        ease 5.5 matrixcolor ContrastMatrix(1.24) * BrightnessMatrix(-0.06)
        ease 4.5 matrixcolor ContrastMatrix(0.98) * BrightnessMatrix(0.01)
        repeat

# Мягкое мерцание и пульсация неоново-голубого свечения у корней и воды
transform bg1_blue_glow_pulse:
    subpixel True
    blend "add"
    block:
        ease 3.5 alpha 0.60
        ease 2.2 alpha 0.90
        ease 1.5 alpha 0.45
        ease 0.35 alpha 0.75
        ease 0.45 alpha 0.50
        ease 3.0 alpha 0.85
        ease 3.5 alpha 0.35
        repeat

image bg_main_menu_1_animated:
    "gui/main_menu/background-1.jpeg"
    subpixel True
    matrixcolor ContrastMatrix(1.0) * BrightnessMatrix(0.0)
    block:
        ease 5.0 matrixcolor ContrastMatrix(1.18) * BrightnessMatrix(-0.04)
        ease 4.0 matrixcolor ContrastMatrix(1.02) * BrightnessMatrix(0.00)
        ease 5.5 matrixcolor ContrastMatrix(1.24) * BrightnessMatrix(-0.06)
        ease 4.5 matrixcolor ContrastMatrix(0.98) * BrightnessMatrix(0.01)
        repeat


################################################################################
## 3. АНИМАЦИИ ДЛЯ BACKGROUND-7 (Горящий замок, мерцание пожара)
################################################################################

# Медленное динамическое горение: изменение контраста, яркости и тепла пламени
image bg_main_menu_7_animated:
    "gui/main_menu/background-7.jpeg"
    subpixel True
    matrixcolor ContrastMatrix(1.0) * BrightnessMatrix(0.0) * TintMatrix("#ffffff")
    block:
        # Плавное нарастание жара пламени (медленно)
        ease 2.5 matrixcolor ContrastMatrix(1.18) * BrightnessMatrix(0.04) * TintMatrix("#fff4e8")
        # Микро-всплеск пламени (языки огня колышутся от порывов тяги)
        ease 0.25 matrixcolor ContrastMatrix(1.25) * BrightnessMatrix(0.07) * TintMatrix("#fff8ee")
        ease 0.35 matrixcolor ContrastMatrix(1.13) * BrightnessMatrix(0.02) * TintMatrix("#ffe8d4")
        # Медленное оседание жара в сторону тления
        ease 3.0 matrixcolor ContrastMatrix(0.96) * BrightnessMatrix(-0.03) * TintMatrix("#ffdcc0")
        # Второе дыхание огня
        ease 2.2 matrixcolor ContrastMatrix(1.14) * BrightnessMatrix(0.03) * TintMatrix("#ffeedc")
        ease 0.20 matrixcolor ContrastMatrix(1.22) * BrightnessMatrix(0.06) * TintMatrix("#fff4e4")
        ease 0.30 matrixcolor ContrastMatrix(1.08) * BrightnessMatrix(0.01) * TintMatrix("#ffe2c8")
        # Возврат в исходное с контрастными клубами дыма
        ease 2.8 matrixcolor ContrastMatrix(1.00) * BrightnessMatrix(0.00) * TintMatrix("#ffffff")
        repeat

# Тлеющие искры и пепел для горящего замка
image fire_embers_particles = SnowBlossom(
    Transform("gui/particle.png", zoom=0.22, matrixcolor=TintMatrix("#ffaa33")),
    count=45,
    border=60,
    xspeed=(-35, 45),
    yspeed=(-75, -210),
    start=5
)
