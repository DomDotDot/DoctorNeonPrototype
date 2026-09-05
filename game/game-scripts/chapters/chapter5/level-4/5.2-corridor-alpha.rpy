# --- КОРИДОР А: МОДУЛЬ ПАТТЕРНОВ (Загадка последовательности) ---

init -1 python:
    import random

    GREEK_ALPHABET = [
        _("Альфа"), _("Бета"), _("Гамма"), _("Дельта"), _("Эпсилон"), _("Дзета"), 
        _("Эта"), _("Тета"), _("Йота"), _("Каппа"), _("Лямбда"), _("Мю"), 
        _("Ню"), _("Кси"), _("Омикрон"), _("Пи"), _("Ро"), _("Сигма"), 
        _("Тау"), _("Ипсилон"), _("Фи"), _("Хи"), _("Пси"), _("Омега")
    ]

    def ch5_generate_alpha_puzzle():
        patterns_db = [
            {"id": "consecutive", "desc": _("Выбор букв был последователен (по 1)"), "func": lambda s: [s, s+1, s+2, s+3, s+4]},
            {"id": "interval_3_2_3_2", "desc": _("Интервал чередовался: 3-2-3-2"), "func": lambda s: [s, s+3, s+5, s+8, s+10]},
            {"id": "interval_5", "desc": _("Интервал был 5 букв"), "func": lambda s: [s, s+5, s+10, s+15, s+20]},
            {"id": "fibonacci", "desc": _("Интервал увеличивался по Фибоначчи: 1-2-3-5"), "func": lambda s: [s, s+1, s+3, s+6, s+11]},
            {"id": "primes", "desc": _("Интервал следовал простым числам: 2-3-5-7"), "func": lambda s: [s, s+2, s+5, s+10, s+17]},
            {"id": "mirror", "desc": _("Интервал был зеркальным: 4-2-2-4"), "func": lambda s: [s, s+4, s+6, s+8, s+12]},
            {"id": "decreasing", "desc": _("Интервал убывал: 4-3-2-1"), "func": lambda s: [s, s+4, s+7, s+9, s+10]},
        ]
        
        # 25% шанс на случайный паттерн без понятного интервала
        is_random = random.random() < 0.25
        
        if not is_random:
            pat = random.choice(patterns_db)
            max_start = 23 - pat["func"](0)[-1]
            start = random.randint(0, max_start)
            seq = pat["func"](start)
            desc_correct = pat["desc"]
        else:
            diffs_to_avoid = [
                [1,1,1,1], [3,2,3,2], [5,5,5,5], 
                [1,2,3,5], [2,3,5,7], [4,2,2,4], [4,3,2,1]
            ]
            while True:
                seq = sorted(random.sample(range(0, 24), 5))
                diffs = [seq[i] - seq[i-1] for i in range(1, 5)]
                # Исключаем случайные попадания в наши паттерны
                if diffs in diffs_to_avoid:
                    continue
                break
            desc_correct = _("Не было определенного интервала")
            
        all_descriptions = [p["desc"] for p in patterns_db] + [_("Не было определенного интервала")]
        all_descriptions.remove(desc_correct)
        
        wrong_final_options = random.sample(all_descriptions, 3)
        final_options = wrong_final_options + [desc_correct]
        random.shuffle(final_options)
        
        rounds = []
        for i in range(5):
            correct_idx = seq[i]
            prev_idx = seq[i-1] if i > 0 else -1
            
            # Доступные неправильные варианты: те, что ДО предыдущего выбора, ИЛИ ПОСЛЕ правильного.
            # Таким образом правильный ответ всегда будет самым "ранним" в алфавите после предыдущего.
            available_wrong = [x for x in range(24) if x <= prev_idx or x > correct_idx]
            
            wrong_choices = random.sample(available_wrong, 3)
            choices_idx = wrong_choices + [correct_idx]
            random.shuffle(choices_idx)
            
            choices_text = [GREEK_ALPHABET[idx] for idx in choices_idx]
            correct_text = GREEK_ALPHABET[correct_idx]
            
            rounds.append({
                "choices": choices_text,
                "correct": correct_text
            })
            
        return rounds, desc_correct, final_options

label ch5_corridor_alpha:
    scene ch05_bg24_v01 with dissolve
    
    if getattr(store, "ch5_corridor_alpha_solved", False):
        narrator "Сервер A гудит стабильно. Терминал погашен. Здесь больше делать нечего."
        jump ch5_satellite_reception_menu
    
    narrator """
        Коридор A — Модуль Паттернов.
        
        Узкий проход, стены которого увешаны кабелями. У стены — массивный сервер.
        
        А на нем - один-единственный пульт управления с терминалом.
    """
    
    neon "{=thoughts}Всего один терминал... и экран просит ввести последовательность.{/thoughts}"
    
    narrator """
        На экране горит надпись: 'ПРОЦЕДУРА АЛИГНМЕНТА АКТИВИРОВАНА'.
        
        Ниже мелким шрифтом выведена памятка.
        (Справка: Альфа, Бета, Гамма, Дельта, Эпсилон, Дзета, Эта, Тета, Йота, Каппа, Лямбда, Мю, Ню, Кси, Омикрон, Пи, Ро, Сигма, Тау, Ипсилон, Фи, Хи, Пси, Омега)
        
        Также на экране мерцает инструкция: 'Выберите из предложенных вариантов ту букву, которая идет первой по алфавиту, УЧИТЫВАЯ ваш предыдущий выбор'.
    """
    
    $ ch5_alpha_rounds, ch5_alpha_correct_pattern, ch5_alpha_final_options = ch5_generate_alpha_puzzle()
    $ ch5_alpha_current_round = 0

label ch5_corridor_alpha_puzzle_loop:
    if ch5_alpha_current_round == 5:
        jump ch5_corridor_alpha_final_question
        
    $ current_round_data = ch5_alpha_rounds[ch5_alpha_current_round]
    $ c0 = current_round_data["choices"][0]
    $ c1 = current_round_data["choices"][1]
    $ c2 = current_round_data["choices"][2]
    $ c3 = current_round_data["choices"][3]
    $ correct_answer = current_round_data["correct"]
    
    narrator "Шаг [ch5_alpha_current_round + 1] из 5. Терминал предлагает четыре варианта:"
    
    menu:
        "[c0!t]":
            $ selected = c0
        "[c1!t]":
            $ selected = c1
        "[c2!t]":
            $ selected = c2
        "[c3!t]":
            $ selected = c3
        "Вернуться в ресепшен":
            jump ch5_satellite_reception_menu
            
    if selected == correct_answer:
        # TODO: missing audio: play sound "sfx/ui_click.opus"
        narrator "Выбор принят. Терминал переходит к следующему шагу."
        $ ch5_alpha_current_round += 1
        jump ch5_corridor_alpha_puzzle_loop
    else:
        # TODO: missing audio: play sound "sfx/alarm_klaxon_single.opus"
        narrator "СИСТЕМНАЯ ОШИБКА. Последовательность нарушена. Сброс алигнмента."
        # Генерация новой загадки при проигрыше, чтобы нельзя было подобрать перебором
        $ ch5_alpha_rounds, ch5_alpha_correct_pattern, ch5_alpha_final_options = ch5_generate_alpha_puzzle()
        $ ch5_alpha_current_round = 0
        jump ch5_corridor_alpha_puzzle_loop

label ch5_corridor_alpha_final_question:
    narrator """
        Ввод 5 символов завершен.
        
        На экране появилась финальная проверка: 'Анализ завершен. Опишите введенный паттерн'.
    """
    
    $ f0 = ch5_alpha_final_options[0]
    $ f1 = ch5_alpha_final_options[1]
    $ f2 = ch5_alpha_final_options[2]
    $ f3 = ch5_alpha_final_options[3]
    
    menu:
        "[f0!t]":
            $ selected_pattern = f0
        "[f1!t]":
            $ selected_pattern = f1
        "[f2!t]":
            $ selected_pattern = f2
        "[f3!t]":
            $ selected_pattern = f3
            
    if selected_pattern == ch5_alpha_correct_pattern:
        # TODO: missing audio: play sound "sfx/power_up.opus"
        narrator """
            Экран вспыхнул зеленым. Сервер A ожил с глубоким, вибрирующим гулом.
            
            Свет в коридоре усилился. На стене загорелась надпись: 'СЕРВЕР A — АКТИВЕН'.
        """
        $ ch5_corridor_alpha_solved = True
        
        neon "Один есть. Дальше — оставшиеся коридоры."
        jump ch5_satellite_reception_menu
    else:
        # TODO: missing audio: play sound "sfx/alarm_klaxon_single.opus"
        narrator "СИСТЕМНАЯ ОШИБКА. Неверный анализ паттерна. Полный сброс."
        $ ch5_alpha_rounds, ch5_alpha_correct_pattern, ch5_alpha_final_options = ch5_generate_alpha_puzzle()
        $ ch5_alpha_current_round = 0
        jump ch5_corridor_alpha_puzzle_loop
