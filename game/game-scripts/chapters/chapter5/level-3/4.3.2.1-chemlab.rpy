# --- ВНУТРЕННОСТЬ ХИМЛАБОРАТОРИИ ---

label ch5_level3_medbay_chemlab:
    scene ch05_cg43_v01 with dissolve
    
    narrator "Стерильный бокс Химической лаборатории. Вокруг разбросаны разбитые колбы, а в центре стола тихо гудит автоматический синтезатор."
    
label ch5_level3_medbay_chemlab_menu:
    menu:
        "Использовать химический Синтезатор":
            scene ch05_cg42_v01 with dissolve
            if has_item("bio_spray"):
                narrator "Синтезатор уже завершил работу. Биомаркер получен."
                jump ch5_level3_medbay_chemlab_menu
            elif has_item("reagent_a") and has_item("reagent_b") and has_item("coolant") and has_item("reagent_d") and has_item("empty_spray"):
                menu:
                    "Синтезировать Биомаркер (Цито-В + Ген-Связь + Охладитель + Реагент-D -> Заправить распылитель)":
                        $ remove_item("reagent_a")
                        $ remove_item("reagent_b")
                        $ remove_item("coolant")
                        $ remove_item("reagent_d")
                        $ remove_item("empty_spray")
                        # TODO: missing audio: play sound "sfx/chemical_mix.opus"
                        narrator "Аппарат пришел в движение. Колбы завращались, смешивая синюю и красную основы. Промышленный охладитель не дает смеси закипеть, а фиолетовый Реагент-D надежно скрепляет ДНК-коннекторы."
                        narrator "Спустя несколько минут лоток выдачи открылся. Готовый биоактивный состав под давлением заправился в присоединенный медицинский распылитель."
                        $ add_item(Item_BioSpray)
                        neon "{=thoughts}Биомаркер готов! Он идеально имитирует ДНК Главврача.{/thoughts}"
                        jump ch5_level3_medbay_chemlab_menu
                    "Уйти":
                        jump ch5_level3_medbay_chemlab_menu
            else:
                if not has_item("empty_spray"):
                    neon "{=thoughts}Синтезатор ожидает ввода четырех активных компонентов и пустой емкости для распыления. Мне нужны: биологическая основа, связующий ДНК-протеин, мощный охладитель для термостабилизации, специальный связующий катализатор и пустой баллончик-распылитель, чтобы заправить готовый состав...{/thoughts}"
                else:
                    neon "{=thoughts}Синтезатор ожидает ввода четырех активных компонентов. По схеме мне нужны: биологическая основа, связующий ДНК-протеин, мощный охладитель для термостабилизации и специальный связующий катализатор...{/thoughts}"
                jump ch5_level3_medbay_chemlab_menu
                
        "Вернуться в Левый коридор":
            jump ch5_level3_medbay_left_corridor
