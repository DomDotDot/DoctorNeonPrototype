screen dlc_selection_screen(all_dlcs, is_first_run=False):
    modal True
    
    # Словарь выбора: {id_dlc: True/False}
    # Логика по умолчанию: 
    # Если это первый запуск -> выбрать всё, чего нет.
    # Если это ручной вызов -> ничего не выбирать, ждать действий игрока.
    default selection_map = get_dlc_initial_selection(all_dlcs, is_first_run)

    
    frame:
        xalign 0.5 yalign 0.5
        xsize 1000 ysize 750
        padding (40, 40)
        
        vbox:
            spacing 20
            
            text _("Менеджер контента") size 40 bold True xalign 0.5
            
            if is_first_run:
                text _("Обнаружен первый запуск. Рекомендуется загрузить выбранные файлы.") size 22 color "#aaa" xalign 0.5
            else:
                text _("Управление дополнительными файлами.") size 22 color "#aaa" xalign 0.5

            viewport:
                scrollbars "vertical"
                mousewheel True
                ysize 450
                
                vbox:
                    spacing 10
                    for item in all_dlcs:
                        $ is_inst = is_dlc_installed(item)
                        $ is_selected = selection_map.get(item['id'], False)
                        
                        button:
                            action ToggleDict(selection_map, item['id'])
                            xfill True
                            padding (10, 10)
                            background ("#333" if is_selected else "#111")
                            
                            hbox:
                                spacing 20
                                align (0.0, 0.5)
                                
                                # Чекбокс
                                text (" ✓ " if is_selected else " ☐ ") size 30 color "#fff" font "DejaVuSans.ttf"
                                
                                vbox:
                                    text "[item['title']!t]" size 24 bold True color "#fff"
                                    text "[item['desc']!t]" size 18 color "#ccc"
                                
                                # Статус справа
                                frame:
                                    xalign 1.0
                                    background None
                                    if is_inst:
                                        text _("Установлено") color "#0f0" size 18
                                    else:
                                        text _("Отсутствует") color "#f00" size 18

            null height 20

            hbox:
                xalign 0.5 spacing 50
                
                textbutton _("Начать загрузку") action Return(selection_map) style "button" text_size 28 padding (20, 10)
                
                textbutton _("Закрыть") action Return({}) style "button" text_size 28 padding (20, 10)


# Экран прогресса
screen dlc_progress_screen():
    modal True
    zorder 200

    timer 0.1 repeat True action Function(renpy.restart_interaction)

    frame:
        xalign 0.5 yalign 0.5 padding (50, 50) xsize 800
        background "#000000dd"
        
        vbox:
            spacing 20
            
            if dlc_state["current_item"]:
                text "[dlc_state['current_item']['title']!t]" size 30 bold True xalign 0.5
            
            # Статус текстом
            if dlc_state["phase"] == "init":
                text _("Подготовка...") xalign 0.5
            elif dlc_state["phase"] == "connecting":
                text _("Подключение к серверу...") xalign 0.5
            elif dlc_state["phase"] == "downloading":

                # Форматирование: 12.5 / 120.0 MB
                $ cur_fmt = "{:.1f}".format(dlc_state['mb_cur'])
                $ tot_fmt = "{:.1f}".format(dlc_state['mb_total'])
                text _("Загрузка: [cur_fmt] из [tot_fmt] МБ") xalign 0.5 size 24
            elif dlc_state["phase"] == "unzipping":
                text _("Распаковка и установка...") xalign 0.5 color "#fd0"
            elif dlc_state["phase"] == "done":
                text _("Готово!") xalign 0.5 color "#0f0"
            elif dlc_state["phase"] == "error":
                text _("ОШИБКА") color "#f00" xalign 0.5 size 30
                text "[dlc_state['error_msg']!t]" size 18 xalign 0.5

            # Полоса загрузки
            bar:
                value dlc_state['progress'] 
                range 1.0 
                ysize 30
                left_bar Frame("gui/bar/left.png", 4, 4)
                right_bar Frame("gui/bar/right.png", 4, 4)

            null height 20
            
            # Кнопки управления в процессе
            if dlc_state["phase"] == "error":
                hbox:
                    xalign 0.5 spacing 30
                    textbutton _("Повторить") action Function(start_download_dlc, dlc_state['current_item'])
                    textbutton _("Пропустить") action Return("skip")
            
            elif dlc_state["phase"] == "done":
                timer 1.0 action Return("next")
            
            else:
                textbutton _("Отмена") action Function(cancel_download) xalign 0.5

label dlc_check_sequence:
    
    # 1. Проверяем, первый ли это запуск менеджера DLC
    if persistent.dlc_setup_completed is None:
        $ is_first_time = True
    else:
        $ is_first_time = False

    
    python:
        missing_any = False
        for d in dlc_catalog:
            if not is_dlc_installed(d):
                missing_any = True
                break
            
    if not is_first_time and not missing_any:
        return

    # Вызываем сам процесс
    call dlc_manager_main(is_first_time) from _call_dlc_manager_main
    
    # Отмечаем, что первичная настройка пройдена
    $ persistent.dlc_setup_completed = True
    return

# Главный лейбл менеджера
label dlc_manager_main(first_run=False, is_in_game=False):
    
    # 1. Показать экран выбора
    call screen dlc_selection_screen(dlc_catalog, first_run)
    $ selected_map = _return # Вернет словарь {id: True/False} или None

    if not isinstance(selected_map, dict):
        return

    # 2. Составить очередь загрузки
    python:
        queue = []
        for item in dlc_catalog:
            if selected_map.get(item['id'], False):
                queue.append(item)

    if not queue:
        return

    # 3. Скачивание по очереди
    $ q_len = len(queue)
    $ q_idx = 0
    
    while q_idx < q_len:
        $ item = queue[q_idx]
        
        # Запускаем поток
        $ start_download_dlc(item)
        
        # Показываем экран, пока поток работает
        call screen dlc_progress_screen
        $ res = _return 
        
        # Обработка результата экрана
        # "next" - успешно, идем дальше
        # "skip" - ошибка, пропускаем
        # иначе (отмена) - прерываем всё
        
        if res == "next":
            pass
        elif res == "skip":
            pass
        else:
            # Прервали
            return

        $ q_idx += 1

    # После скачивания всех файлов
    if q_len > 0:
        python:
            if is_in_game:
                # Тихое автосохранение, чтобы мы вернулись в ту же точку
                renpy.save("auto-dlc", "Обновление файлов DLC")
                persistent.dlc_reload_save = "auto-dlc"
                
            renpy.notify(_("Установка завершена. Выполняется перезапуск..."))
            
        $ renpy.pause(2.0, hard=True)
        $ renpy.utter_restart()

    return