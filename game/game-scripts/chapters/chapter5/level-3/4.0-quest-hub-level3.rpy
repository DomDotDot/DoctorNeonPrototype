# --- ГЛАВА 5: КВЕСТ УРОВЕНЬ 3 ---

init python:
    Item_BlankChip = Item("blank_chip", "Сервисный Чип", "Пустой чип без цифровой подписи.", "images/items/chip.png")
    Item_ReagentA = Item("reagent_a", "Ампула 'Цито-В'", "Красная ампула с биологически активной основой.", "images/items/flask_red.png")
    Item_ReagentB = Item("reagent_b", "Ампула 'Ген-Связь'", "Синяя жидкость, холодная на ощупь.", "images/items/flask_blue.png")
    Item_BioSpray = Item("bio_spray", "Биомаркер", "Синтезированный аэрозоль. Обманет любой ДНК-сканер корпорации.", "images/items/spray.png")
    Item_AdminChip = Item("admin_chip", "Чип Администратора", "Обладает высшим уровнем доступа 'Омега'.", "images/items/chip_green.png")

label ch5_level3_main_hall:
    scene chapter5-test-hublevel3 with dissolve
    play music "music/BGM/Heist_Tension_Low.opus" loop volume 0.3
    
    narrator """
        Уровень 3. Стерильные белые коридоры, резкий медицинский свет.
        Сюда допускался только научный персонал уровня 'Бета' и выше.
    """

label ch5_level3_main_hall_menu:
    scene chapter5-test-hublevel3
    
    menu:
        "Осмотреться":
            narrator """
                Прямо по курсу – 'Отдел Исследований'. Огромные стеклянные двери.
                Слева – Травматология.
                Справа – Медицинский блок (Медбей). Судя по указателям, из Медбея можно попасть в отделы Генетики и Вирусологии.
                Где-то дальше по коридору, за Отделом Исследований, находятся серверная и лаборатория Робототехники.
            """
            jump ch5_level3_main_hall_menu
            
        "Пойти в Отдел Исследований (Центральный ИИ)":
            jump ch5_level3_research
            
        "Зайти в Травматологию":
            jump ch5_level3_trauma
            
        "Зайти в Медицинский блок":
            jump ch5_level3_medbay
            
        "Пройти в дальний холл (Робототехника и Серверная)":
            jump ch5_level3_inner_hall
            
        "Спуститься на Уровень 2 (Лифт)":
            $ ch5_elevator_powered = True # На всякий случай
            jump ch5_level2_elevator

# --- ДАЛЬНИЙ ХОЛЛ (Робототехника и Серверная) ---
label ch5_level3_inner_hall:
    scene bg space_station_rnd_corridor with dissolve
    
    narrator "Здесь освещение было приглушенным. В конце коридора виднелась гигантская укрепленная дверь Серверной."
    
label ch5_level3_inner_hall_menu:
    menu:
        "Зайти в лабораторию Робототехники":
            jump ch5_level3_robotics
            
        "Подойти к дверям Серверной":
            if getattr(store, 'ch5_server_unlocked', False):
                narrator "Двери Серверной открыты. Меня ждет конечная цель."
                menu:
                    "Войти в Серверную (Продолжить сюжет)":
                        jump station_server_room_entry
                    "Вернуться":
                        jump ch5_level3_inner_hall_menu
            else:
                narrator "Тяжелая бронированная дверь. Рядом нет считывателей. Вскрыть её снаружи невозможно."
                neon "Доступ явно управляется удаленно. ИИ 'Архимед' в Отделе Исследований должен помочь."
                jump ch5_level3_inner_hall_menu
                
        "Вернуться в главный коридор 3 Уровня":
            jump ch5_level3_main_hall_menu
