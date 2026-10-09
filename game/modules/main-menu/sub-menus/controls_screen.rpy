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
        (_("🧭 Интерфейс и навигация"), ["arrows", "esc", "h"]),
        (_("⚙️ Система и доступность"), ["s", "v", "shift_a"])
    ]

    MOUSE_CATEGORIES = [
        (_("🖱 Основные действия"), ["lmb", "rmb"]),
        (_("⚙️ Колёсико мыши"), ["mmb", "wheelup", "wheeldown"])
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
    xsize 210
    ysize 50
    background Solid("#101726cc")
    hover_background Solid("#1e293bcc")
    selected_idle_background Solid("#005599cc")
    selected_hover_background Solid("#0077bccc")
    hover_sound "audio/sfx/cursor-hover.opus"
    activate_sound "audio/sfx/button-click.opus"
    padding (10, 8)

style controls_tab_btn_text is text:
    size 16
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
        add Solid("#000000cc")

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
                        text _("⌨️ Клавиатура") style "controls_tab_btn_text"

                    button:
                        style "controls_tab_btn"
                        selected (active_controls_device == "mouse")
                        action [SetVariable("active_controls_device", "mouse"), SetVariable("selected_control_key", "lmb"), SetVariable("hovered_control_key", "")]
                        text _("🖱 Мышь") style "controls_tab_btn_text"

                    button:
                        style "controls_tab_btn"
                        selected (active_controls_device == "gamepad")
                        action [SetVariable("active_controls_device", "gamepad"), SetVariable("selected_control_key", "gp_a"), SetVariable("hovered_control_key", "")]
                        text _("🎮 Геймпад") style "controls_tab_btn_text"

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
                        use keyboard_visual(cur_active_key)
                    elif active_controls_device == "mouse":
                        use mouse_visual(cur_active_key)
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

                                    $ categories = KB_CATEGORIES if active_controls_device == "keyboard" else (MOUSE_CATEGORIES if active_controls_device == "mouse" else GP_CATEGORIES)
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


# Выносная интерактивная плашка (Callout Chip) для схем мыши и геймпада
screen controls_callout_chip(kid, badge_text, desc_text, x_pos, y_pos, w, h, cur_key):
    $ is_sel = (cur_key == kid)
    button:
        pos (x_pos, y_pos)
        xsize w
        ysize h
        background (Solid("#00a8ff") if is_sel else Solid("#101a2bdd"))
        hover_background Solid("#00c3ff")
        hover_sound "audio/sfx/cursor-hover.opus"
        activate_sound "audio/sfx/button-click.opus"
        action [SetVariable("selected_control_key", kid), SetVariable("hovered_control_key", kid)]
        hovered SetVariable("hovered_control_key", kid)
        unhovered SetVariable("hovered_control_key", "")
        padding (10, 4)

        hbox:
            align (0.5, 0.5)
            spacing 6
            text badge_text substitute False:
                size 11
                bold True
                color ("#001122" if is_sel else "#38bdf8")
                yalign 0.5
            text desc_text substitute False:
                size 10
                color ("#002244" if is_sel else "#94a3b8")
                yalign 0.5


# Невидимый кликабельный хотспот на теле мыши / геймпада
screen controls_hotspot(kid, x_pos, y_pos, w, h):
    button:
        pos (x_pos, y_pos)
        xsize w
        ysize h
        background None
        hover_background Solid("#00d4ff22")
        hover_sound "audio/sfx/cursor-hover.opus"
        activate_sound "audio/sfx/button-click.opus"
        action [SetVariable("selected_control_key", kid), SetVariable("hovered_control_key", kid)]
        hovered SetVariable("hovered_control_key", kid)
        unhovered SetVariable("hovered_control_key", "")

