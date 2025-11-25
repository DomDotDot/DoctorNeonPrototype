# 1. Эффект для основной картинки (легкое покачивание)
transform dizzy_sway:
    anchor (0.125, 0.125)
    subpixel True # Для плавности движения
    parallel:
        ease 3.0 xoffset 15
        ease 3.0 xoffset -15
        repeat
    parallel:
        ease 4.0 yoffset 10
        ease 4.0 yoffset -10
        repeat


transform dizzy_ghost_anim_light:
    anchor (0.125, 0.125)
    alpha 0.0             # Начинаем с невидимого
    
    # Блок движения (вправо-вниз, потом влево-вверх)
    block:
        parallel:
            # Появляется и исчезает
            ease 1.0 alpha 0.4 
            ease 1.0 alpha 0.0
        parallel:
            # Плывет вправо-вниз
            ease 2.0 xoffset 20 yoffset 10
        
        # Мгновенный возврат в центр (пока он прозрачный)
        xoffset 0 yoffset 0
        
        parallel:
            # Снова появляется
            ease 1.0 alpha 0.4
            ease 1.0 alpha 0.0
        parallel:
            # Плывет в ДРУГУЮ сторону (влево-вверх)
            ease 2.0 xoffset -20 yoffset -10
            
        xoffset 0 yoffset 0
        repeat

# 2. Эффект для "призрака" (двоение в глазах)
transform dizzy_ghost_anim:
    # Начальная точка (невидимый, в центре)
    alpha 0.0 xoffset 0 yoffset 0 zoom 1.0
    
    # Блок параллельной анимации
    parallel:
        # Прозрачность: плавно появляется и исчезает
        ease 1.5 alpha 0.4 
        ease 1.5 alpha 0.0
        repeat
    parallel:
        # Смещение: "уплывает" в сторону и чуть увеличивается
        ease 3.0 xoffset 40 yoffset 20 zoom 1.05
        # Мгновенный возврат в центр (пока он невидимый из-за alpha 0)
        xoffset 0 yoffset 0 zoom 1.0
        repeat