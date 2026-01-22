    # --- МЕНЮ ИССЛЕДОВАНИЯ ---
    
label station_hub_menu:
    
    scene bg space_station_central_hub with fade
    
    menu:
        "Отправиться в Бар 'Космический Ветер'" if not visited_bar:
            jump station_bar_scene
            
        "Зайти в Часовню Единения" if not visited_chapel:
            jump station_chapel_scene
            
        "Проверить Библиотеку Корпорации" if not visited_library:
            jump station_library_scene
            
        "Направиться к Серверной (Сюжет)" (id="server_room_option"):
            jump station_server_room_entry