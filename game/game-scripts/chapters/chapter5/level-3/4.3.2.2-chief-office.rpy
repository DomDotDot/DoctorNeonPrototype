# --- КАБИНЕТ ГЛАВВРАЧА ---

label ch5_level3_medbay_chief_office:
    scene ch05_cg37_v01 with dissolve
    
    if not store.ch5_medbay_chief_door_opened:
        narrator "Конец левого коридора. Тяжелая дверь из прочного матового стекла преграждает путь в кабинет Главного Врача. На панели считывателя горит надпись: 'ТРЕБУЕТСЯ ДОСТУП ОМЕГА'."
        if not store.ch5_medbay_blank_chip_taken:
            narrator "Но самое удивительное — прямо из паза считывателя торчит забытый кем-то белый пластиковый чип!"
        else:
            narrator "В считывателе пусто — я уже забрала отсюда белый пластиковый чип."
        
        label ch5_medbay_chief_locked_menu:
            menu:
                "Забрать чип из считывателя" if not store.ch5_medbay_blank_chip_taken:
                    $ add_item(Item_BlankChip)
                    $ store.ch5_medbay_blank_chip_taken = True
                    narrator "Я аккуратно вытащила чип. Это пустой Сервисный Чип без какой-либо цифровой подписи."
                    neon "{=thoughts}Кто-то в панике пытался вскрыть дверь кабинета чипом без прав, застрял и бежал, бросив его... В любом случае, пустой чип мне пригодится.{/thoughts}"
                    jump ch5_medbay_chief_locked_menu
                    
                "Применить Чип Администратора" if has_item("admin_chip"):
                    # TODO: missing audio: play sound "sfx/access_granted_chime.opus"
                    narrator "Я приложила Чип Администратора высшего доступа, полученный в Отделе Кадров. Считыватель пискнул приятным зеленым тоном, и стеклянная дверь бесшумно уехала в стену."
                    $ store.ch5_medbay_chief_door_opened = True
                    neon "Проход открыт. Посмотрим, что внутри."
                    jump ch5_level3_medbay_chief_office
                    
                "Вернуться в коридор":
                    jump ch5_level3_medbay_left_corridor
    else:
        scene ch05_cg44_v01 with fade
        narrator "Кабинет Главного Врача. Внутри царил образцовый порядок, контрастирующий с хаосом снаружи. На массивном столе ровно светится большой терминал управления."
            
        label ch5_medbay_chief_office_menu:
            scene ch05_cg44_v01
            menu:
                "Забрать пустой распылитель со стола" if not store.ch5_medbay_empty_spray_taken:
                    $ add_item(Item_EmptySpray)
                    $ store.ch5_medbay_empty_spray_taken = True
                    narrator "Я забрала со стола пустой лабораторный распылитель. Он идеально подойдет для биоактивного состава."
                    jump ch5_medbay_chief_office_menu

                "Осмотреть терминал Главврача":
                    if store.ch5_medbay_mri_unlocked:
                        narrator "Терминал уже выполнил свою роль. Капсула МРТ в кабинете радиологии разблокирована."
                        jump ch5_medbay_chief_office_menu
                    else:
                        menu:
                            "Разблокирвать капсулу Магнитно-Резонансного Томографа":
                                # TODO: missing audio: play sound "sfx/access_granted_chime.opus"

                                $ remove_item("blank_chip")
                                $ store.ch5_medbay_mri_unlocked = True

                                narrator "Экран пискнул: 'АВАРИЙНЫЙ МАГНИТНЫЙ ЗАМОК ТОМОГРАФА ОТКЛЮЧЕН. Капсула готова к ручному открытию'."
                                neon "Отлично! Капсула МРТ разблокирована. Теперь я смогу открыть её в Радиологии и осмотреть изнутри."
                                jump ch5_medbay_chief_office_menu
                            "Назад":
                                jump ch5_medbay_chief_office_menu
                                
                "Вернуться в коридор":
                    jump ch5_level3_medbay_left_corridor
