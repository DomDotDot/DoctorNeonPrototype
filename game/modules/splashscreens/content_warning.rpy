# ==============================================================================
# Экран дисклеймера об использовании нейросетей (Cyber-Glassmorphism Redesign)
# ==============================================================================

init python:
    def save_ai_disclaimer_notification():
        title = _("Использование нейросетей (AI)")
        msg = _(
            "Спасибо, что решили познакомиться с моей историей.\n\n"
            "Все фоны, спрайты персонажей и иллюстрации (CG) были созданы с помощью нейросетей (AI). "
            "Сюжет, диалоги, характеры героев и сценарий являются полностью авторской работой. "
            "Музыка проекта распространяется по лицензии Royalty-Free.\n\n"
            "Вы можете в любой момент настроить режим ИИ-чувствительности или режим 18+ в меню настроек игры."
        )
        if hasattr(store, "add_notification"):
            add_notification("ai_disclaimer", title, msg)

screen content_warning():
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
            # 1. Верхний информационный баннер со статусом ИИ
            # ------------------------------------------------------------------
            frame:
                xfill True
                padding (16, 10)
                background Solid("#181824cc")

                hbox:
                    spacing 15
                    yalign 0.5
                    xfill True

                    text "🤖" size 28 yalign 0.5
                    vbox:
                        yalign 0.5
                        spacing 2
                        text _("ИСПОЛЬЗОВАНИЕ НЕЙРОСЕТЕЙ И АВТОРСКИЙ КОНТЕНТ") size 18 bold True color "#00d4ff"
                        text _("Информация об авторстве сценария, визуальных технологиях и лицензиях.") size 13 color "#94a3b8"

                    frame:
                        xalign 1.0
                        yalign 0.5
                        background None
                        if persistent.ai_sensitive_mode:
                            frame:
                                background Solid("#39ff14")
                                padding (12, 6)
                                text _("🤖 ИИ-ЧУВСТВИТЕЛЬНОСТЬ: ВКЛ") size 12 bold True color "#000000"
                        else:
                            frame:
                                background Solid("#0284c7")
                                padding (12, 6)
                                text _("🎨 ИИ-ГРАФИКА: АКТИВНА") size 12 bold True color "#ffffff"

            # ------------------------------------------------------------------
            # 2. Карточка с текстом обращения автора
            # ------------------------------------------------------------------
            frame:
                style "settings_card"
                background Solid("#141420cc")
                padding (18, 12)
                xfill True

                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    xfill True
                    ysize 190

                    vbox:
                        spacing 10
                        xfill True

                        text _("Привет, дорогой игрок!") bold True size 17 color "#ffffff" xalign 0.5

                        text _("""Спасибо, что решили познакомиться с моей историей. Прежде чем вы окунётесь в этот мир, я хочу быть с вами полностью честным.

Я не художник, а в первую очередь рассказчик. У меня в голове родилась история с персонажами, которых я полюбил, и мне безумно хотелось поделиться ею с кем-то ещё. Визуальная новелла показалась мне идеальным форматом для этого.

Чтобы «оживить» мир и героев, я использовал современные технологии — все фоны, спрайты персонажей и иллюстрации (CG) были созданы с помощью нейросетей (AI). Это стало тем самым мостиком, который позволил визуализировать задуманное.

При этом всё остальное — сюжет, диалоги, характеры персонажей и сама идея — это полностью авторская работа, в которую вложена душа.

Музыка в игре распространяется по лицензии Royalty-Free, за что огромная благодарность её авторам. Эта новелла не является коммерческим проектом и создана исключительно из любви к историям.""") text_align 0.5 xalign 0.5 size 13 color "#cbd5e1" layout "subtitle"

                        text _("Спасибо за ваше понимание! Надеюсь, вам понравится путешествие, которое вас ждёт.") bold True size 14 color "#38bdf8" xalign 0.5 text_align 0.5

            # Информационная плашка о сохранении в Центр Уведомлений
            frame:
                background Solid("#18182acc")
                padding (14, 7)
                xfill True
                hbox:
                    spacing 10
                    yalign 0.5
                    text "📧" size 16 yalign 0.5
                    text _("Текст данного обращения автоматически сохранён в Центре Уведомлений главного меню.") size 12 color "#38bdf8" yalign 0.5

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

                    # Тумблер 1: ИИ-чувствительность
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

                    # Тумблер 2: Режим 18+
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

            null height 4

            # ------------------------------------------------------------------
            # 4. Навигация внизу
            # ------------------------------------------------------------------
            hbox:
                spacing 30
                xalign 0.5

                textbutton _("⬅ Назад"):
                    action Return("back")
                    style "modern_button"
                    xsize 260
                    ysize 46
                    text_size 15
                    background Solid("#222230")
                    hover_background Solid("#333348")

                textbutton _("Начать игру ➔"):
                    action Return("start")
                    style "modern_button"
                    xsize 260
                    ysize 46
                    text_size 15
                    background Solid("#059669")
                    hover_background Solid("#10b981")

    key "game_menu" action Return("back")
