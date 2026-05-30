# --- ГЛАВА 5: КВЕСТ УРОВЕНЬ 3 ---

init python:
    Item_BlankChip = Item("blank_chip", "Сервисный Чип", "Пустой чип без цифровой подписи.", "images/items/chip_blank.png")
    Item_ReagentA = Item("reagent_a", "Ампула 'Цито-В'", "Красная ампула с биологически активной основой.", "images/items/flask_red.png")
    Item_ReagentB = Item("reagent_b", "Ампула 'Ген-Связь'", "Синяя жидкость, холодная на ощупь.", "images/items/flask_blue.png")
    Item_Coolant = Item("coolant", "Охлаждающая жидкость", "Охладитель из медробота. Заменит третий компонент для синтеза.", "images/items/flask_green.png")
    Item_BioSpray = Item("bio_spray", "Биомаркер", "Синтезированный аэрозоль. Обманет любой ДНК-сканер корпорации.", "images/items/spray.png")
    Item_AdminChip = Item("admin_chip", "Чип Администратора", "Обладает высшим уровнем доступа 'Омега'.", "images/items/chip_admin.png")

label ch5_level3_main_hall:
    scene chapter5-test-hublevel3 with dissolve
    play music "music/BGM/Heist_Tension_Low.opus" loop volume 0.3
    
    narrator """
        Уровень 3. Стерильные белые коридоры, резкий медицинский свет.
        Сюда допускался только научный персонал уровня 'Бета' и выше.
    """

label ch5_level3_main_hall_menu:
    scene chapter5-test-hublevel3
    
    menu:
        "Осмотреться":
            narrator """
                Прямо по курсу – 'Отдел Исследований'. Огромные стеклянные двери.

                Слева – Травматология.

                Справа – Медицинский блок (Медбей). Судя по указателям, из Медбея можно попасть в отделы Генетики и Вирусологии.

                Где-то дальше по коридору, за Отделом Исследований, находятся серверная и лаборатория Робототехники.
            """

            $ ch5_level3_examined = True

            if ch5_yellow_alert_known:
                narrator "На стене мерцает жёлтый индикатор тревоги. Указатель к Монорельсу ведёт за Отдел Исследований, в противоположном направлении от серверной."
            jump ch5_level3_main_hall_menu
            
        "Пойти в Отдел Исследований" if ch5_level3_examined:
            jump ch5_level3_research
            
        "Зайти в Травматологию" if ch5_level3_examined:
            jump ch5_level3_trauma
            
        "Зайти в Медицинский блок" if ch5_level3_examined:
            jump ch5_level3_medbay

        "Зайти в Отдел Кадров" if ch5_level3_examined:
            jump ch5_level3_hop_office
            
        "Пройти в дальний холл" if ch5_level3_examined:
            jump ch5_level3_inner_hall

# --- ДАЛЬНИЙ ХОЛЛ (Робототехника и Серверная) ---
label ch5_level3_inner_hall:
    scene bg space_station_rnd_corridor with dissolve
    
    narrator "Здесь освещение было приглушенным. В конце коридора виднелась гигантская укрепленная дверь Серверной."
    
label ch5_level3_inner_hall_menu:
    menu:
        "Зайти в лабораторию Робототехники":
            jump ch5_level3_robotics
            
        "Подойти к дверям Серверной":
            if ch5_server_unlocked:
                narrator "Двери Серверной открыты. Жёлтый индикатор на раме сменился зелёным. Меня ждёт конечная цель."
                menu:
                    "Войти в Серверную":
                        call chapter5_after_quest
                    "Вернуться":
                        jump ch5_level3_inner_hall_menu
            else:
                if not ch5_yellow_alert_known:
                    # Первый подход — узнаём о жёлтой тревоге
                    narrator "Тяжелая бронированная дверь. Я попыталась приложить свой ID к считывателю."
                    
                    play sound "sfx/alarm_klaxon_single.opus"
                    
                    narrator """
                        Панель мигнула жёлтым. На экране появилось сообщение:

                        'ВНИМАНИЕ. Станция находится в режиме ТИХОЙ ЖЁЛТОЙ ТРЕВОГИ (Код: Карантин-7).
                        
                        Доступ к критическим системам заблокирован по протоколу безопасности.
                        
                        Стыковка внешних кораблей запрещена до снятия тревоги.
                        
                        Для экстренного доступа обратитесь к Ядру Коммуникации ИИ.'
                    """
                    
                    $ ch5_yellow_alert_known = True
                    
                    neon """
                        {=thoughts}Жёлтая тревога... Карантин. Вот почему 'Эреб' дрейфует снаружи и не может пристыковаться!
                        
                        {=thoughts}А серверная заблокирована на уровне бортового ИИ станции. Никакой мультитул это не вскроет.
                        
                        {=thoughts}'Ядро Коммуникации ИИ'... Это должно быть где-то на станции. Может, СИВИЛЛА в Отделе Исследований знает, где оно.
                    """
                    jump ch5_level3_inner_hall_menu
                else:
                    narrator "Дверь серверной по-прежнему заблокирована жёлтой тревогой. Мне нужно добраться до Ядра Коммуникации ИИ и снять блокировку."
                    jump ch5_level3_inner_hall_menu
                
        "Вернуться в главный коридор 3 Уровня":
            jump ch5_level3_main_hall_menu
