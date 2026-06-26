# --- МЕДИЦИНСКИЙ БЛОК (МЕДБЕЙ) - ЦЕНТРАЛЬНЫЙ ХАБ ---

label ch5_level3_medbay:
    # Инициализация переменных медбея при первом входе
    if not hasattr(store, 'ch5_medbay_entered') or not store.ch5_medbay_entered:
        $ store.ch5_medbay_entered = True
        $ store.ch5_medbay_door_glitching_seen = False
        $ store.ch5_medbay_mop_propped = False
        $ store.ch5_monorail_terminal_seen = False
        
        $ store.ch5_medbay_mri_unlocked = False
        $ store.ch5_medbay_mri_opened = False
        $ store.ch5_medbay_brochure_read = False
        $ store.ch5_medbay_reagent_d_dispensed = False
        
        $ store.ch5_medbay_radiology_visited = False
        $ store.ch5_medbay_transition_used = False
        $ store.ch5_medbay_right_entered_from_main_hall = False
        
        $ store.ch5_medbay_chief_door_opened = False
        $ store.ch5_medbay_blank_chip_taken = False
        $ store.ch5_medbay_empty_spray_taken = False
        
        scene ch05_bg12_v01 with dissolve
        
        narrator """
            Главный вход в Медицинский блок (Медбей).
            
            Я оказалась в заброшенном зале ожидания. Мягкие кресла покрыты тонким слоем пыли.
            
            Дверь, ведущая в глубину медицинского блока, мигает жёлтым карантинным светодиодом. Никаких замков. Внутренний шлюз гостеприимно приоткрыт.
        """
        
        neon "{=thoughts}Странно... Панель мигает жёлтым, но сам замок отключен. Кто-то объявлял карантин?{/thoughts}"

    jump ch5_level3_medbay_main_menu

# --- ЗАЛ ОЖИДАНИЯ (ТОЧКА ВХОДА) ---
label ch5_level3_medbay_main_menu:
    scene ch05_bg12_v01
    
    menu:
        "Пойти в Левое крыло":
            jump ch5_level3_medbay_left_corridor
            
        "Пойти в Правое крыло":
            jump ch5_level3_medbay_right_corridor
            
        "Пойти в Центральный проход":
            jump ch5_level3_medbay_fwd_corridor
            
        "Выйти":
            jump ch5_level3_main_hall_menu