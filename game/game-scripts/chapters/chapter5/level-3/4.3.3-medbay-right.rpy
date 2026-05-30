# --- ПРАВОЕ КРЫЛО (РАДИОЛОГИЯ: КТ, МРТ, УЗИ) ---

label ch5_level3_medbay_right_corridor:
    scene bg space_station_medbay
    
    # Реплики навигации Неон
    if store.ch5_medbay_transition_used:
        $ store.ch5_medbay_transition_used = False
        if getattr(store, 'ch5_medbay_radiology_visited', False):
            neon "Я здесь уже была, я хожу кругами..."
        else:
            $ store.ch5_medbay_radiology_visited = True
    else:
        # Вошла с главного холла
        if getattr(store, 'ch5_medbay_radiology_visited', False) and not getattr(store, 'ch5_medbay_right_entered_from_main_hall', False):
            neon "Можно было попасть сюда с главного холла?"
        $ store.ch5_medbay_right_entered_from_main_hall = True
        $ store.ch5_medbay_radiology_visited = True

    narrator "Правый коридор Медбея. Отделение радиологии и внутренних болезней. Свет здесь тусклый, указатели ведут к кабинетам КТ, МРТ и УЗИ."
    
label ch5_level3_medbay_right_menu:
    menu:
        "Зайти в кабинет КТ (Компьютерная томография)":
            jump ch5_level3_medbay_ct_room
            
        "Зайти в кабинет МРТ (Магнитно-резонансная томография)":
            jump ch5_level3_medbay_mri_room
            
        "Зайти в кабинет УЗИ (Ультразвуковое исследование)":
            jump ch5_level3_medbay_ultrasound_room
            
        "Зайти в кабинеты врачей":
            narrator "Кабинеты терапевтов и радиологов. Вокруг лишь ряды пустых столов, папки с историями болезней и старые чашки."
            narrator "Я тщательно осмотрела шкафы и ящики, но ничего полезного здесь нет."
            jump ch5_level3_medbay_right_menu

        "Пройти налево по соединительному коридору (в Левое крыло)":
            $ store.ch5_medbay_transition_used = True
            jump ch5_level3_medbay_left_corridor

        "Вернуться в Главный холл":
            jump ch5_level3_medbay_main_hall

# --- КАБИНЕТ КТ ---
label ch5_level3_medbay_ct_room:
    scene bg space_station_medbay with dissolve
    narrator "Кабинет компьютерной томографии. Посреди комнаты возвышается массивное кольцо томографа КТ."
    
label ch5_level3_medbay_ct_menu:
    menu:
        "Запустить сканирование КТ через компьютер":
            play sound "sfx/hydraulic_release.opus"
            narrator "Кольцо томографа со свистом начало вращаться, ускоряясь. На экране управляющего компьютера побежали строки инициализации."
            narrator "Но через пару секунд вращение замедлилось, и на экране вспыхнула ошибка: 'ОШИБКА: ОБЪЕКТ СКАНИРОВАНИЯ ОТСУТСТВУЕТ. Съемка отменена'."
            neon "Ничего интересного. Пустой сканер просто крутится без дела."
            jump ch5_level3_medbay_ct_menu
            
        "Осмотреть сканер КТ":
            narrator "Крупное высокотехнологичное кольцо томографа. Платформа для пациента пуста и аккуратно задвинута. Внутри кольца ничего нет."
            jump ch5_level3_medbay_ct_menu
            
        "Назад в коридор":
            jump ch5_level3_medbay_right_corridor

# --- КАБИНЕТ УЗИ ---
label ch5_level3_medbay_ultrasound_room:
    scene bg space_station_medbay with dissolve
    narrator "Небольшой кабинет УЗИ. Здесь стоит портативный сканер и кушетка."
    
label ch5_level3_medbay_ultrasound_menu:
    menu:
        "Включить аппарат УЗИ":
            narrator "Экран аппарата УЗИ загорелся, но датчики выдают лишь мертвую рябь и белый шум."
            neon "Без живого пациента этот прибор бесполезен."
            jump ch5_level3_medbay_ultrasound_menu
            
        "Назад в коридор":
            jump ch5_level3_medbay_right_corridor

# --- КАБИНЕТ МРТ ---
label ch5_level3_medbay_mri_room:
    scene bg space_station_medbay with dissolve
    narrator "Кабинет МРТ. Огромный цилиндрический аппарат МРТ занимает всю стену. Рядом стоит терминал управления."
    
label ch5_level3_medbay_mri_menu:
    menu:
        "Попробовать запустить МРТ через компьютер":
            if store.ch5_medbay_mri_opened:
                narrator "Экран компьютера МРТ выдает предупреждение: 'ВНИМАНИЕ. Обнаружен посторонний металлический предмет в сканирующем контуре! Запуск заблокирован во избежание повреждения обмоток'."
                neon "Действительно, металлический биндер-зажим блокирует запуск прибора."
                jump ch5_level3_medbay_mri_menu
            else:
                narrator "Я нажала кнопку запуска на компьютере МРТ. Система пискнула и выдала ошибку:"
                narrator "'ОШИБКА ИНИЦИАЛИЗАЦИИ: КАПСУЛА ЗАБЛОКИРОВАНА. Аварийный замок активен. Системное подтверждение требуется на терминале Главного Врача'."
                neon "{=thoughts}МРТ не запускается. Похоже, нужно либо как-то включить его, либо открыть саму капсулу. Но капсула заблокирована на программном уровне.{/thoughts}"
                jump ch5_level3_medbay_mri_menu
                
        "Осмотреть капсулу МРТ":
            if not store.ch5_medbay_mri_unlocked:
                narrator "Круглая капсула томографа наглухо закрыта. Механический рычаг заблокирован электромагнитным фиксатором."
                neon "{=thoughts}Капсула заперта. Напрямую её не вскрыть. Нужно найти способ снять блокировку в терминале Главного Врача.{/thoughts}"
                jump ch5_level3_medbay_mri_menu
            else:
                if not store.ch5_medbay_mri_opened:
                    play sound "sfx/hydraulic_release.opus"
                    narrator "Магнитный замок отключен. Я нажала кнопку открытия, и капсула с тяжелым шипением отъехала в сторону."
                    $ store.ch5_medbay_mri_opened = True
                    jump ch5_level3_medbay_mri_menu
                else:
                    if not store.ch5_medbay_brochure_read:
                        narrator "Внутри открытой капсулы МРТ лежали разбросанные вещи. Но моё внимание привлек кое-какой предмет."
                        narrator "К мощному электромагниту томографа намертво, металлическим зажимом-биндером, прилипла папка с какими-то документами!"
                        narrator "Оторвать её руками невозможно. К счастью, папка раскрыта на нужной странице, и я могу прочитать текст."
                        narrator """
                            Текст научной брошюры:
                            
                            '...ВНИМАНИЕ НАУЧНОМУ ПЕРСОНАЛУ. Для стабилизации соединений белка 'Ген-Связь' и сыворотки 'Цито-В' в автоматическом химическом синтезаторе КАТЕГОРИЧЕСКИ запрещено использовать стандартные соли.
                            
                            Единственным полностью совместимым связующим реагентом является Реагент-D (Био-связующий катализатор), выдаваемый в автоматических настенных диспенсерах по коду допуска 04.'
                        """
                        $ store.ch5_medbay_brochure_read = True
                        neon "{=thoughts}Так вот почему МРТ было заблокировано — этот зажим-биндер прилип намертво и вызвал сбой! Но благодаря этому я теперь вижу, какой реагент отвечает за стабилизацию. Мне нужен Реагент-D из автомата в левом коридоре!{/thoughts}"
                        jump ch5_level3_medbay_mri_menu
                    else:
                        narrator "В открытой капсуле видна папка с брошюрой, намертво притянутая биндером к магниту."
                        jump ch5_level3_medbay_mri_menu
                        
        "Назад в коридор":
            jump ch5_level3_medbay_right_corridor
