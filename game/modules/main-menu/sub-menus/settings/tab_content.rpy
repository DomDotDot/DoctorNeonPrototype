################################################################################
## Раздел 3: Доступность, Моды и DLC (Accessibility & Extensibility)
################################################################################

screen settings_tab_content():
    vbox:
        spacing 10
        xfill True

        # Информационная плашка сверху
        frame:
            xfill True
            padding (16, 10)
            background Solid("#181824cc")

            hbox:
                spacing 14
                yalign 0.5
                xfill True

                text "♿" size 24 yalign 0.5
                vbox:
                    yalign 0.5
                    text _("Специальные возможности, Моды и Дополнения:") size 17 bold True color "#ffffff"
                    text _("Управление аппаратными шейдерами, загрузкой модификаций и DLC контентом.") size 13 color "#aaaaaa"

        # Две колонки по 535px
        hbox:
            spacing 20
            xalign 0.5

            # ==================================================================
            # ЛЕВАЯ КОЛОНКА: Доступность и Оптимизация (535px)
            # ==================================================================
            vbox:
                xsize 535
                spacing 10

                # Карточка 1: Производительность и отображение
                frame:
                    style "settings_card"
                    vbox:
                        spacing 8
                        xfill True

                        text _("ОПТИМИЗАЦИЯ И ИНТЕРФЕЙС") size 15 bold True color "#00d4ff"

                        # GPU-анимации
                        button:
                            xfill True
                            ysize 38
                            style "settings_chip_btn"
                            action ToggleField(persistent, "disable_gpu_animations")
                            tooltip _("Выключение тяжелых аппаратных GLSL-шейдеров, шторма лепестков и динамического параллакса.")
                            hbox:
                                xfill True
                                yalign 0.5
                                text _("⚡ GPU-анимации и шейдеры") size 13 color "#e2e8f0" yalign 0.5
                                $ is_no_gpu = bool(getattr(persistent, "disable_gpu_animations", False))
                                frame:
                                    xalign 1.0
                                    yalign 0.5
                                    background (Solid("#ef4444") if is_no_gpu else Solid("#16a34a"))
                                    padding (8, 3)
                                    text (_("✕ ВЫКЛ") if is_no_gpu else _("✓ ВКЛ")):
                                        size 11
                                        bold True
                                        color "#ffffff"

                        # Крупный шрифт
                        button:
                            xfill True
                            ysize 38
                            style "settings_chip_btn"
                            action ToggleField(persistent, "font_size_large")
                            tooltip _("Увеличивает базовый кегль шрифта диалогов для комфортного чтения.")
                            hbox:
                                xfill True
                                yalign 0.5
                                text _("🔍 Крупный шрифт интерфейса") size 13 color "#e2e8f0" yalign 0.5
                                $ is_large_font = bool(getattr(persistent, "font_size_large", False))
                                frame:
                                    xalign 1.0
                                    yalign 0.5
                                    background (Solid("#39ff14") if is_large_font else Solid("#222230"))
                                    padding (8, 3)
                                    text (_("✓ ВКЛ") if is_large_font else _("✕ ВЫКЛ")) size 11 bold True color ("#000000" if is_large_font else "#888888")

                        # Скрыть ачивки
                        button:
                            xfill True
                            ysize 38
                            style "settings_chip_btn"
                            action ToggleField(persistent, "hide_achievement_notifications")
                            tooltip _("Отключает всплывающие уведомления о получении достижений во время игры.")
                            hbox:
                                xfill True
                                yalign 0.5
                                text _("🏆 Скрыть всплывающие ачивки") size 13 color "#e2e8f0" yalign 0.5
                                $ is_hide_ach = bool(getattr(persistent, "hide_achievement_notifications", False))
                                frame:
                                    xalign 1.0
                                    yalign 0.5
                                    background (Solid("#f59e0b") if is_hide_ach else Solid("#222230"))
                                    padding (8, 3)
                                    text (_("СКРЫТЫ") if is_hide_ach else _("ВИДНЫ")) size 11 bold True color ("#000000" if is_hide_ach else "#888888")

                # Карточка 2: Чувствительный контент
                frame:
                    style "settings_card"
                    vbox:
                        spacing 8
                        xfill True

                        text _("ФИЛЬТРЫ КОНТЕНТА") size 15 bold True color "#00d4ff"

                        button:
                            xfill True
                            ysize 38
                            style "settings_chip_btn"
                            action Function(toggle_sensitive_mode_with_check)
                            tooltip _("Включает отображение откровенных и взрослых сцен новеллы.")
                            hbox:
                                xfill True
                                yalign 0.5
                                text _("🔞 Взрослый контент (18+)") size 13 color "#e2e8f0" yalign 0.5
                                frame:
                                    xalign 1.0
                                    yalign 0.5
                                    background (Solid("#f43f5e") if persistent.sensitive_mode else Solid("#222230"))
                                    padding (8, 3)
                                    text (_("ВКЛЮЧЕН") if persistent.sensitive_mode else _("ВЫКЛ")) size 11 bold True color ("#ffffff" if persistent.sensitive_mode else "#888888")

                        button:
                            xfill True
                            ysize 38
                            style "settings_chip_btn"
                            action Function(toggle_ai_sensitive_with_check)
                            tooltip _("Выключение всех изображений с участием ИИ-генерации.")
                            hbox:
                                xfill True
                                yalign 0.5
                                text _("🤖 ИИ-чувствительность") size 13 color "#e2e8f0" yalign 0.5
                                frame:
                                    xalign 1.0
                                    yalign 0.5
                                    background (Solid("#39ff14") if persistent.ai_sensitive_mode else Solid("#222230"))
                                    padding (8, 3)
                                    text (_("✓ ВКЛ") if persistent.ai_sensitive_mode else _("✕ ВЫКЛ")) size 11 bold True color ("#000000" if persistent.ai_sensitive_mode else "#888888")

            # ==================================================================
            # ПРАВАЯ КОЛОНКА: Моды и DLC (535px)
            # ==================================================================
            vbox:
                xsize 535
                spacing 10

                # Карточка 3: Моды и коммьюнити контент
                frame:
                    style "settings_card"
                    vbox:
                        spacing 8
                        xfill True

                        hbox:
                            xfill True
                            yalign 0.5
                            text _("МОДЫ И КОММЬЮНИТИ") size 15 bold True color "#00d4ff"
                            if persistent.community_content_enabled:
                                text _("● Моды активны") size 12 bold True color "#39ff14" yalign 0.5
                            else:
                                text _("○ Моды выключены") size 12 color "#888888" yalign 0.5

                        text _("Включение поддержки пользовательских модификаций, кастомных скриптов и переводов:") size 12 color "#94a3b8"

                        # Тумблер включения/выключения модов
                        button:
                            xfill True
                            ysize 38
                            style "settings_chip_btn"
                            action ToggleField(persistent, "community_content_enabled")
                            tooltip _("Включить или отключить поддержку модов. При включении в главном меню появится значок 🧩.")
                            hbox:
                                xfill True
                                yalign 0.5
                                hbox:
                                    spacing 6
                                    yalign 0.5
                                    text "🧩" size 15 yalign 0.5
                                    text _("Поддержка коммьюнити контента:"):
                                        style "settings_chip_text"
                                        size 12
                                        color ("#39ff14" if persistent.community_content_enabled else "#cbd5e1")
                                frame:
                                    xalign 1.0
                                    yalign 0.5
                                    background (Solid("#39ff14") if persistent.community_content_enabled else Solid("#222230"))
                                    padding (8, 3)
                                    text (_("✓ ВКЛ") if persistent.community_content_enabled else _("✕ ВЫКЛ")):
                                        size 11
                                        bold True
                                        color ("#000000" if persistent.community_content_enabled else "#888888")

                        # Кнопка прямого входа в менеджер модов
                        button:
                            xfill True
                            ysize 44
                            style "settings_chip_btn"
                            background Solid("#1e293b")
                            hover_background Solid("#334155")
                            action ShowMenu("mod_manager_screen")
                            tooltip _("Открыть полноценный менеджер модификаций для установки и настройки модов")
                            hbox:
                                align (0.5, 0.5)
                                spacing 8
                                text "🧩" size 16 yalign 0.5
                                text _("Открыть Менеджер Модов ▶"):
                                    style "settings_chip_text"
                                    size 13
                                    bold True
                                    color "#38bdf8"
                                    yalign 0.5

                # Карточка 4: Менеджер DLC
                frame:
                    style "settings_card"
                    vbox:
                        spacing 8
                        xfill True

                        hbox:
                            xfill True
                            yalign 0.5
                            text _("DLC И ДОПОЛНЕНИЯ") size 15 bold True color "#00d4ff"
                            text _("Официальный контент") size 12 color "#b87107" yalign 0.5

                        text _("Загрузка сюжетных дополнений, артбуков, саундтрека и дополнительных материалов:") size 12 color "#94a3b8"

                        if not renpy.variant("web"):
                            button:
                                xfill True
                                ysize 44
                                style "settings_chip_btn"
                                background Solid("#2a1f14")
                                hover_background Solid("#3d2c1c")
                                action Function(renpy.call_in_new_context, "dlc_manager_main", is_in_game=not main_menu)
                                tooltip _("Запустить официальный менеджер DLC для проверки и загрузки контента")
                                hbox:
                                    align (0.5, 0.5)
                                    spacing 8
                                    text "📦" size 16 yalign 0.5
                                    text _("Открыть Менеджер DLC ▶"):
                                        style "settings_chip_text"
                                        size 13
                                        bold True
                                        color "#fbbf24"
                                        yalign 0.5
                        else:
                            frame:
                                xfill True
                                ysize 40
                                background Solid("#1a1a24")
                                text _("📦 DLC доступны только в версии для ПК") align (0.5, 0.5) size 12 color "#888888"


