################################################################################
## Экраны сохранений и загрузки (Save & Load Screens)
## Doctor Neon Prototype - Cyber-Glassmorphic Save Architecture
################################################################################

init offset = 2 # Загружается после стандартных экранов

## Точки входа для Ren'Py #######################################################

screen save():
    tag menu
    modal True
    on "show" action [Function(renpy.take_screenshot), SetVariable("save_current_mode", "save"), SetVariable("save_modal_state", None)]
    on "replace" action [Function(renpy.take_screenshot), SetVariable("save_current_mode", "save"), SetVariable("save_modal_state", None)]
    use save_load_core

screen load():
    tag menu
    modal True
    on "show" action [SetVariable("save_current_mode", "load"), SetVariable("save_modal_state", None)]
    on "replace" action [SetVariable("save_current_mode", "load"), SetVariable("save_modal_state", None)]
    use save_load_core


## Основной экран сохранений и загрузки #########################################

screen save_load_core():
    # Вычисление слотов для текущей категории
    $ displayed_slots = []
    if save_selected_category == "manual":
        $ displayed_slots = get_manual_page_slots(save_current_page, count=6)
    elif save_selected_category == "quick":
        $ displayed_slots = get_special_slots("quick", max_slots=10)
    elif save_selected_category == "auto":
        $ displayed_slots = get_special_slots("auto", max_slots=10)
    elif save_selected_category == "recent":
        $ displayed_slots = get_recent_slots(limit=18)

    # Фильтрация по главе (если выбран фильтр)
    $ final_slots = []
    if save_chapter_filter != "all":
        python:
            for s in displayed_slots:
                inf = get_save_slot_info(s)
                if inf and inf.get("chapter_number") == save_chapter_filter:
                    final_slots.append(s)
    else:
        $ final_slots = displayed_slots

    # Автоматическая корректировка выбранного слота
    python:
        if (not save_selected_slot or save_selected_slot not in final_slots) and final_slots:
            save_selected_slot = final_slots[0]
        elif not final_slots:
            save_selected_slot = None

    $ selected_info = get_save_slot_info(save_selected_slot)
    $ known_chapters = get_known_save_chapters()

    ## Глубокий темный фон
    add Solid("#040812f5")

    ## Горячие клавиши
    if save_modal_state:
        key "game_menu" action SetVariable("save_modal_state", None)
    else:
        key "game_menu" action Return()
        key "save_delete" action SmartFileDelete(save_selected_slot)
        if save_selected_category == "manual":
            key "save_page_prev" action SetVariable("save_current_page", max(1, save_current_page - 1))
            key "save_page_next" action SetVariable("save_current_page", min(9, save_current_page + 1))

    frame:
        style "save_main_container"

        vbox:
            spacing 16
            xfill True
            yfill True

            # ==================================================================
            # ШАПКА: Тумблер режимов, категории, фильтры и закрытие
            # ==================================================================
            hbox:
                xfill True
                yalign 0.5

                # 1. Тумблер Режимов: СОХРАНИТЬ | ЗАГРУЗИТЬ
                hbox:
                    spacing 4
                    yalign 0.5

                    # Кнопка "Сохранить" доступна только во время игры
                    button:
                        style "save_mode_toggle_button"
                        selected (save_current_mode == "save")
                        sensitive (not main_menu)
                        action [Function(renpy.take_screenshot), SetVariable("save_current_mode", "save"), SetVariable("save_modal_state", None)]
                        text _("💾 СОХРАНЕНИЕ") style "save_mode_toggle_text"

                    button:
                        style "save_mode_toggle_button"
                        selected (save_current_mode == "load")
                        action [SetVariable("save_current_mode", "load"), SetVariable("save_modal_state", None)]
                        text _("🚀 ЗАГРУЗКА") style "save_mode_toggle_text"

                # 2. Вкладки категорий сохранений
                hbox:
                    xalign 0.5
                    yalign 0.5
                    spacing 8

                    button:
                        style "save_cat_tab_button"
                        selected (save_selected_category == "manual")
                        action [
                            SetVariable("save_selected_category", "manual"),
                            SetVariable("save_selected_slot", None),
                            SetVariable("save_modal_state", None)
                        ]
                        text _("📁 Ручные слоты") style "save_cat_tab_text"

                    button:
                        style "save_cat_tab_button"
                        selected (save_selected_category == "quick")
                        action [
                            SetVariable("save_selected_category", "quick"),
                            SetVariable("save_selected_slot", None),
                            SetVariable("save_modal_state", None)
                        ]
                        text _("⚡ Быстрые") style "save_cat_tab_text"

                    button:
                        style "save_cat_tab_button"
                        selected (save_selected_category == "auto")
                        action [
                            SetVariable("save_selected_category", "auto"),
                            SetVariable("save_selected_slot", None),
                            SetVariable("save_modal_state", None)
                        ]
                        text _("🤖 Автосохранения") style "save_cat_tab_text"

                    button:
                        style "save_cat_tab_button"
                        selected (save_selected_category == "recent")
                        action [
                            SetVariable("save_selected_category", "recent"),
                            SetVariable("save_selected_slot", None),
                            SetVariable("save_modal_state", None)
                        ]
                        text _("⏱ Все недавние") style "save_cat_tab_text"

                # 3. Кнопка возврата / закрытия
                hbox:
                    xalign 1.0
                    yalign 0.5
                    spacing 12

                    if known_chapters:
                        # Селектор фильтрации по главам (циклический выбор)
                        $ filter_label = _("Глава: Все") if save_chapter_filter == "all" else _("Глава: ") + str(save_chapter_filter)
                        textbutton filter_label:
                            style "save_filter_button"
                            action SetVariable("save_chapter_filter", "all" if save_chapter_filter != "all" else (known_chapters[0] if known_chapters else "all"))

                    textbutton _("✕ Закрыть") action Return():
                        style "save_close_button"

            # Тонкая неоновая разделительная линия
            frame:
                xfill True
                ysize 1
                background Solid("#00e5ff33")

            # ==================================================================
            # РАБОЧАЯ ОБЛАСТЬ: Сетка слотов (слева) + Инспектор (справа)
            # ==================================================================
            hbox:
                xfill True
                yfill True
                spacing 24

                # --------------------------------------------------------------
                # ЛЕВАЯ КОЛОНКА: Навигация страниц и сетка слотов
                # --------------------------------------------------------------
                vbox:
                    xsize 1200
                    yfill True
                    spacing 12

                    # Пагинация для ручных слотов
                    if save_selected_category == "manual":
                        hbox:
                            xalign 0.5
                            spacing 6
                            yalign 0.5

                            # Предыдущая страница
                            textbutton _("‹"):
                                style "save_page_nav_btn"
                                sensitive (save_current_page > 1)
                                action [
                                    SetVariable("save_current_page", save_current_page - 1),
                                    SetVariable("save_selected_slot", None),
                                    SetVariable("save_modal_state", None)
                                ]

                            # Кнопки страниц 1..9
                            for p in range(1, 10):
                                button:
                                    style "save_page_num_btn"
                                    selected (save_current_page == p)
                                    action [
                                        SetVariable("save_current_page", p),
                                        SetVariable("save_selected_slot", None),
                                        SetVariable("save_modal_state", None)
                                    ]
                                    text "[p]" style "save_page_num_text"

                            # Следующая страница
                            textbutton _("›"):
                                style "save_page_nav_btn"
                                sensitive (save_current_page < 9)
                                action [
                                    SetVariable("save_current_page", save_current_page + 1),
                                    SetVariable("save_selected_slot", None),
                                    SetVariable("save_modal_state", None)
                                ]

                    # Отображение слотов
                    if save_selected_category == "manual":
                        # Сетка 3x2 для ручных слотов страницы
                        grid 3 2:
                            spacing 16
                            xalign 0.5
                            yalign 0.5

                            for slot_id in final_slots:
                                use save_slot_card(slot_id)

                            # Заполнение пустых мест сетки до 6
                            for pad_idx in range(6 - len(final_slots)):
                                null width 384 height 380
                    else:
                        # Прокручиваемая сетка для Авто / Быстрых / Недавних сохранений
                        if not final_slots:
                            vbox:
                                xalign 0.5
                                yalign 0.5
                                spacing 12
                                null height 100
                                text _("В этой категории пока нет сохранений."):
                                    font gui.text_font
                                    size 24
                                    color "#64748b"
                                    xalign 0.5
                        else:
                            vpgrid:
                                cols 3
                                spacing 16
                                allow_underfull True
                                mousewheel True
                                draggable True
                                scrollbars "vertical"
                                side_spacing 10
                                xfill True
                                yfill True

                                for slot_id in final_slots:
                                    use save_slot_card(slot_id)

                # --------------------------------------------------------------
                # ПРАВАЯ КОЛОНКА: Детализированный Инспектор Сохранения
                # --------------------------------------------------------------
                frame:
                    style "save_inspector_panel"
                    xfill True
                    yfill True

                    use save_inspector_content(save_selected_slot, selected_info, save_current_mode)

    # Реактивный оверлей модальных окон (мгновенное отображение)
    if save_modal_state:
        use save_modal_overlay(save_modal_state)


## Карточка одного слота сохранения ############################################

screen save_slot_card(slot):
    $ info = get_save_slot_info(slot)
    $ is_empty = info["is_empty"]
    $ is_card_selected = (save_selected_slot == slot)

    button:
        style "save_card_button"
        selected is_card_selected
        hover_sound "audio/sfx/cursor-hover.opus"
        activate_sound "audio/sfx/button-click.opus"
        action [
            If(is_card_selected,
               If(save_current_mode == "save",
                  Function(request_slot_save, slot),
                  If(not is_empty, Function(request_slot_load, slot), None)
               ),
               SetVariable("save_selected_slot", slot)
            )
        ]

        vbox:
            spacing 8
            xfill True
            yfill True

            # Верхняя строка карточки: Имя слота + Версия
            hbox:
                xfill True
                yalign 0.5

                text info["slot_label"]:
                    font gui.name_text_font
                    size 17
                    color ("#00e5ff" if is_card_selected else "#cbd5e1")
                    bold True

                if not is_empty:
                    if info["is_version_match"]:
                        frame:
                            style "save_version_badge_ok"
                            text info["version"] style "save_version_badge_text_ok"
                    else:
                        frame:
                            style "save_version_badge_warn"
                            text ("⚠ " + str(info["version"])) style "save_version_badge_text_warn"
                else:
                    text (_("ГОТОВ") if save_current_mode == "save" else _("ПУСТО")):
                        font gui.text_font
                        size 14
                        color ("#38bdf8" if save_current_mode == "save" else "#475569")
                        bold (save_current_mode == "save")

            # Превью скриншота 16:9
            frame:
                style "save_thumbnail_container"
                xsize 354
                ysize 199
                xalign 0.5

                if not is_empty:
                    add FileScreenshot(slot, slot=True):
                        xsize 354
                        ysize 199
                else:
                    if save_current_mode == "save" and not main_menu:
                        # Полупрозрачный снимок текущего кадра для визуального отклика
                        fixed:
                            add FileCurrentScreenshot():
                                xsize 354
                                ysize 199
                                alpha (0.75 if is_card_selected else 0.35)
                            vbox:
                                align (0.5, 0.5)
                                spacing 4
                                text "+":
                                    size 36
                                    color ("#00e5ff" if is_card_selected else "#cbd5e1bb")
                                    xalign 0.5
                                    bold True
                                    outlines [ (1, "#020617ee", 0, 0) ]
                                text (_("Сохранить сюда") if is_card_selected else _("Записать")):
                                    font gui.name_text_font
                                    size 14
                                    color ("#38bdf8" if is_card_selected else "#94a3b8cc")
                                    bold True
                                    xalign 0.5
                                    outlines [ (1, "#020617ee", 0, 0) ]
                    else:
                        vbox:
                            align (0.5, 0.5)
                            spacing 6
                            text "—":
                                size 36
                                color "#334155"
                                xalign 0.5
                            text _("Свободно"):
                                size 16
                                color "#475569"
                                xalign 0.5

            # Нижняя информация карточки: Глава и Дата
            vbox:
                spacing 3
                xfill True

                if not is_empty:
                    text info["full_chapter"]:
                        font gui.name_text_font
                        size 16
                        color "#ffffff"
                        bold True
                        outlines [ (1, "#020617ee", 0, 0) ]

                    hbox:
                        xfill True
                        text info["time_str"]:
                            font gui.text_font
                            size 14
                            color "#94a3b8"

                        text info["runtime_str"]:
                            font gui.text_font
                            size 14
                            color "#00e5ff99"
                            xalign 1.0
                else:
                    if save_current_mode == "save":
                        text (_("Кликните дважды или используйте инспектор") if is_card_selected else _("Кликните для выбора слота")):
                            font gui.text_font
                            size 13
                            color ("#38bdf8" if is_card_selected else "#64748b")
                    else:
                        text _("Слот свободен для записи"):
                            font gui.text_font
                            size 15
                            color "#475569"
                            italic True


## Содержимое правого инспектора сохранения ####################################

screen save_inspector_content(slot, info, mode):
    $ is_empty = info["is_empty"]

    vbox:
        spacing 14
        xfill True
        yfill True

        # Заголовок инспектора
        hbox:
            xfill True
            yalign 0.5

            text (_("ЗАПИСЬ В СЛОТ") if (is_empty and mode == "save") else _("ИНСПЕКТОР СЕЙВА")):
                font gui.name_text_font
                size 20
                color "#00d4ff"
                bold True

            frame:
                if is_empty and mode == "save":
                    style "save_status_badge_ok"
                    text _("ГОТОВ К ЗАПИСИ"):
                        font gui.name_text_font
                        size 13
                        bold True
                        color "#38bdf8"
                elif is_empty:
                    style "save_status_badge_empty"
                    text _("СВОБОДЕН"):
                        font gui.name_text_font
                        size 13
                        bold True
                        color "#94a3b8"
                elif info["is_version_match"]:
                    style "save_status_badge_ok"
                    text _("СОВМЕСТИМО"):
                        font gui.name_text_font
                        size 13
                        bold True
                        color "#00e5a3"
                else:
                    style "save_status_badge_warn"
                    text _("ДРУГАЯ ВЕРСИЯ"):
                        font gui.name_text_font
                        size 13
                        bold True
                        color "#f59e0b"

        frame:
            xfill True
            ysize 1
            background Solid("#30456566")

        # Большое превью скриншота (16:9)
        frame:
            style "save_inspector_preview_frame"
            xsize 560
            ysize 315
            xalign 0.5

            if not is_empty and slot:
                add FileScreenshot(slot, slot=True):
                    xsize 560
                    ysize 315
            else:
                # Вид для пустого слота
                if mode == "save" and not main_menu:
                    fixed:
                        add FileCurrentScreenshot():
                            xsize 560
                            ysize 315

                        frame:
                            align (0.5, 0.90)
                            background Solid("#050c18dd")
                            padding (16, 6)
                            text _("ПРЕВЬЮ: ТЕКУЩИЙ КАДР ДЛЯ СОХРАНЕНИЯ"):
                                font gui.name_text_font
                                size 13
                                bold True
                                color "#00e5ff"
                else:
                    vbox:
                        align (0.5, 0.5)
                        spacing 10
                        text "💾":
                            size 48
                            color "#475569"
                            xalign 0.5
                        text _("Слот свободен для записи"):
                            font gui.name_text_font
                            size 18
                            color "#64748b"
                            xalign 0.5

        # Информационный блок метаданных
        if not is_empty:
            vbox:
                spacing 10
                xfill True

                # Сюжетная глава
                vbox:
                    spacing 2
                    text _("СЮЖЕТ И ГЛАВА:"):
                        font gui.text_font
                        size 12
                        color "#64748b"
                        bold True

                    text info["full_chapter"]:
                        font gui.name_text_font
                        size 19
                        color "#00e5ff"
                        bold True

                # Сетка данных (Версия, Дата, Время)
                grid 2 2:
                    spacing 8
                    xfill True

                    # Версия сборки
                    vbox:
                        spacing 1
                        text _("Версия игры:"):
                            size 12
                            color "#64748b"
                        text info["version"]:
                            size 16
                            color ("#00e5a3" if info["is_version_match"] else "#f59e0b")
                            bold True

                    # Игровое время
                    vbox:
                        spacing 1
                        text _("Время в игре:"):
                            size 12
                            color "#64748b"
                        text info["runtime_str"]:
                            size 16
                            color "#f1f5f9"

                    # Дата сохранения
                    vbox:
                        spacing 1
                        text _("Дата и время:"):
                            size 12
                            color "#64748b"
                        text info["time_str"]:
                            size 15
                            color "#cbd5e1"

                    # Идентификатор слота
                    vbox:
                        spacing 1
                        text _("Идентификатор:"):
                            size 12
                            color "#64748b"
                        text info["slot_label"]:
                            size 15
                            color "#94a3b8"

                # Цитата последнего диалога (если сохранена)
                if info["last_what"]:
                    frame:
                        style "save_dialogue_quote_frame"
                        xfill True

                        vbox:
                            spacing 4
                            if info["last_who"]:
                                text (info["last_who"] + ":"):
                                    font gui.name_text_font
                                    size 14
                                    color "#00e5ff"
                                    bold True

                            text ("«" + str(info["last_what"]) + "»"):
                                font gui.text_font
                                size 14
                                color "#e2e8f0"
                                italic True
                                line_spacing 3

                # Предупреждающая плашка при несовпадении версий
                if not info["is_version_match"]:
                    frame:
                        style "save_warning_callout_frame"
                        xfill True

                        hbox:
                            spacing 10
                            yalign 0.5
                            text "⚠️" size 20 yalign 0.5
                            $ cur_v = str(info["current_version"])
                            text _("Версия сейва отличается от текущей ([cur_v]). При загрузке возможны сбои."):
                                font gui.text_font
                                size 13
                                color "#fcd34d"
                                line_spacing 2
        else:
            # Информация для пустого слота
            if mode == "save":
                vbox:
                    spacing 8
                    xfill True

                    vbox:
                        spacing 2
                        text _("СОХРАНЕНИЕ ТЕКУЩЕГО ПРОГРЕССА:"):
                            font gui.text_font
                            size 12
                            color "#64748b"
                            bold True
                        $ cur_chap_full = str(save_current_chapter_number) + ((" — " + str(save_current_chapter_title)) if save_current_chapter_title else "")
                        text cur_chap_full:
                            font gui.name_text_font
                            size 18
                            color "#38bdf8"
                            bold True

                    grid 2 1:
                        spacing 8
                        xfill True
                        vbox:
                            spacing 1
                            text _("Версия игры:"):
                                size 12
                                color "#64748b"
                            text str(config.version):
                                size 16
                                color "#00e5a3"
                                bold True
                        vbox:
                            spacing 1
                            text _("Выбранный слот:"):
                                size 12
                                color "#64748b"
                            text format_slot_label(slot):
                                size 16
                                color "#00e5ff"
                                bold True
            else:
                vbox:
                    xalign 0.5
                    spacing 8
                    null height 20
                    text _("В этом слоте пока нет данных для загрузки."):
                        font gui.text_font
                        size 16
                        color "#94a3b8"
                        xalign 0.5

        # Отступ перед кнопками
        null height 4

        # Кнопки действий в инспекторе (прижаты к низу)
        vbox:
            yalign 1.0
            spacing 10
            xfill True

            if mode == "load":
                # Режим загрузки
                button:
                    style "save_inspector_action_btn"
                    sensitive (not is_empty and slot is not None)
                    hover_sound "audio/sfx/cursor-hover.opus"
                    activate_sound "audio/sfx/button-click.opus"
                    action SmartFileLoad(slot)
                    text _("🚀 ЗАГРУЗИТЬ СОХРАНЕНИЕ") style "save_inspector_action_text"

                if not is_empty and slot is not None:
                    button:
                        style "save_inspector_danger_btn"
                        hover_sound "audio/sfx/cursor-hover.opus"
                        activate_sound "audio/sfx/button-click.opus"
                        action SmartFileDelete(slot)
                        text _("🗑 Удалить этот сейв") style "save_inspector_danger_text"

            else:
                # Режим сохранения
                button:
                    style "save_inspector_action_btn"
                    sensitive (not main_menu and slot is not None and not str(slot).startswith("auto-"))
                    hover_sound "audio/sfx/cursor-hover.opus"
                    activate_sound "audio/sfx/button-click.opus"
                    action SmartFileSave(slot)
                    text (_("💾 СОХРАНИТЬ В ЭТОТ СЛОТ") if is_empty else _("🔄 ПЕРЕЗАПИСАТЬ СОХРАНЕНИЕ")) style "save_inspector_action_text"

                if not is_empty and slot is not None:
                    button:
                        style "save_inspector_danger_btn"
                        hover_sound "audio/sfx/cursor-hover.opus"
                        activate_sound "audio/sfx/button-click.opus"
                        action SmartFileDelete(slot)
                        text _("🗑 Удалить этот сейв") style "save_inspector_danger_text"


## Реактивное модальное окно (Overlays: Ошибка версий / Перезапись / Удаление) ##

screen save_modal_overlay(m):
    modal True
    zorder 300

    # Затемнение фона с перехватом кликов для отмены
    button:
        style "default"
        xfill True
        yfill True
        background Solid("#020617e6")
        action SetVariable("save_modal_state", None)

    frame:
        style "save_modal_dialog_frame"
        xalign 0.5
        yalign 0.5
        xsize (680 if m.get("type") == "version_warning" else 620)
        padding (32, 28)

        vbox:
            spacing 18
            xfill True

            if m.get("type") == "version_warning":
                # Заголовок предупреждения о версии
                hbox:
                    spacing 14
                    yalign 0.5
                    text "⚠️" size 36
                    text m.get("title", _("НЕСОВПАДЕНИЕ ВЕРСИЙ")):
                        font gui.name_text_font
                        size 24
                        color "#f59e0b"
                        bold True

                frame:
                    xfill True
                    ysize 1
                    background Solid("#f59e0b44")

                vbox:
                    spacing 10
                    xfill True

                    hbox:
                        spacing 12
                        text _("Версия сохранения:"):
                            size 18
                            color "#94a3b8"
                        text str(m.get("save_ver", "")):
                            size 19
                            color "#f59e0b"
                            bold True

                    hbox:
                        spacing 12
                        text _("Текущая версия игры:"):
                            size 18
                            color "#94a3b8"
                        text str(m.get("curr_ver", "")):
                            size 19
                            color "#00e5a3"
                            bold True

                    null height 4

                    text m.get("message", ""):
                        font gui.text_font
                        size 16
                        color "#e2e8f0"
                        line_spacing 4

                frame:
                    xfill True
                    ysize 1
                    background Solid("#f59e0b44")

                hbox:
                    xalign 1.0
                    spacing 16

                    button:
                        style "save_modal_cancel_button"
                        hover_sound "audio/sfx/cursor-hover.opus"
                        activate_sound "audio/sfx/button-click.opus"
                        action SetVariable("save_modal_state", None)
                        text _("Отмена") style "save_modal_cancel_text"

                    button:
                        style "save_modal_confirm_button"
                        hover_sound "audio/sfx/cursor-hover.opus"
                        activate_sound "audio/sfx/button-click.opus"
                        action [SetVariable("save_modal_state", None), Function(execute_slot_load, m.get("slot"))]
                        text _("Загрузить всё равно") style "save_modal_confirm_text"

            else:
                # Обычные подтверждения: Overwrite / Load / Delete
                $ is_danger = m.get("is_danger", False)
                $ m_type = m.get("type", "")

                text m.get("title", ""):
                    font gui.name_text_font
                    size 24
                    color ("#ef4444" if is_danger else "#00e5ff")
                    bold True

                frame:
                    xfill True
                    ysize 1
                    background Solid("#ef444444" if is_danger else "#00e5ff44")

                text m.get("message", ""):
                    font gui.text_font
                    size 18
                    color "#f1f5f9"
                    line_spacing 4

                frame:
                    xfill True
                    ysize 1
                    background Solid("#ef444444" if is_danger else "#00e5ff44")

                hbox:
                    xalign 1.0
                    spacing 16

                    button:
                        style "save_modal_cancel_button"
                        hover_sound "audio/sfx/cursor-hover.opus"
                        activate_sound "audio/sfx/button-click.opus"
                        action SetVariable("save_modal_state", None)
                        text _("Отмена") style "save_modal_cancel_text"

                    button:
                        style ("save_modal_danger_button" if is_danger else "save_modal_confirm_button")
                        hover_sound "audio/sfx/cursor-hover.opus"
                        activate_sound "audio/sfx/button-click.opus"
                        if m_type == "overwrite":
                            action [SetVariable("save_modal_state", None), Function(execute_slot_save, m.get("slot"))]
                            text _("Перезаписать") style "save_modal_confirm_text"
                        elif m_type == "load":
                            action [SetVariable("save_modal_state", None), Function(execute_slot_load, m.get("slot"))]
                            text _("Подтвердить") style "save_modal_confirm_text"
                        elif m_type == "delete":
                            action [SetVariable("save_modal_state", None), Function(execute_slot_delete, m.get("slot"))]
                            text _("Удалить") style "save_modal_confirm_text"
                        else:
                            action SetVariable("save_modal_state", None)
                            text _("ОК") style "save_modal_confirm_text"


## Стили оформления интерфейса сохранений #######################################

style save_main_container is frame:
    xalign 0.5
    yalign 0.5
    xsize 1860
    ysize 1000
    background Frame("gui/textbox.png", 20, 20)
    padding (28, 22, 28, 20)

# Переключатель режимов Сохранение / Загрузка
style save_mode_toggle_button is button:
    xsize 190
    ysize 44
    background Solid("#0b1626cc")
    hover_background Solid("#132845cc")
    selected_idle_background Solid("#0284c7")
    selected_hover_background Solid("#0369a1")
    padding (12, 8)

style save_mode_toggle_text is button_text:
    font gui.name_text_font
    size 17
    bold True
    color "#94a3b8"
    hover_color "#ffffff"
    selected_idle_color "#ffffff"
    selected_hover_color "#ffffff"
    xalign 0.5
    yalign 0.5

# Вкладки категорий
style save_cat_tab_button is button:
    xsize 210
    ysize 44
    background Solid("#071220cc")
    hover_background Solid("#12233acc")
    selected_idle_background Solid("#0e325ecc")
    selected_hover_background Solid("#14447ecc")
    padding (10, 8)

style save_cat_tab_text is button_text:
    font gui.name_text_font
    size 16
    color "#94a3b8"
    hover_color "#ffffff"
    selected_idle_color "#ffffff"
    selected_hover_color "#ffffff"
    xalign 0.5
    yalign 0.5

# Кнопка фильтра
style save_filter_button is button:
    xsize 180
    ysize 44
    background Solid("#0b1626cc")
    hover_background Solid("#1e3a5fcc")
    padding (10, 8)

style save_filter_button_text is button_text:
    font gui.text_font
    size 15
    color "#38bdf8"
    hover_color "#ffffff"
    xalign 0.5
    yalign 0.5

# Кнопка закрытия
style save_close_button is button:
    xsize 140
    ysize 44
    background Solid("#1e293bcc")
    hover_background Solid("#ef4444aa")
    padding (10, 8)

style save_close_button_text is button_text:
    font gui.name_text_font
    size 16
    bold True
    color "#cbd5e1"
    hover_color "#ffffff"
    xalign 0.5
    yalign 0.5

# Навигация по страницам
style save_page_nav_btn is button:
    xsize 44
    ysize 40
    background Solid("#0f172acc")
    hover_background Solid("#1e293bcc")
    insensitive_background Solid("#080d1766")

style save_page_nav_btn_text is button_text:
    font gui.name_text_font
    size 22
    bold True
    color "#38bdf8"
    insensitive_color "#334155"
    xalign 0.5
    yalign 0.5

style save_page_num_btn is button:
    xsize 40
    ysize 40
    background Solid("#0f172acc")
    hover_background Solid("#1e293bcc")
    selected_idle_background Solid("#0284c7")
    selected_hover_background Solid("#0369a1")

style save_page_num_text is button_text:
    font gui.name_text_font
    size 18
    bold True
    color "#94a3b8"
    selected_idle_color "#ffffff"
    selected_hover_color "#ffffff"
    xalign 0.5
    yalign 0.5

# Карточки слотов (с яркой неоновой обводкой при выборе!)
style save_card_button is button:
    xsize 384
    ysize 380
    background Frame(Fixed(Solid("#1e293b66"), Solid("#050c18ee", xmargin=1, ymargin=1), xysize=(100, 100)), 4, 4)
    hover_background Frame(Fixed(Solid("#38bdf8aa"), Solid("#09172eee", xmargin=2, ymargin=2), xysize=(100, 100)), 4, 4)
    selected_idle_background Frame(Fixed(Solid("#00e5ff"), Solid("#0e2444ee", xmargin=2, ymargin=2), xysize=(100, 100)), 4, 4)
    selected_hover_background Frame(Fixed(Solid("#00e5ff"), Solid("#13305aee", xmargin=2, ymargin=2), xysize=(100, 100)), 4, 4)
    padding (14, 12, 14, 12)

style save_thumbnail_container is frame:
    background Solid("#020617")
    padding (0, 0)

# Бейджи версий
style save_version_badge_ok is frame:
    background Solid("#064e3b")
    padding (8, 2, 8, 2)

style save_version_badge_text_ok is text:
    font gui.text_font
    size 12
    bold True
    color "#6ee7b7"

style save_version_badge_warn is frame:
    background Solid("#78350f")
    padding (8, 2, 8, 2)

style save_version_badge_text_warn is text:
    font gui.text_font
    size 12
    bold True
    color "#fcd34d"

# Инспектор справа
style save_inspector_panel is frame:
    background Frame("gui/textbox.png", 20, 20)
    padding (24, 20, 24, 20)

style save_inspector_preview_frame is frame:
    background Solid("#020617")
    padding (0, 0)

style save_status_badge_ok is frame:
    background Solid("#064e3baa")
    padding (10, 4, 10, 4)

style save_status_badge_warn is frame:
    background Solid("#78350faa")
    padding (10, 4, 10, 4)

style save_status_badge_empty is frame:
    background Solid("#1e293baa")
    padding (10, 4, 10, 4)

style save_dialogue_quote_frame is frame:
    background Solid("#0a1628aa")
    padding (14, 10)

style save_warning_callout_frame is frame:
    background Solid("#451a03cc")
    padding (12, 10)

# Кнопки действий инспектора
style save_inspector_action_btn is button:
    xfill True
    ysize 60
    background Solid("#0284c7")
    hover_background Solid("#0369a1")
    insensitive_background Solid("#1e293b66")
    padding (16, 12)

style save_inspector_action_text is button_text:
    font gui.name_text_font
    size 20
    bold True
    color "#ffffff"
    insensitive_color "#475569"
    xalign 0.5
    yalign 0.5

style save_inspector_danger_btn is button:
    xfill True
    ysize 44
    background Solid("#1e293baa")
    hover_background Solid("#b91c1caa")
    padding (10, 8)

style save_inspector_danger_text is button_text:
    font gui.name_text_font
    size 15
    bold True
    color "#f87171"
    hover_color "#ffffff"
    xalign 0.5
    yalign 0.5

# Модальные диалоговые окна
style save_modal_dialog_frame is frame:
    background Frame("gui/textbox.png", 20, 20)

style save_modal_cancel_button is button:
    xsize 150
    ysize 48
    background Solid("#1e293b")
    hover_background Solid("#334155")
    padding (12, 10)

style save_modal_cancel_text is button_text:
    font gui.name_text_font
    size 17
    bold True
    color "#94a3b8"
    hover_color "#ffffff"
    xalign 0.5
    yalign 0.5

style save_modal_confirm_button is button:
    xsize 220
    ysize 48
    background Solid("#0284c7")
    hover_background Solid("#0369a1")
    padding (12, 10)

style save_modal_danger_button is button:
    xsize 180
    ysize 48
    background Solid("#dc2626")
    hover_background Solid("#b91c1c")
    padding (12, 10)

style save_modal_confirm_text is button_text:
    font gui.name_text_font
    size 17
    bold True
    color "#ffffff"
    xalign 0.5
    yalign 0.5
