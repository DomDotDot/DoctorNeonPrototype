label ch3_long_corridor:
    scene bg chapter_3_long-hall-hall with fade
    play music "music/BGM/GreyPaint.opus" fadein 10.0 fadeout 10.0 volume 0.5
    narrator """
    Коридор за сдвинутой решеткой делал пологий изгиб и уходил вглубь заброшенного лабораторного корпуса.

    Здесь царило мертвое безмолвие. Слой пыли поглощал шорох моих шагов.

    Вдоль стен выстроились шеренги пустых металлических бочек из-под реактивов. Справа темнела тяжелая бронированная дверь со светящейся панелью кодового замка — вход в центральную химическую лабораторию.

    Дальше тянулись пустые помещения бывших диспетчерских, раздевалок и архивов.

    А из-под самой дальней двери в конце крыла пробивалась такая тонкая, теплая полоска света и пахло маслами.

    Там явно кто-то был.
    """

    menu ch3_explore_long_corridor:
        "Подойти к дальней двери, откуда тянет растворителем." if not has_equipment_idea:
            narrator "Я подошла к приоткрытой створке и тихо толкнула ее рукой."
            jump ch3_part2_the_cage

        "Осмотреть бронированную дверь химлаборатории.":
            if not chemlab_door_unlocked:
                narrator "На косяке тускло светится мембранная клавиатура электронного замка. Требуется четырехзначный код доступа."
                menu:
                    "Ввести код.":
                        if found_code_clue:
                            $ code_attempt = renpy.input(_("Введите четырехзначный код:"), length=4, allow="0123456789")
                            
                            if code_attempt == "1984":
                                narrator "Замок отозвался сухим щелчком, диод сменился на зеленый. Пароль Петрова подошел."
                                $ chemlab_door_unlocked = True
                                jump ch3_explore_long_corridor
                            else:
                                narrator "Индикатор мигнул красным, выдав протяжный зуммер ошибки."
                                jump ch3_explore_long_corridor
                        else:
                            neon "{=thoughts}Подбирать наугад бессмысленно. Где-то на объекте должна быть подсказка или пропуск персонала.{/thoughts}"
                            jump ch3_explore_long_corridor
                    
                    "Отойти от панели.":
                        jump ch3_explore_long_corridor
            else:
                narrator "Замок деактивирован. Дверь в химлабораторию разблокирована."
                jump ch3_explore_long_corridor

        "[s4!t]" if chemlab_door_unlocked:
            if has_equipment_idea:
                jump ch3_explore_chem_lab
            else:
                narrator "Сначала нужно выяснить, какие именно приборы и компоненты мне понадобятся."
                jump ch3_explore_long_corridor

        "Направиться в южное крыло (Пищевой цех)." if has_equipment_idea:
            jump ch3_explore_food_wing
        
        "Спуститься в административный корпус (Медпункт)." if has_equipment_idea:
            jump ch3_explore_admin_wing

        "Вернуться в мастерскую к Художнику." if has_equipment_idea:
            jump ch3_ingredient_hunt

        "Вернуться к решетке главного холла.":
            jump ch3_hall_explore