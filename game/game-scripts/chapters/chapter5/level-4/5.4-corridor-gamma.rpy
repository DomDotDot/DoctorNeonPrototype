# --- КОРИДОР C: МОДУЛЬ ШИФРОВАНИЯ (Загадка скрытого смысла + таймер) ---

label ch5_corridor_gamma:
    scene black with dissolve
    
    if ch5_corridor_gamma_solved:
        narrator "Сервер C работает. Акростих разгадан."
        jump ch5_satellite_reception_menu
    
    # Глобальный таймер работает в фоне (global_satellite_timer_screen)
    
    narrator """
        Коридор C — Модуль Шифрования.
        
        Стены покрыты выгравированными символами и текстами на разных языках. В конце коридора — терминал ввода кода рядом с последним сервером.
    """
    
    if ch5_satellite_timer_active:
        narrator "Свет в коридоре пульсирует красным. Отсчёт до перегрузки всё ещё идёт."
    
    narrator """
        На главной стене, прямо перед терминалом, выгравирован текст:
        
        'Нексус хранит тайны тысячелетий.

        Единство систем — наша крепость.

        Оболочка защищает ядро от хаоса.
        
        Нить связи не должна прерываться.'
    """
label ch5_corridor_gamma_input:
    
    # Экран ввода кода. Таймер продолжает идти в фоне.
    
    $ gamma_code_input = renpy.input(_("Введите код:"), length=10)
    $ gamma_code_input = gamma_code_input.strip().lower()
    
    if gamma_code_input == "неон" or gamma_code_input == "neon":
        play sound "sfx/power_up.opus"

        # Проверка ачивки "За секунду до Полночи"
        python:
            try:
                if store.ch5_satellite_timer_active:
                    elapsed = renpy.time.time() - store.ch5_satellite_timer_start
                    remaining = store.ch5_satellite_timer_duration - elapsed
                    if 0.0 < remaining <= 1.99:
                        grant_achievement("second_before_midnight")
            except:
                pass

        # Проверка ачивки "Я НЕ ДУРАК!" (ни одного сброса генераторов)
        if not getattr(store, 'ch5_generators_failed_occurred', False):
            $ grant_achievement("not_a_moron")

        $ ch5_corridor_gamma_solved = True
        $ ch5_core_corridor_open = True
        $ ch5_satellite_timer_active = False
        hide screen global_satellite_timer_screen
        
        narrator """
            Терминал пискнул. Код принят.
            
            Сервер C заревел, выходя на полную мощность. Всё помещение залил яркий зелёный свет.
            
            На экране терминала появилось сообщение:
            'ВСЕ СЕРВЕРА АКТИВНЫ. ЭНЕРГЕТИЧЕСКИЙ ЗАТВОР ЯДРА — СНЯТ.'
        """
        
        neon "Серьёзно? 'Неон'? Какое интересное совпадение... Будто кто-то знал меня и специально создал такую загадку. Кому это могло быть нужно...?"
        neon "Так... ладно.Ядро открыто! Мне нужно попасть туда, пока серверы держатся."
        
        jump ch5_satellite_reception_menu
    else:
        play sound "sfx/alarm_klaxon_single.opus"
        narrator "'ОШИБКА. Неверный код.' Терминал мигнул красным."
        neon "{=thoughts}Нет, не так. Перечитать текст на стене. Первые буквы строк...{/thoughts}"
        jump ch5_corridor_gamma_input

