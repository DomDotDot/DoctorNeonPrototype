# --- КОРИДОР А: МОДУЛЬ ПАТТЕРНОВ (Загадка последовательности) ---

label ch5_corridor_alpha:
    scene bg space_station_maintenance_tunnel with dissolve
    
    if ch5_corridor_alpha_solved:
        narrator "Генератор A гудит стабильно. Терминалы погашены. Здесь больше делать нечего."
        jump ch5_satellite_reception_menu
    
    narrator """
        Коридор A — Модуль Паттернов.
        
        Узкий проход, стены которого увешаны кабелями и трубами. В конце коридора — массивный генератор, покрытый индикаторами.
        
        Перед генератором — пять терминалов, расположенных полукругом. Каждый подсвечен своим цветом.
    """
    
    neon "{=thoughts}Пять терминалов. На каждом — символ. Нужно активировать их в правильном порядке.{/thoughts}"
    
    narrator """
        На экране каждого терминала — греческий символ:
        
        Терминал 1: Ωмега (Ω)
        Терминал 2: Αльфа (Α)
        Терминал 3: Γамма (Γ)
        Терминал 4: Βета (Β)
        Терминал 5: Δельта (Δ)
        
        Над генератором висела табличка:
        'Начало определяет конец. Порядок — это сила.'
    """
    
    neon "{=thoughts}Греческий алфавит... Начало определяет конец...{/thoughts}"
    
    # Простая последовательность: нужно нажать 5 кнопок в правильном порядке
    $ alpha_sequence = []
    $ alpha_correct = [2, 4, 3, 5, 1]  # Альфа(2), Бета(4), Гамма(3), Дельта(5), Омега(1)
    
label ch5_corridor_alpha_puzzle:
    
    $ alpha_progress = len(alpha_sequence)
    
    if alpha_progress == 5:
        if alpha_sequence == alpha_correct:
            play sound "sfx/power_up.opus"
            narrator """
                Все пять терминалов загорелись зелёным одновременно. Генератор ожил с глубоким, вибрирующим гулом.
                
                Свет в коридоре усилился. На стене вспыхнул индикатор: 'ГЕНЕРАТОР A — АКТИВЕН'.
            """
            $ ch5_corridor_alpha_solved = True
            neon "Один есть. Дальше — коридор B."
            jump ch5_satellite_reception_menu
        else:
            play sound "sfx/alarm_klaxon_single.opus"
            narrator "Терминалы мигнули красным и сбросились. Неправильная последовательность."
            $ alpha_sequence = []
            jump ch5_corridor_alpha_puzzle
    
    narrator "Нажато терминалов: [alpha_progress] из 5."
    
    menu:
        "Нажать Терминал 1 (Ω Омега)":
            $ alpha_sequence.append(1)
            jump ch5_corridor_alpha_puzzle
        "Нажать Терминал 2 (Α Альфа)":
            $ alpha_sequence.append(2)
            jump ch5_corridor_alpha_puzzle
        "Нажать Терминал 3 (Γ Гамма)":
            $ alpha_sequence.append(3)
            jump ch5_corridor_alpha_puzzle
        "Нажать Терминал 4 (Β Бета)":
            $ alpha_sequence.append(4)
            jump ch5_corridor_alpha_puzzle
        "Нажать Терминал 5 (Δ Дельта)":
            $ alpha_sequence.append(5)
            jump ch5_corridor_alpha_puzzle
        "Сбросить последовательность":
            $ alpha_sequence = []
            narrator "Все терминалы погасли. Начинаю заново."
            jump ch5_corridor_alpha_puzzle
        "Вернуться в ресепшен":
            $ alpha_sequence = []
            jump ch5_satellite_reception_menu
