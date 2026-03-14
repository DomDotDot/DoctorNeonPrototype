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
    $ ch5_cargo_solved = False
    $ ch5_library_examined = False
    $ ch5_bar_code_known = False
    $ ch5_bar_unlocked = False
    $ ch5_ejection_examined = False
    $ ch5_elevator_powered = False
    return

# --- ГЛАВНЫЙ ХОЛЛ (УРОВЕНЬ 2) ---
label ch5_level2_main_hall:
    scene bg space_station_central_hub with fade
    play music "music/BGM/Space_Station_Atmosphere.opus" loop volume 0.3
    
    narrator """
        Главный холл второго уровня. Транзитная зона и Паспортный контроль остались позади.
        
        Здесь было тише, но не спокойнее. В воздухе висело напряжение.
        Люди старались не смотреть друг другу в глаза, торопясь по своим делам.
    """
    
label ch5_level2_main_hall_menu:
    scene bg space_station_central_hub
    
    menu:
        "Осмотреть холл" if not ch5_elevator_powered:
            narrator """
                Большое круглое помещение.
                Направо ведет коридор к зоне Карго и грузовым лифтам (Аргон пошел туда).
                Налево — Цифровая Библиотека.
                Прямо по курсу виднеются неоновые вывески Бара "Космический Ветер".
                Чуть правее Бара находятся Часовня и сектор выброса тел в космос.
                А в самом темном углу холла — пассажирский лифт и лестничная площадка.
            """
            jump ch5_level2_main_hall_menu
            
        "Подойти к лифту":
            jump ch5_level2_elevator
            
        "Пойти в зону Карго":
            jump ch5_level2_cargo
            
        "Зайти в Цифровую Библиотеку":
            jump ch5_level2_library
            
        "Пойти в Бар 'Космический Ветер'":
            jump ch5_level2_bar
            
        "Осмотреть сектор выброса тел":
            jump ch5_level2_ejection
            
# --- ЛИФТ (УРОВЕНЬ 2) ---
label ch5_level2_elevator:
    scene bg space_station_corridor_main with dissolve
    
    if ch5_elevator_powered:
        narrator "Лифт работает. Индикаторы горят зеленым."
        menu:
            "Ехать на Уровень 3 (Исследования и Медбей)":
                jump ch5_level3_main_hall
            "Вернуться в холл":
                jump ch5_level2_main_hall_menu
    else:
        narrator "Я подошла к дверям лифта. Индикаторы на панели были мертвы. Питание отключено."
        neon "Лестничная площадка заблокирована гермодверьми. Значит, единственный путь наверх — этот лифт."
        narrator "Я осмотрела технический щиток рядом с дверью. Он был вскрыт."
        neon "Кто-то вытащил энергетическую ячейку. Мне нужно найти замену и зарядить её, иначе на 3-й этаж не попасть."
        
        if has_item("charged_battery"):
            menu:
                "Установить Заряженную батарею":
                    $ remove_item("charged_battery")
                    $ ch5_elevator_powered = True
                    play sound "sfx/power_up.opus"
                    narrator "Я вставила тяжелую батарею в слот. Щелчок контактов, гул — и панель лифта ожила, засветившись мягким зеленым светом."
                    jump ch5_level2_elevator
                "Вернуться в холл":
                    jump ch5_level2_main_hall_menu
        else:
            jump ch5_level2_main_hall_menu

# --- КАРГО ---
label ch5_level2_cargo:
    scene bg space_station_transit_zone with dissolve
    
    if ch5_cargo_solved:
        narrator "В зоне Карго суетятся погрузчики. Аргон где-то там, следит за 'Эребом'. Мне не стоит здесь задерживаться."
        jump ch5_level2_main_hall_menu
        
    narrator """
        Зона Карго. Горы ящиков, шум экзоскелетов и ругань грузчиков.
        Я осмотрела технические помещения у входа. В одной из каморок лежал брошенный комбинезон техника.
    """
    
    menu:
        "Обыскать шкафчики и комбинезон":
            narrator "Я проверила карманы. Пусто. Но на дне одного из шкафчиков, под грудой проводов, я нашла нечто полезное."
            narrator "Головоломка замка шкафчика оказалась несложной: нужно было замкнуть цепь питания мультитулом."
            # Миниатюрный логический вывод для эффекта
            neon "Если соединить синий провод с красным, игнорируя землю, замок должен открыться."
            play sound "sfx/multitool_click.opus"
            narrator "Щелчок. Дверца поддалась."
            $ add_item(Item_MaintenanceKeycard)
            $ ch5_cargo_solved = True
            jump ch5_level2_cargo
            
        "Вернуться в холл":
            jump ch5_level2_main_hall_menu

# --- ЦИФРОВАЯ БИБЛИОТЕКА ---
label ch5_level2_library:
    scene bg space_station_library with dissolve
    
    narrator "Цифровая библиотека Гелиоса. Ряды мерцающих терминалов, за которыми сидят люди с пустыми глазами, поглощая виртуальный контент."
    
    if not ch5_library_examined:
        narrator "Терминал администратора закрыт служебной дверью. Проход заблокирован."
        
        if has_item("maintenance_keycard"):
            menu:
                "Использовать Сервисную карту":
                    play sound "sfx/door_slide_tech.opus"
                    narrator "Магнитный замок щелкнул, и я прошла в служебное помещение."
                    narrator "На столе админа лежал личный датапад."
                    neon "Посмотрим... Журнал смен. 'Бармен из Космического Ветра опять забыл код от своей подсобки. Я поставил ему год основания Веритаса, пусть попробует забыть это'."
                    $ ch5_bar_code_known = True
                    $ ch5_library_examined = True
                    neon "{=thoughts}Год основания Веритаса... 2054. Отлично.{/thoughts}"
                    jump ch5_level2_library
                "Вернуться в холл":
                    jump ch5_level2_main_hall_menu
        else:
            neon "{=thoughts}Мне нужен доступ техника, чтобы пройти туда.{/thoughts}"
            jump ch5_level2_main_hall_menu
    else:
        narrator "Здесь больше нет ничего полезного."
        jump ch5_level2_main_hall_menu

# --- БАР 'КОСМИЧЕСКИЙ ВЕТЕР' ---
label ch5_level2_bar:
    scene bg space_station_bar with dissolve
    
    narrator "Бар 'Космический Ветер'. Неоновый полумрак, тихая музыка и запах дешевого синтетического алкоголя."
    
    if ch5_bar_unlocked:
        if has_item("uncharged_battery") or has_item("charged_battery") or ch5_elevator_powered:
            narrator "В подсобке пусто. Батарею я уже забрала."
        else:
            narrator "Я снова зашла в подсобку."
            menu:
                "Взять батарею":
                    narrator "В углу, среди ящиков с алкоголем, валялась резервная батарея от погрузчика."
                    $ add_item(Item_UnchargedBattery)
                "Уйти":
                    pass
        jump ch5_level2_main_hall_menu
        
    narrator "Дверь в подсобку закрыта на кодовый замок."
    
    menu:
        "Ввести код 2054" if ch5_bar_code_known:
            play sound "sfx/hacking_success_beep.opus"
            narrator "Дверь пискнула и открылась."
            $ ch5_bar_unlocked = True
            jump ch5_level2_bar
            
        "Попытаться взломать":
            narrator "Замок слишком примитивный для удаленного взлома, здесь физическая панель со стертыми кнопками. Нужен код."
            jump ch5_level2_main_hall_menu
            
        "Уйти":
            jump ch5_level2_main_hall_menu

# --- СЕКТОР ВЫБРОСА ТЕЛ ---
label ch5_level2_ejection:
    scene bg space_station_chapel with dissolve
    
    narrator "Рядом с Часовней находился сектор утилизации и космического выброса. Суровое напоминание о том, как легко здесь оборваться жизни."
    narrator "Здесь стояли мощные индукционные катушки, обеспечивающие работу катапульт."
    
    if has_item("uncharged_battery"):
        menu:
            "Поместить разряженную батарею в катушку":
                $ remove_item("uncharged_battery")
                play sound "sfx/electric_zap.opus"
                narrator "Громкое гудение наполнило комнату. Синие молнии заскользили по корпусу батареи."
                narrator "Процесс занял пару минут. Индикатор на батарее загорелся зеленым."
                $ add_item(Item_ChargedBattery)
                jump ch5_level2_main_hall_menu
            "Отмена":
                jump ch5_level2_main_hall_menu
    else:
        narrator "Гудение трансформаторов бьет по ушам. Энергии здесь хватило бы, чтобы запитать небольшой городской квартал, но мне не к чему её приложить."
        jump ch5_level2_main_hall_menu
