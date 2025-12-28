# Определение персонажей игры.
    # Этот файл содержит стили и экраны, которые используются в игре.

init:
        transform flip:
                xzoom -1.0
                yalign 1.0
        transform restore_flip:
                xzoom 1.0
                yalign 1.0
        transform midright:
            xalign 0.75
            yalign 1.0
        transform midleft:
            xalign 0.25
            yalign 1.0
        transform enter_from_left(target_pos):
            xalign -1.0
            yalign 1.0
            linear 0.7
        transform enter_from_right(target_pos):
            xalign -1.0
            yalign 1.0
            linear 0.25

        $ flash = Fade(0.5, 0, 0.5, color="#FFFFFF")
return

image white = "#FFFFFF"

image ctc_blink:
    "images/ctc/ctc_general.png"
    linear 0.75 alpha 1.0
    linear 0.75 alpha 0.0
    repeat

image ctc_neon:
    "images/ctc/ctc_neon.png"
    alpha 0.0
    linear 2
    linear 0.25 alpha 1.0

image ctc_seraphina:
        "images/ctc/ctc_seraphina.png"
        anchor (0.5, 0.5)
        align (0.5, 0.5)
        yoffset 6  
        xoffset 14

        easein_quint 1.0 zoom 0.85
        easeout_quint 0.5 zoom 1.0
        easein_quint 0.25 zoom 0.85
        easeout_quint 0.5 zoom 1.0
        repeat

image ctc_nari:
    anchor (0.5, 0.5)
    align (0.5, 0.5)
    
    yoffset 6  
    xoffset 14

    # Целое сердце
    "images/ctc/ctc_nari.png"
    zoom 1
    
    # easein_quint 1.0 zoom 1

    # Анимация "Вдребезги" (Тряска)
    linear 0.05 xoffset 18
    linear 0.05 xoffset 10
    linear 0.05 xoffset 18
    linear 0.05 xoffset 10
    linear 0.05 xoffset 14

    # Разбитое сердце
    "images/ctc/ctc_nari_broken.png"
    easeout_quint 0.1 zoom 1