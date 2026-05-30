# --- ОТДЕЛ КАДРОВ (HoP OFFICE) ---

init python:
    import random
    
    def generate_unique_pin(length=4):
        digits = list("0123456789")
        random.shuffle(digits)
        return "".join(digits[:length])
        
    def check_bulls_and_cows(secret, guess):
        bulls = 0
        cows = 0
        for i in range(len(secret)):
            if guess[i] == secret[i]:
                bulls += 1
            elif guess[i] in secret:
                cows += 1
        return bulls, cows

label ch5_level3_coolant_receive:

    narrator "По его шее пульсировали прозрачные трубки с густой зелёной жидкостью — мощным промышленным охладителем."
    neon "{=thoughts}Это та самая жидкость, которую я видела у сломанного медробота. Синтезатор в Медбее требует охладитель для реакции. Эта жидкость идеально подойдёт... И чтобы её забрать, мне не нужен талон.{/thoughts}"
    menu:
        "Вырвать трубку охлаждения у Автоматона":
            play sound "sfx/glass_shatter.opus"
            narrator "Я резким движением пробила стекло своей силой и вцепилась в толстую трубку на шее робота. Стекло разлетелось на куски, будто это были лепестки, а я с силой дернула трубку на себя."
            "Автоматон" "ВНИМАНИЕ. НАНЕСЕН УЩЕРБ ИМУЩЕСТВУ КОМПАНИИ. ПРОТОКОЛ ЗАЩИТЫ..."
            play sound "sfx/hydraulic_release.opus"
            narrator "Но я рванула со всей силы. Трубка с треском оборвалась. Автоматон задергался, заискрил и медленно осел на стол, издав протяжный механический писк."
            narrator "Я быстро подставила пустую колбу под льющуюся зеленую жидкость."
            $ add_item(Item_Coolant)
            $ store.ch5_hop_coolant_received = True
            neon "Извини, приятель. Очередь слишком длинная."
        "Не трогать":
            neon "{=thoughts}Пока не буду его ломать.{/thoughts}"
            # fall through to ch5_hop_menu
return

label ch5_level3_hop_office:
    scene bg space_station_office with dissolve
    
    narrator "Отдел Кадров. Просторное помещение с рядами пустых кресел для ожидания. В дальнем конце, за пуленепробиваемым стеклом, неподвижно сидела фигура."
    
    if not hasattr(store, 'ch5_hop_ticket'):
        $ store.ch5_hop_ticket = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + "-" + str(random.randint(10, 99))
        $ store.ch5_hop_current_ticket = "A-01"
        $ store.ch5_hop_pin = generate_unique_pin()
        $ store.ch5_hop_hacked = False
        $ store.ch5_hop_chip_received = False
        $ store.ch5_hop_coolant_received = False

    if ch5_hop_coolant_received:
        narrator "За стеклом валялся искрящийся Автоматон с вырванными трубками. Больше он никого не обслужит."
        jump ch5_level3_inner_hall_menu

    if store.ch5_hop_chip_received and not store.ch5_hop_coolant_received and getattr(store, 'ch5_coolant_idea_unlocked', False):
        narrator "Я снова подошла к окну Автоматона."
        call ch5_level3_coolant_receive from _call_ch5_level3_coolant_receive
                
label ch5_hop_menu:
    if not store.ch5_hop_coolant_received:
        narrator "Над окном висело электронное табло. Текущий талон: [store.ch5_hop_current_ticket]."

    menu:
        "Подойти к окну Автоматона":
            if store.ch5_hop_coolant_received:
                narrator "Он сломан."
                jump ch5_hop_menu
                
            narrator "За стеклом сидел сервисный Автоматон устаревшей модели. Его стеклянные глаза пусто смотрели сквозь меня."
            
            if store.ch5_hop_chip_received and not store.ch5_hop_coolant_received:
                if getattr(store, 'ch5_coolant_idea_unlocked', False):
                    call ch5_level3_coolant_receive from _call_ch5_level3_coolant_receive_1
                else:
                    "Автоматон" "Ваш запрос уже обработан. Следующий!"
            elif store.ch5_hop_hacked:
                "Автоматон" "Талон [store.ch5_hop_ticket]. Пройдите к кассе... то есть, окну. Тип обращения?"
                neon "Запрос на повышение уровня доступа до чипа Администратора."
                
                if not getattr(store, 'ch5_hop_ticket_correct', True):
                    "Автоматон" "Внимание. Ваш текущий запрос не совпадает с темой выданного талона. В обслуживании отказано. Пожалуйста, возьмите новый талон."
                    neon "Серьёзно?! Ты же просто железка без эмоций!"
                    "Автоматон" "Порядок есть порядок. Следующий!"
                    narrator "Мне придется делать всё это заново..."
                    $ store.ch5_hop_ticket_taken = False
                    $ store.ch5_hop_hacked = False
                    $ store.ch5_hop_ticket = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + "-" + str(random.randint(10, 99))
                    $ store.ch5_hop_pin = generate_unique_pin()
                else:
                    "Автоматон" "Обработка запроса... Подождите."
                    play sound "sfx/printer_buzz.opus"
                    narrator "Из щели под стеклом с тихим щелчком выскочил Чип Администратора с высшей сигнатурой."
                    $ add_item(Item_AdminChip)
                    $ store.ch5_hop_chip_received = True
                    neon "{=thoughts}Отлично. Чип Администратора у меня. Теперь можно открыть кабинет главврача в Медбее!{/thoughts}"
                    $ store.ch5_hop_hacked = False
                    $ store.ch5_hop_ticket_taken = False
                    
                    call ch5_level3_coolant_receive from _call_ch5_level3_coolant_receive_2
            else:
                "Автоматон" "Пожалуйста, возьмите талон в терминале и ожидайте своей очереди."
                neon "Но тут больше никого нет!"
                "Автоматон" "Компания 'Гелиос' заботится о своих сотрудниках. Даже если сейчас никого нет, пожалуйста, следуйте процедурам."
                "Автоматон" "Сейчас обслуживается талон: [store.ch5_hop_current_ticket]." 
            jump ch5_hop_menu
            
        "Взять талон в терминале" if not getattr(store, 'ch5_hop_ticket_taken', False):
            if store.ch5_hop_coolant_received:
                narrator "Мне больше не нужны талоны."
                jump ch5_hop_menu

            narrator "Экран терминала выдал 5 вариантов темы запроса."
            menu:
                "Оформление отпуска":
                    $ store.ch5_hop_ticket_correct = False
                "Выдача дубликата пустого сервисного чипа":
                    $ store.ch5_hop_ticket_correct = False
                "Жалоба на условия труда":
                    $ store.ch5_hop_ticket_correct = False
                "Запрос на повышение уровня доступа":
                    $ store.ch5_hop_ticket_correct = True
                "Увольнение по собственному желанию":
                    $ store.ch5_hop_ticket_correct = False
                    
            play sound "sfx/ticket_print.opus"
            narrator "Терминал с жужжанием выдал мне талон."
            narrator "На нём было напечатано: '[store.ch5_hop_ticket]'."
            neon "{=thoughts}Серьёзно? Если сейчас обслуживают другой талон, мне придётся ждать вечность!{/thoughts}"
            $ store.ch5_hop_ticket_taken = True
            jump ch5_hop_menu
            
        "Модифицировать электронное табло очереди" if getattr(store, 'ch5_hop_ticket_taken', False) and not store.ch5_hop_hacked:
            
            narrator "Я подошла к управляющему терминалу табло. Экран заблокирован 4-значным PIN-кодом."
            neon "{=thoughts}Система диагностики откликается. Я могу попытаться подобрать код перехватом сигналов.{/thoughts}"
            narrator "Правила дешифровки: 4 уникальные цифры. 'Бык' — цифра угадана и на своём месте. 'Корова' — цифра угадана, но не на своём месте."
            
            label ch5_hop_minigame:
                $ player_guess = renpy.input(_("Введите 4 уникальные цифры (или 'exit' для выхода):"), length=4, allow="0123456789").strip()
                
                if player_guess.lower() == 'exit':
                    jump ch5_hop_menu
                    
                if len(player_guess) != 4 or not player_guess.isdigit() or len(set(player_guess)) != 4:
                    narrator "Ошибка ввода. Требуется ровно 4 УНИКАЛЬНЫЕ цифры."
                    jump ch5_hop_minigame
                    
                $ b_count, c_count = check_bulls_and_cows(store.ch5_hop_pin, player_guess)
                
                if b_count == 4:
                    play sound "sfx/access_granted_chime.opus"
                    narrator "Доступ разрешен. Режим администратора активирован."
                    narrator "Я вручную ввела свой номер талона: [store.ch5_hop_ticket]."
                    play sound "sfx/ding_ding.opus"
                    $ store.ch5_hop_current_ticket = store.ch5_hop_ticket
                    $ store.ch5_hop_hacked = True
                    narrator "Табло мигнуло и высветило мой номер. По всему залу раздался приятный женский голос: 'Талон [store.ch5_hop_ticket], пройдите к окну'."
                    jump ch5_hop_menu
                else:
                    play sound "sfx/error_buzz.opus"
                    narrator "Результат дешифровки: Быки: [b_count], Коровы: [c_count]."
                    jump ch5_hop_minigame
                    
        "Отойти в коридор":
            jump ch5_level3_main_hall_menu
