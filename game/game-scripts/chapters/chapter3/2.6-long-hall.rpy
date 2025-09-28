label ch3_long_corridor:
    # Неон в темном коридоре за шкафчиком
    scene bg chapter_3_long-hall-hall with fade # Фон: темный, узкий служебный коридор
    play music "music/BGM/GreyPaint.ogg" fadein 15.0 fadeout 15.0 volume 0.125
    narrator """
    Коридор, открывшийся за воротами, делал небольшой изгиб влево, а затем резко поворачивал направо.

    Я оказалась в другом мире. Здесь было тихо. Пыль лежала ровным, нетронутым слоем, поглощая звуки
    
    Все пространство было завалено металлическими бочками, которые приходилось осторожно обходить.

    Сразу, справа, находилась запертая армированная дверь. Я сразу поняла, куда она ведет – это была та самая комната, которую блокировал шкаф в главном холле.
    
    Теперь я могла подойти к ней. На ней не было ручки, только панель с цифровым замком.

    Это крыло завода, казалось, спало летаргическим сном. Я шла по коридору, заглядывая в пустые комнаты: бывшие офисы, раздевалки, душевые. Везде царило запустение.

    В конце коридора блестела металлическая дверь.

    Но из-под одной двери пробивалась тонкая полоска тусклого света.
    """

    menu ch3_explore_long_corridor:
        "Открыть и войти в комнату с металлической дверью" if not has_equipment_idea:
            narrator "Я подошла к приоткрытой двери, и осторожно толкнула дверь. Она была не заперта."
            jump ch3_part2_the_cage
        "Осмотреть армированную дверь.":
            if not chemlab_door_unlocked:
                narrator "На двери блестит панель кодового замка. Нужен четырёхзначный код."
                menu:
                    "Попробовать ввести код.":
                        if found_code_clue:
                            # Экран ввода кода
                            $ code_attempt = renpy.input("Введите четырёхзначный  код:", length=4, allow="0123456789")
                            
                            if code_attempt == "1984":
                                # play sound "sounds/keypad_success.ogg"
                                narrator "Щелчок! Зеленый огонек. Я была права. Дверь в Хим. лабораторию открыта."
                                $ chemlab_door_unlocked = True
                                jump ch3_explore_long_corridor
                            else:
                                # play sound "sounds/keypad_fail.ogg"
                                narrator "Неправильный код. Панель мигнула красным. Хм, значит, я ошиблась в догадке, или ввожу не то."
                                jump ch3_explore_long_corridor
                        else:
                            neon "{=thoughts}Я понятия не имею, какой здесь может быть код. Просто тыкать наугад бессмысленно. Подсказка должна быть где-то здесь.{/thoughts}"
                            jump ch3_explore_long_corridor
                    
                    "Отойти.":
                        jump ch3_explore_long_corridor
            else:
                narrator "Дверь в Хим. лабораторию открыта."
                jump ch3_explore_long_corridor

        "Войти в Хим. лабораторию." if chemlab_door_unlocked:
            if has_equipment_idea:
                jump ch3_explore_chem_lab
            else:
                narrator "Мне незачем туда идти."
                jump ch3_explore_long_corridor

        "Идти в южное крыло (Пищевой цех)." if has_equipment_idea:
            jump ch3_explore_food_wing
        
        "Идти на первый этаж (Административное крыло)." if has_equipment_idea:
            jump ch3_explore_admin_wing

        "Вернуться к Художнику." if has_equipment_idea:
            jump ch3_ingredient_hunt

        "Вернуться в Холл":
            jump ch3_hall_explore
