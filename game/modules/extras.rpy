screen content_warning():

    tag menu

    frame:

        align(0.5, 0.5)
        xmargin 50
        xpadding 100

        vbox:
            
            align(0.5, 0.5)
            spacing 50
            # xfill True
            style_prefix "presplash"

            label _("Дисклеймер") xalign 0.5

            text _("Привет, дорогой игрок!") text_align 0.5 xalign 0.5

            null height 20

            text _("""Спасибо, что решили познакомиться с моей историей. Прежде чем вы окунетесь в этот мир, я хочу быть с вами полностью честным.

Я не художник, а в первую очередь рассказчик.

У меня в голове родилась история с персонажами, которых я полюбил, и мне безумно хотелось поделиться ею с кем-то ещё. Визуальная новелла показалась мне идеальным форматом для этого.

Чтобы «оживить» мир и героев, я использовал современные технологии - все фоны, спрайты персонажей и иллюстрации (CG) были созданы с помощью нейросетей (AI). Это стало для меня тем самым мостиком, который позволил визуализировать то, что я придумал.

При этом всё остальное — сюжет, диалоги, характеры персонажей и сама идея - это полностью моя авторская работа, в которую я вложил душу.

Также хочу отметить, что в игре используется музыка, распространяемая по лицензии Royalty-Free, за что я безмерно благодарен её создателям.

Эта новелла не является коммерческим проектом и создана исключительно из любви к историям.""") text_align 0.5 xalign 0.5 size 20

            null height 40

            text _("Спасибо за ваше понимание! Надеюсь, вам понравится путешествие, которое вас ждёт.") text_align 0.5 xalign 0.5

            textbutton _("Подтвердить") action Return() xalign 0.5 text_align 0.5 text_size 55
    


## Splashscreen Settings##################################
##
## A custom screen that tells players to adjust their settings in the Preferences
## Screen. Edited so you don't have to keep track of two different pages.

screen splash_settings():

    tag menu

    frame:

        align(0.5, 0.5)
        xmargin 50
        xpadding 100

        vbox:
            
            align(0.5, 0.5)
            spacing 50
            # xfill True
            style_prefix "presplash"

            label _("Установите настройки") xalign 0.5

            text _("В следующем меню вы можете задать настройки игры. Эти параметры можно изменить в любое время в меню.") text_align 0.5 xalign 0.5

            textbutton _("Подтвердить") action Return() xalign 0.5 text_align 0.5 text_size 55

# --- Сам экран ---
screen content_warning_screen():
    tag menu
    modal True
    
    # 1. Задний фон всего экрана (затемнение)
    add Solid("#000000") alpha 0.9

    # 2. Основная рамка
    frame:
        style "warning_frame"
        
        # 3. Водяной знак "!" на фоне (zorder не нужен, просто рисуем первым)
        # Он будет ПОД текстом внутри рамки
        text "!":
            size 600
            color "#ff000050"
            align (0.5, 0.55)
            font "DejaVuSans.ttf" # Лучше использовать жирный шрифт

        vbox:
            spacing 30
            align (0.5, 0.5)

            # Заголовок
            label _("ВНИМАНИЕ: КОНТЕНТ 18+") style "warning_title"

            # Разделительная черта (красная)
            add Solid("#ff3333") xsize 800 ysize 2 xalign 0.5 alpha 0.5

            text _("Данная визуальная новелла содержит материалы, предназначенные исключительно для взрослой аудитории.") xalign 0.5
            
            null height 20

            text _("{b}Игра затрагивает следующие темы:{/b}"):
                style "warning_text"
            text _("• {b}Жестокое насилие и кровь:{/b} Сцены физической расправы, использование холодного и огнестрельного оружия, детальные описания травм."):
                style "warning_text"
            text _("• {b}Боди-хоррор и Инсектофобия:{/b} Детальные описания и изображения изуродованных тел, паразитирование насекомых в человеческом теле, трипофобия. Элементы боди-хоррора."):
                style "warning_text"
            text _("• {b}Психологическое насилие:{/b} Газлайтинг, манипуляции, потеря контроля над телом и разумом, темы/упоминание суицида и селфхарма."):
                style "warning_text"
            text _("• {b}Сексуальный подтекст и Недобровольные действия:{/b} Сцены с намеками на принуждение, домогательства, употребление веществ, лишающих воли, и фетишизированного насилия. Фан-сервис и нетрадиционные отношения."):
                style "warning_text"
            text _("• {b}Прочее:{/b} Ненормативная лексика, употребление алкоголя, осквернение тел умерших."):
                style "warning_text"

            # Детальное описание
            #text _("{b}Эта игра содержит сцены, предназначенные только для взрослой аудитории.{/b}\n\nСюда могут входить: насилие, ненормативная лексика, употребление веществ и откровенные сцены сексуального характера.\nЕсли вам нет 18 лет или данный контент для вас неприемлем, пожалуйста, не включайте этот режим."):
            #   style "warning_text"

            null height 20
            
            add Solid("#ff3333") xsize 800 ysize 2 xalign 0.5 alpha 0.5

            # Блок управления настройкой
            # Мы используем кнопку, которая меняет свой вид и текст
            button:
                style_prefix "warning_button"
                xalign 0.5
                action ToggleField(persistent, "sensitive_mode")

                # Звук при нажатии
                # activate_sound "audio/click.ogg" 

                # Оформление кнопки (Фон и отступы)
                background Solid("#222") # Можно использовать стандартный фон кнопок или 
                hover_background Solid("#444")
                padding (40, 20)
                
                hbox:
                    spacing 25
                    align (0.5, 0.5)

                    # 1. ВИЗУАЛЬНЫЙ ЧЕКБОКС (Крупный и заметный)
                    if persistent.sensitive_mode:
                        text "[[X]" color "#ff0000" size 60 bold True yalign 0.5
                    else:
                        text "[[  ]" color "#666666" size 60 bold True yalign 0.5

                    # 2. ТЕКСТОВОЕ ОПИСАНИЕ
                    vbox:
                        yalign 0.5
                        spacing 5

                        # Заголовок состояния
                        if persistent.sensitive_mode:
                            text _("РЕЖИМ 18+: ВКЛЮЧЕН") color "#ff3333" size 40 bold True
                        else:
                            text _("РЕЖИМ 18+: ВЫКЛЮЧЕН") color "#aaaaaa" size 40 bold True

                        # Пояснение (критически важно для понимания)
                        text "Нажмите, чтобы переключить (влияет только на CG)" color "#888888" size 20
                        
            text _("ВАЖНО: Настройка «Режим 18+» скрывает только откровенные и особо жестокие иллюстрации (CG). Текстовое повествование остается неизменным и может вызвать дискомфорт независимо от настроек графики."):
                xalign 0.5 color "#aaaaaa" size 20
            text _("Если вам нет 18 лет или вы чувствительны к подобным темам - пожалуйста, воздержитесь от игры."):
                xalign 0.5 color "#aaaaaa" size 20

            null height 30

            # Кнопка подтверждения
            textbutton _("ПОДТВЕРДИТЬ И НАЧАТЬ"):
                action Return() 
                xalign 0.5
                text_size 50
                text_color "#ffffff"
                text_hover_color "#ff3333" # Краснеет при наведении



style presplash_label:
    top_margin gui.pref_spacing
    bottom_margin 3
    text_align 0.5

style presplash_label_text:
    yalign 1.0
    size 100


# --- Стили для экрана предупреждения ---
style warning_frame:
    background Frame(Solid("#2b0505bb"), 10, 10) # Темно-красный фон
    xalign 0.5
    yalign 0.5
    xsize 1920
    ysize 720
    padding (60, 60)
    # Делаем красную обводку
    xfill True

style warning_title:
    color "#ff3333" # Ярко-красный заголовок
    size 80
    xalign 0.5
    bold True
    font "fonts/WDXLLubrifontTC-Regular.ttf" # Укажите ваш шрифт, если есть

style warning_text:
    color "#e0e0e0" # Светло-серый текст
    size 26
    xalign 0.5
    text_align 0.5
    layout "subtitle" # Позволяет тексту красиво переноситься

style warning_button_text:
    size 35
    idle_color "#888888"
    hover_color "#ffffff"
    selected_color "#ff3333" # Красный, если выбрано
    xalign 0.5