# =============================================================================
# ТРАНСФОРМАЦИИ И ГРАФИЧЕСКИЕ РЕСУРСЫ ДЛЯ ДОСТИЖЕНИЙ
# =============================================================================

# Авторесайз иконки (с сохранением пропорций fit="contain")
transform ach_icon_thumb(w=90, h=90):
    fit "contain"
    xysize (w, h)
    align (0.5, 0.5)

transform ach_icon_locked(w=90, h=90):
    fit "contain"
    xysize (w, h)
    align (0.5, 0.5)
    matrixcolor TintMatrix("#777777") * SaturationMatrix(0.15)

transform ach_toast_appear:
    on show:
        alpha 0.0 yoffset -30
        easein 0.3 alpha 1.0 yoffset 0
    on hide:
        easeout 0.3 alpha 0.0 yoffset -20

# Дефолтные графические заглушки для иконок
image ach_default_icon_unlocked:
    Composite(
        (128, 128),
        (0, 0), Solid("#102538"),
        (4, 4), Solid("#0066cc", xsize=120, ysize=120),
        (8, 8), Solid("#141e2b", xsize=112, ysize=112),
        (0, 0), Text("★", size=70, color="#ffcc00", align=(0.5, 0.5))
    )

image ach_default_icon_locked:
    Composite(
        (128, 128),
        (0, 0), Solid("#18181b"),
        (4, 4), Solid("#333333", xsize=120, ysize=120),
        (8, 8), Solid("#121214", xsize=112, ysize=112),
        (0, 0), Text("🔒", size=50, color="#555555", align=(0.5, 0.5))
    )


# =============================================================================
# ОСНОВНОЙ ЭКРАН ДОСТИЖЕНИЙ (ВКЛАДКА "ВОСПОМИНАНИЯ")
# =============================================================================
screen achievements_screen():
    tag menu
    modal True
    zorder 25

    if main_menu:
        use main_menu_background
    else:
        add Solid("#000000b3")

    key "game_menu" action (ShowMenu("memory_recollection") if main_menu else Return())

    # Фильтр списка
    default current_filter = "all"

    # Получаем актуальную статистику
    $ unlocked_count, total_count, percent_val = get_achievements_stats()

    # Фильтрация списка достижений
    python:
        if current_filter == "all":
            displayed_achievements = achievements_list
        elif current_filter == "unlocked":
            displayed_achievements = [a for a in achievements_list if a.is_unlocked()]
        elif current_filter == "locked":
            displayed_achievements = [a for a in achievements_list if not a.is_unlocked()]
        elif current_filter == "normal":
            displayed_achievements = [a for a in achievements_list if a.ach_type == ACH_TYPE_NORMAL]
        elif current_filter == "hidden":
            displayed_achievements = [a for a in achievements_list if a.ach_type == ACH_TYPE_HIDDEN]
        elif current_filter == "tracking":
            displayed_achievements = [a for a in achievements_list if a.ach_type == ACH_TYPE_TRACKING]
        else:
            displayed_achievements = achievements_list

    frame:
        style "modern_panel_wide"

        vbox:
            style "modern_vbox"
            spacing 15

            # Заголовок
            label _("Достижения") style "modern_title_label" bottom_margin 10

            # Статистика и общий прогресс-бар
            vbox:
                xalign 0.5
                spacing 6

                hbox:
                    xalign 0.5
                    spacing 10
                    text _("Разблокировано:"):
                        size 18
                        color "#aaaaaa"
                    text "[unlocked_count] / [total_count] ([percent_val]%)":
                        size 18
                        bold True
                        color ("#2ea043" if percent_val == 100 else "#ffffff")

                bar:
                    value unlocked_count
                    range (total_count if total_count > 0 else 1)
                    xsize 700
                    ysize 10
                    left_bar Solid("#0066cc")
                    right_bar Solid("#222222")
                    xalign 0.5

            null height 5

            # Панель фильтров
            hbox:
                xalign 0.5
                spacing 10

                textbutton _("Все"):
                    action SetScreenVariable("current_filter", "all")
                    style "ach_filter_button"
                    selected (current_filter == "all")

                textbutton _("Обычные"):
                    action SetScreenVariable("current_filter", "normal")
                    style "ach_filter_button"
                    selected (current_filter == "normal")

                textbutton _("Скрытые"):
                    action SetScreenVariable("current_filter", "hidden")
                    style "ach_filter_button"
                    selected (current_filter == "hidden")

                textbutton _("Прогресс"):
                    action SetScreenVariable("current_filter", "tracking")
                    style "ach_filter_button"
                    selected (current_filter == "tracking")

                textbutton _("Открытые"):
                    action SetScreenVariable("current_filter", "unlocked")
                    style "ach_filter_button"
                    selected (current_filter == "unlocked")

            null height 5

            # Список достижений (Viewport)
            viewport:
                xsize 1100
                ysize 500
                xalign 0.5
                scrollbars "vertical"
                mousewheel True
                draggable True

                vbox:
                    spacing 10
                    xfill True

                    if not displayed_achievements:
                        frame:
                            background None
                            xfill True
                            ysize 200
                            text _("В этой категории нет достижений."):
                                color "#666666"
                                size 22
                                align (0.5, 0.5)

                    for ach in displayed_achievements:
                        $ is_un = ach.is_unlocked()

                        button:
                            style "ach_card_button"
                            action Show("achievement_detail", ach=ach)
                            hover_sound "audio/sfx/cursor-hover.opus"

                            hbox:
                                spacing 18
                                yalign 0.5
                                xfill True

                                # 1. Иконка с авторесайзом
                                frame:
                                    xysize (84, 84)
                                    background Solid("#111115")
                                    padding (0, 0)
                                    yalign 0.5

                                    if is_un:
                                        add ach.get_icon_displayable() at ach_icon_thumb(84, 84)
                                    else:
                                        add ach.get_icon_displayable() at ach_icon_locked(84, 84)

                                # 2. Описание и информация
                                vbox:
                                    yalign 0.5
                                    spacing 4
                                    xfill True

                                    hbox:
                                        spacing 10
                                        yalign 0.5

                                        # Название
                                        text ach.get_display_name():
                                            size 21
                                            bold True
                                            color ("#ffffff" if is_un else "#999999")

                                        # Бейдж типа
                                        if ach.ach_type == ACH_TYPE_HIDDEN:
                                            frame:
                                                background Solid("#66339944")
                                                padding (6, 2)
                                                yalign 0.5
                                                text _("Скрытое") size 13 color "#c8a2c8"
                                        elif ach.ach_type == ACH_TYPE_TRACKING:
                                            frame:
                                                background Solid("#0066cc44")
                                                padding (6, 2)
                                                yalign 0.5
                                                text _("Прогресс") size 13 color "#66a3e0"
                                        else:
                                            frame:
                                                background Solid("#33333344")
                                                padding (6, 2)
                                                yalign 0.5
                                                text _("Обычное") size 13 color "#888888"

                                        # Дата разблокировки
                                        if is_un:
                                            text ach.get_unlock_time_string():
                                                size 13
                                                color "#2ea043"
                                                xalign 1.0
                                                yalign 0.5

                                    # Описание
                                    text ach.get_display_description():
                                        size 15
                                        color ("#cccccc" if is_un else "#666666")

                                    # Для трекинг-ачивок: мини-прогрессбар
                                    if ach.ach_type == ACH_TYPE_TRACKING:
                                        null height 2
                                        hbox:
                                            spacing 10
                                            yalign 0.5

                                            bar:
                                                value ach.get_progress()
                                                range ach.max_progress
                                                xsize 300
                                                ysize 8
                                                left_bar Solid("#0066cc")
                                                right_bar Solid("#222222")
                                                yalign 0.5

                                            text "[ach.get_progress()] / [ach.max_progress]":
                                                size 13
                                                color ("#2ea043" if is_un else "#888888")
                                                yalign 0.5

                                # 3. Статус-значок справа
                                frame:
                                    background None
                                    xsize 40
                                    yalign 0.5
                                    if is_un:
                                        text "✓" size 26 color "#2ea043" align (0.5, 0.5) bold True
                                    else:
                                        text "🔒" size 20 color "#444444" align (0.5, 0.5)

            null height 15

            # Кнопка НАЗАД
            textbutton _("Назад"):
                action (ShowMenu("memory_recollection") if main_menu else Return())
                style "modern_back_button"


# =============================================================================
# МОДАЛЬНОЕ ОКНО ДЕТАЛЬНОГО ПРОСМОТРА ДОСТИЖЕНИЯ
# =============================================================================
screen achievement_detail(ach):
    modal True
    zorder 100

    # Клик вне окна закрывает его
    button:
        xfill True
        yfill True
        action Hide("achievement_detail")

    # Подложка
    add Solid("#000000aa")

    $ is_un = ach.is_unlocked()

    frame:
        align (0.5, 0.5)
        xsize 680
        padding (35, 30)
        background Solid("#141418ee")

        vbox:
            xalign 0.5
            spacing 18

            # Большая иконка с авторесайзом
            frame:
                xalign 0.5
                xysize (160, 160)
                background Solid("#0c0c10")
                padding (0, 0)

                if is_un:
                    add ach.get_icon_displayable() at ach_icon_thumb(160, 160)
                else:
                    add ach.get_icon_displayable() at ach_icon_locked(160, 160)

            # Название
            text ach.get_display_name():
                size 26
                bold True
                xalign 0.5
                text_align 0.5
                color ("#ffffff" if is_un else "#aaaaaa")

            # Тип и статус
            hbox:
                xalign 0.5
                spacing 15

                if ach.ach_type == ACH_TYPE_HIDDEN:
                    text _("Тип: Скрытое") size 16 color "#c8a2c8"
                elif ach.ach_type == ACH_TYPE_TRACKING:
                    text _("Тип: Прогресс") size 16 color "#66a3e0"
                else:
                    text _("Тип: Обычное") size 16 color "#888888"

                text "•" size 16 color "#555555"

                if is_un:
                    text _("Статус: Получено") size 16 color "#2ea043" bold True
                else:
                    text _("Статус: Заблокировано") size 16 color "#888888"

            # Полное описание
            frame:
                background Solid("#1c1c24")
                xfill True
                padding (20, 15)

                vbox:
                    spacing 6
                    text _("Описание / Способ получения:") size 14 color "#888888"
                    text ach.get_display_description():
                        size 17
                        color ("#ffffff" if is_un else "#cccccc")

            # Прогресс (если трекинг)
            if ach.ach_type == ACH_TYPE_TRACKING:
                vbox:
                    xfill True
                    spacing 6

                    hbox:
                        xfill True
                        text _("Текущий прогресс:") size 15 color "#aaaaaa"
                        text "[ach.get_progress()] / [ach.max_progress]" size 15 bold True color "#ffffff" align (1.0, 0.5)

                    bar:
                        value ach.get_progress()
                        range ach.max_progress
                        xfill True
                        ysize 12
                        left_bar Solid("#0066cc")
                        right_bar Solid("#222222")

            # Дата получения
            if is_un and ach.get_unlock_time_string():
                text _("Дата получения: [ach.get_unlock_time_string()]"):
                    size 14
                    color "#2ea043"
                    xalign 0.5

            null height 5

            # Кнопка закрытия
            textbutton _("Закрыть"):
                action Hide("achievement_detail")
                style "modern_button"
                xsize 250
                ysize 50
                xalign 0.5


# =============================================================================
# ВСПЛЫВАЮЩИЙ TOAST ПРИ ПОЛУЧЕНИИ ДОСТИЖЕНИЯ ВО ВРЕМЯ ИГРЫ
# =============================================================================
screen achievement_popup_toast(ach):
    zorder 200

    # Автоматически скрывается через 4 секунды
    timer 4.0 action Hide("achievement_popup_toast")

    frame:
        at ach_toast_appear
        align (0.98, 0.05)
        xsize 440
        ysize 95
        padding (12, 10)
        background Frame(Fixed(Solid("#0066cc"), Solid("#101015", xmargin=2, ymargin=2), xysize=(100,100)), 4, 4)

        hbox:
            spacing 14
            yalign 0.5

            # Иконка
            frame:
                xysize (72, 72)
                background Solid("#1a1a22")
                padding (0, 0)
                yalign 0.5
                add ach.get_icon_displayable() at ach_icon_thumb(72, 72)

            # Текст
            vbox:
                yalign 0.5
                spacing 3
                text _("ДОСТИЖЕНИЕ ПОЛУЧЕНО!") size 14 bold True color "#ffcc00"
                text ach.get_display_name() size 18 bold True color "#ffffff"


# =============================================================================
# СТИЛИ КАРТОЧЕК И ФИЛЬТРОВ ДОСТИЖЕНИЙ
# =============================================================================
style ach_card_button is button:
    background Solid("#00000080")
    hover_background Solid("#ffffff15")
    xfill True
    padding (16, 12)
    ysize 100

style ach_filter_button is button:
    background Solid("#00000099")
    hover_background Solid("#ffffff25")
    selected_background Solid("#0066cc")
    xsize 180
    ysize 40
    padding (10, 5)

style ach_filter_button_text is button_text:
    size 17
    bold True
    xalign 0.5
    yalign 0.5
    color "#aaaaaa"
    hover_color "#ffffff"
    selected_color "#ffffff"
