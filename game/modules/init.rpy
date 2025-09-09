# Определение персонажей игры.
    # Этот файл содержит стили и экраны, которые используются в игре.

init:
        transform flip:
                xzoom -1.0
        transform restore_flip:
                xzoom 1.0
        transform midright:
            xcenter 0.75
        transform midleft:
            xcenter 0.25
        transform enter_from_left(target_pos):
            xcenter -1.0
            ycenter 1.0
            linear 0.7
        transform enter_from_right(target_pos):
            xcenter -1.0
            ycenter 1.0
            linear 0.25

        $ flash = Fade(0.5, 0, 0.5, color="#FFFFFF")
return

image ctc_blink:
    "gui/ctc_general.png"
    linear 0.75 alpha 1.0
    linear 0.75 alpha 0.0
    repeat

image ctc_neon:
    "gui/ctc_neon.png"
    alpha 0.0
    linear 2
    linear 0.25 alpha 1.0