label secret_scene_vol1:

    window hide dissolve

    scene bg chapter_4-5 sewers with Dissolve(5.0)
    show bg chapter_4-5 sewers at walking_zoom(4.0)
    
    # Звук шагов (опционально)
    # play sound "audio/steps.opus" loop
    
    $ renpy.pause(4.0, hard=True)
    
    # stop sound fadeout 0.5

    scene black with dissolve

    show 12cg-2 at blur_flicker
    
    # play audio "audio/light_buzz.opus"
    
    $ renpy.pause(3.0, hard=True)

    scene black with Dissolve(2.0)
    
    # Возвращаем интерфейс
    window show dissolve

return