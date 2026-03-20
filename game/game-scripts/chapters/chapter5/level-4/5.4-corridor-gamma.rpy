# --- КОРИДОР C: МОДУЛЬ ШИФРОВАНИЯ (Загадка скрытого смысла + таймер) ---

label ch5_corridor_gamma:
    scene bg space_station_hos_office with dissolve
    
    if ch5_corridor_gamma_solved:
        narrator "Генератор C работает. Акростих разгадан."
        jump ch5_satellite_reception_menu
    
    # Проверяем таймер
    if ch5_satellite_timer_active:
        $ ch5_time_elapsed = renpy.time.time() - ch5_satellite_timer_start
        $ ch5_time_remaining = max(0, ch5_satellite_timer_duration - ch5_time_elapsed)
        $ ch5_time_remaining_int = int(ch5_time_remaining)
        
        if ch5_time_remaining <= 0:
            jump ch5_satellite_timer_expired
    
    narrator """
        Коридор C — Модуль Шифрования.
        
        Стены покрыты выгравированными символами и текстами на разных языках. В конце коридора — терминал ввода кода рядом с последним генератором.
    """
    
    if ch5_satellite_timer_active:
        narrator "На потолке мигает красный таймер: [ch5_time_remaining_int] секунд до перегрузки!"
    
    narrator """
        На главной стене, прямо перед терминалом, выгравирован текст:
        
        'Нексус хранит тайны тысячелетий.
        Единство систем — наша крепость.
        Оболочка защищает ядро от хаоса.
        Нить связи не должна прерываться.'
    """
    
    neon """
        {=thoughts}Первые буквы каждой строки... Н, Е, О, Н.
        
        'НЕОН'. Это... моё имя? Или совпадение?
        
        Не важно. Это код.{/thoughts}
    """

label ch5_corridor_gamma_input:
    
    # Проверяем таймер снова
    if ch5_satellite_timer_active:
        $ ch5_time_elapsed = renpy.time.time() - ch5_satellite_timer_start
        $ ch5_time_remaining = max(0, ch5_satellite_timer_duration - ch5_time_elapsed)
        $ ch5_time_remaining_int = int(ch5_time_remaining)
        
        if ch5_time_remaining <= 0:
            jump ch5_satellite_timer_expired
    
    $ gamma_code_input = renpy.input(_("Введите код (первые буквы строк):"), length=10)
    $ gamma_code_input = gamma_code_input.strip().lower()
    
    if gamma_code_input == "неон" or gamma_code_input == "neon":
        play sound "sfx/power_up.opus"
        
        narrator """
            Терминал пискнул. Код принят.
            
            Генератор C заревел, выходя на полную мощность. Всё помещение залил яркий зелёный свет.
            
            На экране терминала появилось сообщение:
            'ВСЕ ГЕНЕРАТОРЫ АКТИВНЫ. ЭНЕРГЕТИЧЕСКИЙ ЗАТВОР ЯДРА — СНЯТ.'
        """
        
        $ ch5_corridor_gamma_solved = True
        $ ch5_core_corridor_open = True
        $ ch5_satellite_timer_active = False
        
        neon "Ядро открыто! Мне нужно попасть туда, пока генераторы держатся!"
        
        jump ch5_satellite_reception_menu
    else:
        play sound "sfx/alarm_klaxon_single.opus"
        narrator "'ОШИБКА. Неверный код.' Терминал мигнул красным."
        neon "{=thoughts}Нет, не так. Перечитать текст на стене. Первые буквы строк...{/thoughts}"
        jump ch5_corridor_gamma_input

# --- ТАЙМЕР ИСТЁК ---
label ch5_satellite_timer_expired:
    play sound "sfx/alarm_klaxon_single.opus"
    
    narrator """
        Потолок залил тревожный красный свет. Из динамиков раздался механический голос:
        
        'ПЕРЕГРУЗКА ГЕНЕРАТОРОВ. СБРОС СИСТЕМ. ПОВТОРИТЕ ПРОЦЕДУРУ АКТИВАЦИИ.'
    """
    
    $ ch5_satellite_timer_active = False
    $ ch5_corridor_beta_solved = False
    $ ch5_corridor_gamma_solved = False
    $ ch5_core_corridor_open = False
    
    neon "Чёрт! Не успела. Генераторы сбросились. Придётся начинать со второго коридора заново."
    
    jump ch5_satellite_reception_menu
