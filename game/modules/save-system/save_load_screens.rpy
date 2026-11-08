################################################################################
## Экраны сохранений и загрузки (Save & Load Screens)
## Doctor Neon Prototype — Native Cyber-Glassmorphic Save Architecture
################################################################################

init offset = 2

## Точки входа для Ren'Py #######################################################

screen save():
    tag menu
    use save_load_screen("save")

screen load():
    tag menu
    use save_load_screen("load")


## Основной экран сохранений и загрузки #########################################

screen save_load_screen(mode="load"):

    add gui.main_menu_background
    add Solid("#030712bf")

    # Горячие клавиши навигации по страницам (Q / E + стандартные клавиши Ren'Py)
    key "save_page_prev" action FilePagePrevious(max=9, wrap=False, auto=True, quick=True)
    key "save_page_next" action FilePageNext(max=9, wrap=False, auto=True, quick=True)
    key "K_q" action FilePagePrevious(max=9, wrap=False, auto=True, quick=True)
    key "q" action FilePagePrevious(max=9, wrap=False, auto=True, quick=True)
    key "Q" action FilePagePrevious(max=9, wrap=False, auto=True, quick=True)
    key "K_e" action FilePageNext(max=9, wrap=False, auto=True, quick=True)
    key "e" action FilePageNext(max=9, wrap=False, auto=True, quick=True)
    key "E" action FilePageNext(max=9, wrap=False, auto=True, quick=True)
    key "game_menu" action Return()

    use global_tooltip_display

    frame:
        style "modern_panel_wide"
        xsize 1280
        padding (32, 22)

        vbox:
            spacing 14
            xfill True

            # -----------------------------------------------------------------
            # Шапка: Переключатель режимов (слева) и Навигация страниц (справа)
            # -----------------------------------------------------------------
            hbox:
                xfill True
                yalign 0.5

                # Переключатель «Сохранение / Загрузка»
                hbox:
                    spacing 8
                    yalign 0.5

                    button:
                        style "saveload_mode_btn"
                        selected (mode == "save")
                        sensitive (not main_menu)
                        action ShowMenu("save")
                        tooltip (_("Режим сохранения прогресса") if not main_menu else _("Сохранение доступно только во время игры"))
                        text _("💾 Сохранение") style "saveload_mode_text"

                    button:
                        style "saveload_mode_btn"
                        selected (mode == "load")
                        action ShowMenu("load")
                        tooltip _("Режим загрузки сохранённой игры")
                        text _("📂 Загрузка") style "saveload_mode_text"

                # Полоса страниц: [ ◀ Q ] [ Авто ] [ Быстрые ] [ 1..9 ] [ E ▶ ]
                hbox:
                    xalign 1.0
                    yalign 0.5
                    spacing 5

                    button:
                        style "saveload_page_arrow_btn"
                        action FilePagePrevious(max=9, wrap=False, auto=True, quick=True)
                        tooltip _("Предыдущая страница [[Клавиша Q]]")
                        text "◀ Q" style "saveload_page_arrow_text"

                    if config.has_autosave:
                        button:
                            style "saveload_page_special_btn"
                            action FilePage("auto")
                            tooltip _("Автоматические сохранения")
                            text _("Авто") style "saveload_page_btn_text"

                    if config.has_quicksave:
                        button:
                            style "saveload_page_special_btn"
                            action FilePage("quick")
                            tooltip _("Быстрые сохранения")
                            text _("Быстрые") style "saveload_page_btn_text"

                    for page in range(1, 10):
                        button:
                            style "saveload_page_num_btn"
                            action FilePage(page)
                            tooltip (_("Страница {}") .format(page))
                            text "[page]" style "saveload_page_btn_text"

                    button:
                        style "saveload_page_arrow_btn"
                        action FilePageNext(max=9, wrap=False, auto=True, quick=True)
                        tooltip _("Следующая страница [[Клавиша E]]")
                        text "E ▶" style "saveload_page_arrow_text"

            # Неоновая разделительная линия
            frame:
                xfill True
                ysize 1
                background Solid("#00e5ff33")

            # Подсказка, если открыт режим сохранения на странице «Авто»
            if mode == "save" and FileCurrentPage() == "auto":
                frame:
                    style "saveload_readonly_banner"
                    hbox:
                        spacing 10
                        xalign 0.5
                        yalign 0.5
                        text _("🔒 Автосохранения перезаписываются самой игрой. Выберите страницу 1–9 или «Быстрые» для сохранения."):
                            size 14
                            color "#38bdf8"
                            yalign 0.5

            # -----------------------------------------------------------------
            # Сетка слотов 3 × 2
            # -----------------------------------------------------------------
            grid 3 2:
                spacing 20
                xalign 0.5
                yalign 0.5

                for i in range(6):
                    $ slot = i + 1
                    use save_slot_card(slot, mode)

            # -----------------------------------------------------------------
            # Нижняя панель: Подсказки горячих клавиш, Sync и кнопка «Назад»
            # -----------------------------------------------------------------
            hbox:
                xfill True
                yalign 0.5

                text _("[[ ESC ]] — Выйти    [[ Q / E ]] — Страницы    [[ DEL ]] — Удалить слот"):
                    substitute False
                    size 13
                    color "#64748b"
                    yalign 0.5

                hbox:
                    xalign 1.0
                    yalign 0.5
                    spacing 12

                    if config.has_sync:
                        if mode == "save":
                            textbutton _("☁ Выгрузить Sync"):
                                action UploadSync()
                                style "settings_mini_btn"
                                text_style "settings_mini_btn_text"
                                yalign 0.5
                        else:
                            textbutton _("☁ Скачать Sync"):
                                action DownloadSync()
                                style "settings_mini_btn"
                                text_style "settings_mini_btn_text"
                                yalign 0.5

                    textbutton _("← Назад"):
                        action Return()
                        style "modern_back_button"
                        ysize 40
                        xsize 170
                        text_size 16


## Карточка одного слота сохранения ############################################

screen save_slot_card(slot, mode):
    $ is_loadable = FileLoadable(slot)
    $ is_auto_page = (FileCurrentPage() == "auto")
    $ can_save_here = (mode == "save" and not main_menu and not is_auto_page)

    fixed:
        xsize 388
        ysize 284

        # Основная интерактивная кнопка слота (нативные FileLoad / FileSave)
        button:
            style "saveload_card_btn"
            xfill True
            yfill True
            action (FileLoad(slot) if mode == "load" else FileSave(slot))

            key "save_delete" action FileDelete(slot)

            vbox:
                spacing 6
                xfill True
                yfill True

                # 1. Верхняя строка карточки: номер слота и статус
                hbox:
                    xfill True
                    ysize 22
                    yalign 0.5

                    text get_save_slot_title(slot):
                        style "saveload_slot_badge_text"
                        yalign 0.5

                # 2. Превью скриншота (16:9) или аккуратная заглушка пустого слота
                frame:
                    style "saveload_thumb_frame"
                    xsize 360
                    ysize 186
                    xalign 0.5

                    if is_loadable:
                        add FileScreenshot(slot):
                            size (360, 186)
                            align (0.5, 0.5)
                    else:
                        vbox:
                            align (0.5, 0.5)
                            spacing 4

                            text (_("＋ Свободный слот") if can_save_here else _("Пустой слот")):
                                style "saveload_empty_title_text"

                            if can_save_here:
                                text _("Нажмите, чтобы сохранить"):
                                    style "saveload_empty_sub_text"

                # 3. Подвал карточки: название главы и дата/время
                vbox:
                    spacing 2
                    xfill True

                    if is_loadable:
                        text format_save_slot_chapter(FileSaveName(slot)):
                            style "saveload_chapter_text"

                        text FileTime(slot, format=_("{#file_time}%d.%m.%Y в %H:%M"), empty=""):
                            style "saveload_time_text"
                    else:
                        text (_("Доступно для записи") if can_save_here else _("Нет данных")):
                            style "saveload_chapter_empty_text"

                        text "—":
                            style "saveload_time_text"

        # Кнопка удаления слота (крестик X в правом верхнем углу карточки)
        if is_loadable:
            button:
                style "saveload_delete_btn"
                action FileDelete(slot)
                tooltip _("Удалить сохранение [[Клавиша Delete]]")
                text "X" style "saveload_delete_btn_text"


################################################################################
## Стили Cyber-Glassmorphic Save & Load
################################################################################

style saveload_mode_btn is button:
    background Solid("#121726cc")
    hover_background Solid("#1e293bcc")
    selected_idle_background Solid("#0284c7")
    selected_hover_background Solid("#0369a1")
    insensitive_background Solid("#0f172a66")
    xsize 185
    ysize 40
    padding (12, 6)
    hover_sound "audio/sfx/cursor-hover.opus"
    activate_sound "audio/sfx/button-click.opus"

style saveload_mode_text is text:
    size 15
    bold True
    color "#94a3b8"
    hover_color "#ffffff"
    selected_color "#ffffff"
    insensitive_color "#475569"
    align (0.5, 0.5)

style saveload_page_arrow_btn is button:
    background Solid("#0f172a99")
    hover_background Solid("#1e293bcc")
    insensitive_background Solid("#0f172a44")
    xsize 54
    ysize 38
    padding (6, 4)
    hover_sound "audio/sfx/cursor-hover.opus"
    activate_sound "audio/sfx/button-click.opus"

style saveload_page_arrow_text is text:
    size 13
    bold True
    color "#38bdf8"
    hover_color "#ffffff"
    insensitive_color "#334155"
    align (0.5, 0.5)

style saveload_page_special_btn is button:
    background Solid("#121726cc")
    hover_background Solid("#1e293bcc")
    selected_idle_background Solid("#0284c7")
    selected_hover_background Solid("#0369a1")
    ysize 38
    xminimum 84
    padding (12, 4)
    hover_sound "audio/sfx/cursor-hover.opus"
    activate_sound "audio/sfx/button-click.opus"

style saveload_page_num_btn is button:
    background Solid("#121726cc")
    hover_background Solid("#1e293bcc")
    selected_idle_background Solid("#0284c7")
    selected_hover_background Solid("#0369a1")
    xsize 38
    ysize 38
    padding (4, 4)
    hover_sound "audio/sfx/cursor-hover.opus"
    activate_sound "audio/sfx/button-click.opus"

style saveload_page_btn_text is text:
    size 14
    bold True
    color "#94a3b8"
    hover_color "#ffffff"
    selected_color "#ffffff"
    align (0.5, 0.5)

style saveload_readonly_banner is frame:
    xfill True
    ysize 32
    background Solid("#0c192ecc")
    padding (14, 4)

style saveload_card_btn is button:
    background Frame(Fixed(Solid("#1e293b88"), Solid("#0b111ecc", xmargin=1, ymargin=1), xysize=(100, 100)), 4, 4)
    hover_background Frame(Fixed(Solid("#00e5ffaa"), Solid("#111c30dd", xmargin=2, ymargin=2), xysize=(100, 100)), 4, 4)
    insensitive_background Frame(Fixed(Solid("#1e293b44"), Solid("#080c16aa", xmargin=1, ymargin=1), xysize=(100, 100)), 4, 4)
    padding (14, 10, 14, 10)
    hover_sound "audio/sfx/cursor-hover.opus"
    activate_sound "audio/sfx/button-click.opus"

style saveload_slot_badge_text is text:
    size 13
    bold True
    color "#38bdf8"

style saveload_thumb_frame is frame:
    background Solid("#040812")
    padding (0, 0)

style saveload_empty_title_text is text:
    size 16
    bold True
    color "#475569"
    xalign 0.5
    text_align 0.5

style saveload_empty_sub_text is text:
    size 13
    color "#38bdf899"
    xalign 0.5
    text_align 0.5

style saveload_chapter_text is text:
    size 15
    bold True
    color "#f1f5f9"
    xmaximum 356

style saveload_chapter_empty_text is text:
    size 14
    color "#475569"

style saveload_time_text is text:
    size 12
    color "#94a3b8"

style saveload_delete_btn is button:
    xpos 0.965
    ypos 0.03
    xanchor 1.0
    yanchor 0.0
    xsize 26
    ysize 24
    background Solid("#1e293bcc")
    hover_background Solid("#dc2626")
    padding (0, 0)
    hover_sound "audio/sfx/cursor-hover.opus"
    activate_sound "audio/sfx/button-click.opus"

style saveload_delete_btn_text is text:
    align (0.5, 0.5)
    size 14
    bold True
    color "#cbd5e1"
    hover_color "#ffffff"
