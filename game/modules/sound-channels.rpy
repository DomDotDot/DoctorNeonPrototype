init python:

    renpy.music.register_channel("ambient", mixer="ambient", loop=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("ui_sfx", mixer="sfx", loop=False, tight=True)
    renpy.music.register_channel("ambient1", mixer="ambient", loop=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    
    config.auto_voice = "voice/{id}.ogg"