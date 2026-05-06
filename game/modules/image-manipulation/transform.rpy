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

# Комбинированный эффект: Глитч + Параллакс (от мыши)
# Требует наличия функции mouse_parallax_func (из effects.rpy)
transform scene_parallax(amount=20):
    align (0.5, 0.5)
    xysize (int(config.screen_width * 1.05), int(config.screen_height * 1.05))
    function mouse_parallax_func(amount)


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
