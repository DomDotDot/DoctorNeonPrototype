################################################################################
## Модуль визуализации клавиатуры и мыши (Doctor Neon Prototype)
################################################################################

################################################################################
## Визуализатор клавиатуры
################################################################################

screen keyboard_visual(cur_key):
    frame:
        style "controls_device_frame"
        xfill True
        ysize 560

        vbox:
            spacing 14
            xfill True

            # Заголовок секции клавиатуры
            hbox:
                xfill True
                yalign 0.5
                text _("РАСКЛАДКА КЛАВИАТУРЫ") size 12 bold True color "#64748b"
                text _("Подсвеченные клавиши функциональны") size 11 color "#475569"

            # Основная клавиатура + Блок навигации (стрелки и PgUp/PgDn)
            hbox:
                spacing 14
                xfill True

                # Основная раскладка клавиш
                vbox:
                    spacing 3
                    xsize 820

                    # Ряд 1: Esc + F-клавиши
                    hbox:
                        spacing 3
                        for kid, lbl, w, is_func in KB_ROW1:
                            if kid is None:
                                null width w
                            else:
                                use keycap_button(kid, lbl, w, 32, cur_key, is_func)

                    # Ряд 2: Цифры
                    hbox:
                        spacing 3
                        for kid, lbl, w, is_func in KB_ROW2:
                            use keycap_button(kid, lbl, w, 34, cur_key, is_func)

                    # Ряд 3: Tab + QWERTY
                    hbox:
                        spacing 3
                        for kid, lbl, w, is_func in KB_ROW3:
                            use keycap_button(kid, lbl, w, 34, cur_key, is_func)

                    # Ряд 4: Caps + ASDF + Enter
                    hbox:
                        spacing 3
                        for kid, lbl, w, is_func in KB_ROW4:
                            use keycap_button(kid, lbl, w, 34, cur_key, is_func)

                    # Ряд 5: Shift + ZXCV + Shift
                    hbox:
                        spacing 3
                        for kid, lbl, w, is_func in KB_ROW5:
                            use keycap_button(kid, lbl, w, 34, cur_key, is_func)

                    # Ряд 6: Ctrl, Alt, Пробел
                    hbox:
                        spacing 3
                        for kid, lbl, w, is_func in KB_ROW6:
                            use keycap_button(kid, lbl, w, 36, cur_key, is_func)

                # Блок навигации клавиатуры: PgUp/PgDn + Стрелки
                vbox:
                    spacing 4
                    xsize 150

                    text _("НАВИГАЦИЯ") size 11 bold True color "#64748b" xalign 0.5

                    # PgUp / PgDn
                    hbox:
                        spacing 4
                        xalign 0.5
                        use keycap_button("pgup", "PgUp ▲", 70, 34, cur_key, True)
                        use keycap_button("pgdown", "PgDn ▼", 70, 34, cur_key, True)

                    null height 16

                    # Стрелка Вверх
                    hbox:
                        xalign 0.5
                        use keycap_button("arrows", "▲", 48, 34, cur_key, True)

                    # Стрелки Влево, Вниз, Вправо
                    hbox:
                        spacing 3
                        xalign 0.5
                        use keycap_button("arrows", "◄", 46, 34, cur_key, True)
                        use keycap_button("arrows", "▼", 46, 34, cur_key, True)
                        use keycap_button("arrows", "►", 46, 34, cur_key, True)

            # Разделительная линия
            frame:
                background Solid("#1e293b88")
                xfill True
                ysize 1

            # Информационная панель быстрых горячих клавиш
            frame:
                background Solid("#080f1e88")
                xfill True
                padding (16, 12)
                vbox:
                    spacing 8
                    text _("⚡ БЫСТРЫЕ КОМБИНАЦИИ И ГОРЯЧИЕ КЛАВИШИ") size 12 bold True color "#38bdf8"
                    hbox:
                        spacing 14
                        xfill True

                        frame:
                            background Solid("#0f172a")
                            xsize 225
                            padding (10, 8)
                            vbox:
                                spacing 2
                                text "F5 / F6" size 12 bold True color "#00d4ff"
                                text _("Быстрое сохранение / загрузка") size 10 color "#94a3b8"

                        frame:
                            background Solid("#0f172a")
                            xsize 225
                            padding (10, 8)
                            vbox:
                                spacing 2
                                text "F11 / Alt+Enter" size 12 bold True color "#00d4ff"
                                text _("Полноэкранный режим игры") size 10 color "#94a3b8"

                        frame:
                            background Solid("#0f172a")
                            xsize 225
                            padding (10, 8)
                            vbox:
                                spacing 2
                                text "Space ␣" size 12 bold True color "#00d4ff"
                                text _("Листание без случайного выбора") size 10 color "#94a3b8"

                        frame:
                            background Solid("#0f172a")
                            xsize 225
                            padding (10, 8)
                            vbox:
                                spacing 2
                                text "Tab ↹ / Ctrl" size 12 bold True color "#00d4ff"
                                text _("Авто-пропуск / Ускорение") size 10 color "#94a3b8"


################################################################################
## Визуализатор мыши (HUD Cyberpunk)
################################################################################

screen mouse_visual(cur_key):
    frame:
        style "controls_device_frame"
        xfill True
        ysize 560

        vbox:
            spacing 6
            xfill True

            # Заголовок секции мыши
            hbox:
                xfill True
                yalign 0.5
                text _("ИНТЕРАКТИВНАЯ СХЕМА МЫШИ") size 12 bold True color "#64748b"
                text _("Наведите на элементы мыши или выносные плашки") size 11 color "#475569"

            # Графический HUD мыши (980 x 480)
            fixed:
                xsize 980
                ysize 480
                xalign 0.5

                # 1. Базовый чертёж мыши с линиями-выносками
                add "gui/controls/mouse_base.png"

                # 2. Неоновый оверлей активной клавиши
                if cur_key == "lmb":
                    add "gui/controls/mouse_glow_lmb.png"
                elif cur_key == "rmb":
                    add "gui/controls/mouse_glow_rmb.png"
                elif cur_key == "mmb":
                    add "gui/controls/mouse_glow_mmb.png"
                elif cur_key == "wheelup":
                    add "gui/controls/mouse_glow_wheelup.png"
                elif cur_key == "wheeldown":
                    add "gui/controls/mouse_glow_wheeldown.png"

                # 3. Интерактивные выносные плашки (Callout Chips)
                # Левая сторона
                use controls_callout_chip("lmb", "🖱 ЛКМ (Левый клик)", _("Диалог / Выбор"), 20, 86, 250, 38, cur_key)
                use controls_callout_chip("wheelup", "▲ Колёсико вверх", _("Откат назад"), 20, 206, 250, 38, cur_key)

                # Правая сторона
                use controls_callout_chip("rmb", "🖱 ПКМ (Правый клик)", _("Меню / Назад"), 710, 86, 250, 38, cur_key)
                use controls_callout_chip("mmb", "⏺ СКМ (Клик колёсиком)", _("Скрыть интерфейс"), 710, 186, 250, 38, cur_key)
                use controls_callout_chip("wheeldown", "▼ Колёсико вниз", _("Вперёд по сюжету"), 710, 276, 250, 38, cur_key)

                # 4. Физические интерактивные зоны на самом корпусе мыши
                use controls_hotspot("lmb", 400, 80, 75, 120)
                use controls_hotspot("rmb", 505, 80, 75, 120)
                use controls_hotspot("wheelup", 480, 95, 20, 32)
                use controls_hotspot("mmb", 480, 127, 20, 26)
                use controls_hotspot("wheeldown", 480, 153, 20, 32)




# Кнопка отдельной клавиши клавиатуры
screen keycap_button(kid, label_text, w, h, cur_key, is_functional):
    $ is_active = (cur_key == kid and is_functional)
    button:
        xsize w
        ysize h
        if is_functional:
            background (Solid("#00a8ff") if is_active else Solid("#0e1e33"))
            hover_background Solid("#00c3ff")
            hover_sound "audio/sfx/cursor-hover.opus"
            activate_sound "audio/sfx/button-click.opus"
            action [SetVariable("selected_control_key", kid), SetVariable("hovered_control_key", kid)]
            hovered SetVariable("hovered_control_key", kid)
            unhovered SetVariable("hovered_control_key", "")
            text label_text substitute False:
                align (0.5, 0.5)
                size (11 if len(label_text) > 4 else 12)
                bold True
                color ("#001122" if is_active else "#38bdf8")
        else:
            background Solid("#10152288")
            text label_text substitute False:
                align (0.5, 0.5)
                size 11
                color "#334155"


