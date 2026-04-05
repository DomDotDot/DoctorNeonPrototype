label splashscreen:
    
    # Автоподгрузка при перезапуске после скачивания файлов DLC
    if getattr(persistent, "dlc_reload_save", None):
        $ save_name = persistent.dlc_reload_save
        $ persistent.dlc_reload_save = None
        $ renpy.load(save_name)

    # -----------------------------------------------------------
    # 1. ТЕХНИЧЕСКИЕ ПРОВЕРКИ (На черном фоне)
    # -----------------------------------------------------------
    scene black
    
    # Сначала проверяем обновления (если у вас есть эта функция)
    if hasattr(store, 'check_for_updates'):
        $ check_for_updates()

    $ renpy.pause(0.5, hard=True)

    # -----------------------------------------------------------
    # 2. ПОКАЗ ЛОГОТИПОВ (ЕДИНАЯ ЗАСТАВКА)
    # -----------------------------------------------------------
    call _intro_splash_sequence from _call__intro_splash_sequence


    # -----------------------------------------------------------
    # 3. НАСТРОЙКИ ПРИ ПЕРВОМ ЗАПУСКЕ (ИЛИ ОБНОВЛЕНИИ)
    # -----------------------------------------------------------
    
    # Если версия изменилась или это первый запуск
    if persistent.last_run_version != config.version:
        
        # Сброс флага "видел сплэш", чтобы игрок увидел новые дисклеймеры/логотипы
        $ persistent.seen_splash = False
        
        # Сбрасываем проверку DLC, чтобы модули заново инициализировались если надо
        $ persistent.dlc_setup_completed = None
        
        # Обновляем записанную версию
        $ persistent.last_run_version = config.version
        
        # Если это совсем первый запуск (или переход со старой версии без этого флага)
        if persistent.firstlaunch:
            # Выбор языка (если есть такой экран)
            if renpy.has_screen("language_selection_screen"):
                call screen language_selection_screen
            $ persistent.firstlaunch = False

        # Предупреждение о контенте (показываем при каждом обновлении версии или первом запуске)
        call screen content_warning_screen with dissolve
        call screen content_warning with dissolve
        
        #TODO Настройки доступности (размер текста и т.д)
        # call screen accessibility_settings 

    # -----------------------------------------------------------
    # 4. ПРОВЕРКИ DLC И ОБНОВЛЕНИЙ
    # -----------------------------------------------------------
    
    if renpy.has_label("_call_dlc_check_sequence"):
        call dlc_check_sequence from _call_dlc_check_sequence

    if hasattr(store, 'updater_state'):
        $ wait_time = 0.0
        while updater_state["status"] == "checking" and wait_time < 3.0:
            $ renpy.pause(0.1, hard=True)
            $ wait_time += 0.1
            
        if updater_state["status"] == "update_available":
            call show_updater_prompt from _call_show_updater_prompt

    return