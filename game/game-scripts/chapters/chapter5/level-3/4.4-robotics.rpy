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