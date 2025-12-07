label splashscreen_dlc:
    
    call dlc_manager_flow from _call_dlc_manager_flow
    
    return

label dlc_manager_flow:
    python:
        # Список только тех DLC, которые еще НЕ установлены
        uninstalled_dlcs = []
        for item in available_dlcs:
            check_path = os.path.join(config.gamedir, item['check_file'])
            if not os.path.exists(check_path):
                uninstalled_dlcs.append(item)

    # 2. Если устанавливать нечего - выход
    if not uninstalled_dlcs:
        return


    # 3кран выбора
    # В _return будет список DLC, которые игрок отметил галочками.
    call screen dlc_selection_screen(uninstalled_dlcs)
    $ download_queue = _return

    # 4. Если игрок нажал "Пропустить всё" или ничего не выбрал - выход
    if not download_queue:
        return

    # 5. Скачивание файлов по очереди
    python:
        for i, dlc_to_download in enumerate(download_queue):
            
            renpy.store.current_dlc_data = dlc_to_download
            
            # Заголовок:  "Загрузка музыки (1 / 3)"
            renpy.store.dl_seq_current = i + 1
            renpy.store.dl_seq_total = len(download_queue)

            # Поток скачивания для ТЕКУЩЕГО dlc
            start_download_current()

            renpy.call_screen("dlc_progress_screen")
    return