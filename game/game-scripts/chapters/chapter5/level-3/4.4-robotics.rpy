# --- РОБОТОТЕХНИКА ---

# Стили для премиального неонового интерфейса
style cyber_button:
    background Solid("#00f0ff22")
    hover_background Solid("#00f0ff44")
    insensitive_background Solid("#222222")
    padding (15, 10)
    xminimum 140
    align (0.5, 0.5)

style cyber_button_text:
    color "#00f0ff"
    hover_color "#ffffff"
    size 16
    bold True
    align (0.5, 0.5)

style cyber_button_pink:
    background Solid("#ff339922")
    hover_background Solid("#ff339944")
    insensitive_background Solid("#222222")
    padding (15, 10)
    xminimum 90
    align (0.5, 0.5)

style cyber_button_pink_text:
    color "#ff3399"
    hover_color "#ffffff"
    size 16
    bold True
    align (0.5, 0.5)

style cyber_action_button:
    background Solid("#00ff6633")
    hover_background Solid("#00ff6666")
    padding (20, 12)
    align (0.5, 0.5)

style cyber_action_button_text:
    color "#00ff66"
    hover_color "#ffffff"
    size 18
    bold True
    align (0.5, 0.5)

style cyber_exit_button:
    background Solid("#444444")
    hover_background Solid("#666666")
    padding (20, 12)
    align (0.5, 0.5)

style cyber_exit_button_text:
    color "#cccccc"
    hover_color "#ffffff"
    size 18
    bold True
    align (0.5, 0.5)

init python:
    def ch5_turn_hours(amount):
        # Вращение часов по кругу от 1 до 12
        store.ch5_clock_hours = (store.ch5_clock_hours + amount - 1) % 12 + 1
        renpy.play("sfx/multitool_click.opus", channel="sound")
        
    def ch5_turn_minutes(amount):
        # Вращение минут
        new_min = store.ch5_clock_minutes + amount
        if new_min >= 60:
            hours_change = new_min // 60
            store.ch5_clock_minutes = new_min % 60
            # Перевод часовой стрелки вперед
            store.ch5_clock_hours = (store.ch5_clock_hours + hours_change - 1) % 12 + 1
        elif new_min < 0:
            hours_change = (abs(new_min) + 59) // 60
            store.ch5_clock_minutes = (new_min % 60 + 60) % 60
            # Перевод часовой стрелки назад
            store.ch5_clock_hours = (store.ch5_clock_hours - hours_change - 1) % 12 + 1
        else:
            store.ch5_clock_minutes = new_min
        renpy.play("sfx/multitool_click.opus", channel="sound")

# Экран интерактивной калибровки гидравлики
screen ch5_hydraulic_puzzle_screen():
    modal True
    
    # Затемнение заднего плана
    add Solid("#080c10ee")
    
    # Основное окно терминала
    frame:
        align (0.5, 0.5)
        xysize (1000, 800)
        background Frame(Solid("#0d131aee"), 10, 10)
        padding (30, 30)
        
        vbox:
            spacing 25
            xfill True
            
            # Заголовок терминала
            vbox:
                spacing 5
                xalign 0.5
                text _("ГИДРАВЛИЧЕСКИЙ ТЕРМИНАЛ УПРАВЛЕНИЯ") color "#00f0ff" size 30 bold True xalign 0.5 outlines [(2, "#002b3d", 0, 0)]
                text _("СТАТУС: АВАРИЙНЫЙ ЗАЖИМ ГИДРАВЛИКИ") color "#ff3366" size 16 bold True xalign 0.5
            
            # Разделительная линия
            add Solid("#00f0ff44") ysize 2 xalign 0.5 xsize 900
            
            # ИНСТРУМЕНТ И ЦИФЕРБЛАТ
            fixed:
                xysize (360, 360)
                xalign 0.5
                
                # Задний фон циферблата
                frame:
                    background Solid("#121f2dee")
                    xysize (340, 340)
                    align (0.5, 0.5)
                    # Окантовка циферблата
                    add Solid("#00f0ff", xsize=340, ysize=4) align (0.5, 0.0)
                    add Solid("#00f0ff", xsize=340, ysize=4) align (0.5, 1.0)
                    add Solid("#00f0ff", xsize=4, ysize=340) align (0.0, 0.5)
                    add Solid("#00f0ff", xsize=4, ysize=340) align (1.0, 0.5)
                
                # Сетка прибора
                add Solid("#00f0ff11", xsize=1, ysize=300) align (0.5, 0.5)
                add Solid("#00f0ff11", xsize=300, ysize=1) align (0.5, 0.5)
                
                # Текстовые метки скрыты для удаления очевидных подсказок о часах
                
                # Вычисление углов стрелок
                # 30 градусов на час + 0.5 градуса за каждую минуту
                $ hour_angle = (store.ch5_clock_hours % 12) * 30 + store.ch5_clock_minutes * 0.5
                # 6 градусов на минуту
                $ minute_angle = store.ch5_clock_minutes * 6
                
                # ЧАСОВАЯ СТРЕЛКА (Короткая, толстая, голубая)
                add Solid("#00f0ff", xsize=8, ysize=90):
                    xpos 180
                    ypos 180
                    anchor (0.5, 1.0)
                    transform_anchor True
                    rotate hour_angle
                    subpixel True
                    
                # МИНУТНАЯ СТРЕЛКА (Длинная, тонкая, розовая)
                add Solid("#ff3399", xsize=4, ysize=130):
                    xpos 180
                    ypos 180
                    anchor (0.5, 1.0)
                    transform_anchor True
                    rotate minute_angle
                    subpixel True
                    
                # Центральная ось
                add Solid("#ffffff", xsize=14, ysize=14):
                    xpos 180
                    ypos 180
                    anchor (0.5, 0.5)
            
            # ИНФОРМАЦИОННАЯ ПАНЕЛЬ СТАТУСА
            if store.ch5_robotics_last_attempt is not None:
                frame:
                    background Solid("#ff33661a")
                    padding (15, 12)
                    xalign 0.5
                    xsize 800
                    vbox:
                        spacing 5
                        xfill True
                        if getattr(store, 'ch5_robotics_reset_occurred', False):
                            text _("АВАРИЙНЫЙ СБРОС: ПРЕВЫШЕН ЛИМИТ КАЛИБРОВКИ!") color "#ff3366" size 16 bold True xalign 0.5
                            text _("Калибровка сброшена. Зарегистрированное перед сбросом давление: [store.ch5_robotics_last_attempt] PSI") color "#ff99b2" size 14 xalign 0.5
                        else:
                            text _("КРИТИЧЕСКОЕ ОТКЛОНЕНИЕ ФАЗОВОГО ДАВЛЕНИЯ!") color "#ff3366" size 16 bold True xalign 0.5
                            text _("Зарегистрировано на датчиках: [store.ch5_robotics_last_attempt] PSI | Требуемый сдвиг: 314 PSI") color "#ff99b2" size 14 xalign 0.5
            else:
                frame:
                    background Solid("#00f0ff11")
                    padding (15, 12)
                    xalign 0.5
                    xsize 800
                    vbox:
                        spacing 5
                        xfill True
                        text _("СИСТЕМНЫЙ СТАТУС: ОЖИДАНИЕ СТАБИЛИЗАЦИИ") color "#00f0ff" size 15 bold True xalign 0.5
                        text _("Отрегулируйте механические вентили для балансировки давления по Пи-константе.") color "#a3f0ff" size 13 xalign 0.5
            
            # УПРАВЛЕНИЕ ВЕНТИЛЯМИ
            hbox:
                xalign 0.5
                spacing 80
                
                # ВЕНТИЛЬ А: ЧАСЫ
                vbox:
                    spacing 12
                    xsize 380
                    text _("Вентиль крупной калибровки\n(Коаксиальный сдвиг)") color "#00f0ff" size 15 bold True xalign 0.5 text_align 0.5
                    
                    hbox:
                        xalign 0.5
                        spacing 15
                        textbutton "↺ -1" action Function(ch5_turn_hours, -1) style "cyber_button"
                        textbutton "+1 ↻" action Function(ch5_turn_hours, 1) style "cyber_button"
                
                # ВЕНТИЛЬ B: МИНУТЫ
                vbox:
                    spacing 12
                    xsize 380
                    text _("Вентиль точной калибровки\n(Микрофазовая подстройка)") color "#ff3399" size 15 bold True xalign 0.5 text_align 0.5
                    
                    hbox:
                        xalign 0.5
                        spacing 10
                        textbutton "↺ -5" action Function(ch5_turn_minutes, -5) style "cyber_button_pink"
                        textbutton "-1" action Function(ch5_turn_minutes, -1) style "cyber_button_pink"
                        textbutton "+1" action Function(ch5_turn_minutes, 1) style "cyber_button_pink"
                        textbutton "+5 ↻" action Function(ch5_turn_minutes, 5) style "cyber_button_pink"

            # Разделительная линия
            add Solid("#00f0ff22") ysize 1 xalign 0.5 xsize 900
            
            # КНОПКИ ДЕЙСТВИЙ
            hbox:
                xalign 0.5
                spacing 40
                
                textbutton _("ПРИМЕНИТЬ КАЛИБРОВКУ") action Jump("ch5_robotics_check_calibration") style "cyber_action_button"
                textbutton _("ОТОЙТИ ОТ ТЕРМИНАЛА") action Jump("ch5_robotics_abort") style "cyber_exit_button"


label ch5_level3_robotics:
    scene ch05_bg17_v01 with dissolve
    
    narrator "Сборочный цех. На столах лежали недосообранные прототипы дронов охраны."
    
    if not hasattr(store, 'ch5_robotics_solved') or not ch5_robotics_solved:
        narrator "В дальней части комнаты огромный манипулятор завис над конвейером. В его железной хватке была зажата красная ампула — 'Цито-В'."
        if not ch5_is_biomarker_quest_active():
            neon "{=thoughts}Химический реагент 'Цито-В'... Но сейчас мне это не нужно, да и доставать её оттуда слишком хлопотно.{/thoughts}"
            jump ch5_level3_inner_hall_menu

        neon "Манипулятор заклинило на 'мертвой хватке'. Если я попытаюсь вырвать ампулу силой, она попросту лопнет."
        
        narrator "Я подошла к терминалу управления гидравликой."
        
        # Инициализируем переменные времени (полностью случайно на стрелках)
        if not hasattr(store, 'ch5_clock_hours') or store.ch5_clock_hours is None:
            $ store.ch5_clock_hours = renpy.random.randint(1, 12)
            $ store.ch5_clock_minutes = renpy.random.randint(0, 59)
            $ store.ch5_robotics_last_attempt = None
            
        label ch5_robot_puzzle:
            call screen ch5_hydraulic_puzzle_screen
            
        label ch5_robotics_check_calibration:
            $ current_pressure = store.ch5_clock_hours * 100 + store.ch5_clock_minutes
            if store.ch5_clock_hours == 3 and store.ch5_clock_minutes == 14:
                hide screen ch5_hydraulic_puzzle_screen
                play sound "sfx/hydraulic_release.opus"
                narrator "С громким шипением система сбросила давление. Манипулятор медленно разжал стальные пальцы."
                narrator "Ампула 'Цито-В' мягко упала на ленту конвейера."
                $ add_item(Item_ReagentA)
                $ ch5_robotics_solved = True
                
                # Чистим переменные после успешного прохождения
                $ store.ch5_clock_hours = None
                $ store.ch5_clock_minutes = None
                $ store.ch5_robotics_last_attempt = None
                $ store.ch5_robotics_fail_count = None
                $ store.ch5_robotics_reset_occurred = None
                jump ch5_level3_inner_hall_menu
            else:
                $ store.ch5_robotics_fail_count = getattr(store, 'ch5_robotics_fail_count', 0) + 1
                $ store.ch5_robotics_last_attempt = current_pressure
                play sound "sfx/error_buzz.opus"
                
                if store.ch5_robotics_fail_count % 2 == 0:
                    # Сброс на рандомные значения при каждой второй ошибке!
                    $ store.ch5_clock_hours = renpy.random.randint(1, 12)
                    $ store.ch5_clock_minutes = renpy.random.randint(0, 59)
                    $ store.ch5_robotics_reset_occurred = True
                    # Потрясем экран для анимации сброса!
                    with hpunch
                    narrator "КРИТИЧЕСКИЙ СБОЙ: Давление в системе нестабильно. Терминал сбросил калибровку вентилей на случайные значения!"
                else:
                    $ store.ch5_robotics_reset_occurred = False
                    
                jump ch5_robot_puzzle
                
        label ch5_robotics_abort:
            hide screen ch5_hydraulic_puzzle_screen
            jump ch5_level3_inner_hall_menu
    else:
        narrator "Манипулятор безвольно висит. Ампула 'Цито-В' уже у меня."
        jump ch5_level3_inner_hall_menu