init python:
    import datetime
    def play_main_menu_music():

        music_map = {
            0: main_menu_music_default,
            1: main_menu_music_unlocked_1,
            2: main_menu_music_unlocked_2,
            3: main_menu_music_unlocked_3,
            4: main_menu_music_unlocked_4
        }
        track = music_map.get(persistent.main_menu_level, main_menu_music_default)
        renpy.music.play(track, fadein=1.0, if_changed=True)


################################################################################
## Главное меню (HUB)
################################################################################

screen main_menu_background():

    on "show" action Function(play_main_menu_music)
    on "replace" action Function(play_main_menu_music)

    # Фон с параллаксом
    add "main_menu_bg_dynamic":
        at mouse_parallax(30)

    # Частицы
    if datetime.datetime.now().month in (12, 1, 2):
        add SnowBlossom("gui/particle.png", count=120, border=50, xspeed=(20, 50), yspeed=(20, 50), start=10) id "main_menu_effect"

    # Виньетка
    add "gui/main_menu/vignette.png" alpha 0.4

    # Логотип
    add "main_menu_logo" xalign 0.5 ypos 25

screen main_menu():
    tag menu
    zorder 10
    
    use main_menu_background 

    # Основной блок навигации
    vbox:
        style "main_menu_vbox"

        textbutton _("Играть") action ShowMenu("play_menu") style "main_menu_button"
        textbutton _("Настройки") action ShowMenu("settings_menu") style "main_menu_button"
        
        if renpy.has_screen("memory_recollection"):
            textbutton _("Воспоминания") action ShowMenu("memory_recollection") style "main_menu_button"
        
        #textbutton _("Персонажи") action ShowMenu("bio_menu") style "main_menu_button"

        $ unread = get_unread_count() # Считаем количество в переменную
        
        if unread > 0:
            # Используем переменную unread внутри текста
            textbutton _("Уведомления ([unread])") action ShowMenu("notification_center") style "main_menu_button" text_color "#a11919"
        else:
            textbutton _("Уведомления") action ShowMenu("notification_center") style "main_menu_button"

        textbutton _("Об игре") action ShowMenu("about_menu") style "main_menu_button"
        textbutton _("Выход") action Quit(confirm=True) style "main_menu_button"