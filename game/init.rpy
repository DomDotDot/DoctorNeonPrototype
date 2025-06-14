# Определение персонажей игры.
    # Ключевые персонажи
define neon = Character('Неон', color="#1f4bc4", image="neon", ctc="ctc_blink", ctc_position="nestled")
define marcus = Character('Маркус', color="#967230", image="marcus", what_slow_cps_multiplier=0.85, ctc="ctc_blink", ctc_position="nestled")
define alex = Character('Алекс', color="#b41f5d", image="alex", what_slow_cps_multiplier=1.25, ctc="ctc_blink", ctc_position="nestled")
define oganesson = Character("[oganesson_display_name]", color="#663399", image="oganesson", dynamic=True, what_slow_cps_multiplier=0.75, ctc="ctc_blink", ctc_position="nestled")

    # Вспомогательные персонажи
define narrator = Character(None, what_size=25, ctc="ctc_blink", ctc_position="nestled")
define narrator_nvl = Character(None, kind=nvl)

define unknown = Character('Неизвестный', color="#ffffff", ctc="ctc_blink", ctc_position="nestled")
define unknown_f = Character('Неизвестная', color="#ffffff", ctc="ctc_blink", ctc_position="nestled")
define fcs = Character('Система Управление Полётом', color="#a30e0e")

    # Второстепенные персонажи
define petrovich = Character('Петрович', color="#7a7a7a", image="petrovich", ctc="ctc_blink", ctc_position="nestled")

define ceo = Character('Господин Бауманн (CEO)', color="#305a96", image="ceo_boss", ctc="ctc_blink", ctc_position="nestled") # Генеральный директор
define cro = Character('Доктор Грубенманн (CRO)', color="#753636", image="cro_boss", ctc="ctc_blink", ctc_position="nestled") # Руководитель исследований

define bully1 = Character('Задира 1', color="#b32424", image="bully", ctc="ctc_blink", ctc_position="nestled")
define bully2 = Character('Задира 2', color="#b32424", image="bully", ctc="ctc_blink", ctc_position="nestled")

define anna = Character('Анна', color="#d96411", image="anna", ctc="ctc_blink", ctc_position="nestled")
define sophie = Character('Софи', color="#d1c682", image="sophie", ctc="ctc_blink", ctc_position="nestled")

define headteacher = Character('Завуч', color="#808080", image="headteacher", ctc="ctc_blink", ctc_position="nestled")

# Кастомные стили
style thoughts:
        italic True
style yell:
        size 60
style whisper:
        size 20
        italic True

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

image ctc_blink:
    "gui/ctc.png"
    linear 0.75 alpha 1.0
    linear 0.75 alpha 0.0
    repeat

init python:

    renpy.music.register_channel("ambient", mixer="ambient", loop=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("ui_sfx", mixer="sfx", loop=False, tight=True)

init python:
    def slow_punctuation(str_to_test):
        return (str_to_test
            .replace("... ", "...{w=1.5} ")
            .replace(", ", ",{w=0.5} ")
            .replace(". ", ".{w=1.0} ")
            .replace("! ", "!{w=1.0} ")
            .replace("? ", "?{w=1.0} ")
            .replace(": ", ":{w=0.5} ")
            .replace("— ", "—{w=0.25} ")
            .replace(" —", " —{w=0.25} ")
            .replace("-", "-{w=0.25}")
            )
    config.say_menu_text_filter = slow_punctuation

# Переменные:

default oganesson_name_revealed = False
default oganesson_display_name = "Опекунша (размыто)"

# Технические функции

label reveal_oganesson_name:
    $ oganesson_name_revealed = True
    $ oganesson_display_name = "Оганесон"
