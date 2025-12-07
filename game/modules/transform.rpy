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
    anchor (0,0)
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