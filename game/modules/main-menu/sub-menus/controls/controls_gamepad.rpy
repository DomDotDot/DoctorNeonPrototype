################################################################################
## Модуль визуализации геймпада (Doctor Neon Prototype)
################################################################################

################################################################################
## Визуализатор геймпада (HUD Cyberpunk)
################################################################################

screen gamepad_visual(cur_key):
    frame:
        style "controls_device_frame"
        xfill True
        ysize 560

        vbox:
            spacing 6
            xfill True

            # Заголовок секции геймпада
            hbox:
                xfill True
                yalign 0.5
                text _("ИНТЕРАКТИВНАЯ СХЕМА ГЕЙМПАДА") size 12 bold True color "#64748b"
                if GamepadExists():
                    text _("● Геймпад подключён и готов") size 11 bold True color "#39ff14"
                else:
                    text _("○ Геймпад не обнаружен (Xbox, PlayStation, Switch)") size 11 color "#64748b"

            # Графический HUD геймпада (980 x 480)
            fixed:
                xsize 980
                ysize 480
                xalign 0.5

                # 1. Базовый чертёж геймпада с выносными линиями
                add "gui/controls/gamepad_base.png"

                # 2. Неоновый оверлей активной кнопки
                if cur_key == "gp_lt":
                    add "gui/controls/gp_glow_lt.png"
                elif cur_key == "gp_rt":
                    add "gui/controls/gp_glow_rt.png"
                elif cur_key == "gp_lb":
                    add "gui/controls/gp_glow_lb.png"
                elif cur_key == "gp_rb":
                    add "gui/controls/gp_glow_rb.png"
                elif cur_key == "gp_dpad":
                    add "gui/controls/gp_glow_dpad.png"
                elif cur_key == "gp_lstick":
                    add "gui/controls/gp_glow_lstick.png"
                elif cur_key == "gp_rstick":
                    add "gui/controls/gp_glow_rstick.png"
                elif cur_key == "gp_back":
                    add "gui/controls/gp_glow_back.png"
                elif cur_key == "gp_start":
                    add "gui/controls/gp_glow_start.png"
                elif cur_key == "gp_a":
                    add "gui/controls/gp_glow_a.png"
                elif cur_key == "gp_b":
                    add "gui/controls/gp_glow_b.png"
                elif cur_key == "gp_x":
                    add "gui/controls/gp_glow_x.png"
                elif cur_key == "gp_y":
                    add "gui/controls/gp_glow_y.png"

                # 3. Интерактивные выносные плашки (Callout Chips)
                # Левая сторона
                use controls_callout_chip("gp_lt", "LT / L2", _("Откат назад"), 10, 22, 220, 36, cur_key)
                use controls_callout_chip("gp_lb", "LB / L1", _("Откат назад"), 10, 77, 220, 36, cur_key)
                use controls_callout_chip("gp_back", "⧉ Back", _("Гид / Настройки"), 10, 128, 220, 34, cur_key)
                use controls_callout_chip("gp_dpad", "🞤 D-Pad", _("Навигация"), 10, 172, 220, 36, cur_key)
                use controls_callout_chip("gp_lstick", "🕹 L-Stick", _("Курсор / Выбор"), 10, 287, 220, 36, cur_key)

                # Правая сторона
                use controls_callout_chip("gp_rt", "RT / R2", _("Листание диалога"), 750, 23, 220, 34, cur_key)
                use controls_callout_chip("gp_rb", "RB / R1", _("Вперёд по сюжету"), 750, 78, 220, 34, cur_key)
                use controls_callout_chip("gp_start", "☰ Start", _("Игровое меню"), 750, 114, 220, 32, cur_key)
                use controls_callout_chip("gp_y", "🆈 / △", _("Скрыть интерфейс"), 750, 144, 220, 32, cur_key)
                use controls_callout_chip("gp_x", "🆇 / ◻", _("Пропуск текста"), 750, 184, 220, 32, cur_key)
                use controls_callout_chip("gp_b", "🅱 / ⭘", _("Назад / Меню"), 750, 224, 220, 32, cur_key)
                use controls_callout_chip("gp_a", "🅰 / ✕", _("Выбор / Диалог"), 750, 264, 220, 32, cur_key)
                use controls_callout_chip("gp_rstick", "🕹 R-Stick", _("Прокрутка списков"), 750, 308, 220, 34, cur_key)

                # 4. Физические интерактивные зоны на самом корпусе геймпада
                use controls_hotspot("gp_lt", 345, 55, 48, 42)
                use controls_hotspot("gp_rt", 588, 55, 48, 42)
                use controls_hotspot("gp_lb", 315, 92, 70, 28)
                use controls_hotspot("gp_rb", 595, 92, 70, 28)
                use controls_hotspot("gp_dpad", 305, 175, 70, 70)
                use controls_hotspot("gp_lstick", 385, 275, 60, 60)
                use controls_hotspot("gp_rstick", 535, 275, 60, 60)
                use controls_hotspot("gp_back", 395, 138, 22, 22)
                use controls_hotspot("gp_start", 565, 138, 22, 22)
                use controls_hotspot("gp_y", 627, 172, 26, 26)
                use controls_hotspot("gp_b", 652, 197, 26, 26)
                use controls_hotspot("gp_a", 627, 222, 26, 26)
                use controls_hotspot("gp_x", 602, 197, 26, 26)

                # Кнопка калибровки геймпада
                textbutton _("⚙️ Калибровать геймпад"):
                    action GamepadCalibrate()
                    xalign 0.5
                    ypos 440
                    style "settings_chip_btn"




# Карточка бампера / триггера геймпада
screen gamepad_btn_card(kid, badge_text, desc_text, w, h, cur_key):
    $ is_sel = (cur_key == kid)
    button:
        xsize w
        ysize h
        background (Solid("#00a8ff") if is_sel else Solid("#141e30"))
        hover_background Solid("#00bfff")
        hover_sound "audio/sfx/cursor-hover.opus"
        activate_sound "audio/sfx/button-click.opus"
        action [SetVariable("selected_control_key", kid), SetVariable("hovered_control_key", kid)]
        hovered SetVariable("hovered_control_key", kid)
        unhovered SetVariable("hovered_control_key", "")
        hbox:
            align (0.5, 0.5)
            spacing 6
            text badge_text substitute False:
                size 12
                bold True
                color ("#001122" if is_sel else "#38bdf8")
            text desc_text substitute False:
                size 11
                color ("#002244" if is_sel else "#94a3b8")


# Кнопка действия геймпада (A/B/X/Y)
screen gamepad_action_btn(kid, badge_text, desc_text, tag_color, cur_key):
    $ is_sel = (cur_key == kid)
    button:
        xsize 135
        ysize 44
        background (Solid("#00a8ff") if is_sel else Solid("#141e30"))
        hover_background Solid("#00bfff")
        hover_sound "audio/sfx/cursor-hover.opus"
        activate_sound "audio/sfx/button-click.opus"
        action [SetVariable("selected_control_key", kid), SetVariable("hovered_control_key", kid)]
        hovered SetVariable("hovered_control_key", kid)
        unhovered SetVariable("hovered_control_key", "")
        vbox:
            align (0.5, 0.5)
            spacing 1
            text badge_text substitute False:
                size 12
                bold True
                color ("#001122" if is_sel else tag_color)
                xalign 0.5
            text desc_text substitute False:
                size 10
                color ("#002244" if is_sel else "#94a3b8")
                xalign 0.5


