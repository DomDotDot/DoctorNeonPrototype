# --- ТАЙМЕР ИСТЁК ---
label ch5_satellite_timer_expired:
    hide screen global_satellite_timer_screen
    play sound "sfx/alarm_klaxon_single.opus"
    
    narrator """
        Потолок залил тревожный красный свет. Из динамиков раздался механический голос:
        
        'ПЕРЕГРУЗКА СЕРВЕРОВ. СБРОС СИСТЕМ. ПОВТОРИТЕ ПРОЦЕДУРУ АКТИВАЦИИ.'
    """
    
    $ ch5_satellite_timer_active = False
    $ ch5_corridor_alpha_solved = False
    $ ch5_corridor_beta_solved = False
    $ ch5_corridor_gamma_solved = False
    $ ch5_core_corridor_open = False
    
    neon "Чёрт! Не успела. Сервера перезагрузились. Придётся начинать со второго коридора заново."
    
    jump ch5_satellite_reception_menu