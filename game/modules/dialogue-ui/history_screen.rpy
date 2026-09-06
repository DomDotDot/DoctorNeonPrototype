################################################################################
## Модуль истории диалогов (History / Message Log Screen)
## Doctor Neon Prototype - Cyber-Messenger Glassmorphic Interface
################################################################################

## Это определяет, какие теги могут отображаться на экране истории.
define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }

init python:
    def is_history_protagonist(h):
        """Проверяет, принадлежит ли реплика Неон (протагонисту)."""
        if not h or not h.who:
            return False
        if getattr(h, "image_tag", None) == "neon":
            return True
        who_str = str(h.who).strip()
        return who_str in (_("Неон"), "Неон", "Neon", getattr(renpy.store.neon, "name", "Неон"))

    class HistoryScrollTo(Action):
        """Быстрая прокрутка списка истории диалогов в самое начало или в конец."""
        def __init__(self, id, target="bottom"):
            self.id = id
            self.target = target

        def __call__(self):
            w = renpy.get_widget(None, self.id)
            if w and hasattr(w, "yadjustment") and w.yadjustment is not None:
                if self.target == "top":
                    w.yadjustment.change(0)
                else:
                    w.yadjustment.change(w.yadjustment.range)
            renpy.restart_interaction()


screen history():

    tag menu
    modal True
    zorder 150
    predict False

    ## Затемнённый полупрозрачный фон поверх игрового экрана
    add Solid("#060a14f0")

    key "game_menu" action Return()
    key "hide_windows" action Return()

    frame:
        style "history_panel"

        vbox:
            spacing 14
            xfill True
            yfill True

            # Верхняя панель (Заголовок + Кнопка закрытия)
            hbox:
                xfill True
                yalign 0.5

                text _("ИСТОРИЯ ДИАЛОГОВ"):
                    font gui.name_text_font
                    size 28
                    color "#00d4ff"
                    bold True
                    outlines [ (1, "#002851aa", 0, 0) ]
                    yalign 0.5

                textbutton _("✕ Закрыть") action Return():
                    style "history_close_button"

            # Тонкая неоновая разделительная линия
            frame:
                xfill True
                ysize 1
                background Solid("#30456566")

            # Список реплик в стиле мессенджера
            viewport:
                id "history_vp"
                scrollbars "vertical"
                mousewheel True
                draggable True
                pagekeys True
                yinitial 1.0
                side_spacing 14

                vbox:
                    spacing 14
                    xfill True

                    for h in _history_list:
                        $ _is_neon = is_history_protagonist(h)
                        $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)

                        if _is_neon:
                            ## Реплика Неон (Протагонист): прижата вправо, изумрудный кибер-пузырь, без имени
                            frame:
                                style "history_bubble_neon"
                                xalign 1.0
                                xmaximum 1020

                                hbox:
                                    spacing 10
                                    xalign 1.0

                                    text what:
                                        style "history_text_neon"
                                        substitute False

                                    if getattr(h, "voice", None) and getattr(h.voice, "filename", None):
                                        textbutton "🔊":
                                            style "history_voice_btn"
                                            action Play("voice", h.voice.filename)

                        elif h.who:
                            ## Реплика собеседника: прижата влево, тёмно-синий кибер-пузырь, с именем в фирменном цвете
                            frame:
                                style "history_bubble_other"
                                xalign 0.0
                                xmaximum 1020

                                vbox:
                                    spacing 6

                                    hbox:
                                        spacing 10
                                        yalign 0.5

                                        $ _speaker_color = h.who_args.get("color", "#5b8eef")
                                        text h.who:
                                            font gui.name_text_font
                                            size 22
                                            bold True
                                            color _speaker_color
                                            yalign 0.5

                                        if getattr(h, "voice", None) and getattr(h.voice, "filename", None):
                                            textbutton "🔊":
                                                style "history_voice_btn"
                                                action Play("voice", h.voice.filename)

                                    text what:
                                        style "history_text_other"
                                        substitute False

                        else:
                            ## Мысли / Нарратив: по центру, нейтральный тёмный пузырь, текст курсивом без заголовка
                            frame:
                                style "history_bubble_narrator"
                                xalign 0.5
                                xmaximum 880

                                text what:
                                    style "history_text_narrator"
                                    substitute False

                    if not _history_list:
                        null height 150
                        text _("История диалогов пуста."):
                            font gui.text_font
                            size 26
                            color "#556677"
                            xalign 0.5
                        null height 150

            # Тонкая разделительная линия перед футером
            frame:
                xfill True
                ysize 1
                background Solid("#30456566")

            # Нижняя панель (Подсказки + Быстрый скролл + Кнопка возврата)
            hbox:
                xfill True
                yalign 0.5

                text _("Прокрутка: Колесо мыши / Стрелки   •   Закрыть: ESC / ПКМ"):
                    font gui.text_font
                    size 16
                    color "#556677"
                    yalign 0.5

                # Кнопки быстрой прокрутки в самое начало и в самый конец
                hbox:
                    xalign 0.5
                    spacing 10
                    yalign 0.5

                    textbutton _("▲ В начало"):
                        style "history_nav_button"
                        action HistoryScrollTo("history_vp", "top")

                    textbutton _("▼ В конец"):
                        style "history_nav_button"
                        action HistoryScrollTo("history_vp", "bottom")

                textbutton _("Вернуться в игру") action Return():
                    style "history_return_button"


## Стили основного контейнера ##################################################

style history_panel is frame:
    xalign 0.5
    yalign 0.5
    xsize 1420
    ysize 930
    background Frame("gui/textbox.png", 20, 20)
    padding (36, 24, 36, 20)

## Стили пузырей сообщений (Messenger Bubbles) ##################################

style history_bubble_neon is frame:
    background Frame("gui/history_bubble_neon.png", 16, 16)
    padding (22, 14, 22, 14)

style history_bubble_other is frame:
    background Frame("gui/history_bubble_other.png", 16, 16)
    padding (22, 14, 22, 14)

style history_bubble_narrator is frame:
    background Frame("gui/history_bubble_narrator.png", 16, 16)
    padding (24, 12, 24, 14)

## Стили текста ################################################################

style history_text_neon is default:
    font gui.text_font
    size 24
    color "#f0fdf4"
    line_spacing 4

style history_text_other is default:
    font gui.text_font
    size 24
    color "#e2ebf5"
    line_spacing 4

style history_text_narrator is default:
    font gui.text_font
    size 22
    color "#94a3b8"
    italic True
    xalign 0.5
    text_align 0.5
    line_spacing 4

## Стили кнопок управления #####################################################

style history_close_button is default:
    background Frame("gui/button/quick_idle.png", 8, 8)
    hover_background Frame("gui/button/quick_hover.png", 8, 8)
    padding (16, 6, 16, 6)
    xalign 1.0
    yalign 0.5
    hover_sound "audio/sfx/cursor-hover.opus"
    activate_sound "audio/sfx/button-click.opus"

style history_close_button_text is button_text:
    font gui.text_font
    size 18
    idle_color "#a0b2c6"
    hover_color "#ffffff"
    xalign 0.5
    yalign 0.5

style history_nav_button is default:
    background Frame("gui/button/quick_idle.png", 8, 8)
    hover_background Frame("gui/button/quick_hover.png", 8, 8)
    padding (14, 5, 14, 5)
    yalign 0.5
    hover_sound "audio/sfx/cursor-hover.opus"
    activate_sound "audio/sfx/button-click.opus"

style history_nav_button_text is button_text:
    font gui.text_font
    size 16
    idle_color "#8ea8c4"
    hover_color "#ffffff"
    xalign 0.5
    yalign 0.5

style history_return_button is default:
    background Frame("gui/button/quick_idle.png", 8, 8)
    hover_background Frame("gui/button/quick_hover.png", 8, 8)
    padding (20, 8, 20, 8)
    xalign 1.0
    yalign 0.5
    hover_sound "audio/sfx/cursor-hover.opus"
    activate_sound "audio/sfx/button-click.opus"

style history_return_button_text is button_text:
    font gui.text_font
    size 19
    idle_color "#c0d4ec"
    hover_color "#ffffff"
    xalign 0.5
    yalign 0.5

style history_voice_btn is default:
    padding (4, 1, 4, 1)
    yalign 0.5
    hover_sound "audio/sfx/cursor-hover.opus"
    activate_sound "audio/sfx/button-click.opus"

style history_voice_btn_text is button_text:
    size 18
    idle_color "#5b8eef"
    hover_color "#00d4ff"

style history_vp_vscrollbar is vscrollbar:
    xsize 8
    unscrollable "hide"
    base_bar Solid("#ffffff12")
    thumb Solid("#5b8eefaa")
    hover_thumb Solid("#00d4ff")

style history_vscrollbar is history_vp_vscrollbar
