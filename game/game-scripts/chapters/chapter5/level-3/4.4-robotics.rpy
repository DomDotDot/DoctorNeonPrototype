# --- РОБОТОТЕХНИКА ---
label ch5_level3_robotics:
    scene bg space_station_robotics with dissolve
    
    narrator "Сборочный цех. На столах лежали недосообранные прототипы дронов охраны."
    
    if not hasattr(store, 'ch5_robotics_solved') or not ch5_robotics_solved:
        narrator "В дальней части комнаты огромный манипулятор завис над конвейером. В его железной хватке была зажата красная ампула — 'Цито-В'."
        neon "Манипулятор заклинило на 'мертвой хватке'. Если я попытаюсь вырвать ампулу силой, она попросту лопнет."
        
        narrator "Я подошла к терминалу управления гидравликой."
        
        if not hasattr(store, 'ch5_robotics_target_pressure'):
            $ store.ch5_robotics_target_pressure = 314
            $ store.ch5_robotics_current_pressure = renpy.random.randint(150, 250)
            
        label ch5_robot_puzzle:
            narrator "На экране мерцала надпись: 'СИСТЕМНЫЙ СБОЙ ДАВЛЕНИЯ. Требуется ручная калибровка.'"
            narrator "Ниже горела подсказка местного инженера: 'Внимание, целевое давление для сброса 'мертвой хватки' манипулятора должно равняться константе Пи, умноженной на 100.'"
            narrator "Текущее давление в системе: [store.ch5_robotics_current_pressure] PSI."
            
            menu:
                "Крутить большой красный вентиль (+50 PSI)":
                    $ store.ch5_robotics_current_pressure += 50
                    play sound "sfx/multitool_click.opus"
                    jump ch5_robot_puzzle_check
                    
                "Крутить синий вентиль (-15 PSI)":
                    $ store.ch5_robotics_current_pressure -= 15
                    play sound "sfx/multitool_click.opus"
                    jump ch5_robot_puzzle_check
                    
                "Крутить жёлтый вентиль (+7 PSI)":
                    $ store.ch5_robotics_current_pressure += 7
                    play sound "sfx/multitool_click.opus"
                    jump ch5_robot_puzzle_check
                    
                "Отойти":
                    jump ch5_level3_inner_hall_menu

        label ch5_robot_puzzle_check:
            if store.ch5_robotics_current_pressure == store.ch5_robotics_target_pressure:
                play sound "sfx/hydraulic_release.opus"
                narrator "С громким шипением система сбросила давление. Манипулятор медленно разжал стальные пальцы."
                narrator "Ампула 'Цито-В' мягко упала на ленту конвейера."
                $ add_item(Item_ReagentA)
                $ ch5_robotics_solved = True
                jump ch5_level3_inner_hall_menu
            elif store.ch5_robotics_current_pressure > 450 or store.ch5_robotics_current_pressure < 50:
                play sound "sfx/error_buzz.opus"
                narrator "Терминал мигнул красным: 'КРИТИЧЕСКОЕ ЗНАЧЕНИЕ ДАВЛЕНИЯ. Аварийный сброс до случайного безопасного значения.'"
                $ store.ch5_robotics_current_pressure = renpy.random.randint(150, 250)
                jump ch5_robot_puzzle
            else:
                jump ch5_robot_puzzle
    else:
        narrator "Манипулятор безвольно висит. Ампула 'Цито-В' уже у меня."
        jump ch5_level3_inner_hall_menu