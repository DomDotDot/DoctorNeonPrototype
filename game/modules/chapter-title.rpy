################################################################################
## Экран титула главы (Chapter Intro Screen)
## Doctor Neon Prototype - Cinematic Glass & Animated Branch Loading
################################################################################

## Глобальный переход: волна из левого нижнего угла в правый верхний
define chapter_wave_dissolve = ImageDissolve("gui/wave_mask.png", 0.85, ramplen=128)

## Анимация прорастания ветви (Индикатор загрузки, ~15 FPS) #####################

image chapter_branch_growth:
    "gui/branch1.png"
    0.25
    "gui/branch2.png"
    0.25
    "gui/branch3.png"
    0.125
    "gui/branch4.png"
    0.125
    "gui/branch5.png"
    0.125
    "gui/branch6.png"
    0.065
    "gui/branch7.png"
    0.065
    "gui/branch8.png"
    0.065
    "gui/branch9.png"
    0.065
    "gui/branch10.png"
    0.065
    "gui/branch11.png"
    0.065
    "gui/branch12.png"
    0.065
    "gui/branch13.png"
    0.065
    "gui/branch14.png"
    0.065
    "gui/branch15.png"
    0.065
    "gui/branch16.png"
    0.125
    "gui/branch17.png"
    0.125
    "gui/branch18.png"
    0.25
    "gui/branch19.png"
    # По завершении роста ветвь остаётся статичной и чёткой


## Трансформы плавного каскадного появления ####################################

transform chapter_fade:
    on show:
        alpha 0.0
        easein 0.5 alpha 1.0
    on hide:
        easeout 0.3 alpha 0.0

transform chapter_number_appear:
    alpha 0.0 yoffset -10
    pause 0.15
    easein 0.45 alpha 1.0 yoffset 0

transform chapter_divider_expand:
    xalign 0.5
    xsize 40
    alpha 0.0
    pause 0.35
    parallel:
        easein 0.25 alpha 1.0
    parallel:
        easein 0.70 xsize 650

transform chapter_title_appear:
    alpha 0.0 yoffset 10
    pause 0.50
    easein 0.55 alpha 1.0 yoffset 0

transform chapter_branch_appear:
    alpha 0.0
    pause 0.55
    easein 0.25 alpha 0.95

transform chapter_sub_appear:
    alpha 0.0
    pause 0.85
    easein 0.60 alpha 1.0

transform chapter_hint_appear:
    alpha 0.0
    pause 1.8
    easein 0.8 alpha 0.35

# Захлёстывающая диагональная волна: полный проход через весь экран с оверхедом
# Стартует строго за лево-нижним углом и уходит далеко за право-верхний угол
transform chapter_wave_wipe:
    alpha 0.0
    xpos -4300
    ypos 500
    pause 3.0
    alpha 1.0
    easein 1.25 xpos -1300 ypos -1300


## Экран показа главы ##########################################################

screen chapter_screen(chapter_text, title_text, subtitle_text=None):
    modal True
    zorder 200

    on "show" action Function(start_chapter_tracking)

    # Автоматическое завершение после полного прохода волны за пределы экрана
    timer 4.5 action [Hide('chapter_screen', transition=None), Return()]

    # Возможность пропустить показ кликом или клавишами
    key "dismiss" action [Hide('chapter_screen', transition=Dissolve(0.3)), Return()]
    key "button_select" action [Hide('chapter_screen', transition=Dissolve(0.3)), Return()]

    # Полноэкранная прозрачная кнопка для пропуска по клику
    button:
        style "empty"
        xfill True
        yfill True
        action [Hide('chapter_screen', transition=Dissolve(0.3)), Return()]

    # Фон: глубокий темный космос с контрастом к черной волне
    frame:
        style "empty"
        xfill True
        yfill True
        background "#081022"
        at chapter_fade

    # Центрированный блок заголовка и ветви (единая композиция)
    fixed:
        align (0.5, 0.5)
        xsize 1100
        ysize 450

        # Анимированная растущая ветвь: расположена вплотную к заголовку справа с оверлапом
        add "chapter_branch_growth":
            xpos 0.5
            ypos 0.5
            xoffset 180
            yoffset -150
            at chapter_branch_appear

        # Текстовый блок (строго по центру экрана)
        vbox:
            align (0.5, 0.5)
            spacing 14

            text chapter_text:
                style "chapter_number_style"
                at chapter_number_appear

            # Дивайдер: 9-slice расширение из центра
            frame:
                style "empty"
                xalign 0.5
                background Frame("gui/dialogue_divider.png", 60, 0)
                ysize 4
                at chapter_divider_expand

            text title_text:
                style "chapter_title_style"
                at chapter_title_appear

            if subtitle_text:
                text subtitle_text:
                    style "chapter_subtitle_style"
                    at chapter_sub_appear

    # Захлёстывающая диагональная волна с контрастным неоновым гребнем
    # 6000x4500 полотно полностью укрывает экран и уходит за край с оверхедом
    add "gui/wave_wipe.png":
        at chapter_wave_wipe

    # Ненавязчивая подсказка внизу экрана
    text _("Нажмите в любое место для продолжения"):
        style "chapter_skip_hint"
        at chapter_hint_appear


## Стили оформления текста #####################################################

style chapter_number_style is default:
    color "#00e5ff"
    font gui.name_text_font
    size 34
    xalign 0.5
    text_align 0.5
    bold True
    outlines [ (1, "#002851aa", 0, 0) ]

style chapter_title_style is default:
    color "#ffffff"
    font gui.name_text_font
    size 58
    xalign 0.5
    text_align 0.5
    bold True
    outlines [ (2, "#030712ee", 0, 0), (1, "#00e5ff33", 0, 0) ]

style chapter_subtitle_style is default:
    color "#94a3b8"
    font gui.text_font
    size 24
    xalign 0.5
    text_align 0.5
    italic True
    top_margin 6

style chapter_skip_hint is default:
    color "#64748b"
    font gui.text_font
    size 15
    xalign 0.5
    yalign 0.95