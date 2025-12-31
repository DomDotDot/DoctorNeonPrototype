# Определим картинки-заглушки и стили
image oga_prof_img = "images/sprites/oganesson/oganesson shadowed.avif" # Замени на свои пути
image sera_prof_img = "images/sprites/seraphina/seraphina neutral.avif"
image unknown_prof_img = "images/sprites/illusion/illusion shadowed.avif"

# Основной экран
screen bio_menu():
    tag menu
    add "#0b1019" # Темно-синий фон как на скрине

    # Кнопка выхода
    textbutton "Закрыть":
        action Return()
        align (0.95, 0.05)
        text_color "#ffffff"

    hbox:
        align (0.5, 0.5)
        spacing 40
        ysize 900

        # --- ЛЕВАЯ КОЛОНКА: СПИСОК ПЕРСОНАЖЕЙ ---
        frame:
            background "#0f1623" # Чуть светлее фона
            xsize 300
            ysize 900
            padding (20, 20)

            viewport:
                mousewheel True
                draggable True
                scrollbars "vertical"
                
                vbox:
                    spacing 10
                    for char in all_bios:
                        if char.seen:
                            textbutton char.name:
                                action SetVariable("active_bio_char", char)
                                text_size 30
                                text_hover_color "#3498db"
                                text_selected_color "#3498db"
                                # Если этот персонаж выбран сейчас, красим
                                if active_bio_char == char:
                                    text_color "#3498db"
                                else:
                                    text_color "#888888"
                        else:
                            text "???" color "#444" size 30

        # --- ПРАВАЯ ЧАСТЬ: ИНФОРМАЦИЯ ---
        if active_bio_char:
            hbox:
                spacing 30
                
                # 1. АРТ ПЕРСОНАЖА
                frame:
                    background None
                    xsize 400 ysize 800
                    # Если мы не знаем имя (совсем не знакомы), показываем силуэт
                    if active_bio_char.name_known:
                        add active_bio_char.image_tag:
                            fit "contain"
                            yalign 1.0
                    else:
                        add "unknown_prof_img":
                            fit "contain"
                            yalign 1.0

                # 2. ТЕКСТОВАЯ ИНФОРМАЦИЯ (Скроллируемая зона)
                viewport:
                    mousewheel True
                    draggable True
                    scrollbars "vertical"
                    xsize 800
                    ysize 900
                    
                    vbox:
                        spacing 15
                        
                        # ЗАГОЛОВОК
                        hbox:
                            spacing 15
                            text active_bio_char.get_display_name() size 50 color "#3498db" bold True
                            text active_bio_char.get_display_gender() size 40 color "#888" yalign 0.6 font "DejaVuSans.ttf"

                        null height 10

                        # ТАБЛИЦА ДАННЫХ (Имитация Grid как на скрине)
                        # Используем вспомогательный экран или просто макрос vbox
                        
                        # Names
                        use bio_row("Names", active_bio_char.get_display_name())
                        
                        # Aliases
                        if active_bio_char.aliases:
                            use bio_row("Aliases", ", ".join(active_bio_char.aliases))

                        # Measurements / Age
                        hbox:
                            spacing 50
                            use bio_field("Height", active_bio_char.height)
                            use bio_field("Age", active_bio_char.age)

                        # Внешность
                        use bio_row("Hair", active_bio_char.hair)
                        use bio_row("Eyes", active_bio_char.eyes)
                        use bio_row("Clothes", active_bio_char.clothes)

                        null height 10
                        
                        # Характер и Роль
                        use bio_row("Personality", active_bio_char.personality)
                        use bio_row("Role", active_bio_char.role)
                        
                        # Элемент (Сила)
                        use bio_row("Element", active_bio_char.element)

                        # Engages In (Грехи)
                        use bio_row("Engages in", ", ".join(active_bio_char.get_engages_list()))

                        null height 20
                        
                        # РАЗДЕЛИТЕЛЬ
                        frame:
                            ysize 2
                            xfill True
                            background "#3498db"
                        
                        null height 20

                        # ОПИСАНИЕ (Постепенное открытие)
                        text "Description" size 30 color "#fff" bold True
                        
                        vbox:
                            spacing 15
                            if active_bio_char.desc_level > 0:
                                for i in range(active_bio_char.desc_level):
                                    if i < len(active_bio_char.desc_stages):
                                        text active_bio_char.desc_stages[i] color "#ccc" layout "subtitle" size 22
                            else:
                                text _("Информация пока недоступна.") color "#555" italic True

# Вспомогательный компонент для строки (Заголовок: Значение)
screen bio_row(label_t, value_t):
    hbox:
        spacing 20
        text label_t:
            min_width 180
            color "#3498db" # Голубой цвет заголовков
            size 22
            bold True
        text value_t:
            color "#eee"
            size 22
            layout "subtitle" # Позволяет тексту переноситься

# Вспомогательный компонент для короткого поля (Height: 180cm)
screen bio_field(label_t, value_t):
    hbox:
        spacing 10
        text label_t + ":":
            color "#3498db"
            size 22
        text value_t:
            color "#eee"
            size 22