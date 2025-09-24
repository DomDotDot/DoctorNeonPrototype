image splash_anim_1:

    "gui/renpy-logo.png"
    xalign 0.5 yalign 0.5 alpha 0.0
    ease_quad 5.0 alpha 1.0 zoom 2.0

default persistent.firstlaunch = False

label splashscreen:

    ## Here begins our splashscreen animation.
    play sound "sfx/short-logo.mp3" volume 0.25
    show splash_anim_1
    show text "{size=30}Made with Ren'Py [renpy.version_only]{/s}":
        xalign 0.5 yalign 0.8 alpha 0.0
        pause 4.0
        linear 1.0 alpha 1.0
        
    ## The first time the game is launched, players cannot skip the animation.
    if not persistent.seen_splash:
            
        ## No input will be detected for the set time stated.
        ## Set this to be a little longer than how long the animation takes.
        $ renpy.pause(8.5, hard=True)
    
        $ persistent.seen_splash = True
        
    ## Players can skip the animation in subsequent launches of the game.
    else:
    
        if renpy.pause(8.5):
    
            call skip_splash from _call_skip_splash

    scene black
    with fade
    
    label skip_splash:
    
        pass

    ## The first time the game is launched, players can set their accessibility settings.
    if not persistent.firstlaunch:

        call screen language_selection_screen

        call screen content_warning
        
        call screen splash_settings

        call screen preferences

        ## This screen will not appear in subsequent launches of the game when
        ## the following variable becomes true.
        $ persistent.firstlaunch = True

return