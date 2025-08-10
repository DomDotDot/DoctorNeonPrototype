# Определение персонажей игры.
    # Ключевые персонажи
define neon = Character(_('Неон'), color="#1f4bc4", image="neon", ctc="ctc_blink", ctc_position="nestled")
define marcus = Character(_('Маркус'), color="#967230", image="marcus", what_slow_cps_multiplier=0.85, ctc="ctc_blink", ctc_position="nestled")
define alex = Character(_('Алекс'), color="#b41f5d", image="alex", what_slow_cps_multiplier=1.25, ctc="ctc_blink", ctc_position="nestled")
define oganesson = Character("[oganesson_display_name]", color="#663399", image="oganesson", dynamic=True, what_slow_cps_multiplier=0.75, ctc="ctc_blink", ctc_position="nestled")

    # Вспомогательные персонажи
define narrator = Character(None, what_size=25, ctc="ctc_blink", ctc_position="nestled")
define narrator_nvl = Character(None, kind=nvl)

define unknown = Character(_('Неизвестный'), color="#ffffff", ctc="ctc_blink", ctc_position="nestled")
define unknown_f = Character(_('Неизвестная'), color="#ffffff", ctc="ctc_blink", ctc_position="nestled")
define fcs = Character(_('Система Управление Полётом'), color="#a30e0e", voice_tag="fcs")

    # Второстепенные персонажи
define hans = Character(_('Ханс'), color="#7a7a7a", image="hans", ctc="ctc_blink", ctc_position="nestled")

define ceo = Character(_('Господин Бауманн (CEO)'), color="#305a96", image="ceo_boss", ctc="ctc_blink", ctc_position="nestled") # Генеральный директор
define cro = Character(_('Доктор Грубенманн (CRO)'), color="#753636", image="cro_boss", ctc="ctc_blink", ctc_position="nestled") # Руководитель исследований

define anna = Character(_('Анна'), color="#d96411", image="anna", ctc="ctc_blink", ctc_position="nestled")
define sophie = Character(_('Софи'), color="#d1c682", image="sophie", ctc="ctc_blink", ctc_position="nestled")

define headteacher = Character(_('Завуч'), color="#808080", image="headteacher", ctc="ctc_blink", ctc_position="nestled")

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

# Определяем стили для нашего текста, чтобы легко менять его вид
style chapter_number_style:
    # Белый цвет, размер 40, выравнивание по центру
    color "#FFFFFF"
    size 40
    xalign 0.5
    # Отступ снизу, чтобы отделить от названия главы
    bottom_margin 20

style chapter_title_style:
    # Белый цвет, размер 60 (крупнее), выравнивание по центру
    color "#FFFFFF"
    size 60
    xalign 0.5

# Определение самого экрана
# Он принимает два параметра: chapter_text и title_text
screen chapter_screen(chapter_text, title_text):
 
    # modal True делает экран модальным. Это значит, что игрок не сможет
    # взаимодействовать с элементами под этим экраном (например, прокликивать диалог).
    modal True
    

    # on "show" определяет действие, которое выполнится при показе экрана.
    # Здесь мы запускаем таймер на 4 секунды.
    # По истечении времени экран скроется с анимацией растворения (dissolve).
    #on "show":
    timer 4.0 action [Hide('chapter_screen', transition=dissolve), Return()]
    
    # Добавляем сплошной черный фон на весь экран
    frame:
        xalign 0.5
        yalign 0.5
        background "#000000ff" # Слегка прозрачный фон
        padding (50, 50)

    # vbox - это контейнер, который располагает элементы вертикально.
    # Мы центрируем его по горизонтали и вертикали.
    vbox:
        xalign 0.5
        yalign 0.5

        # Первый текст, использующий параметр chapter_text и свой стиль
        text chapter_text style "chapter_number_style"

        # Второй текст, использующий параметр title_text и свой стиль
        text title_text style "chapter_title_style"

image ctc_blink:
    "gui/ctc.png"
    linear 0.75 alpha 1.0
    linear 0.75 alpha 0.0
    repeat

init python:

    renpy.music.register_channel("ambient", mixer="ambient", loop=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("ui_sfx", mixer="sfx", loop=False, tight=True)
    
    config.auto_voice = "voice/{id}.ogg"

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

init python:
    oganesson_name_revealed = False

    if _preferences.language == "english_us":
        oganesson_display_name = _("Trustee")
    else:
        oganesson_display_name = _("Опекунша")


# Технические функции

label reveal_oganesson_name:
    $ oganesson_name_revealed = True

    if _preferences.language == "english_us":
        $ oganesson_display_name = _("Oganesson")
    else:
        $ oganesson_display_name = _("Оганесон")