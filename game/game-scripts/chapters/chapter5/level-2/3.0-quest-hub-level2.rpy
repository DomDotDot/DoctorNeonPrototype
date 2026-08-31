# --- ГЛАВА 5: КВЕСТ УРОВЕНЬ 2 ---

init python:
    # Инициализация предметов для Главы 5
    Item_MaintenanceKeycard = Item("maintenance_keycard", _("Сервисная карта"), _("Ключ-карта технического персонала Орбитали."), "images/items/keycard.png")
    Item_UnchargedBattery = Item("uncharged_battery", _("Разряженная батарея"), _("Тяжелая энергетическая ячейка для крупной техники. Полностью пуста."), "images/items/battery.png")
    Item_ChargedBattery = Item("charged_battery", _("Заряженная батарея"), _("Энергетическая ячейка, гудящая от переполняющей её энергии."), "images/items/battery.png")
    Item_BartenderUniform = Item("bartender_uniform", _("Униформа бармена"), _("Рабочий комбинезон персонала бара 'Космический Ветер'. Пахнет дешёвым виски и потом."), "images/items/uniform_bartender.png")

label ch5_quest_init:
    # Вызывается один раз перед началом квеста
    $ inventory_allowed = True
    $ inventory_list = []
    
    show screen inventory_listener
    
    # Флаги Уровня 2
    $ ch5_level2_examined = False
    $ ch5_cargo_solved = False
    $ ch5_library_examined = False
    $ ch5_bar_code_existance_known = False
    $ ch5_bar_code_known = False
    $ ch5_bar_unlocked = False
    $ ch5_ejection_examined = False
    $ ch5_elevator_powered = False
    $ ch5_elevator_powered = False
    $ ch5_bartender_talked = False
    
    # Флаги нового саб-квеста
    $ ch5_cargo_first_visit = True
    $ ch5_visited_bar = False
    $ ch5_visited_chapel = False
    $ ch5_visited_library = False
    $ ch5_dorms_article_found = False
    $ ch5_chapel_priest_state = 0
    $ ch5_read_folklore = False
    $ ch5_priest_reject_points = 0
    $ ch5_chapel_realization_triggered = False
    
    # Флаги Дормов
    $ ch5_dorms_time = 0
    $ ch5_dorms_searched = False
    $ ch5_dorms_event_triggered = False
    $ ch5_bar_fight_agreed = False
    $ ch5_got_uniform = False
    
    # Флаги Уровня 3 (монорельс + спутник)
    $ ch5_level3_examined = False
    $ ch5_yellow_alert_known = False
    $ ch5_monorail_access = False
    $ ch5_ai_core_complete = False
    $ ch5_server_unlocked = False
    $ store.ch5_entered_server_room = False
    
    # Флаги спутника
    $ ch5_satellite_reception_examined = False
    $ ch5_corridor_alpha_solved = False
    $ ch5_corridor_beta_solved = False
    $ ch5_corridor_gamma_solved = False
    $ ch5_core_corridor_open = False
    $ ch5_satellite_timer_active = False
    $ ch5_satellite_timer_start = 0.0
    $ ch5_satellite_timer_duration = 90.0
    
    # Лорные флаги спутника
    $ ch5_ai_asked_alert = False
    $ ch5_ai_asked_personnel = False
    $ ch5_ai_asked_omega = False
    $ ch5_ai_asked_erebus = False
    return

# --- ГЛАВНЫЙ ХОЛЛ (УРОВЕНЬ 2) ---
label ch5_level2_main_hall:
    scene ch05_bg01_v01 with fade
    play music "music/BGM/ComatoseExtended.opus" loop volume 0.25
    
    narrator """
        Главный холл второго уровня. Транзитная зона и Паспортный контроль остались позади.
        
        Здесь было тише, но не спокойнее. В воздухе висело напряжение.

        Люди старались не смотреть друг другу в глаза, торопясь по своим делам.
    """
    
label ch5_level2_main_hall_menu:
    scene ch05_bg01_v01 with fade
    
    menu:
        "Осмотреть холл" if not ch5_elevator_powered:
            narrator """
                Большое круглое помещение.

                Направо ведет коридор к зоне Карго и грузовым лифтам. Аргон пошел туда.

                Налево — Цифровая Библиотека.

                Прямо по курсу виднеются неоновые вывески Бара 'Космический Ветер'.
                Рядом с баром находится вход в Дормы — жилые блоки персонала.

                Чуть правее Бара находятся Часовня и сектор выброса тел в космос.

                А в центре холла — пассажирский лифт, который может доставить тебя на другие уровни станции.
            """
            $ ch5_level2_examined = True
            jump ch5_level2_main_hall_menu
            
        "Подойти к лифту" if ch5_level2_examined:
            jump ch5_level2_elevator
            
        "Пойти в зону Карго" if ch5_level2_examined:
            jump ch5_level2_cargo
            
        "Зайти в Цифровую Библиотеку" if ch5_level2_examined:
            jump ch5_level2_library
            
        "Пройти в Дормы" if ch5_level2_examined:
            jump ch5_level2_dorms
            
        "Пойти в Бар 'Космический Ветер'" if ch5_level2_examined:
            jump ch5_station_bar_scene
        
        "Зайти в космическую Часовню" if ch5_level2_examined:
            jump ch5_station_chapel_scene