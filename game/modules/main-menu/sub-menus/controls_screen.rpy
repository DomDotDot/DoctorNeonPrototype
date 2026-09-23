################################################################################
## Интерактивный экран управления (Controls / Help Screen)
## Doctor Neon Prototype
## Glassmorphism UI, интерактивная визуализация клавиатуры, мыши и геймпада,
## двусторонняя подсветка клавиш и карточка-инспектор.
################################################################################

default active_controls_device = "keyboard"
default hovered_control_key = ""
default selected_control_key = "enter"

init -1 python:
    # Словарь со всеми действиями и подсказками
    CONTROLS_INFO = {
        # --- КЛАВИАТУРА ---
        "enter": {
            "title": _("Продвижение диалога и выбор"),
            "badge": "Enter ↵",
            "category": _("Диалог и сюжет"),
            "desc": _("Продвигает диалог вперёд, подтверждает выбранные пункты в меню и вариантах ответа."),
            "device": "keyboard"
        },
        "space": {
            "title": _("Продвижение без выбора"),
            "badge": "Space ␣",
            "category": _("Диалог и сюжет"),
            "desc": _("Быстро листает диалог вперёд, но предотвращает случайный выбор вариантов в меню ответов."),
            "device": "keyboard"
        },
        "ctrl": {
            "title": _("Быстрый пропуск (удержание)"),
            "badge": "Ctrl",
            "category": _("Диалог и сюжет"),
            "desc": _("Удерживайте для ускоренной перемотки уже прочитанного ранее текста диалогов."),
            "device": "keyboard"
        },
        "tab": {
            "title": _("Режим авто-пропуска"),
            "badge": "Tab ↹",
            "category": _("Диалог и сюжет"),
            "desc": _("Включает или выключает непрерывный режим авто-пропуска текста до следующего выбора."),
            "device": "keyboard"
        },
        "pgup": {
            "title": _("Откат назад (Rollback)"),
            "badge": "Page Up",
            "category": _("Диалог и сюжет"),
            "desc": _("Возвращает повествование на предыдущие реплики, если вы случайно пропустили фразу."),
            "device": "keyboard"
        },
        "pgdown": {
            "title": _("Возврат вперёд"),
            "badge": "Page Down",
            "category": _("Диалог и сюжет"),
            "desc": _("Возвращает вперёд по сюжету после использования отката назад."),
            "device": "keyboard"
        },
        "arrows": {
            "title": _("Навигация по интерфейсу"),
            "badge": "▲ ▼ ◄ ►",
            "category": _("Интерфейс и меню"),
            "desc": _("Перемещение курсора и фокуса между кнопками, меню и вариантами сюжетных выборов."),
            "device": "keyboard"
        },
        "esc": {
            "title": _("Игровое меню / Пауза"),
            "badge": "Esc",
            "category": _("Интерфейс и меню"),
            "desc": _("Открывает главное меню паузы (сохранение, загрузка, настройки) или возвращает назад."),
            "device": "keyboard"
        },
        "h": {
            "title": _("Скрыть интерфейс"),
            "badge": "H",
            "category": _("Интерфейс и меню"),
            "desc": _("Скрывает текст диалогов и весь интерфейс, позволяя насладиться фоном или артом."),
            "device": "keyboard"
        },
        "s": {
            "title": _("Снимок экрана (Скриншот)"),
            "badge": "S",
            "category": _("Система"),
            "desc": _("Делает моментальный снимок экрана и сохраняет его в директорию игры."),
            "device": "keyboard"
        },
        "v": {
            "title": _("Синтезатор речи (TTS)"),
            "badge": "V",
            "category": _("Доступность"),
            "desc": _("Включает встроенный синтезатор речи Ren'Py для чтения реплик вслух."),
            "device": "keyboard"
        },
        "shift_a": {
            "title": _("Меню специальных возможностей"),
            "badge": "Shift + A",
            "category": _("Доступность"),
            "desc": _("Открывает расширенные настройки доступности: крупный шрифт, высокий контраст, озвучка."),
            "device": "keyboard"
        },

        # --- МЫШЬ ---
        "lmb": {
            "title": _("Левый клик (ЛКМ)"),
            "badge": "🖱 ЛКМ",
            "category": _("Мышь"),
            "desc": _("Основное действие: продвижение текста диалога, активация кнопок интерфейса и выбор ответов."),
            "device": "mouse"
        },
        "rmb": {
            "title": _("Правый клик (ПКМ)"),
            "badge": "🖱 ПКМ",
            "category": _("Мышь"),
            "desc": _("Открытие меню паузы во время игры или возврат назад из настроек и подменю."),
            "device": "mouse"
        },
        "mmb": {
            "title": _("Клик колёсиком (СКМ)"),
            "badge": "🖱 СКМ",
            "category": _("Мышь"),
            "desc": _("Быстро скрывает диалоговое окно и все элементы пользовательского интерфейса."),
            "device": "mouse"
        },
        "wheelup": {
            "title": _("Колёсико вверх ▲"),
            "badge": "🖱 Колёсико ▲",
            "category": _("Мышь"),
            "desc": _("Откат диалога назад: просмотр предыдущих прочитанных реплик сюжета."),
            "device": "mouse"
        },
        "wheeldown": {
            "title": _("Колёсико вниз ▼"),
            "badge": "🖱 Колёсико ▼",
            "category": _("Мышь"),
            "desc": _("Возврат вперёд по диалогу после выполненного отката назад."),
            "device": "mouse"
        },

        # --- ГЕЙМПАД ---
        "gp_a": {
            "title": _("Действие / Выбор (A / ✕)"),
            "badge": "🅰 / ✕",
            "category": _("Геймпад: Действия"),
            "desc": _("Продвижение диалога, подтверждение действия в меню и выбор сюжетных развилок."),
            "device": "gamepad"
        },
        "gp_b": {
            "title": _("Назад / Меню (B / ⭘)"),
            "badge": "🅱 / ⭘",
            "category": _("Геймпад: Интерфейс"),
            "desc": _("Открытие меню паузы во время игры или возврат в предыдущее меню."),
            "device": "gamepad"
        },
        "gp_x": {
            "title": _("Пропуск диалогов (X / ◻)"),
            "badge": "🆇 / ◻",
            "category": _("Геймпад: Действия"),
            "desc": _("Ускоренная перемотка уже прочитанного текста при удержании кнопки."),
            "device": "gamepad"
        },
        "gp_y": {
            "title": _("Скрыть интерфейс (Y / △)"),
            "badge": "🆈 / △",
            "category": _("Геймпад: Интерфейс"),
            "desc": _("Скрывает текст диалога и все экранные панели для чистого обзора арта."),
            "device": "gamepad"
        },
        "gp_dpad": {
            "title": _("Крестовина (D-Pad)"),
            "badge": "🞤 D-Pad",
            "category": _("Геймпад: Навигация"),
            "desc": _("Точная навигация по кнопкам меню, настройкам и вариантам сюжетного выбора."),
            "device": "gamepad"
        },
        "gp_lstick": {
            "title": _("Левый стик (L-Stick)"),
            "badge": "🕹 L-Stick",
            "category": _("Геймпад: Навигация"),
            "desc": _("Плавная навигация по экранным элементам и перемещение курсора интерфейса."),
            "device": "gamepad"
        },
        "gp_rstick": {
            "title": _("Правый стик (R-Stick)"),
            "badge": "🕹 R-Stick",
            "category": _("Геймпад: Навигация"),
            "desc": _("Прокрутка списков, истории диалогов и журнала событий."),
            "device": "gamepad"
        },
        "gp_lb": {
            "title": _("Левый бампер (LB / L1)"),
            "badge": "LB / L1",
            "category": _("Геймпад: Сюжет"),
            "desc": _("Откат диалога назад на одну или несколько реплик."),
            "device": "gamepad"
        },
        "gp_rb": {
            "title": _("Правый бампер (RB / R1)"),
            "badge": "RB / R1",
            "category": _("Геймпад: Сюжет"),
            "desc": _("Возврат вперёд по диалогу после использования отката назад."),
            "device": "gamepad"
        },
        "gp_lt": {
            "title": _("Левый триггер (LT / L2)"),
            "badge": "LT / L2",
            "category": _("Геймпад: Сюжет"),
            "desc": _("Аналоговый триггер для отката реплик диалога назад во времени."),
            "device": "gamepad"
        },
        "gp_rt": {
            "title": _("Правый триггер (RT / R2)"),
            "badge": "RT / R2",
            "category": _("Геймпад: Действия"),
            "desc": _("Удобное листание диалога указательным пальцем без перемещения кисти."),
            "device": "gamepad"
        },
        "gp_start": {
            "title": _("Кнопка Start (Меню / ☰)"),
            "badge": "Start ☰",
            "category": _("Геймпад: Система"),
            "desc": _("Вызов игрового меню паузы, сохранений, загрузок и настроек."),
            "device": "gamepad"
        },
        "gp_back": {
            "title": _("Кнопка Back (Гид / ⧉)"),
            "badge": "Back ⧉",
            "category": _("Геймпад: Система"),
            "desc": _("Системное меню контроллера и вспомогательные функции Ren'Py."),
            "device": "gamepad"
        },
    }

    # Категории для каталога действий
    KB_CATEGORIES = [
        (_("💬 Диалог и сюжет"), ["enter", "space", "ctrl", "tab", "pgup", "pgdown"]),
        (_("🧭 Интерфейс и навигация"), ["arrows", "esc", "h", "lmb", "rmb", "mmb", "wheelup", "wheeldown"]),
        (_("⚙️ Система и доступность"), ["s", "v", "shift_a"])
    ]

    GP_CATEGORIES = [
        (_("💬 Диалог и действия"), ["gp_a", "gp_rt", "gp_x", "gp_lb", "gp_lt", "gp_rb"]),
        (_("🧭 Навигация и меню"), ["gp_dpad", "gp_lstick", "gp_rstick", "gp_b", "gp_y"]),
        (_("⚙️ Система и калибровка"), ["gp_start", "gp_back"])
    ]

    # Раскладка клавиатуры по рядам (id, надпись, ширина, активна ли)
    KB_ROW1 = [
        ("esc", "Esc", 58, True),
        (None, "", 16, False),
        ("f1", "F1", 45, False), ("f2", "F2", 45, False), ("f3", "F3", 45, False), ("f4", "F4", 45, False),
        (None, "", 16, False),
        ("f5", "F5", 45, False), ("f6", "F6", 45, False), ("f7", "F7", 45, False), ("f8", "F8", 45, False),
        (None, "", 16, False),
        ("f9", "F9", 45, False), ("f10", "F10", 45, False), ("f11", "F11", 45, False), ("f12", "F12", 45, False),
    ]
    KB_ROW2 = [
        ("tilde", "` ~", 42, False),
        ("1", "1", 42, False), ("2", "2", 42, False), ("3", "3", 42, False), ("4", "4", 42, False),
        ("5", "5", 42, False), ("6", "6", 42, False), ("7", "7", 42, False), ("8", "8", 42, False),
        ("9", "9", 42, False), ("0", "0", 42, False), ("minus", "-", 42, False), ("eq", "=", 42, False),
        ("back", "⌫ Back", 82, False)
    ]
    KB_ROW3 = [
        ("tab", "Tab ↹", 68, True),
        ("q", "Q", 42, False), ("w", "W", 42, False), ("e", "E", 42, False), ("r", "R", 42, False),
        ("t", "T", 42, False), ("y", "Y", 42, False), ("u", "U", 42, False), ("i", "I", 42, False),
        ("o", "O", 42, False), ("p", "P", 42, False), ("lb", "[[", 42, False), ("rb", "]", 42, False),
        ("slash", "\\", 48, False)
    ]
    KB_ROW4 = [
        ("caps", "Caps", 78, False),
        ("shift_a", "A", 42, True),
        ("s", "S", 42, True),
        ("d", "D", 42, False), ("f", "F", 42, False), ("g", "G", 42, False),
        ("h", "H", 42, True),
        ("j", "J", 42, False), ("k", "K", 42, False), ("l", "L", 42, False),
        ("semi", ";", 42, False), ("quote", "'", 42, False),
        ("enter", "Enter ↵", 90, True)
    ]
    KB_ROW5 = [
        ("shift_a", "Shift ⇧", 100, True),
        ("z", "Z", 42, False), ("x", "X", 42, False), ("c", "C", 42, False),
        ("v", "V", 42, True),
        ("b", "B", 42, False), ("n", "N", 42, False), ("m", "M", 42, False),
        ("comma", ",", 42, False), ("dot", ".", 42, False), ("qmark", "/", 42, False),
        ("shift_r", "Shift", 108, False)
    ]
    KB_ROW6 = [
        ("ctrl", "Ctrl", 68, True),
        ("win", "⊞", 46, False),
        ("alt", "Alt", 46, False),
        ("space", "─── Space (Пробел) ───", 270, True),
        ("alt_r", "Alt", 46, False),
        ("win_r", "⊞", 46, False),
        ("ctrl_r", "Ctrl", 68, True)
    ]


################################################################################
## Стили экрана управления
################################################################################

style controls_main_panel is frame:
    background Solid("#080c16f2")
    xalign 0.5
    yalign 0.5
    xsize 1660
    ysize 950
    padding (36, 26)
    modal True

style controls_tab_btn is button:
    xsize 300
    ysize 52
    background Solid("#101726cc")
    hover_background Solid("#1e293bcc")
    selected_idle_background Solid("#005599cc")
    selected_hover_background Solid("#0077bccc")
    hover_sound "audio/sfx/cursor-hover.opus"
    activate_sound "audio/sfx/button-click.opus"
    padding (12, 8)

style controls_tab_btn_text is text:
    size 18
    bold True
    color "#94a3b8"
    hover_color "#ffffff"
    selected_color "#ffffff"
    align (0.5, 0.5)

style controls_device_frame is frame:
    background Solid("#0d1322cc")
    padding (18, 16)

style controls_inspector_frame is frame:
    background Solid("#0d172acc")
    padding (20, 16)

style controls_catalog_frame is frame:
    background Solid("#0d1322cc")
    padding (18, 16)

style controls_action_btn is button:
    xfill True
    ysize 52
    background Solid("#131c2ecc")
    hover_background Solid("#1e2c48cc")
    selected_idle_background Solid("#004d80cc")
    selected_hover_background Solid("#0066aacc")
    hover_sound "audio/sfx/cursor-hover.opus"
    activate_sound "audio/sfx/button-click.opus"
    padding (14, 8)


################################################################################
## Главный экран управления (help / controls_screen)
################################################################################

screen controls_screen():
    tag menu
    use help

screen help():
    tag menu
    zorder 25
    modal True

    on "show" action Function(grant_achievement, "novice")
    on "replace" action Function(grant_achievement, "novice")

    if main_menu:
        use main_menu_background
    else:
        use pause_background

    key "game_menu" action (ShowMenu("about_menu") if main_menu else Return())

    # Вычисление активной клавиши для подсветки
    $ cur_active_key = hovered_control_key if hovered_control_key else selected_control_key

    frame:
        style "controls_main_panel"

        vbox:
            spacing 14
            xfill True

            # -----------------------------------------------------------------
            # ВЕРХНЯЯ СТРОКА: Заголовок и переключение режимов ввода
            # -----------------------------------------------------------------
            hbox:
                xfill True
                yalign 0.5

                hbox:
                    spacing 12
                    yalign 0.5
                    text "🎮" size 28 yalign 0.5
                    text _("СХЕМА УПРАВЛЕНИЯ") size 26 bold True color "#00d4ff" yalign 0.5

                hbox:
                    xalign 1.0
                    yalign 0.5
                    spacing 10

                    button:
                        style "controls_tab_btn"
                        selected (active_controls_device == "keyboard")
                        action [SetVariable("active_controls_device", "keyboard"), SetVariable("selected_control_key", "enter"), SetVariable("hovered_control_key", "")]
                        text _("⌨️ Клавиатура и Мышь") style "controls_tab_btn_text"

                    button:
                        style "controls_tab_btn"
                        selected (active_controls_device == "gamepad")
                        action [SetVariable("active_controls_device", "gamepad"), SetVariable("selected_control_key", "gp_a"), SetVariable("hovered_control_key", "")]
                        text _("🎮 Геймпад / Джойстик") style "controls_tab_btn_text"

            # Разделительная неоновая линия
            frame:
                background Solid("#0088cc44")
                xfill True
                ysize 2

            # -----------------------------------------------------------------
            # ЦЕНТРАЛЬНАЯ ОБЛАСТЬ: Устройство (слева) + Каталог действий (справа)
            # -----------------------------------------------------------------
            hbox:
                spacing 20
                xfill True

                # =============================================================
                # ЛЕВАЯ КОЛОНКА (1020px): Визуализатор + Инспектор клавиши
                # =============================================================
                vbox:
                    xsize 1020
                    spacing 12

                    if active_controls_device == "keyboard":
                        use keyboard_mouse_visual(cur_active_key)
                    else:
                        use gamepad_visual(cur_active_key)

                    # Карточка-инспектор текущей клавиши
                    use key_inspector_card(cur_active_key)

                # =============================================================
                # ПРАВАЯ КОЛОНКА (540px): Каталог действий
                # =============================================================
                vbox:
                    xsize 540
                    spacing 8

                    frame:
                        style "controls_catalog_frame"
                        xfill True
                        ysize 740

                        vbox:
                            spacing 10
                            xfill True

                            hbox:
                                xfill True
                                yalign 0.5
                                text _("📋 КАТАЛОГ ДЕЙСТВИЙ") size 15 bold True color "#00d4ff"
                                text _("Наведите для подсветки") size 11 color "#64748b" yalign 0.5

                            frame:
                                background Solid("#0088cc22")
                                xfill True
                                ysize 1

                            viewport:
                                scrollbars "vertical"
                                mousewheel True
                                draggable True
                                pagekeys True
                                xfill True
                                yfill True

                                vbox:
                                    spacing 14
                                    xfill True

                                    $ categories = KB_CATEGORIES if active_controls_device == "keyboard" else GP_CATEGORIES
                                    for cat_title, key_ids in categories:
                                        vbox:
                                            spacing 5
                                            xfill True

                                            text cat_title size 13 bold True color "#38bdf8"

                                            for kid in key_ids:
                                                if kid in CONTROLS_INFO:
                                                    $ item = CONTROLS_INFO[kid]
                                                    $ is_sel = (cur_active_key == kid)
                                                    button:
                                                        style "controls_action_btn"
                                                        selected is_sel
                                                        action [SetVariable("selected_control_key", kid), SetVariable("hovered_control_key", kid)]
                                                        hovered SetVariable("hovered_control_key", kid)
                                                        unhovered SetVariable("hovered_control_key", "")

                                                        hbox:
                                                            xfill True
                                                            yalign 0.5

                                                            vbox:
                                                                spacing 1
                                                                yalign 0.5
                                                                text item["title"] substitute False:
                                                                    size 13
                                                                    bold True
                                                                    color ("#ffffff" if is_sel else "#cbd5e1")
                                                                text item["category"] substitute False:
                                                                    size 10
                                                                    color ("#00d4ff" if is_sel else "#64748b")

                                                            frame:
                                                                xalign 1.0
                                                                yalign 0.5
                                                                background (Solid("#00a8ff") if is_sel else Solid("#1e293b"))
                                                                padding (8, 3)
                                                                text item["badge"] substitute False:
                                                                    size 11
                                                                    bold True
                                                                    color ("#001122" if is_sel else "#94a3b8")

            # -----------------------------------------------------------------
            # НИЖНЯЯ ПАНЕЛЬ: Подсказка и кнопка "Назад"
            # -----------------------------------------------------------------
            hbox:
                xfill True
                yalign 0.5

                hbox:
                    spacing 8
                    yalign 0.5
                    text "💡" size 16 yalign 0.5
                    text _("Нажимайте на клавиши схемы или выбирайте действия из каталога справа для просмотра описания.") size 13 color "#64748b" yalign 0.5

                textbutton _("◀ Назад"):
                    action (ShowMenu("about_menu") if main_menu else Return())
                    style "modern_back_button"
                    xalign 1.0
                    yalign 0.5


################################################################################
## Визуализатор клавиатуры и мыши
################################################################################

screen keyboard_mouse_visual(cur_key):
    frame:
        style "controls_device_frame"
        xfill True
        ysize 560

        vbox:
            spacing 8
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

            # Разделитель между клавиатурой и мышью
            frame:
                background Solid("#1e293b88")
                xfill True
                ysize 1

            # -----------------------------------------------------------------
            # Блок мыши
            # -----------------------------------------------------------------
            vbox:
                spacing 6
                xfill True

                text _("УПРАВЛЕНИЕ МЫШЬЮ") size 12 bold True color "#64748b"

                hbox:
                    spacing 12
                    xalign 0.5

                    # Левая кнопка мыши (ЛКМ)
                    $ is_lmb = (cur_key == "lmb")
                    button:
                        xsize 290
                        ysize 74
                        background (Solid("#00a8ff") if is_lmb else Solid("#141d2f"))
                        hover_background Solid("#00bfff")
                        hover_sound "audio/sfx/cursor-hover.opus"
                        activate_sound "audio/sfx/button-click.opus"
                        action [SetVariable("selected_control_key", "lmb"), SetVariable("hovered_control_key", "lmb")]
                        hovered SetVariable("hovered_control_key", "lmb")
                        unhovered SetVariable("hovered_control_key", "")
                        vbox:
                            align (0.5, 0.5)
                            spacing 2
                            text "🖱 ЛКМ (Левый клик)" size 13 bold True color ("#001122" if is_lmb else "#38bdf8") xalign 0.5
                            text _("Диалог / Выбор / Меню") size 11 color ("#002244" if is_lmb else "#94a3b8") xalign 0.5

                    # Колёсико мыши (СКМ + Прокрутка)
                    vbox:
                        spacing 3
                        xsize 340

                        # Прокрутка вверх
                        $ is_wup = (cur_key == "wheelup")
                        button:
                            xfill True
                            ysize 26
                            background (Solid("#00a8ff") if is_wup else Solid("#162238"))
                            hover_background Solid("#00bfff")
                            hover_sound "audio/sfx/cursor-hover.opus"
                            activate_sound "audio/sfx/button-click.opus"
                            action [SetVariable("selected_control_key", "wheelup"), SetVariable("hovered_control_key", "wheelup")]
                            hovered SetVariable("hovered_control_key", "wheelup")
                            unhovered SetVariable("hovered_control_key", "")
                            text "▲ Прокрутка вверх — Откат назад" size 11 bold True color ("#001122" if is_wup else "#7dd3fc") align (0.5, 0.5)

                        # Клик колёсиком (СКМ)
                        $ is_mmb = (cur_key == "mmb")
                        button:
                            xfill True
                            ysize 26
                            background (Solid("#00a8ff") if is_mmb else Solid("#131d2f"))
                            hover_background Solid("#00bfff")
                            hover_sound "audio/sfx/cursor-hover.opus"
                            activate_sound "audio/sfx/button-click.opus"
                            action [SetVariable("selected_control_key", "mmb"), SetVariable("hovered_control_key", "mmb")]
                            hovered SetVariable("hovered_control_key", "mmb")
                            unhovered SetVariable("hovered_control_key", "")
                            text "⏺ Клик колёсиком (СКМ) — Скрыть UI" size 11 bold True color ("#001122" if is_mmb else "#94a3b8") align (0.5, 0.5)

                        # Прокрутка вниз
                        $ is_wdown = (cur_key == "wheeldown")
                        button:
                            xfill True
                            ysize 26
                            background (Solid("#00a8ff") if is_wdown else Solid("#162238"))
                            hover_background Solid("#00bfff")
                            hover_sound "audio/sfx/cursor-hover.opus"
                            activate_sound "audio/sfx/button-click.opus"
                            action [SetVariable("selected_control_key", "wheeldown"), SetVariable("hovered_control_key", "wheeldown")]
                            hovered SetVariable("hovered_control_key", "wheeldown")
                            unhovered SetVariable("hovered_control_key", "")
                            text "▼ Прокрутка вниз — Вперёд по сюжету" size 11 bold True color ("#001122" if is_wdown else "#7dd3fc") align (0.5, 0.5)

                    # Правая кнопка мыши (ПКМ)
                    $ is_rmb = (cur_key == "rmb")
                    button:
                        xsize 290
                        ysize 74
                        background (Solid("#00a8ff") if is_rmb else Solid("#141d2f"))
                        hover_background Solid("#00bfff")
                        hover_sound "audio/sfx/cursor-hover.opus"
                        activate_sound "audio/sfx/button-click.opus"
                        action [SetVariable("selected_control_key", "rmb"), SetVariable("hovered_control_key", "rmb")]
                        hovered SetVariable("hovered_control_key", "rmb")
                        unhovered SetVariable("hovered_control_key", "")
                        vbox:
                            align (0.5, 0.5)
                            spacing 2
                            text "🖱 ПКМ (Правый клик)" size 13 bold True color ("#001122" if is_rmb else "#38bdf8") xalign 0.5
                            text _("Игровое меню / Назад") size 11 color ("#002244" if is_rmb else "#94a3b8") xalign 0.5


################################################################################
## Визуализатор геймпада
################################################################################

screen gamepad_visual(cur_key):
    frame:
        style "controls_device_frame"
        xfill True
        ysize 560

        vbox:
            spacing 14
            xfill True

            # Верхняя полоса: Триггеры и Бамперы
            vbox:
                spacing 4
                xfill True
                text _("ВЕРХНИЕ ТРИГГЕРЫ И БАМПЕРЫ") size 12 bold True color "#64748b" xalign 0.5

                hbox:
                    spacing 10
                    xalign 0.5

                    # Левый триггер LT
                    use gamepad_btn_card("gp_lt", "LT / L2", _("Откат назад"), 210, 48, cur_key)
                    # Левый бампер LB
                    use gamepad_btn_card("gp_lb", "LB / L1", _("Откат назад"), 210, 48, cur_key)

                    # Центр - Индикатор
                    frame:
                        background Solid("#0a0f1c")
                        xsize 80
                        ysize 48
                        text "🎮" size 24 align (0.5, 0.5)

                    # Правый бампер RB
                    use gamepad_btn_card("gp_rb", "RB / R1", _("Откат вперёд"), 210, 48, cur_key)
                    # Правый триггер RT
                    use gamepad_btn_card("gp_rt", "RT / R2", _("Диалог"), 210, 48, cur_key)

            # Основное тело геймпада
            frame:
                background Solid("#090e1aee")
                padding (24, 18)
                xfill True

                hbox:
                    xfill True
                    yalign 0.5

                    # ЛЕВОЕ КРЫЛО: Крестовина (D-Pad) + Левый стик
                    vbox:
                        xsize 340
                        spacing 12
                        xalign 0.5

                        text _("КРЕСТОВИНА (D-PAD)") size 12 bold True color "#64748b" xalign 0.5

                        # Схема крестовины
                        $ is_dpad = (cur_key == "gp_dpad")
                        button:
                            xsize 220
                            ysize 72
                            xalign 0.5
                            background (Solid("#00a8ff") if is_dpad else Solid("#131e33"))
                            hover_background Solid("#00bfff")
                            hover_sound "audio/sfx/cursor-hover.opus"
                            activate_sound "audio/sfx/button-click.opus"
                            action [SetVariable("selected_control_key", "gp_dpad"), SetVariable("hovered_control_key", "gp_dpad")]
                            hovered SetVariable("hovered_control_key", "gp_dpad")
                            unhovered SetVariable("hovered_control_key", "")
                            vbox:
                                align (0.5, 0.5)
                                spacing 2
                                text "▲ ◄ 🞤 ► ▼" size 16 bold True color ("#001122" if is_dpad else "#38bdf8") xalign 0.5
                                text _("Навигация по меню") size 11 color ("#002244" if is_dpad else "#94a3b8") xalign 0.5

                        # Левый стик
                        $ is_ls = (cur_key == "gp_lstick")
                        button:
                            xsize 220
                            ysize 52
                            xalign 0.5
                            background (Solid("#00a8ff") if is_ls else Solid("#131e33"))
                            hover_background Solid("#00bfff")
                            hover_sound "audio/sfx/cursor-hover.opus"
                            activate_sound "audio/sfx/button-click.opus"
                            action [SetVariable("selected_control_key", "gp_lstick"), SetVariable("hovered_control_key", "gp_lstick")]
                            hovered SetVariable("hovered_control_key", "gp_lstick")
                            unhovered SetVariable("hovered_control_key", "")
                            hbox:
                                align (0.5, 0.5)
                                spacing 8
                                text "🕹" size 18 yalign 0.5
                                vbox:
                                    yalign 0.5
                                    spacing 1
                                    text "L-Stick (Левый стик)" size 12 bold True color ("#001122" if is_ls else "#cbd5e1")
                                    text _("Плавная навигация") size 10 color ("#002244" if is_ls else "#64748b")

                    # ЦЕНТР: Системные кнопки (Back / Start)
                    vbox:
                        xsize 220
                        spacing 14
                        xalign 0.5
                        yalign 0.5

                        text _("СИСТЕМА") size 12 bold True color "#64748b" xalign 0.5

                        $ is_back = (cur_key == "gp_back")
                        button:
                            xsize 180
                            ysize 44
                            xalign 0.5
                            background (Solid("#00a8ff") if is_back else Solid("#152033"))
                            hover_background Solid("#00bfff")
                            hover_sound "audio/sfx/cursor-hover.opus"
                            activate_sound "audio/sfx/button-click.opus"
                            action [SetVariable("selected_control_key", "gp_back"), SetVariable("hovered_control_key", "gp_back")]
                            hovered SetVariable("hovered_control_key", "gp_back")
                            unhovered SetVariable("hovered_control_key", "")
                            text "⧉ Back / Guide" size 12 bold True color ("#001122" if is_back else "#94a3b8") align (0.5, 0.5)

                        $ is_start = (cur_key == "gp_start")
                        button:
                            xsize 180
                            ysize 44
                            xalign 0.5
                            background (Solid("#00a8ff") if is_start else Solid("#152033"))
                            hover_background Solid("#00bfff")
                            hover_sound "audio/sfx/cursor-hover.opus"
                            activate_sound "audio/sfx/button-click.opus"
                            action [SetVariable("selected_control_key", "gp_start"), SetVariable("hovered_control_key", "gp_start")]
                            hovered SetVariable("hovered_control_key", "gp_start")
                            unhovered SetVariable("hovered_control_key", "")
                            text "☰ Start / Menu" size 12 bold True color ("#001122" if is_start else "#94a3b8") align (0.5, 0.5)

                    # ПРАВОЕ КРЫЛО: Кнопки действий (A/B/X/Y) + Правый стик
                    vbox:
                        xsize 340
                        spacing 8
                        xalign 0.5

                        text _("КНОПКИ ДЕЙСТВИЙ") size 12 bold True color "#64748b" xalign 0.5

                        # Ромб кнопок A/B/X/Y
                        grid 2 2:
                            xalign 0.5
                            spacing 6

                            # X / ◻
                            use gamepad_action_btn("gp_x", "🆇 / ◻", _("Пропуск"), "#38bdf8", cur_key)
                            # Y / △
                            use gamepad_action_btn("gp_y", "🆈 / △", _("Скрыть UI"), "#facc15", cur_key)
                            # A / ✕
                            use gamepad_action_btn("gp_a", "🅰 / ✕", _("Выбор / Диалог"), "#4ade80", cur_key)
                            # B / ⭘
                            use gamepad_action_btn("gp_b", "🅱 / ⭘", _("Назад / Меню"), "#f87171", cur_key)

                        null height 2

                        # Правый стик
                        $ is_rs = (cur_key == "gp_rstick")
                        button:
                            xsize 240
                            ysize 52
                            xalign 0.5
                            background (Solid("#00a8ff") if is_rs else Solid("#131e33"))
                            hover_background Solid("#00bfff")
                            hover_sound "audio/sfx/cursor-hover.opus"
                            activate_sound "audio/sfx/button-click.opus"
                            action [SetVariable("selected_control_key", "gp_rstick"), SetVariable("hovered_control_key", "gp_rstick")]
                            hovered SetVariable("hovered_control_key", "gp_rstick")
                            unhovered SetVariable("hovered_control_key", "")
                            hbox:
                                align (0.5, 0.5)
                                spacing 8
                                text "🕹" size 18 yalign 0.5
                                vbox:
                                    yalign 0.5
                                    spacing 1
                                    text "R-Stick (Правый стик)" size 12 bold True color ("#001122" if is_rs else "#cbd5e1")
                                    text _("Прокрутка списков") size 10 color ("#002244" if is_rs else "#64748b")

            # Нижняя полоса геймпада: Калибровка и статус подключения
            hbox:
                xfill True
                yalign 0.5

                if GamepadExists():
                    text _("● Геймпад подключён и активен") size 12 bold True color "#39ff14" yalign 0.5
                else:
                    text _("○ Геймпад не обнаружен (поддерживаются Xbox, PlayStation, Switch и DirectInput)") size 12 color "#64748b" yalign 0.5

                textbutton _("⚙️ Калибровать геймпад"):
                    action GamepadCalibrate()
                    xalign 1.0
                    yalign 0.5
                    style "settings_chip_btn"


################################################################################
## Карточка-инспектор текущей клавиши
################################################################################

screen key_inspector_card(cur_key):
    frame:
        style "controls_inspector_frame"
        xfill True
        ysize 150

        $ cur_info = CONTROLS_INFO.get(cur_key, CONTROLS_INFO["enter"])

        vbox:
            spacing 6
            xfill True
            yalign 0.5

            # Верхняя строка бейджей
            hbox:
                spacing 10
                yalign 0.5

                # Бейдж названия клавиши
                frame:
                    background Solid("#004488")
                    padding (12, 4)
                    text cur_info["badge"] substitute False:
                        size 16
                        bold True
                        color "#00f0ff"

                # Бейдж категории
                frame:
                    background Solid("#1e293b")
                    padding (10, 4)
                    text cur_info["category"] substitute False:
                        size 12
                        bold True
                        color "#94a3b8"

                # Бейдж устройства
                $ dev_name = _("Клавиатура") if cur_info["device"] == "keyboard" else (_("Мышь") if cur_info["device"] == "mouse" else _("Геймпад"))
                frame:
                    background Solid("#111827")
                    padding (10, 4)
                    text dev_name substitute False:
                        size 12
                        color "#64748b"

            # Название действия
            text cur_info["title"] substitute False:
                size 18
                bold True
                color "#ffffff"

            # Подробное пояснение
            text cur_info["desc"] substitute False:
                size 13
                color "#cbd5e1"


################################################################################
## Вспомогательные компоненты
################################################################################

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
