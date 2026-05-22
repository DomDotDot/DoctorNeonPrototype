label ch5_level2_elevator:
    scene ch05_bg07_v01 with fade
    
    if ch5_elevator_powered:
        narrator "Лифт работает. Индикаторы горят зеленым."
        menu:
            "Ехать на Уровень 3":
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