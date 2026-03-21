# --- РОБОТОТЕХНИКА ---
label ch5_level3_robotics:
    scene bg space_station_robotics with dissolve
    
    narrator "Сборочный цех. На столах лежали недосообранные прототипы дронов охраны."
    
    if not hasattr(store, 'ch5_robotics_solved') or not ch5_robotics_solved:
        narrator "В дальней части комнаты огромный манипулятор завис над конвейером. В его железной хватке была зажата красная ампула — 'Цито-В'."
        neon "Манипулятор заклинило на 'мертвой хватке'. Если я попытаюсь вырвать ампулу силой, она попросту лопнет."
        
        narrator "Я подошла к терминалу управления гидравликой."
        
        if not hasattr(store, 'ch5_robotics_formula_idx'):
            $ store.ch5_robotics_formula_idx = renpy.random.randint(0, 2)
            
        label ch5_robot_puzzle:
            narrator "На экране мерцала надпись: 'СИСТЕМНЫЙ СБОЙ ДАВЛЕНИЯ. Ручные вентили отключены. Требуется аварийный сброс давления.'"
            
            if store.ch5_robotics_formula_idx == 0:
                $ ch5_robot_hint = "Корень из 144, умноженный на константу Пи (до сотых: 3.14)."
                $ ch5_robot_ans = ["37.68", "37,68"]
            elif store.ch5_robotics_formula_idx == 1:
                $ ch5_robot_hint = "Квадрат числа 12 минус 44."
                $ ch5_robot_ans = ["100", "100.0", "100,0"]
            else:
                $ ch5_robot_hint = "Корень из 256 плюс 15."
                $ ch5_robot_ans = ["31", "31.0", "31,0"]
                
            narrator "Ниже горела подсказка местного инженера: 'Значение сброса: [ch5_robot_hint]'"
                
            menu:
                "Ввести значение на цифровой клавиатуре":
                    $ player_input = renpy.input("Введите значение (только цифры и точка/запятая):").strip()
                    
                    if player_input in ch5_robot_ans:
                        play sound "sfx/hydraulic_release.opus"
                        narrator "С громким шипением система сбросила давление. Манипулятор медленно разжал стальные пальцы."
                        narrator "Ампула 'Цито-В' мягко упала на ленту конвейера."
                        $ add_item(Item_ReagentA)
                        $ ch5_robotics_solved = True
                        jump ch5_level3_inner_hall_menu
                    else:
                        play sound "sfx/error_buzz.opus"
                        narrator "Терминал мигнул красным: 'ОШИБКА ДАВЛЕНИЯ. Отказ системы.' Значение неверно."
                        jump ch5_robot_puzzle
                        
                "Покрутить механические вентили":
                    narrator "Я попробовала повернуть один из ручных вентилей."
                    narrator "Манометр хаотично прыгнул с 15 до 80 PSI, затем упал до нуля. 'Ручные вентили отключены', — гласила надпись. Это бесполезно."
                    jump ch5_robot_puzzle
                    
                "Отойти":
                    jump ch5_level3_inner_hall_menu
    else:
        narrator "Манипулятор безвольно висит. Ампула 'Цито-В' уже у меня."
        jump ch5_level3_inner_hall_menu