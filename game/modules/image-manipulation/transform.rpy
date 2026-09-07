# Эффект легкого покачивания
transform dizzy_sway:
    anchor (0.125, 0.125)
    subpixel True

    parallel:
        ease 3.0 xoffset 15
        ease 3.0 xoffset -15
        repeat
    parallel:
        ease 4.0 yoffset 10
        ease 4.0 yoffset -10
        repeat

# Эффект легкого покачивания (16:9 версия)
transform dizzy_sway169:
    xalign 0.5 yalign 0.5
    zoom 1.03125
    subpixel True

    parallel:
        ease 3.0 xoffset 15
        ease 3.0 xoffset -15
        repeat
    parallel:
        ease 4.0 yoffset 10
        ease 4.0 yoffset -10
        repeat


# Эффект покачивания (призрак)
transform dizzy_ghost_anim_light:
    anchor (0.125, 0.125)
    alpha 0.0
    
    # Блок движения (вправо-вниз, потом влево-вверх)
    block:
        parallel:
            ease 1.0 alpha 0.4 
            ease 1.0 alpha 0.0
        parallel:
            ease 2.0 xoffset 20 yoffset 10
        
        xoffset 0 yoffset 0
        
        parallel:
            ease 1.0 alpha 0.4
            ease 1.0 alpha 0.0
        parallel:
            ease 2.0 xoffset -20 yoffset -10
            
        xoffset 0 yoffset 0
        repeat

# Эффект покачивания (призрак) (16:9 версия)
transform dizzy_ghost_anim_light169:
    anchor (0,0)
    alpha 0.0
    
    block:
        parallel:
            ease 1.0 alpha 0.4 
            ease 1.0 alpha 0.0
        parallel:
            ease 2.0 xoffset 20 yoffset 10
        
        xoffset 0 yoffset 0
        
        parallel:
            ease 1.0 alpha 0.4
            ease 1.0 alpha 0.0
        parallel:
            ease 2.0 xoffset -20 yoffset -10
            
        xoffset 0 yoffset 0
        repeat

# 2. Эффект двоения в глазах
transform dizzy_ghost_anim:
    alpha 0.0 xoffset 0 yoffset 0 zoom 1.0
    
    parallel:
        ease 1.5 alpha 0.4 
        ease 1.5 alpha 0.0
        repeat
    parallel:
        ease 3.0 xoffset 40 yoffset 20 zoom 1.05
        xoffset 0 yoffset 0 zoom 1.0
        repeat


# Трансформация искажения (Жар)
transform heat_haze:
    # Медленное волнообразное движение
    parallel:
        easein_quint 2 blur 5
        easein_quint 2 blur 1
        repeat

# Эффект ходьбы (Зум в центр)
transform walking_zoom(time_duration):
    align (0.5, 0.5) 
    zoom 1.0

    easein time_duration zoom 1.4

# Эффект страшного мигания с блюром
transform blur_flicker:

    blur 15.0 
    align (0.5, 0.5)
    

    block:
        choice:
            # Вариант 1: Горит нормально
            alpha 1.0
            pause 0.1
        choice:
            # Вариант 2: Слегка тускнеет
            alpha 0.6
            pause 0.05
        choice:
            # Вариант 3: Полная темнота (лампа погасла)
            alpha 0.0
            pause 0.1
            alpha 1.0
        choice:
            # Вариант 4: Быстрый стробоскоп
            alpha 0.2
            pause 0.05
            alpha 1.0
            pause 0.05
        
        repeat

# Эффект глитча (треск изображения)
transform glitch_effect:
    block:
        # Случайная пауза перед каждым глитчем
        choice:
            pause 2.0
        choice:
            pause 3.5
        choice:
            pause 5.0
            
        # Сам эффект искажения (смещение + изменение масштаба и прозрачности)
        parallel:
            choice:
                alpha 0.5
                pause 0.04
                alpha 0.8
                pause 0.04
                alpha 1.0
            choice:
                # Без изменения прозрачности
                pause 0.08
        parallel:
            xzoom 1.03 yzoom 0.97
            pause 0.04
            xzoom 0.97 yzoom 1.03
            pause 0.04
            xzoom 1.0 yzoom 1.0
        parallel:
            xoffset 15 yoffset -10
            pause 0.04
            xoffset -15 yoffset 10
            pause 0.04
            xoffset 0 yoffset 0
            
        repeat

# Эффект Параллакса (от мыши):
# speed=0.0 — мгновенный 1:1 отклик без задержки и статтеров
# speed=1.0 — плавная кинематографичная инерция (доводка)
transform scene_parallax(amount=20, speed=0.0):
    align (0.5, 0.5)
    subpixel True
    zoom (1.0 + max(0.06, abs(amount) * 0.0012))
    function mouse_parallax_func(amount, speed)

# Чистый аппаратный GPU-шейдер параллакса (сдвигает UV в видеопамяти)
# Без смещения матриц дисплейбла, без пересчетов лейаута
transform gpu_parallax(amount=40, speed=0.0):
    shader "custom.parallax"
    u_parallax_zoom (1.0 - min(0.2, max(0.05, abs(amount) * 0.0015)))
    u_parallax (0.0, 0.0)
    function gpu_parallax_func(amount, speed)


# Комбинированный эффект: Покачивание (dizzy_sway) + Мигание (blur_flicker)
# Чтобы применить оба сразу, можно использовать в скрипте:
# show image "name" at dizzy_sway, blur_flicker
# Или использовать этот готовый пресет:
transform sway_and_flicker:
    # Копируем свойства blur_flicker
    blur 15.0 
    align (0.5, 0.5)
    
    # Копируем свойства dizzy_sway
    subpixel True
    
    parallel:
        ease 3.0 xoffset 15
        ease 3.0 xoffset -15
        repeat
    parallel:
        ease 4.0 yoffset 10
        ease 4.0 yoffset -10
        repeat
    parallel:
        block:
            choice:
                alpha 1.0
                pause 0.1
            choice:
                alpha 0.6
                pause 0.05
            choice:
                alpha 0.0
                pause 0.1
                alpha 1.0
            choice:
                alpha 0.2
                pause 0.05
                alpha 1.0
                pause 0.05
            repeat


# Эффект турбулентности / порывов воздуха
# Непрерывный эффект для сцен разгерметизации, открытого космоса, сильного ветра или бури.
# Мягкие сглаженные кривые (easein/easeout) создают ощущение массы воздуха и аэродинамики,
# без резкого дребезга и рывков.
transform turbulence:
    align (0.5, 0.5)
    subpixel True
    zoom 1.06

    # Горизонтальные порывы ветра (неравномерные накаты и спады)
    parallel:
        easein 0.7 xoffset 28
        easeout 0.5 xoffset 10
        easein 0.4 xoffset 36
        easeout 0.9 xoffset -8
        easein 0.6 xoffset -24
        easeout 0.7 xoffset 6
        ease 0.9 xoffset 0
        repeat

    # Вертикальные потоки и провалы воздуха (аэродинамическая нестабильность)
    parallel:
        easein 0.8 yoffset -18
        easeout 0.6 yoffset -6
        easein 0.5 yoffset -26
        easeout 1.0 yoffset 14
        ease 0.8 yoffset -4
        easeout 0.7 yoffset 0
        repeat

    # Легкий аэродинамический крен от ветра (roll / наклон)
    parallel:
        easein 0.9 rotate 1.2
        easeout 0.7 rotate -0.6
        easein 0.6 rotate 1.5
        easeout 1.1 rotate -1.0
        ease 0.9 rotate 0.0
        repeat

    # Пульсация воздушного давления (наплыв и откат зума)
    parallel:
        easein 1.1 zoom 1.08
        easeout 0.8 zoom 1.055
        easein 0.6 zoom 1.085
        easeout 1.2 zoom 1.06
        repeat

# Синоним для соблюдения единого стиля именования 16:9 (по аналогии с dizzy_sway169)
transform turbulence169:
    turbulence

# Одиночный порыв воздуха (плавный наплыв потока с последующим возвратом в исходное положение)
# Подходит для разового броска взрывной волны или внезапного воздушного удара
transform air_gust:
    align (0.5, 0.5)
    subpixel True
    zoom 1.06

    parallel:
        easein_cubic 0.45 xoffset 38
        easeout 0.35 xoffset 16
        easein 0.25 xoffset 26
        easeout_quad 0.95 xoffset 0

    parallel:
        easein_cubic 0.45 yoffset -20
        easeout 0.4 yoffset -6
        easeout_quad 0.85 yoffset 0

    parallel:
        easein_cubic 0.45 rotate 1.4 zoom 1.085
        easeout 0.4 rotate -0.5 zoom 1.065
        easeout_quad 0.85 rotate 0.0 zoom 1.06

# Циклические порывы воздуха (спокойствие -> нарастающий порыв ветра -> спад -> повтор)
transform air_gust_loop:
    align (0.5, 0.5)
    subpixel True
    zoom 1.06

    block:
        # Относительное затишье с легким дыханием воздуха
        parallel:
            ease 1.4 xoffset 6 yoffset -4 rotate 0.3 zoom 1.06
            ease 1.4 xoffset -4 yoffset 3 rotate -0.2 zoom 1.062

        # Налетает порыв воздуха
        parallel:
            easein 0.5 xoffset 34
            easeout 0.35 xoffset 14
            easein 0.3 xoffset 24
            easeout_quad 0.95 xoffset 0

        parallel:
            easein 0.5 yoffset -22
            easeout 0.4 yoffset -6
            easeout_quad 0.85 yoffset 0

        parallel:
            easein 0.5 rotate 1.4 zoom 1.085
            easeout 0.4 rotate -0.6 zoom 1.065
            easeout_quad 0.8 rotate 0.0 zoom 1.06

        # Небольшая пауза между порывами
        pause 0.6

        repeat

