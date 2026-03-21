# --- МЕДБЕЙ ---
label ch5_level3_medbay:
    scene bg space_station_medbay with dissolve
    
    narrator "Главная приемная медицинского блока. В центре комнаты стоял сложный хирургический синтезатор. Рядом находился терминал Главного Врача."
    
label ch5_level3_medbay_menu:
    menu:
        "Осмотреть терминал Главврача":
            if has_item("admin_chip"):
                narrator "Мне здесь больше нечего делать."
            else:
                narrator "Голоэкран терминала мерцал красным. 'Требуется биометрическое подтверждение ДНК Главного Врача'."
                if has_item("bio_spray") and has_item("blank_chip"):
                    menu:
                        "Распылить Биомаркер на сканер и применить Пустой чип":
                            $ remove_item("bio_spray")
                            $ remove_item("blank_chip")
                            play sound "sfx/spray_hiss.opus"
                            narrator "Я распылила аэрозоль на стекло сканера. Затем вставила пустой чип в разъем."
                            play sound "sfx/access_granted_chime.opus"
                            narrator "Терминал пискнул. 'ДНК подтверждено. Доступ уровня Омега предоставлен'."
                            neon "Отлично. Копирую профиль на чип."
                            $ add_item(Item_AdminChip)
                            jump ch5_level3_medbay_menu
                        "Вернуться":
                            jump ch5_level3_medbay_menu
                else:
                    neon "{=thoughts}ДНК сканер... Мне нужен способ обмануть его биодатчики. И пустой чип, чтобы записать допуск.{/thoughts}"
            jump ch5_level3_medbay_menu
            
        "Осмотреть синтезатор":
            if has_item("bio_spray"):
                narrator "Синтезатор уже использован. Биомаркер готов."
                jump ch5_level3_medbay_menu
            elif has_item("reagent_a") and has_item("reagent_b") and has_item("coolant"):
                menu:
                    "Смешать Цито-В, Ген-Связь и Охлаждающую жидкость":
                        $ remove_item("reagent_a")
                        $ remove_item("reagent_b")
                        $ remove_item("coolant")
                        play sound "sfx/chemical_mix.opus"
                        narrator "Аппарат загудел, смешивая компоненты. Охлаждающая жидкость была необходима для стабилизации реакции."
                        narrator "Через несколько мгновений в лотке появился маленький баллончик-спрей."
                        $ add_item(Item_BioSpray)
                        neon "{=thoughts}Биомаркер готов. Он обманет любой ДНК-сканер на станции.{/thoughts}"
                        jump ch5_level3_medbay_menu
                    "Уйти":
                        jump ch5_level3_medbay_menu
            else:
                neon "{=thoughts}Синтезатор ждет ввода компонентов. Судя по схеме, мне нужны: биологическая основа (Цито-В), связующий агент (Ген-Связь) и сильный охладитель, чтобы смесь не воспламенилась.{/thoughts}"
                jump ch5_level3_medbay_menu
                
        "Пройти в Вирусологию":
            jump ch5_level3_virology
            
        "Пройти в Генетику":
            jump ch5_level3_genetics
            
        "Вернуться в коридор":
            jump ch5_level3_main_hall_menu