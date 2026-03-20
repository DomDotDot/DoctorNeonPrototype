# --- ГЛАВА 5: КВЕСТ УРОВЕНЬ 2 ---

init python:
    # Инициализация предметов для Главы 5
    Item_MaintenanceKeycard = Item("maintenance_keycard", "Сервисная карта", "Ключ-карта технического персонала Орбитали.", "images/items/keycard.png")
    Item_UnchargedBattery = Item("uncharged_battery", "Разряженная батарея", "Тяжелая энергетическая ячейка для крупной техники. Полностью пуста.", "images/items/battery_empty.png")
    Item_ChargedBattery = Item("charged_battery", "Заряженная батарея", "Энергетическая ячейка, гудящая от переполняющей её энергии.", "images/items/battery_full.png")

label ch5_quest_init:
    # Вызывается один раз перед началом квеста
    $ inventory_allowed = True
    $ inventory_list = []
    
    show screen inventory_listener
    
    # Флаги Уровня 2
    $ ch5_level2_examined = False
    $ ch5_cargo_solved = False
    $ ch5_library_examined = False
    $ ch5_bar_code_known = False
    $ ch5_bar_unlocked = False
    $ ch5_ejection_examined = False
    $ ch5_elevator_powered = False
    return

# --- ГЛАВНЫЙ ХОЛЛ (УРОВЕНЬ 2) ---
label ch5_level2_main_hall:
    scene chapter5-test-hublevel1 with fade
    play music "music/BGM/Space_Station_Atmosphere.opus" loop volume 0.3
    
    narrator """
        Главный холл второго уровня. Транзитная зона и Паспортный контроль остались позади.
        
        Здесь было тише, но не спокойнее. В воздухе висело напряжение.

        Люди старались не смотреть друг другу в глаза, торопясь по своим делам.
    """
    
label ch5_level2_main_hall_menu:
    scene chapter5-test-hublevel1
    
    menu:
        "Осмотреть холл" if not ch5_elevator_powered:
            narrator """
                Большое круглое помещение.

                Направо ведет коридор к зоне Карго и грузовым лифтам. Аргон пошел туда.

                Налево — Цифровая Библиотека.

                Прямо по курсу виднеются неоновые вывески Бара "Космический Ветер".

                Чуть правее Бара находятся Часовня и сектор выброса тел в космос.

                А в самом темном углу холла — пассажирский лифт и лестничная площадка.
            """
            $ ch5_level2_examined = True
            jump ch5_level2_main_hall_menu
            
        "Подойти к лифту" if ch5_level2_examined:
            jump ch5_level2_elevator
            
        "Пойти в зону Карго" if ch5_level2_examined:
            jump ch5_level2_cargo
            
        "Зайти в Цифровую Библиотеку" if ch5_level2_examined:
            jump ch5_level2_library
            
        "Пойти в Бар 'Космический Ветер'" if ch5_level2_examined:
            jump ch5_station_bar_scene
        
        "Зайти в космическую Часовню" if ch5_level2_examined:
            jump ch5_station_chapel_scene