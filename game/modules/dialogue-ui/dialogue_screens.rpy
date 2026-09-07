################################################################################
## Модуль интерфейса диалогов (Say & Quick Menu)
## Doctor Neon Prototype - Glassmorphism & Cyberpunk Theme
################################################################################

## Экран say ###################################################################
##
## Этот экран используется для отображения диалогов игроку в режиме чтения.
## Имя персонажа и белая разделительная линия строго зафиксированы сверху,
## а текст реплики плавно растёт вниз внутри единого монолитного блока тёмного стекла.

screen say(who, what):

    window:
        id "window"

        if who is not None:
            vbox:
                xalign 0.5
                ypos 16
                spacing 4

                $ _name_fx = get_name_effect(who)
                if _name_fx is not None:
                    add _name_fx xalign 0.5
                else:
                    text who id "who" xalign 0.5

                add "gui/dialogue_divider.png" xalign 0.5

        text what id "what":
            xalign 0.5
            ypos (74 if who is not None else 36)
            xsize gui.dialogue_width
            text_align gui.dialogue_text_xalign

    ## Боковое изображение ("голова"), если используется
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0

    # Ачивка "Вдумчивый читатель": 3 минуты на реплике Неон
    if who is not None and (who == _("Неон") or who == "Неон" or who == "Neon" or who == neon.name):
        timer 180.0 action Function(grant_achievement, "thoughtful_reader")


init python:
    if 'namebox' not in config.character_id_prefixes:
        config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label

style window:
    xalign 0.5
    xsize gui.textbox_width
    ysize gui.textbox_height
    yalign gui.textbox_yalign
    padding (40, 0, 40, 0)

    background Frame("gui/textbox.png", 20, 20)

style namebox:
    xalign 0.5
    yalign 0.5

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign 0.5
    text_align 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xalign 0.5
    xsize gui.dialogue_width
    text_align gui.dialogue_text_xalign

    adjust_spacing False


## Экран быстрого меню #########################################################
##
## Высокотехнологичные кибер-плашки быстрого меню с подсветкой и звуками.

screen quick_menu():

    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"

            xalign 0.5
            ypos 1030
            spacing 10

            textbutton _("Назад") action Rollback()
            textbutton _("История") action ShowMenu('history')
            textbutton _("Пропуск") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Авто") action Preference("auto-forward", "toggle")
            textbutton _("Сохранить") action ShowMenu('save')
            textbutton _("Б.Сохр") action QuickSave()
            textbutton _("Б.Загр") action QuickLoad()
            textbutton _("Опции") action ShowMenu('settings_menu')


init python:
    if "quick_menu" not in config.overlay_screens:
        config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_button is default
style quick_button_text is button_text

style quick_button:
    background Frame("gui/button/quick_idle.png", 10, 10)
    hover_background Frame("gui/button/quick_hover.png", 10, 10)
    selected_background Frame("gui/button/quick_selected.png", 10, 10)
    insensitive_background Frame("gui/button/quick_insensitive.png", 10, 10)
    padding (16, 6, 16, 6)
    xalign 0.5
    yalign 0.5
    hover_sound "audio/sfx/cursor-hover.opus"
    activate_sound "audio/sfx/button-click.opus"

style quick_button_text:
    font gui.text_font
    size 20
    idle_color "#a0b2c6"
    hover_color "#ffffff"
    selected_color "#00e5ff"
    insensitive_color "#48526277"
    xalign 0.5
    yalign 0.5
