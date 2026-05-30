# --- МЕДИЦИНСКИЙ БЛОК (МЕДБЕЙ) - ЦЕНТРАЛЬНЫЙ ХАБ ---

label ch5_level3_medbay:
    # Инициализация переменных медбея при первом входе
    if not hasattr(store, 'ch5_medbay_entered') or not store.ch5_medbay_entered:
        $ store.ch5_medbay_entered = True
        $ store.ch5_medbay_door_glitching_seen = False
        $ store.ch5_medbay_mop_propped = False
        $ store.ch5_medbay_terminal_seen = False
        
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
        
    scene bg space_station_medbay with dissolve
    
    narrator """
        Главный вход в Медицинский блок (Медбей).
        
        Я оказалась в заброшенном зале ожидания. Мягкие кресла покрыты тонким слоем пыли, рекламные голоэкраны с медпрепаратами безвольно погасли.
        
        Дверь, ведущая в глубину медицинского блока, мигает жёлтым карантинным светодиодом. Никаких замков. Внутренний шлюз гостеприимно приоткрыт.
    """
    
    neon "{=thoughts}Странно... Панель мигает жёлтым, предупреждая о биологической изоляции, но сам замок отключен. Тот, кто объявлял карантин, очень торопился... или хотел, чтобы кто-то вошел.{/thoughts}"

# --- ЗАЛ ОЖИДАНИЯ (ТОЧКА ВХОДА) ---
label ch5_level3_medbay_waiting_room:
    scene bg space_station_medbay
    
    menu:
        "Пройти в главные коридоры Медбея":
            narrator "Я переступила порог шлюза. Дверь за моей спиной тихо зашуршала, но осталась незапертой."
            jump ch5_level3_medbay_main_hall
            
        "Выйти на Уровень 3 (В холл)":
            jump ch5_level3_main_hall_menu

# --- ГЛАВНЫЙ ХОЛЛ МЕДБЕЯ (ЦЕНТРАЛЬНЫЙ ПЕРЕКРЕСТОК) ---
label ch5_level3_medbay_main_hall:
    scene bg space_station_medbay with dissolve
    
    narrator "Главный холл. Стерильные белые коридоры расходятся во все четыре стороны. Гнетущая тишина прерывается лишь ровным гулом вентиляции."
    
label ch5_level3_medbay_main_menu:
    menu:
        "Пойти в Левое крыло (Химическая лаборатория и кабинет Главврача)":
            jump ch5_level3_medbay_left_corridor
            
        "Пойти в Правое крыло (Отделение радиологии и внутренних болезней)":
            jump ch5_level3_medbay_right_corridor
            
        "Пойти в Центральный проход (Операционные, Генетика и Травматология)":
            jump ch5_level3_medbay_fwd_corridor
            
        "Вернуться в Зал ожидания":
            jump ch5_level3_medbay_waiting_room