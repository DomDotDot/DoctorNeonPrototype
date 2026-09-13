# ==============================================================================
# Doctor Neon - Community Content & Mod Manager Screens
# ==============================================================================

screen mod_manager_screen():
    tag menu
    zorder 50
    modal True

    if main_menu:
        use main_menu_background
    else:
        add Solid("#000000b3")
        
    key "game_menu" action ShowMenu("settings_menu")

    frame:
        style "modern_panel"
        xsize 1180
        padding (35, 30)

        vbox:
            spacing 12
            xfill True

            # Заголовок
            label _("Коммьюнити Контент и Моды") style "modern_title_label"

            # Мастер-тумблер включения/выключения
            frame:
                xfill True
                padding (18, 12)
                background Solid("#181824cc")

                hbox:
                    spacing 20
                    yalign 0.5
                    xfill True

                    vbox:
                        yalign 0.5
                        text _("Поддержка коммьюнити контента:") size 19 bold True color "#ffffff"
                        text _("Включает видимость и загрузку сторонних модификаций и переводов.") size 14 color "#aaaaaa"

                    frame:
                        xalign 1.0
                        yalign 0.5
                        background None
                        if persistent.community_content_enabled:
                            textbutton _("🟢 ВКЛЮЧЕНО (Выключить)"):
                                action Function(disable_community_content)
                                text_size 17
                                text_bold True
                                text_color "#000000"
                                background Solid("#39ff14")
                                hover_background Solid("#55ff44")
                                padding (18, 8)
                        else:
                            textbutton _("⚪ ВЫКЛЮЧЕНО (Включить)"):
                                action Show("community_content_warning_modal")
                                text_size 17
                                text_bold True
                                text_color "#ffffff"
                                background Solid("#444455")
                                hover_background Solid("#666677")
                                padding (18, 8)

            # Контентная область
            if not persistent.community_content_enabled:
                # Режим ВЫКЛЮЧЕН - моды скрыты, отображается информационный баннер
                frame:
                    xfill True
                    ysize 400
                    padding (30, 30)
                    background Solid("#12121acc")

                    vbox:
                        xalign 0.5
                        yalign 0.5
                        spacing 18

                        text "🔒" size 44 xalign 0.5
                        text _("КОММЬЮНИТИ КОНТЕНТ ОТКЛЮЧЕН") size 22 bold True color "#ffaa00" xalign 0.5
                        text _("Сторонние модификации и пользовательские локализации скрыты и не загружаются в память игры.\nЧтобы просмотреть список установленных дополнений и активировать их, включите опцию выше.") size 16 color "#cccccc" text_align 0.5 xalign 0.5

                        null height 10

                        hbox:
                            xalign 0.5
                            spacing 20
                            textbutton _("Включить коммьюнити контент"):
                                action Show("community_content_warning_modal")
                                text_size 19
                                text_bold True
                                text_color "#000000"
                                background Solid("#39ff14")
                                hover_background Solid("#55ff44")
                                padding (22, 10)

                            textbutton _("📁 Открыть папку mods/"):
                                action Function(open_mods_folder)
                                text_size 19
                                text_color "#ffffff"
                                background Solid("#2a2a3a")
                                hover_background Solid("#3a3a4a")
                                padding (22, 10)

            else:
                # Режим ВКЛЮЧЕН - поиск, фильтрация, приоритеты и настройки
                $ all_mods = get_discovered_mods()
                $ filtered_mods = get_filtered_mods()
                $ enabled_count = len(getattr(persistent, "enabled_mods", []))

                # Строка поиска и фильтрации
                frame:
                    xfill True
                    padding (12, 8)
                    background Solid("#141420cc")

                    hbox:
                        spacing 12
                        yalign 0.5
                        xfill True

                        # Кнопка / поле поиска
                        hbox:
                            spacing 6
                            yalign 0.5

                            $ search_btn_text = ("🔍 " + mod_search_query) if mod_search_query else _("🔍 Поиск...")
                            textbutton search_btn_text:
                                action Show("mod_search_modal")
                                text_size 15
                                text_color ("#39ff14" if mod_search_query else "#aaaaaa")
                                background Solid("#222233")
                                hover_background Solid("#333344")
                                padding (12, 6)

                            if mod_search_query:
                                textbutton "✖":
                                    action Function(clear_mod_search_query)
                                    text_size 15
                                    text_color "#ff5555"
                                    background Solid("#332222")
                                    hover_background Solid("#442222")
                                    padding (8, 6)

                        # Фильтры по категориям
                        hbox:
                            spacing 6
                            yalign 0.5

                            textbutton _("Все"):
                                action Function(set_mod_category_filter, "all")
                                text_size 14
                                text_color ("#000000" if mod_category_filter == "all" else "#cccccc")
                                background (Solid("#00d4ff") if mod_category_filter == "all" else Solid("#222233"))
                                padding (10, 6)

                            textbutton _("Переводы"):
                                action Function(set_mod_category_filter, "translation")
                                text_size 14
                                text_color ("#000000" if mod_category_filter == "translation" else "#cccccc")
                                background (Solid("#00d4ff") if mod_category_filter == "translation" else Solid("#222233"))
                                padding (10, 6)

                            textbutton _("Ассеты"):
                                action Function(set_mod_category_filter, "asset_replacement")
                                text_size 14
                                text_color ("#000000" if mod_category_filter == "asset_replacement" else "#cccccc")
                                background (Solid("#00d4ff") if mod_category_filter == "asset_replacement" else Solid("#222233"))
                                padding (10, 6)

                            textbutton _("Модули"):
                                action Function(set_mod_category_filter, "modular")
                                text_size 14
                                text_color ("#000000" if mod_category_filter == "modular" else "#cccccc")
                                background (Solid("#00ffcc") if mod_category_filter == "modular" else Solid("#222233"))
                                padding (10, 6)

                            textbutton _("Активные"):
                                action Function(set_mod_category_filter, "active")
                                text_size 14
                                text_color ("#000000" if mod_category_filter == "active" else "#cccccc")
                                background (Solid("#39ff14") if mod_category_filter == "active" else Solid("#222233"))
                                padding (10, 6)

                        # Сортировка
                        frame:
                            xalign 1.0
                            yalign 0.5
                            background None

                            $ sort_label = _("По приоритету ↓") if mod_sort_mode == "priority" else (_("По имени A-Z") if mod_sort_mode == "name" else _("По автору"))
                            textbutton ("↕ " + sort_label):
                                action Function(cycle_mod_sort_mode)
                                text_size 14
                                text_color "#ffaa00"
                                background Solid("#2a2a38")
                                hover_background Solid("#3a3a48")
                                padding (10, 6)

                # Статистика
                hbox:
                    xfill True
                    text _("Показано: {0} из {1} | Активно: {2}").format(len(filtered_mods), len(all_mods), enabled_count) size 15 color "#888888" yalign 0.5
                    
                    if getattr(persistent, "mod_priorities", None):
                        textbutton _("Сбросить приоритеты к дефолтным"):
                            action Function(reset_mod_priorities)
                            text_size 13
                            text_color "#ffaa00"
                            background None
                            xalign 1.0
                            yalign 0.5

                # Список модов
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    ysize 330

                    if len(filtered_mods) == 0:
                        vbox:
                            xalign 0.5
                            yalign 0.5
                            spacing 12
                            null height 50
                            text "🔍" size 36 xalign 0.5
                            text _("Модификации не найдены.") size 18 color "#ffffff" xalign 0.5
                            text _("Попробуйте изменить запрос поиска или выбранный фильтр.") size 15 color "#888888" xalign 0.5
                    else:
                        vbox:
                            spacing 10
                            xfill True

                            for mod in filtered_mods:
                                $ mod_id = mod["id"]
                                $ is_active = is_mod_enabled(mod_id)
                                $ icon_disp = get_mod_icon_displayable(mod)
                                $ mod_type = mod.get("type", "general")
                                $ cur_priority = get_mod_priority(mod_id)
                                $ has_custom_pri = mod_id in getattr(persistent, "mod_priorities", {})
                                $ has_settings = mod.get("has_settings", False)

                                frame:
                                    xfill True
                                    padding (12, 10)
                                    background (Solid("#1c2233cc") if is_active else Solid("#13131bcc"))

                                    hbox:
                                        spacing 14
                                        yalign 0.5
                                        xfill True

                                        # Управление приоритетом (стрелки ▲ / ▼)
                                        vbox:
                                            xsize 44
                                            yalign 0.5
                                            spacing 1

                                            textbutton "▲":
                                                action Function(adjust_mod_priority, mod_id, 1)
                                                text_size 14
                                                text_color "#39ff14"
                                                background Solid("#1a2a22")
                                                hover_background Solid("#2a4a33")
                                                padding (6, 1)
                                                xalign 0.5
                                                tooltip _("Повысить приоритет")

                                            text str(cur_priority) size 13 bold True color ("#39ff14" if has_custom_pri else "#888888") xalign 0.5 tooltip _("Текущий приоритет загрузки")

                                            textbutton "▼":
                                                action Function(adjust_mod_priority, mod_id, -1)
                                                text_size 14
                                                text_color "#ffaa00"
                                                background Solid("#2a221a")
                                                hover_background Solid("#4a3322")
                                                padding (6, 1)
                                                xalign 0.5
                                                tooltip _("Понизить приоритет")

                                        # Квадратная 1:1 превью-иконка
                                        frame:
                                            xsize 72
                                            ysize 72
                                            padding (2, 2)
                                            background (Solid("#39ff1444") if is_active else Solid("#252533"))

                                            if icon_disp:
                                                add icon_disp xsize 68 ysize 68 fit "contain" xalign 0.5 yalign 0.5
                                            else:
                                                text ("🌐" if mod_type == "translation" else "🧩") size 32 xalign 0.5 yalign 0.5

                                        # Информация о моде
                                        vbox:
                                            spacing 3
                                            xsize 620

                                            hbox:
                                                spacing 10
                                                text mod["name"] size 20 bold True color ("#39ff14" if is_active else "#ffffff")
                                                text ("v" + mod["version"]) size 14 color "#888888" yalign 0.5

                                                # Бейджи типа мода (экранированные для Ren'Py!)
                                                if mod_type == "translation":
                                                    text _("[[ПЕРЕВОД]]") substitute False size 13 bold True color "#00d4ff" yalign 0.5
                                                elif mod_type == "modular":
                                                    text _("[[МОДУЛЬ]]") substitute False size 13 bold True color "#00ffcc" yalign 0.5
                                                elif mod_type == "asset_replacement":
                                                    text _("[[АССЕТЫ]]") substitute False size 13 bold True color "#ffaa00" yalign 0.5
                                                elif mod_type == "script":
                                                    text _("[[СЦЕНАРИЙ]]") substitute False size 13 bold True color "#bb88ff" yalign 0.5
                                                else:
                                                    text _("[[МОД]]") substitute False size 13 bold True color "#aaaaaa" yalign 0.5

                                            text (_("Автор: ") + mod["author"]) size 14 color "#aaaaaa"
                                            
                                            if mod.get("description"):
                                                text mod["description"] size 14 color "#dddddd"

                                        # Правый блок: шестеренка настроек (если есть) и статус активности
                                        hbox:
                                            xalign 1.0
                                            yalign 0.5
                                            spacing 10

                                            # Шестеренка настроек (отображается ТОЛЬКО если мододел включил настройки)
                                            if has_settings:
                                                textbutton "⚙":
                                                    action Show("mod_settings_screen", mod=mod)
                                                    text_size 22
                                                    text_color "#00d4ff"
                                                    background Solid("#182838")
                                                    hover_background Solid("#284868")
                                                    padding (12, 8)
                                                    tooltip _("Настройки модификации")

                                            # Кнопка включения/отключения
                                            if is_active:
                                                textbutton _("АКТИВЕН"):
                                                    action Function(toggle_mod, mod_id)
                                                    text_size 16
                                                    text_bold True
                                                    text_color "#000000"
                                                    background Solid("#39ff14")
                                                    hover_background Solid("#55ff44")
                                                    padding (16, 8)
                                            else:
                                                textbutton _("ОТКЛЮЧЕН"):
                                                    action Function(toggle_mod, mod_id)
                                                    text_size 16
                                                    text_bold True
                                                    text_color "#ffffff"
                                                    background Solid("#333344")
                                                    hover_background Solid("#555566")
                                                    padding (16, 8)

            null height 5

            # Нижняя панель действий
            hbox:
                xalign 0.5
                spacing 25

                textbutton _("📁 Папка модов"):
                    action Function(open_mods_folder)
                    style "modern_button"
                    xsize 230
                    ysize 55
                    text_size 19

                textbutton _("🔄 Обновить список"):
                    action Function(rescan_mods)
                    style "modern_button"
                    xsize 230
                    ysize 55
                    text_size 19

                textbutton _("Назад"):
                    action ShowMenu("settings_menu")
                    style "modern_button"
                    xsize 180
                    ysize 55
                    text_size 19


################################################################################
## Экран настроек отдельного мода (Mod Settings Screen)
################################################################################

screen mod_settings_screen(mod):
    modal True
    zorder 250

    add Solid("#000000cc")

    frame:
        style "modern_panel"
        xsize 880
        padding (35, 30)

        vbox:
            spacing 16
            xfill True

            # Шапка
            hbox:
                spacing 12
                yalign 0.5
                text "⚙" size 26 color "#00d4ff" yalign 0.5
                text (_("Настройки: ") + mod["name"]) size 24 bold True color "#ffffff" yalign 0.5

            $ schema = mod.get("settings_schema") or {}
            $ options = schema.get("options", [])

            if schema.get("description"):
                text schema["description"] size 15 color "#aaaaaa"

            null height 5

            # Список настроек
            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True
                ysize 380

                if len(options) == 0:
                    vbox:
                        xalign 0.5
                        yalign 0.5
                        null height 80
                        text _("У этого мода нет доступных параметров конфигурации.") size 18 color "#888888" xalign 0.5
                else:
                    vbox:
                        spacing 12
                        xfill True

                        for opt in options:
                            $ opt_id = opt.get("id")
                            $ opt_name = opt.get("name", opt_id)
                            $ opt_type = opt.get("type", "toggle")
                            $ opt_desc = opt.get("description", "")
                            $ cur_val = get_mod_setting(mod["id"], opt_id, opt.get("default"))

                            frame:
                                xfill True
                                padding (14, 10)
                                background Solid("#161622cc")

                                hbox:
                                    xfill True
                                    yalign 0.5
                                    spacing 15

                                    # Название и описание
                                    vbox:
                                        xsize 500
                                        spacing 2

                                        text opt_name size 18 bold True color "#ffffff"
                                        if opt_desc:
                                            text opt_desc size 14 color "#aaaaaa"

                                    # Интерактивный контрол в зависимости от типа
                                    frame:
                                        xalign 1.0
                                        yalign 0.5
                                        background None

                                        if opt_type == "toggle":
                                            textbutton ("🟢 ВКЛ" if cur_val else "⚪ ВЫКЛ"):
                                                action Function(toggle_mod_setting, mod["id"], opt_id)
                                                text_size 16
                                                text_bold True
                                                text_color ("#000000" if cur_val else "#ffffff")
                                                background (Solid("#39ff14") if cur_val else Solid("#333344"))
                                                hover_background (Solid("#55ff44") if cur_val else Solid("#444455"))
                                                padding (18, 6)

                                        elif opt_type == "slider":
                                            $ min_v = opt.get("min", 0)
                                            $ max_v = opt.get("max", 100)
                                            $ step_v = opt.get("step", 5)

                                            hbox:
                                                spacing 8
                                                yalign 0.5

                                                textbutton "−":
                                                    action Function(adjust_slider_setting, mod["id"], opt_id, -step_v, min_v, max_v)
                                                    text_size 18
                                                    background Solid("#2a2a3a")
                                                    hover_background Solid("#3a3a4a")
                                                    padding (10, 3)

                                                text str(cur_val) size 16 bold True color "#39ff14" yalign 0.5 xsize 45 text_align 0.5

                                                textbutton "+":
                                                    action Function(adjust_slider_setting, mod["id"], opt_id, step_v, min_v, max_v)
                                                    text_size 18
                                                    background Solid("#2a2a3a")
                                                    hover_background Solid("#3a3a4a")
                                                    padding (10, 3)

                                        elif opt_type == "choice":
                                            $ choices_list = opt.get("choices", [])
                                            $ display_label = cur_val
                                            python:
                                                for c in choices_list:
                                                    if isinstance(c, dict) and c.get("value") == cur_val:
                                                        display_label = c.get("label", cur_val)
                                                        break

                                            textbutton (str(display_label) + " 🔁"):
                                                action Function(cycle_choice_setting, mod["id"], opt_id, choices_list)
                                                text_size 15
                                                text_color "#00d4ff"
                                                background Solid("#1e2a3a")
                                                hover_background Solid("#2e3a4a")
                                                padding (12, 6)

                                        elif opt_type == "input":
                                            textbutton ("« " + str(cur_val) + " » ✏️"):
                                                action Show("mod_text_input_modal", title=_("Изменить: ") + opt_name, current_val=str(cur_val), mod_id=mod["id"], opt_id=opt_id)
                                                text_size 15
                                                text_color "#39ff14"
                                                background Solid("#222230")
                                                hover_background Solid("#333344")
                                                padding (12, 6)

            null height 5

            # Нижняя панель
            hbox:
                xalign 0.5
                spacing 30

                textbutton _("Сбросить по умолчанию"):
                    action Function(reset_mod_settings, mod["id"])
                    text_size 18
                    text_color "#ffaa00"
                    background Solid("#332211")
                    hover_background Solid("#553311")
                    padding (20, 10)

                textbutton _("Закрыть"):
                    action Hide("mod_settings_screen")
                    text_size 18
                    text_color "#ffffff"
                    background Solid("#2a2a3a")
                    hover_background Solid("#3a3a4a")
                    padding (25, 10)

    key "game_menu" action Hide("mod_settings_screen")


################################################################################
## Модальное окно поиска (Search Modal)
################################################################################

screen mod_search_modal():
    modal True
    zorder 350

    add Solid("#000000cc")
    default search_input = mod_search_query

    frame:
        style "modern_panel"
        xsize 620
        padding (35, 30)

        vbox:
            spacing 20
            xalign 0.5

            text _("Поиск модификаций:") size 22 bold True color "#00d4ff" xalign 0.5
            text _("Введите текст для поиска по названию, автору или описанию:") size 15 color "#aaaaaa" xalign 0.5

            frame:
                background Solid("#11111acc")
                padding (15, 10)
                xfill True

                input:
                    value ScreenVariableInputValue("search_input")
                    length 35
                    size 22
                    color "#ffffff"

            hbox:
                spacing 20
                xalign 0.5

                textbutton _("Применить"):
                    action [Function(set_mod_search_query, search_input), Hide("mod_search_modal")]
                    text_size 19
                    text_bold True
                    text_color "#000000"
                    background Solid("#39ff14")
                    hover_background Solid("#55ff44")
                    padding (20, 8)

                textbutton _("Сбросить"):
                    action [Function(clear_mod_search_query), Hide("mod_search_modal")]
                    text_size 19
                    text_color "#ffffff"
                    background Solid("#444455")
                    hover_background Solid("#555566")
                    padding (20, 8)

                textbutton _("Отмена"):
                    action Hide("mod_search_modal")
                    text_size 19
                    text_color "#ffffff"
                    background Solid("#222233")
                    hover_background Solid("#333344")
                    padding (20, 8)

    key "game_menu" action Hide("mod_search_modal")


################################################################################
## Модальное окно текстового ввода настройки (Text Input Modal)
################################################################################

screen mod_text_input_modal(title, current_val, mod_id, opt_id):
    modal True
    zorder 350

    add Solid("#000000cc")
    default input_val = current_val

    frame:
        style "modern_panel"
        xsize 620
        padding (35, 30)

        vbox:
            spacing 20
            xalign 0.5

            text title size 20 bold True color "#00d4ff" xalign 0.5

            frame:
                background Solid("#11111acc")
                padding (15, 10)
                xfill True

                input:
                    value ScreenVariableInputValue("input_val")
                    length 40
                    size 22
                    color "#ffffff"

            hbox:
                spacing 20
                xalign 0.5

                textbutton _("Сохранить"):
                    action [Function(set_mod_setting, mod_id, opt_id, input_val), Hide("mod_text_input_modal")]
                    text_size 19
                    text_bold True
                    text_color "#000000"
                    background Solid("#39ff14")
                    hover_background Solid("#55ff44")
                    padding (20, 8)

                textbutton _("Отмена"):
                    action Hide("mod_text_input_modal")
                    text_size 19
                    text_color "#ffffff"
                    background Solid("#444455")
                    hover_background Solid("#555566")
                    padding (20, 8)

    key "game_menu" action Hide("mod_text_input_modal")


################################################################################
## Модальное окно предупреждения (Warning Modal)
################################################################################

screen community_content_warning_modal():
    modal True
    zorder 300

    add Solid("#000000cc")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 820
        padding (45, 40)
        background Solid("#12121af5")

        vbox:
            spacing 22
            xalign 0.5

            # Заголовок
            hbox:
                xalign 0.5
                spacing 15
                text "⚠️" size 34 yalign 0.5
                text _("ВНИМАНИЕ: СТОРОННИЙ КОНТЕНТ") size 26 bold True color "#ff9900" yalign 0.5

            null height 5

            # Дисклеймер
            vbox:
                spacing 12
                text _("Модификации и коммьюнити-контент создаются сторонними авторами.") size 17 color "#e0e0e0"
                text _("Они могут работать нестабильно, вызывать ошибки, портить файлы сохранений или приводить к вылетам игры.") size 17 color "#e0e0e0"
                text _("Разработчики игры не несут ответственности за работу сторонних модов.") size 17 color "#aaaaaa"
                text _("Используйте пользовательский контент с осторожностью!") size 18 bold True color "#ff5555"

            null height 5

            text _("Вы действительно хотите включить поддержку коммьюнити контента?") size 19 bold True color "#ffffff" xalign 0.5

            null height 10

            # Кнопки выбора
            hbox:
                xalign 0.5
                spacing 40

                textbutton _("Включить"):
                    action [Function(enable_community_content), Hide("community_content_warning_modal")]
                    text_size 20
                    text_bold True
                    text_color "#000000"
                    background Solid("#39ff14")
                    hover_background Solid("#55ff44")
                    padding (30, 12)

                textbutton _("Отмена"):
                    action Hide("community_content_warning_modal")
                    text_size 20
                    text_bold True
                    text_color "#ffffff"
                    background Solid("#444455")
                    hover_background Solid("#666677")
                    padding (30, 12)

    key "game_menu" action Hide("community_content_warning_modal")


################################################################################
## Экраны оверлеев модов (Mod API Overlays)
################################################################################

screen mod_main_menu_overlays():
    zorder 45
    if getattr(persistent, "community_content_enabled", False):
        $ _active_overlays = get_active_mod_overlays(category="main_menu")
        for _ov in _active_overlays:
            if renpy.has_screen(_ov):
                use expression _ov

screen mod_ingame_overlays():
    zorder 75
    if getattr(persistent, "community_content_enabled", False):
        $ _active_ingame = get_active_mod_overlays(category="ingame")
        for _ov in _active_ingame:
            if renpy.has_screen(_ov):
                use expression _ov

init python:
    if "mod_ingame_overlays" not in config.overlay_screens:
        config.overlay_screens.append("mod_ingame_overlays")

