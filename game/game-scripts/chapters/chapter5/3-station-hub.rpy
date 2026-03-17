    # --- МЕНЮ ИССЛЕДОВАНИЯ ---
    
label station_hub_menu:
    
    scene chapter5-test-arrival with fade
    
    menu:
        "Отправиться в Бар 'Космический Ветер'" if not visited_bar:
            jump station_bar_scene
            
        "Зайти в Часовню Единения" if not visited_chapel:
            jump station_chapel_scene
            
        "Проверить Библиотеку Корпорации" if not visited_library:
            jump ch5_level2_library
            
        "Направиться к Серверной (Сюжет)" (id="server_room_option"):
            jump station_server_room_entry