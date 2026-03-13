# --- ГЛАВА 5: КВЕСТ УРОВЕНЬ 3 ---

init python:
    Item_BlankChip = Item("blank_chip", "Сервисный Чип", "Пустой чип без цифровой подписи.", "images/items/chip.png")
    Item_ReagentA = Item("reagent_a", "Ампула 'Цито-В'", "Красная ампула с биологически активной основой.", "images/items/flask_red.png")
    Item_ReagentB = Item("reagent_b", "Ампула 'Ген-Связь'", "Синяя жидкость, холодная на ощупь.", "images/items/flask_blue.png")
    Item_BioSpray = Item("bio_spray", "Биомаркер", "Синтезированный аэрозоль. Обманет любой ДНК-сканер корпорации.", "images/items/spray.png")
    Item_AdminChip = Item("admin_chip", "Чип Администратора", "Обладает высшим уровнем доступа 'Омега'.", "images/items/chip_green.png")

label ch5_level3_main_hall:
    scene bg space_station_corridor_main with dissolve
    play music "music/BGM/Heist_Tension_Low.opus" loop volume 0.3
    
    narrator """
        Уровень 3. Стерильные белые коридоры, резкий медицинский свет.
        Сюда допускался только научный персонал уровня 'Бета' и выше.
    """

label ch5_level3_main_hall_menu:
    scene bg space_station_corridor_main
    
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

# --- ОТДЕЛ ИССЛЕДОВАНИЙ (ТЕРМИНАЛ ИИ) ---
label ch5_level3_research:
    scene bg space_station_lab with dissolve
    
    narrator "Отдел исследований был пуст. В центре возвышалась голографическая проекция дежурного ИИ 'Архимед'."
    
    "Архимед (ИИ)" "Отказ в доступе. Текущий уровень угрозы: Код Желтый. Предъявите чип Администратора."
    
    if has_item("admin_chip"):
        menu:
            "Вставить Чип Администратора":
                $ remove_item("admin_chip")
                play sound "sfx/access_granted_chime.opus"
                "Архимед (ИИ)" "Доступ подтвержден. Приветствую, Администратор."
                "Архимед (ИИ)" "Внимание. В связи с протоколом 'Омега', ИИ требует верификации логической цепи."
                neon "Логическое тестирование... Стандартная процедура защиты от кибератак. Давай сюда свою загадку."
                
                label ch5_ai_riddle:
                    "Архимед (ИИ)" """
                        Дано три сервера: Альфа, Бета, Гамма. 
                        Один из них всегда говорит правду (Главный), один всегда лжет (Троян), один отвечает случайно (Резерв).
                        Альфа говорит: 'Бетта — это Троян'.
                        Бетта говорит: 'Альфа лжет'.
                        Гамма говорит: 'Я не Троян'.
                        Кто из них Троян?
                    """
                    menu:
                        "Альфа":
                            "Архимед (ИИ)" "Ошибка логики. Верификация не пройдена."
                            jump ch5_ai_riddle
                        "Бета":
                            "Архимед (ИИ)" "Ошибка логики. Верификация не пройдена."
                            jump ch5_ai_riddle
                        "Гамма":
                            "Архимед (ИИ)" "Ответ принят. Вектор мышления человека подтвержден. Чем могу служить?"
                            neon "Разблокируй дверь Сектора 'Серверная'."
                            play sound "sfx/door_slide_tech.opus"
                            "Архимед (ИИ)" "Дверь разблокирована."
                            $ ch5_server_unlocked = True
                            jump ch5_level3_main_hall_menu
    else:
        neon "{=thoughts}Мне нужен Чип Администратора, чтобы заставить его слушать.{/thoughts}"
        jump ch5_level3_main_hall_menu

# --- ТРАВМАТОЛОГИЯ ---
label ch5_level3_trauma:
    scene bg space_station_clinic with dissolve
    
    narrator "Палаты Травматологии были пусты, но койки несли следы недавнего присутствия пациентов. Капельницы были сорваны в спешке."
    neon "{=thoughts}Ничего полезного, только разбросанные бинты. Эвакуация здесь проходила в панике.{/thoughts}"
    jump ch5_level3_main_hall_menu

# --- МЕДБЕЙ ---
label ch5_level3_medbay:
    scene bg space_station_medbay with dissolve
    
    narrator "Главная приемная медицинского блока. В центре комнаты стоял сложный хирургический синтезатор. Рядом находился терминал Главного Врача."
    
label ch5_level3_medbay_menu:
    menu:
        "Осмотреть терминал Главврача":
            if has_item("admin_chip"):
                narrator "Мне здесь больше нечего делать."
            else:
                narrator "Голоэкран терминала мерцал красным. 'Требуется биометрическое подтверждение ДНК Главного Врача'."
                if has_item("bio_spray") and has_item("blank_chip"):
                    menu:
                        "Распылить Биомаркер на сканер и применить Пустой чип":
                            $ remove_item("bio_spray")
                            $ remove_item("blank_chip")
                            play sound "sfx/spray_hiss.opus"
                            narrator "Я распылила аэрозоль на стекло сканера. Затем вставила пустой чип в разъем."
                            play sound "sfx/access_granted_chime.opus"
                            narrator "Терминал пискнул. 'ДНК подтверждено. Доступ уровня Омега предоставлен'."
                            neon "Отлично. Копирую профиль на чип."
                            $ add_item(Item_AdminChip)
                            jump ch5_level3_medbay_menu
                        "Вернуться":
                            jump ch5_level3_medbay_menu
                else:
                    neon "{=thoughts}ДНК сканер... Мне нужен способ обмануть его биодатчики. И пустой чип, чтобы записать допуск.{/thoughts}"
            jump ch5_level3_medbay_menu
            
        "Осмотреть синтезатор":
            if has_item("reagent_a") and has_item("reagent_b"):
                menu:
                    "Смешать Цито-В и Ген-Связь":
                        $ remove_item("reagent_a")
                        $ remove_item("reagent_b")
                        play sound "sfx/chemical_mix.opus"
                        narrator "Аппарат загудел, смешивая компоненты в маленьком баллончике-спрее."
                        $ add_item(Item_BioSpray)
                        jump ch5_level3_medbay_menu
                    "Уйти":
                        jump ch5_level3_medbay_menu
            else:
                narrator "Синтезатор ждет ввода компонентов. У меня их пока нет."
                jump ch5_level3_medbay_menu
                
        "Пройти в Вирусологию":
            jump ch5_level3_virology
            
        "Пройти в Генетику":
            jump ch5_level3_genetics
            
        "Вернуться в коридор":
            jump ch5_level3_main_hall_menu

# --- ВИРУСОЛОГИЯ ---
label ch5_level3_virology:
    scene bg space_station_virology with dissolve
    
    narrator "Сектор Вирусологии. Желтые предупреждающие знаки биологической опасности."
    
    if not hasattr(store, 'ch5_virology_looted') or not ch5_virology_looted:
        narrator "В одном из охладителей мигала красная лампочка."
        menu:
            "Осмотреть охладитель":
                narrator "Внутри находилась капсула 'Цито-В'."
                neon "Базовый биоматериал. Может пригодиться."
                $ add_item(Item_ReagentA)
                $ ch5_virology_looted = True
                jump ch5_level3_virology
            "Уйти":
                jump ch5_level3_medbay_menu
    else:
        narrator "Охладители пусты. Больше ничего ценного."
        jump ch5_level3_medbay_menu

# --- ГЕНЕТИКА ---
label ch5_level3_genetics:
    scene bg space_station_genetics with dissolve
    
    narrator "Отдел Генетики. Ряды секвенаторов ДНК тихо гудели в темноте."
    
    if not hasattr(store, 'ch5_genetics_looted') or not ch5_genetics_looted:
        narrator "На одном из столов я заметила открытый кейс с химикатами."
        menu:
            "Осмотреть кейс":
                narrator "Синяя жидкость в ампуле 'Ген-Связь'."
                neon "Протеиновый коннектор для ДНК. Беру."
                $ add_item(Item_ReagentB)
                $ ch5_genetics_looted = True
                jump ch5_level3_genetics
            "Уйти":
                jump ch5_level3_medbay_menu
    else:
        narrator "Лаборатория уже обыскана."
        jump ch5_level3_medbay_menu

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

# --- РОБОТОТЕХНИКА ---
label ch5_level3_robotics:
    scene bg space_station_robotics with dissolve
    
    narrator "Сборочный цех. На столах лежали недосообранные прототипы дронов охраны."
    
    if not hasattr(store, 'ch5_robotics_solved') or not ch5_robotics_solved:
        narrator "В дальней части комнаты огромный манипулятор завис над конвейером. В его зажимах я увидела то, что искала: неформатированный сервисный чип."
        neon "Манипулятор заклинило на 'мертвой хватке'. Мне нужно перераспределить давление в поршнях, чтобы он разжал пальцы."
        
        # Головоломка: Три вентиля (A, B, C). Нужно набрать ровно давление 50.
        # Вентиль А: +20, Вентиль Б: -10, Вентиль C: +15
        # Старт с 0.
        $ robot_pressure = 0
        
        label ch5_robot_puzzle:
            narrator "Текущее давление в гидросистеме: [robot_pressure] PSI. Необходимо: 50 PSI."
            
            if robot_pressure == 50:
                play sound "sfx/hydraulic_release.opus"
                narrator "С громким шипением манипулятор разжал пальцы. Чип со звоном упал на ленту."
                $ add_item(Item_BlankChip)
                $ ch5_robotics_solved = True
                jump ch5_level3_inner_hall_menu
                
            menu:
                "Повернуть Вентиль A (+20)":
                    $ robot_pressure += 20
                    jump ch5_robot_puzzle
                "Повернуть Вентиль B (-10)":
                    $ robot_pressure -= 10
                    jump ch5_robot_puzzle
                "Повернуть Вентиль C (+15)":
                    $ robot_pressure += 15
                    jump ch5_robot_puzzle
                "Сбросить давление (0)":
                    $ robot_pressure = 0
                    jump ch5_robot_puzzle
                "Отойти":
                    jump ch5_level3_inner_hall_menu
    else:
        narrator "Манипулятор безвольно висит. Чип уже у меня."
        jump ch5_level3_inner_hall_menu
