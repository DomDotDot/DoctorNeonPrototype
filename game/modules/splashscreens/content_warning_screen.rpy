# --- Контент Варнинг Экран ---
screen content_warning_screen():
    tag menu
    modal True
    
    add Solid("#000000") alpha 0.9

    frame:
        style "modern_panel_wide"
        xsize 1400

        text "!":
            size 300
            color "#ff000064"
            align (0.5, 0.25)
            font "DejaVuSans.ttf"

        vbox:
            style "modern_vbox"
            spacing 25

            # Заголовок
            label _("ВНИМАНИЕ: КОНТЕНТ 18+") text_color "#ff3333" text_size 60 xalign 0.5 text_bold True bottom_margin 10

            add Solid("#ff3333") xsize 1100 ysize 2 xalign 0.5 alpha 0.5

            text _("Данная визуальная новелла содержит материалы, предназначенные исключительно для взрослой аудитории.") xalign 0.5 size 24 color "#e8e8e8" text_align 0.5
            
            # Темы
            vbox:
                spacing 10
                xalign 0.5
                text _("{b}Игра затрагивает следующие темы:{/b}") size 22 color "#cccccc" xalign 0.5
                text _("• {b}Жестокое насилие и кровь:{/b} Сцены физической расправы, использование холодного и огнестрельного оружия, детальные описания травм.") size 20 color "#aaaaaa" xalign 0.5 text_align 0.5 layout "subtitle"
                text _("• {b}Боди-хоррор и Инсектофобия:{/b} Детальные описания и изображения изуродованных тел, паразитирование насекомых в человеческом теле, трипофобия. Элементы боди-хоррора.") size 20 color "#aaaaaa" xalign 0.5 text_align 0.5 layout "subtitle"
                text _("• {b}Психологическое насилие:{/b} Газлайтинг, манипуляции, потеря контроля над телом и разумом, темы/упоминание суицида и селфхарма.") size 20 color "#aaaaaa" xalign 0.5 text_align 0.5 layout "subtitle"
                text _("• {b}Сексуальный подтекст и Недобровольные действия:{/b} Сцены с намеками на принуждение, домогательства, употребление веществ, лишающих воли, и фетишизированного насилия. Фан-сервис и нетрадиционные отношения.") size 20 color "#aaaaaa" xalign 0.5 text_align 0.5 layout "subtitle"
                text _("• {b}Прочее:{/b} Ненормативная лексика, употребление алкоголя, осквернение тел умерших.") size 20 color "#aaaaaa" xalign 0.5 text_align 0.5 layout "subtitle"

            add Solid("#ff3333") xsize 1100 ysize 2 xalign 0.5 alpha 0.5

            # Кнопка включения режима
            button:
                xalign 0.5
                xsize 700
                ysize 120
                background Solid("#222222cc")
                hover_background Solid("#444444cc")
                action ToggleField(persistent, "sensitive_mode")
                hover_sound "audio/sfx/cursor-hover.opus" 
                activate_sound "audio/sfx/button-click.opus"
                
                hbox:
                    spacing 25
                    align (0.5, 0.5)

                    if persistent.sensitive_mode:
                        text "[[ X ]" color "#ff3333" size 50 bold True yalign 0.5 font "DejaVuSans.ttf"
                    else:
                        text "[[   ]" color "#666666" size 50 bold True yalign 0.5 font "DejaVuSans.ttf"

                    vbox:
                        yalign 0.5
                        spacing 5

                        if persistent.sensitive_mode:
                            text _("РЕЖИМ 18+: ВКЛЮЧЕН") color "#ff3333" size 30 bold True
                        else:
                            text _("РЕЖИМ 18+: ВЫКЛЮЧЕН") color "#aaaaaa" size 30 bold True

                        text _("Нажмите, чтобы переключить (влияет только на CG)") color "#888888" size 18

            text _("ВАЖНО: Настройка «Режим 18+» скрывает только откровенные и особо жестокие иллюстрации (CG). Текстовое повествование остается неизменным и может вызвать дискомфорт независимо от настроек графики.") xalign 0.5 color "#aaaaaa" size 18 text_align 0.5 layout "subtitle"
            text _("Если вам нет 18 лет или вы чувствительны к подобным темам - пожалуйста, воздержитесь от игры.") xalign 0.5 color "#aaaaaa" size 18 text_align 0.5 layout "subtitle"

            null height 15

            textbutton _("ПОДТВЕРДИТЬ И НАЧАТЬ"):
                action Return() 
                style "danger_button"
                xsize 400
                xalign 0.5
