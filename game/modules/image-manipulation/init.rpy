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
    xoffset 15

    "images/ctc/ctc_general.png"
    linear 0.75 alpha 1.0
    linear 0.75 alpha 0.0
    repeat

image ctc_neon:
    xoffset 15

    "images/ctc/ctc_neon.png"
    alpha 0.0
    linear 2
    linear 0.25 alpha 1.0

image ctc_silence:
    xoffset 0

    "images/ctc/ctc_silence.png"

    easein_quint 2 alpha 1.0
    easeout_quint 2 alpha 0.0
    repeat



image ctc_celeste:
    xoffset 15

    "images/ctc/ctc_celeste.png"
    alpha 0.0
    linear 0.5
    linear 0.25 alpha 1.0

image ctc_seraphina:
        "images/ctc/ctc_seraphina.png"
        anchor (0.5, 0.5)
        align (0.5, 0.5)
        yoffset 6  
        xoffset 15

        easein_quint 1.0 zoom 0.85
        easeout_quint 0.5 zoom 1.0
        easein_quint 0.25 zoom 0.85
        easeout_quint 0.5 zoom 1.0
        repeat

image ctc_nari:
    anchor (0.5, 0.5)
    align (0.5, 0.5)
    
    yoffset 6  
    xoffset 15

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

image ctc_oganesson:
    xoffset 15

    # Первое появление с dissolve
    alpha 0.0
    "images/ctc/ctc_oganesson_1.png"
    linear 0.4 alpha 1.0

    # Луп: два лотуса плавно сменяют друг друга
    block:
        "images/ctc/ctc_oganesson_1.png" with Dissolve(2.0)
        pause(1.85)

        "images/ctc/ctc_oganesson_2.png" with Dissolve(1.5)
        pause(1.45)

        "images/ctc/ctc_oganesson_3.png" with Dissolve(0.4)
        pause(2.0)

        "images/ctc/ctc_oganesson_2.png" with Dissolve(0.4)
        pause(0.35)

        repeat


image ctc_akane:
    xoffset 15

    # Первое появление с dissolve
    alpha 0.0
    "images/ctc/ctc_akane_1.png"
    linear 0.4 alpha 1.0
    pause(1.0)

    "images/ctc/ctc_akane_2.png" with Dissolve(3.0)
