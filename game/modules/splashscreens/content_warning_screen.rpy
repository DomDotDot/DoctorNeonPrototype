# ==============================================================================
# Экран предупреждения о контенте 18+ (Cyber-Glassmorphism Redesign)
# ==============================================================================

screen content_warning_screen():
    tag menu
    modal True
    zorder 100

    if main_menu:
        use main_menu_background
        add Solid("#000000cc")
    else:
        add Solid("#000000eb")

    frame:
        style "modern_panel_wide"
        xsize 1240
        padding (35, 20)
        background Solid("#0e131ff2")
        xalign 0.5
        yalign 0.5

        vbox:
            spacing 10
            xfill True

            # ------------------------------------------------------------------
            # 1. Верхний информационный баннер со статусом режима 18+
            # ------------------------------------------------------------------
            frame:
                xfill True
                padding (16, 10)
                background Solid("#181824cc")

                hbox:
                    spacing 15
                    yalign 0.5
                    xfill True

                    text "🔞" size 28 yalign 0.5
                    vbox:
                        yalign 0.5
                        spacing 2
                        text _("ВНИМАНИЕ: ВОЗРАСТНОЙ РЕЙТИНГ 18+") size 18 bold True color "#f43f5e"
                        text _("Материалы и темы предназначены исключительно для совершеннолетней аудитории.") size 13 color "#94a3b8"

                    frame:
                        xalign 1.0
                        yalign 0.5
                        background None
                        if persistent.sensitive_mode:
                            frame:
                                background Solid("#f43f5e")
                                padding (12, 6)
                                text _("🔞 РЕЖИМ 18+: ВКЛЮЧЕН") size 12 bold True color "#ffffff"
                        else:
                            frame:
                                background Solid("#1e293b")
                                padding (12, 6)
                                text _("🛡️ РЕЖИМ 18+: ВЫКЛ (ЦЕНЗУРА)") size 12 bold True color "#94a3b8"

            # ------------------------------------------------------------------
            # 2. Карточка тематических триггеров (Сетка 2x3)
            # ------------------------------------------------------------------
            frame:
                style "settings_card"
                background Solid("#141420cc")
                padding (16, 12)
                xfill True

                vbox:
                    spacing 8
                    xfill True

                    hbox:
                        xfill True
                        yalign 0.5
                        text _("ТЕМАТИЧЕСКИЕ ТРИГГЕРЫ И ЭЛЕМЕНТЫ ПОВЕСТВОВАНИЯ") size 14 bold True color "#00d4ff"
                        text _("Предупреждение о содержании") size 12 color "#888888" yalign 0.5

                    grid 2 3:
                        spacing 8
                        xfill True

                        # Триггер 1
                        frame:
                            background Solid("#18182acc")
                            padding (10, 6)
                            xfill True
                            hbox:
                                spacing 10
                                text "🩸" size 18 yalign 0.0
                                vbox:
                                    text _("Жестокое насилие и кровь") size 13 bold True color "#e2e8f0"
                                    text _("Физическая расправа, оружие, травмы и ранения.") size 11 color "#94a3b8" layout "subtitle"

                        # Триггер 2
                        frame:
                            background Solid("#18182acc")
                            padding (10, 6)
                            xfill True
                            hbox:
                                spacing 10
                                text "🪱" size 18 yalign 0.0
                                vbox:
                                    text _("Боди-хоррор и паразиты") size 13 bold True color "#e2e8f0"
                                    text _("Изувеченные тела, насекомые-паразиты, трипофобия, мутации.") size 11 color "#94a3b8" layout "subtitle"

                        # Триггер 3
                        frame:
                            background Solid("#18182acc")
                            padding (10, 6)
                            xfill True
                            hbox:
                                spacing 10
                                text "🧠" size 18 yalign 0.0
                                vbox:
                                    text _("Психологическое насилие") size 13 bold True color "#e2e8f0"
                                    text _("Газлайтинг, манипуляции, потеря контроля над разумом, темы суицида.") size 11 color "#94a3b8" layout "subtitle"

                        # Триггер 4
                        frame:
                            background Solid("#18182acc")
                            padding (10, 6)
                            xfill True
                            hbox:
                                spacing 10
                                text "⚠️" size 18 yalign 0.0
                                vbox:
                                    text _("Сексуализированный подтекст") size 13 bold True color "#e2e8f0"
                                    text _("Намёки на принуждение, одурманивающие вещества, фетишизированное насилие.") size 11 color "#94a3b8" layout "subtitle"

                        # Триггер 5
                        frame:
                            background Solid("#18182acc")
                            padding (10, 6)
                            xfill True
                            hbox:
                                spacing 10
                                text "🍷" size 18 yalign 0.0
                                vbox:
                                    text _("Табуированная лексика и вещества") size 13 bold True color "#e2e8f0"
                                    text _("Ненормативная лексика, употребление алкоголя, психоактивные вещества.") size 11 color "#94a3b8" layout "subtitle"

                        # Триггер 6 (Инфо)
                        frame:
                            background Solid("#18182acc")
                            padding (10, 6)
                            xfill True
                            hbox:
                                spacing 10
                                text "🛡️" size 18 yalign 0.0
                                vbox:
                                    text _("Ограничение 18+") size 13 bold True color "#e2e8f0"
                                    text _("Если вы чувствительны к данным темам, пожалуйста, воздержитесь от прохождения.") size 11 color "#94a3b8" layout "subtitle"

            # ------------------------------------------------------------------
            # 3. Интерактивный блок настроек (Явные тумблеры как в меню настроек)
            # ------------------------------------------------------------------
            frame:
                style "settings_card"
                background Solid("#141420cc")
                padding (16, 12)
                xfill True

                vbox:
                    spacing 8
                    xfill True

                    hbox:
                        xfill True
                        yalign 0.5
                        text _("ПАРАМЕТРЫ КОНТЕНТА (МОЖНО ИЗМЕНИТЬ В ЛЮБОЙ МОМЕНТ В НАСТРОЙКАХ)") size 14 bold True color "#00d4ff"
                        text _("Управление режимами") size 12 color "#888888" yalign 0.5

                    # Тумблер 1: Режим 18+
                    button:
                        xfill True
                        ysize 46
                        style "settings_chip_btn"
                        action Function(toggle_sensitive_mode_with_check)
                        tooltip _("Включает или выключает отображение откровенных и особо жестоких иллюстраций (CG).")
                        hbox:
                            xfill True
                            yalign 0.5
                            spacing 12
                            text "🔞" size 20 yalign 0.5
                            vbox:
                                yalign 0.5
                                spacing 2
                                text _("Взрослый контент (Режим 18+)") size 13 bold True color "#e2e8f0"
                                if persistent.sensitive_mode:
                                    text _("Откровенные и жестокие иллюстрации (CG) отображаются без цензуры") size 11 color "#fca5a5"
                                else:
                                    text _("Откровенные иллюстрации заменены цензурными версиями (влияет только на CG)") size 11 color "#94a3b8"
                            frame:
                                xalign 1.0
                                yalign 0.5
                                background (Solid("#f43f5e") if persistent.sensitive_mode else Solid("#222230"))
                                padding (12, 5)
                                text (_("✓ ВКЛЮЧЕН") if persistent.sensitive_mode else _("✕ ВЫКЛ (ЦЕНЗУРА)")) size 11 bold True color ("#ffffff" if persistent.sensitive_mode else "#888888")

                    # Тумблер 2: ИИ-чувствительность
                    button:
                        xfill True
                        ysize 46
                        style "settings_chip_btn"
                        action Function(toggle_ai_sensitive_with_check)
                        tooltip _("Включает или выключает скрытие нейросетевых изображений (замена заглушкой).")
                        hbox:
                            xfill True
                            yalign 0.5
                            spacing 12
                            text "🤖" size 20 yalign 0.5
                            vbox:
                                yalign 0.5
                                spacing 2
                                text _("ИИ-чувствительность (AI Sensitive Mode)") size 13 bold True color "#e2e8f0"
                                if persistent.ai_sensitive_mode:
                                    text _("Изображения с участием нейросетей скрыты и заменены системными экранами") size 11 color "#86efac"
                                else:
                                    text _("Изображения и иллюстрации отображаются в штатном режиме") size 11 color "#94a3b8"
                            frame:
                                xalign 1.0
                                yalign 0.5
                                background (Solid("#39ff14") if persistent.ai_sensitive_mode else Solid("#222230"))
                                padding (12, 5)
                                text (_("✓ ВКЛ (СКРЫТО)") if persistent.ai_sensitive_mode else _("✕ ВЫКЛ (АКТИВНО)")) size 11 bold True color ("#000000" if persistent.ai_sensitive_mode else "#888888")

            # Важное пояснение
            text _("ВАЖНО: Настройка «Режим 18+» скрывает только откровенные и жестокие иллюстрации (CG). Текстовое повествование остаётся неизменным.") size 11 color "#888888" text_align 0.5 xalign 0.5 layout "subtitle"

            null height 4

            # ------------------------------------------------------------------
            # 4. Навигация внизу
            # ------------------------------------------------------------------
            hbox:
                spacing 30
                xalign 0.5

                textbutton _("В главное меню"):
                    action Return("cancel")
                    style "modern_button"
                    xsize 260
                    ysize 46
                    text_size 15
                    background Solid("#222230")
                    hover_background Solid("#333348")

                textbutton _("Далее ➔"):
                    action Return("next")
                    style "modern_button"
                    xsize 260
                    ysize 46
                    text_size 15
                    background Solid("#f43f5e")
                    hover_background Solid("#fb7185")

    key "game_menu" action Return("cancel")
