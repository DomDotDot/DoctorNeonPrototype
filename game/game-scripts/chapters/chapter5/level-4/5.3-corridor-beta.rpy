# --- КОРИДОР B: МОДУЛЬ ЛОГИКИ (Загадка рычагов + ТАЙМЕР) ---

# Стили для футуристической панели управления
style beta_cyber_green_button:
    background Solid("#33cc6622")
    hover_background Solid("#33cc6644")
    padding (20, 12)
    align (0.5, 0.5)

style beta_cyber_green_button_text:
    color "#33cc66"
    hover_color "#ffffff"
    size 18
    bold True
    align (0.5, 0.5)

style beta_cyber_exit_button:
    background Solid("#444444")
    hover_background Solid("#666666")
    padding (20, 12)
    align (0.5, 0.5)

style beta_cyber_exit_button_text:
    color "#cccccc"
    hover_color "#ffffff"
    size 18
    bold True
    align (0.5, 0.5)

init python:
    def ch5_toggle_lever(lever_name):
        # Переключаем логическое состояние рычага
        if lever_name == "red":
            store.beta_lever_red = not store.beta_lever_red
        elif lever_name == "blue":
            store.beta_lever_blue = not store.beta_lever_blue
        elif lever_name == "yellow":
            store.beta_lever_yellow = not store.beta_lever_yellow
            
        renpy.play("sfx/multitool_click.opus", channel="sound")
        
        # Активация обратного отсчета при первом переключении любого рычага
        if (store.beta_lever_red or store.beta_lever_blue or store.beta_lever_yellow) and not store.ch5_satellite_timer_active:
            store.ch5_satellite_timer_active = True
            store.ch5_satellite_timer_start = renpy.time.time()
            store.ch5_satellite_timer_duration = 90.0
            renpy.show_screen("global_satellite_timer_screen")
            store.ch5_corridor_beta_show_timer_dialogue = True

# Экран панели управления рычагами
screen ch5_lever_puzzle_screen():
    modal True
    
    # Затемнение фона
    add Solid("#080c10ee")
    
    # Основная рамка пульта управления
    frame:
        align (0.5, 0.5)
        xysize (1000, 800)
        background Frame(Solid("#0d131aee"), 10, 10)
        padding (30, 30)
        
        vbox:
            spacing 20
            xfill True
            
            # Заголовок терминала
            vbox:
                spacing 5
                xalign 0.5
                text "РАСПРЕДЕЛИТЕЛЬНАЯ ПАНЕЛЬ: МОДУЛЬ ЛОГИКИ" color "#00f0ff" size 30 bold True xalign 0.5 outlines [(2, "#002b3d", 0, 0)]
                text "СТАТУС: ТРЕБУЕТСЯ СИНХРОНИЗАЦИЯ ЗАТВОРОВ" color "#ff9900" size 16 bold True xalign 0.5
            
            # Разделитель
            add Solid("#00f0ff44") ysize 2 xalign 0.5 xsize 900
            
            # Схема-легенда взаимосвязей затворов
            frame:
                background Solid("#121f2dee")
                padding (20, 15)
                xalign 0.5
                xsize 850
                vbox:
                    spacing 6
                    xalign 0.5
                    text "СХЕМА СОЕДИНЕНИЙ ДАТЧИКОВ ЗАТВОРОВ:" color "#00f0ff" size 14 bold True xalign 0.5
                    text "• КРАСНЫЙ РУБИЛЬНИК ────► Переключает затворы I и III" color "#ff4d4d" size 13 xalign 0.5
                    text "• СИНИЙ РУБИЛЬНИК ──────► Переключает затвор II" color "#3399ff" size 13 xalign 0.5
                    text "• ЖЁЛТЫЙ РУБИЛЬНИК ─────► Переключает затворы I и II" color "#e6b800" size 13 xalign 0.5
            
            # РУКАВА РЫЧАГОВ
            hbox:
                xalign 0.5
                spacing 90
                
                # КРАСНЫЙ РЫЧАГ
                vbox:
                    spacing 15
                    xsize 200
                    text "КРАСНЫЙ" color "#ff4d4d" size 16 bold True xalign 0.5
                    
                    button:
                        xysize (90, 250)
                        xalign 0.5
                        action [Function(ch5_toggle_lever, "red"), Return("lever_toggled")]
                        background Solid("#16222fee")
                        hover_background Solid("#203144ee")
                        
                        # Внутренний трек скольжения
                        add Solid("#ff4d4d33", xsize=8, ysize=210) align (0.5, 0.5)
                        
                        # Рукоятка левера
                        frame:
                            xysize (70, 36)
                            background Solid("#ff4d4d" if beta_lever_red else "#5c1d1d")
                            if beta_lever_red:
                                align (0.5, 0.08)
                            else:
                                align (0.5, 0.92)
                            add Solid("#ffffffcc", xsize=40, ysize=4) align (0.5, 0.5)
                
                # СИНИЙ РЫЧАГ
                vbox:
                    spacing 15
                    xsize 200
                    text "СИНИЙ" color "#3399ff" size 16 bold True xalign 0.5
                    
                    button:
                        xysize (90, 250)
                        xalign 0.5
                        action [Function(ch5_toggle_lever, "blue"), Return("lever_toggled")]
                        background Solid("#16222fee")
                        hover_background Solid("#203144ee")
                        
                        # Внутренний трек скольжения
                        add Solid("#3399ff33", xsize=8, ysize=210) align (0.5, 0.5)
                        
                        # Рукоятка левера
                        frame:
                            xysize (70, 36)
                            background Solid("#3399ff" if beta_lever_blue else "#143a5c")
                            if beta_lever_blue:
                                align (0.5, 0.08)
                            else:
                                align (0.5, 0.92)
                            add Solid("#ffffffcc", xsize=40, ysize=4) align (0.5, 0.5)
                
                # ЖЁЛТЫЙ РЫЧАГ
                vbox:
                    spacing 15
                    xsize 200
                    text "ЖЁЛТЫЙ" color "#e6b800" size 16 bold True xalign 0.5
                    
                    button:
                        xysize (90, 250)
                        xalign 0.5
                        action [Function(ch5_toggle_lever, "yellow"), Return("lever_toggled")]
                        background Solid("#16222fee")
                        hover_background Solid("#203144ee")
                        
                        # Внутренний трек скольжения
                        add Solid("#e6b80033", xsize=8, ysize=210) align (0.5, 0.5)
                        
                        # Рукоятка левера
                        frame:
                            xysize (70, 36)
                            background Solid("#e6b800" if beta_lever_yellow else "#5c4a00")
                            if beta_lever_yellow:
                                align (0.5, 0.08)
                            else:
                                align (0.5, 0.92)
                            add Solid("#ffffffcc", xsize=40, ysize=4) align (0.5, 0.5)
            
            # Разделитель
            add Solid("#00f0ff22") ysize 1 xalign 0.5 xsize 900
            
            # НИЖНИЕ КНОПКИ ДЕЙСТВИЙ
            hbox:
                xalign 0.5
                spacing 50
                
                textbutton "ДЁРНУТЬ ГЛАВНЫЙ РУБИЛЬНИК (ЗЕЛЁНЫЙ)" action Return("check_calibration") style "beta_cyber_green_button"
                textbutton "ВЕРНУТЬСЯ В РЕСЕПШЕН" action Return("abort") style "beta_cyber_exit_button"


label ch5_corridor_beta:
    scene black with dissolve
    
    if ch5_corridor_beta_solved:
        narrator "Сервер B работает. Рычаги зафиксированы в правильных позициях."
        jump ch5_satellite_reception_menu
    
    narrator """
        Коридор B — Модуль Логики.
        
        Более широкое помещение с низким потолком. В центре — панель управления с тремя массивными рычагами.
        
        Перед панелью — экран, отображающий схему:
    """
    
    narrator """
        Схема на экране:
        
        Три управляющих рычага (Красный, Синий, Жёлтый) и один главный рубильник (Зелёный).
        
        Красный рычаг: переключает затворы I и III
        Синий рычаг: переключает затвор II
        Жёлтый рычаг: переключает затворы I и II
        
        ВНИМАНИЕ. СИСТЕМА ДАТЧИКОВ ЗАТВОРОВ ПОВРЕЖДЕНА. 
        Текущий статус выводится только один раз при инициализации.
        
        Инициализация...
        Рычаги: Красный (ВНИЗ), Синий (ВНИЗ), Жёлтый (ВНИЗ).
        Затворы: Все 3 затвора ЗАКРЫТЫ.
        
        Цель: ОТКРЫТЬ ВСЕ ТРИ ЗАТВОРА. 
        Выставите рычаги в правильную комбинацию и подтвердите Зелёным рубильником.
        В случае ошибки — принудительный аппаратный сброс.
    """
    
    neon """
        {=thoughts}Логическая головоломка со сбросом. Если я нажму всё подряд и дёрну зелёный — придётся начинать сначала.
        
        Нужно продумать комбинацию заранее...
    """
    
    # Инициализируем переменные при входе
    $ beta_lever_red = False
    $ beta_lever_blue = False
    $ beta_lever_yellow = False
    $ store.ch5_corridor_beta_show_timer_dialogue = False
    
label ch5_corridor_beta_puzzle:
    
    # Вычисляем состояние затворов (для внутренней логики)
    $ beta_gate_I = (beta_lever_red != beta_lever_yellow)
    $ beta_gate_II = (beta_lever_blue != beta_lever_yellow)
    $ beta_gate_III = beta_lever_red
    
    # Вызываем экран с рычагами
    call screen ch5_lever_puzzle_screen
    $ res = _return
    
    # Обрабатываем событие запуска таймера
    if getattr(store, 'ch5_corridor_beta_show_timer_dialogue', False):
        $ store.ch5_corridor_beta_show_timer_dialogue = False
        play sound "sfx/alarm_klaxon_single.opus"
        narrator """
            В ту же секунду на экранах появилось мигающее красное предупреждение:
            'ВНИМАНИЕ: ПРОТОКОЛ ОБРАТНОГО ОТСЧЁТА АКТИВИРОВАН. 
            ПЕРЕГРУЗКА БАЗОВЫХ СЕРВЕРОВ ЧЕРЕЗ 90 СЕКУНД.
            ЗАВЕРШИТЕ АКТИВАЦИЮ СЕРВЕРОВ B И C.'
        """
        neon "Девяносто секунд?! Нужно торопиться!"
        
    # Обрабатываем действия кнопок экрана
    if res == "check_calibration":
        play sound "sfx/heavy_switch.opus"
        if beta_gate_I and beta_gate_II and beta_gate_III:
            play sound "sfx/power_up.opus"
            narrator """
                Все три затвора с грохотом открылись! Сервер B завибрировал и начал набирать мощность.
                
                Индикатор сменился на зелёный: 'СЕРВЕР B — АКТИВЕН'.
            """
            $ ch5_corridor_beta_solved = True
            $ store.ch5_corridor_beta_show_timer_dialogue = None
            neon "Второй готов! Остался только коридор C. Время поджимает!"
            jump ch5_satellite_reception_menu
        else:
            play sound "sfx/error_buzz.opus"
            # Физическая тряска экрана при сбое сброса!
            with vpunch
            narrator "'ОШИБКА КОНФИГУРАЦИИ. ПРИНУДИТЕЛЬНЫЙ СБРОС.' Затворы со скрежетом вернулись в исходное положение, а рычаги отщёлкнулись вниз."
            $ beta_lever_red = False
            $ beta_lever_blue = False
            $ beta_lever_yellow = False
            jump ch5_corridor_beta_puzzle
            
    elif res == "abort":
        jump ch5_satellite_reception_menu
        
    jump ch5_corridor_beta_puzzle
