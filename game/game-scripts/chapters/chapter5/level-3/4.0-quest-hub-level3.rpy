# --- ГЛАВА 5: КВЕСТ УРОВЕНЬ 3 ---

init python:
    Item_BlankChip = Item("blank_chip", _("Сервисный Чип"), _("Пустой чип без цифровой подписи."), "images/items/chip_blank.png")
    Item_ReagentA = Item("reagent_a", _("Ампула 'Цито-В'"), _("Красная ампула с биологически активной основой."), "images/items/flask_red.png")
    Item_ReagentB = Item("reagent_b", _("Ампула 'Ген-Связь'"), _("Синяя жидкость, холодная на ощупь."), "images/items/flask_blue.png")
    Item_Coolant = Item("coolant", _("Охлаждающая жидкость"), _("Охладитель из медробота. Заменит третий компонент для синтеза."), "images/items/flask_green.png")
    Item_BioSpray = Item("bio_spray", _("Биомаркер"), _("Синтезированный аэрозоль. Обманет любой ДНК-сканер корпорации."), "images/items/spray.png")
    Item_AdminChip = Item("admin_chip", _("Чип Администратора"), _("Обладает высшим уровнем доступа 'Омега'."), "images/items/chip_admin.png")
    Item_ReagentD = Item("reagent_d", _("Реагент-D"), _("Био-связующий катализатор из диспенсера."), "images/items/flask_purple.png")
    Item_Mop = Item("mop", _("Швабра"), _("Прочная техническая швабра с металлической ручкой."), "images/items/mop.png")
    Item_EmptySpray = Item("empty_spray", _("Пустой распылитель"), _("Лабораторный баллончик-аэрозоль без содержимого."), "images/items/spray.png")

label ch5_level3_main_hall:
    scene ch05_bg11_v01 with dissolve
    play music "music/BGM/Caduceus.mp3" loop volume 0.25
    
    narrator """
        Уровень 3. Стерильные белые коридоры, резкий медицинский свет.

        Сюда допускался только научный персонал уровня 'Бета' и выше.
    """

label ch5_level3_main_hall_menu:
    scene ch05_bg11_v01
    
    menu:
        "Осмотреться":
            narrator """
                Прямо по курсу – 'Отдел Исследований'. Огромные стеклянные двери.

                Слева – Травматология.

                Справа – Медицинский блок. Судя по указателям, из Медбея можно попасть в отделы Генетики и Вирусологии.

                Где-то дальше по коридору, за Отделом Исследований, находятся серверная и лаборатория Робототехники.
            """

            $ ch5_level3_examined = True

            if ch5_yellow_alert_known:
                narrator "На стене мерцает жёлтый индикатор тревоги. Указатель к Монорельсу ведёт за Отдел Исследований, в противоположном направлении от серверной."
            jump ch5_level3_main_hall_menu
            
        "Пойти в Отдел Исследований" if ch5_level3_examined:
            jump ch5_level3_research
            
        "Зайти в Травматологию" if ch5_level3_examined:
            if getattr(store, 'ch5_trauma_unlocked_from_inside', False):
                jump ch5_level3_trauma
            else:
                neon "Дверь заблокирована изнутри. Судя по карте, есть обходной путь через Медицинский блок."
                jump ch5_level3_main_hall_menu
            
        "Зайти в Медицинский блок" if ch5_level3_examined:
            jump ch5_level3_medbay

        "Зайти в Отдел Кадров" if ch5_level3_examined:
            jump ch5_level3_hop_office
            
        "Пройти в дальний холл" if ch5_level3_examined:
            jump ch5_level3_inner_hall

# --- ДАЛЬНИЙ ХОЛЛ (Робототехника и Серверная) ---
label ch5_level3_inner_hall:
    if not getattr(store, 'ch5_medbay_door_glitching_seen', False):
        $ store.ch5_inner_hall_visited_before_glitch = True
    
    if getattr(store, 'ch5_level3_mop_taken', False):
        scene ch05_bg15_v02 with dissolve
    else:
        scene ch05_bg15_v01 with dissolve
    
    narrator "Здесь освещение было приглушенным. В конце коридора виднелась гигантская укрепленная дверь Серверной."
    
label ch5_level3_inner_hall_menu:
    if getattr(store, 'ch5_level3_mop_taken', False):
        scene ch05_bg15_v02 with dissolve
    else:
        scene ch05_bg15_v01 with dissolve
    menu:
        "Зайти в лабораторию Робототехники":
            jump ch5_level3_robotics
            
        "Осмотреть швабру на полу" if getattr(store, 'ch5_medbay_door_glitching_seen', False) and not has_item("mop") and not getattr(store, 'ch5_level3_mop_taken', False):
            if getattr(store, 'ch5_inner_hall_visited_before_glitch', False):
                neon "Раньше я не замечала швабру, валяющуюся на полу, но теперь, когда я на неё смотрю, она будет идеальной подпоркой для двери в лабораторию с синтезатором."
            else:
                neon "О, эта швабра идеально подойдет для подпорки. Идеально."
            $ add_item(Item_Mop)
            $ store.ch5_level3_mop_taken = True
            jump ch5_level3_inner_hall_menu
            
        "Подойти к дверям Серверной":
            if ch5_server_unlocked:
                narrator "Двери Серверной открыты. Жёлтый индикатор на раме сменился зелёным. Меня ждёт конечная цель."
                menu:
                    "Войти в Серверную":
                        call chapter5_after_quest from _call_chapter5_after_quest
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
