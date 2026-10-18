init python:

    renpy.music.register_channel("ambient", mixer="ambient", loop=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("menu_sfx", mixer="menu_sfx", loop=False, tight=True)
    renpy.music.register_channel("ui_sfx", mixer="menu_sfx", loop=False, tight=True)
    renpy.music.register_channel("ui_sfx1", mixer="menu_sfx", loop=False, tight=True)
    renpy.music.register_channel("ambient1", mixer="ambient", loop=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    
    config.play_channel = "menu_sfx"
    config.auto_voice = "voice/{id}.ogg"

    if "menu_sfx" not in preferences.volumes:
        preferences.volumes["menu_sfx"] = 0.8