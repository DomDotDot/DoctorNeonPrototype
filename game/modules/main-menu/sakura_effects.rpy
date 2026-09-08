################################################################################
## Динамическая анимация лепестков Сакуры (Sakura Wind & Wave System)
## По аналогии со схемой волны wave_wipe.png в chapter-title.rpy
## Doctor Neon Prototype - Main Menu Ambient FX
################################################################################

init -1:

    ## Регистрация графических ассетов сакуры
    image sakura_petal_1 = "gui/main_menu/sakura/petal_1.png"
    image sakura_petal_2 = "gui/main_menu/sakura/petal_2.png"
    image sakura_petal_3 = "gui/main_menu/sakura/petal_3.png"
    image sakura_petal_cluster = "gui/main_menu/sakura/petal_cluster.png"
    image sakura_petal_bokeh = "gui/main_menu/sakura/petal_bokeh.png"
    image sakura_wave_overlay = "gui/main_menu/sakura/sakura_wave_wipe.png"


################################################################################
## Трансформы волнового наката (Wave Wipe / Wind Surge)
## По аналогии с chapter_wave_wipe из chapter-title.rpy
################################################################################

# Спокойный волновой порыв весеннего бриза (для background-4, Level 3)
transform sakura_wave_pass_breeze(delay_start=1.2):
    subpixel True
    xpos -2200
    ypos -1000
    alpha 0.0
    rotate 4
    zoom 1.0
    pause delay_start
    block:
        alpha 0.0
        xpos -2200
        ypos -1000
        parallel:
            easein 1.5 alpha 0.65
            pause 1.6
            easeout 2.2 alpha 0.0
        parallel:
            easein_quad 5.3 xpos 1000 ypos 550
        pause 8.5
        repeat

# Мощный штормовой накат волны лепестков (Сакура Фубуки для background-5, Level 4)
# Волна 1: стремительный прорыв основного фронта
transform sakura_wave_storm_front(delay_start=0.4):
    subpixel True
    xpos -2400
    ypos -1150
    alpha 0.0
    rotate 7
    zoom 1.15
    pause delay_start
    block:
        alpha 0.0
        xpos -2400
        ypos -1150
        parallel:
            easein 0.6 alpha 0.90
            pause 1.4
            easeout 1.6 alpha 0.0
        parallel:
            easein_cubic 3.6 xpos 1250 ypos 680
        pause 3.8
        repeat

# Волна 2: вторичный завихряющийся эшелон (со сдвигом по фазе и углу)
transform sakura_wave_storm_eddy(delay_start=2.6):
    subpixel True
    xpos -2100
    ypos -900
    alpha 0.0
    rotate 2
    zoom 0.95
    pause delay_start
    block:
        alpha 0.0
        xpos -2100
        ypos -900
        parallel:
            easein 0.8 alpha 0.75
            pause 1.2
            easeout 1.5 alpha 0.0
        parallel:
            easein_quad 3.5 xpos 1350 ypos 750
        pause 4.2
        repeat


################################################################################
## Трансформы индивидуальных лепестков (3D Tumbling & Dynamic Flutter)
################################################################################

# Параметрический трансформ полета лепестка с 3D-кувырканием и синусоидальным сносом
transform sakura_fly(sx, sy, ex, ey, fall_time, delay_time, scale_val=1.0, sway_dist=30, spin_angle=360):
    subpixel True
    xpos sx
    ypos sy
    alpha 0.0
    zoom scale_val
    pause delay_time
    block:
        alpha 0.0
        xpos sx
        ypos sy
        parallel:
            easein 0.5 alpha 1.0
            pause max(0.1, fall_time - 1.2)
            easeout 0.7 alpha 0.0
        parallel:
            ease fall_time xpos ex
        parallel:
            ease fall_time ypos ey
        parallel:
            # 3D-кувыркание: переворачивание лепестка + гармоническое раскачивание на ветру + вращение
            ease (fall_time * 0.25) xzoom (scale_val * 0.1) xoffset sway_dist rotate (spin_angle * 0.25)
            ease (fall_time * 0.25) xzoom (-scale_val) xoffset 0 rotate (spin_angle * 0.50)
            ease (fall_time * 0.25) xzoom (-scale_val * 0.1) xoffset (-sway_dist) rotate (spin_angle * 0.75)
            ease (fall_time * 0.25) xzoom scale_val xoffset 0 rotate spin_angle
        pause (delay_time * 0.4 + 0.3)
        repeat

# Стремительный пролет крупного размытого лепестка перед объективом (Foreground Bokeh)
transform sakura_bokeh_rush(sx, sy, ex, ey, fly_time, delay_time, scale_val=1.8):
    subpixel True
    xpos sx
    ypos sy
    alpha 0.0
    zoom scale_val
    pause delay_time
    block:
        alpha 0.0
        xpos sx
        ypos sy
        parallel:
            easein 0.4 alpha 0.85
            pause max(0.1, fly_time - 0.8)
            easeout 0.4 alpha 0.0
        parallel:
            ease fly_time xpos ex
        parallel:
            ease fly_time ypos ey
        parallel:
            ease (fly_time * 0.5) xzoom (scale_val * 0.1) rotate 90
            ease (fly_time * 0.5) xzoom (-scale_val) rotate 180
        pause (delay_time + 4.0)
        repeat


################################################################################
## Экраны эффекта сакуры для главного меню
################################################################################

# ЭКРАН 1: Весенний бриз для background-4 (Level 3)
# Умеренная плотность, мягкие волны порывов, эстетичное парение
screen sakura_menu_breeze():
    zorder 5

    # --- Слой 1: Фоновая волна ветра (накат волны лепестков через сад) ---
    #add "sakura_wave_overlay":
        #at sakura_wave_pass_breeze(1.0)

    # --- Слой 2: Средний план (живые кувыркающиеся лепестки сада) ---
    # Потоки начинаются от кроны сакуры (x ~ 400..1200, y ~ -80..350)
    # и уходят по ветру через сад вправо-вниз (x ~ 1400..2100, y ~ 900..1250)
    add "sakura_petal_1" at sakura_fly(550, -40, 1680, 1100, 7.5, 0.2, scale_val=0.85, sway_dist=35, spin_angle=270)
    add "sakura_petal_2" at sakura_fly(780, 60, 1850, 1150, 6.8, 1.1, scale_val=0.90, sway_dist=40, spin_angle=-220)
    add "sakura_petal_3" at sakura_fly(420, 120, 1580, 1180, 8.2, 2.3, scale_val=0.75, sway_dist=28, spin_angle=310)
    add "sakura_petal_cluster" at sakura_fly(680, 20, 1920, 1120, 6.2, 3.5, scale_val=0.80, sway_dist=45, spin_angle=190)

    add "sakura_petal_1" at sakura_fly(900, 100, 1980, 1200, 7.0, 4.2, scale_val=0.78, sway_dist=32, spin_angle=-180)
    add "sakura_petal_2" at sakura_fly(620, 180, 1720, 1160, 7.8, 5.0, scale_val=0.92, sway_dist=38, spin_angle=290)
    add "sakura_petal_3" at sakura_fly(480, 220, 1640, 1220, 8.5, 6.1, scale_val=0.70, sway_dist=25, spin_angle=-240)
    add "sakura_petal_cluster" at sakura_fly(820, 40, 2040, 1140, 6.5, 7.2, scale_val=0.85, sway_dist=42, spin_angle=210)

    # Дальний план (мелкие фоновые лепестки)
    add "sakura_petal_1" at sakura_fly(500, 280, 1420, 1150, 9.5, 0.8, scale_val=0.48, sway_dist=20, spin_angle=160)
    add "sakura_petal_2" at sakura_fly(720, 320, 1550, 1190, 9.0, 3.2, scale_val=0.52, sway_dist=22, spin_angle=-190)
    add "sakura_petal_3" at sakura_fly(860, 250, 1620, 1210, 10.0, 5.8, scale_val=0.45, sway_dist=18, spin_angle=230)

    # --- Слой 3: Передний план (крупные размытые боке-лепестки перед камерой) ---
    add "sakura_petal_bokeh" at sakura_bokeh_rush(180, -120, 2080, 1180, 3.8, 2.5, scale_val=1.9)
    add "sakura_petal_bokeh" at sakura_bokeh_rush(620, -160, 2150, 1050, 3.4, 7.8, scale_val=2.2)


# ЭКРАН 2: Буря сакуры (Сакура Фубуки) для background-5 (Level 4)
# Высокая динамика, частые порывистые волны, плотный летящий шторм
screen sakura_menu_storm():
    zorder 5

    # --- Слой 1: Двойной волновой фронт (накатывающие порывы шторма) ---
    #add "sakura_wave_overlay":
        #at sakura_wave_storm_front(0.3)

    #add "sakura_wave_overlay":
        #at sakura_wave_storm_eddy(2.5)

    # --- Слой 2: Плотный поток лепестков средней дистанции (штормовые скорости) ---
    add "sakura_petal_1" at sakura_fly(420, -60, 1950, 1080, 4.2, 0.1, scale_val=0.95, sway_dist=50, spin_angle=420)
    add "sakura_petal_2" at sakura_fly(680, 40, 2100, 1120, 3.8, 0.6, scale_val=1.05, sway_dist=55, spin_angle=-380)
    add "sakura_petal_3" at sakura_fly(350, 100, 1880, 1160, 4.5, 1.0, scale_val=0.88, sway_dist=42, spin_angle=460)
    add "sakura_petal_cluster" at sakura_fly(580, -20, 2050, 1100, 3.5, 1.5, scale_val=1.00, sway_dist=60, spin_angle=340)

    add "sakura_petal_1" at sakura_fly(820, 80, 2180, 1150, 4.0, 1.9, scale_val=0.90, sway_dist=48, spin_angle=-400)
    add "sakura_petal_2" at sakura_fly(510, 160, 1980, 1200, 4.3, 2.4, scale_val=1.10, sway_dist=52, spin_angle=390)
    add "sakura_petal_3" at sakura_fly(400, 200, 1850, 1240, 4.7, 2.8, scale_val=0.82, sway_dist=40, spin_angle=-430)
    add "sakura_petal_cluster" at sakura_fly(750, 20, 2220, 1130, 3.6, 3.3, scale_val=0.95, sway_dist=58, spin_angle=360)

    add "sakura_petal_1" at sakura_fly(600, 110, 2060, 1170, 3.9, 3.7, scale_val=0.98, sway_dist=46, spin_angle=410)
    add "sakura_petal_2" at sakura_fly(480, 70, 1940, 1110, 4.1, 4.1, scale_val=0.92, sway_dist=50, spin_angle=-390)
    add "sakura_petal_3" at sakura_fly(700, 190, 2140, 1220, 4.4, 4.6, scale_val=0.85, sway_dist=44, spin_angle=450)
    add "sakura_petal_cluster" at sakura_fly(390, 130, 1910, 1180, 3.7, 5.0, scale_val=1.02, sway_dist=56, spin_angle=350)

    # Фоновые слои ветра
    add "sakura_petal_1" at sakura_fly(550, 260, 1680, 1160, 5.8, 0.4, scale_val=0.55, sway_dist=30, spin_angle=280)
    add "sakura_petal_2" at sakura_fly(780, 300, 1820, 1200, 5.5, 1.8, scale_val=0.58, sway_dist=32, spin_angle=-260)
    add "sakura_petal_3" at sakura_fly(460, 340, 1600, 1250, 6.2, 3.2, scale_val=0.50, sway_dist=28, spin_angle=310)
    add "sakura_petal_1" at sakura_fly(850, 220, 1890, 1190, 5.4, 4.5, scale_val=0.52, sway_dist=34, spin_angle=-290)

    # --- Слой 3: Передний план (частые штормовые пролеты боке-лепестков) ---
    add "sakura_petal_bokeh" at sakura_bokeh_rush(100, -150, 2180, 1150, 2.4, 0.8, scale_val=2.3)
    add "sakura_petal_bokeh" at sakura_bokeh_rush(550, -180, 2260, 1080, 2.2, 2.8, scale_val=2.5)
    add "sakura_petal_bokeh" at sakura_bokeh_rush(320, -140, 2120, 1190, 2.5, 4.8, scale_val=2.1)
