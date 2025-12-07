# В options.rpy задай версии

label splashscreen_dlc:
    
    # Запускаем нашу цепочку проверок
    call dlc_manager_flow
    
    return

label dlc_manager_flow:
    python:
        # 1. Собираем список только тех DLC, которые еще НЕ установлены
        uninstalled_dlcs = []
        for item in available_dlcs:
            check_path = os.path.join(config.gamedir, item['check_file'])
            if not os.path.exists(check_path):
                uninstalled_dlcs.append(item)

    # 2. Если устанавливать нечего - выходим
    if not uninstalled_dlcs:
        return

    # 3. Показываем экран выбора и ждем, пока игрок сделает выбор.
    # В _return будет список DLC, которые игрок отметил галочками.
    call screen dlc_selection_screen(uninstalled_dlcs)
    $ download_queue = _return

    # 4. Если игрок нажал "Пропустить всё" или ничего не выбрал - выходим
    if not download_queue:
        return

    # 5. Начинаем скачивать выбранные файлы по очереди
    python:
        # Используем цикл for, это чище, чем renpy-цикл с jump
        for i, dlc_to_download in enumerate(download_queue):
            
            # Готовим переменные для экрана прогресса
            renpy.store.current_dlc_data = dlc_to_download
            
            # Формируем красивый заголовок, например "Загрузка музыки (1 / 3)"
            renpy.store.dl_queue_title = "{} ({} / {})".format(
                dlc_to_download['title'], 
                i + 1, 
                len(download_queue)
            )

            # Запускаем поток скачивания для ТЕКУЩЕГО dlc
            start_download_current()

            # Показываем экран прогресса и ЖДЕМ, пока он не закроется
            # (по кнопке "Далее" или "Пропустить этот пак")
            renpy.call_screen("dlc_progress_screen")

    # 6. Все выбранные DLC скачаны, выходим
    return