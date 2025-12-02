# --- СТИЛИ И ТРАНСФОРМАЦИИ ---
transform gal_thumb_hover:
    zoom 1.05
    ease 0.2 zoom 1.05

image gallery_locked_thumb:
    Solid("#000") # Черный фон
    size(384, 216) # Размер как в конфиге
    Text("?", size=60, color="#555", align=(0.5, 0.5))

# --- ЭКРАН МЕНЮ ГАЛЕРЕИ ---
screen gallery():
    tag menu
    add "gui/main_menu.png" # Фон галереи

    use game_menu("Галерея"): # Используем стандартный шаблон меню
        
        vpgrid:
            cols 3
            spacing 20
            draggable True
            mousewheel True
            scrollbars "vertical"
            xalign 0.5
            yalign 0.5

            allow_underfull True 
            
            for item in gallery_items:
                if item.is_visible():
                    # Кнопка открытого CG
                    button:
                        xysize (384, 216) # Размер кнопки
                        background Solid("#333") # Серый фон, если картинка прозрачная

                        add item.thumb:
                            fit "cover"
                            xysize (384, 216)

                        # Если картинка не найдена/битая, этот текст будет виден поверх серого фона
                        if not renpy.loadable(item.thumb) and not renpy.has_image(item.thumb):
                            text "Нет файла:\n" + str(item.thumb):
                                size 14 
                                color "#f00" 
                                align (0.5, 0.5) 
                                text_align 0.5
                            
                        # Эффекты при наведении
                        hover_foreground Solid("#ffffff22")
                        
                        # Счетчик (например 1/3)
                        frame:
                            background Solid("#00000080")
                            align (0.95, 0.95)
                            padding (5, 2)
                            text "[item.num_unlocked()]/[item.num_total()]":
                                size 14
                                color "#fff"
                        
                        # Название
                        text item.name:
                            align (0.5, 0.1)
                            text_align 0.5
                            size 22
                            bold True
                            outlines [(2, "#000", 0, 0)]

                        action Show("gallery_view", item=item)
                        hovered Play("audio", "sfx/cursor-hover.wav") 

                else:
                    add "gallery_locked_thumb"

# --- ЭКРАН ПРОСМОТРА (СЛАЙДШОУ) ---
screen gallery_view(item):
    modal True
    tag menu # Чтобы перекрывало другие меню
    
    # Получаем список ТОЛЬКО открытых картинок
    $ unlocked_imgs = item.get_unlocked_list()
    
    # Переменная экрана для отслеживания текущего индекса
    default idx = 0
    
    # Данные текущей картинки
    if unlocked_imgs:
        $ current_img, current_desc = unlocked_imgs[idx]

        # Черный фон
        add "#000"

        # Само изображение
        # fit "contain" гарантирует, что картинка влезет в экран целиком
        add current_img:
            fit "contain"
            xalign 0.5
            yalign 0.5
            at transform:
                alpha 0.0
                ease 0.25 alpha 1.0

        # Клик по всему экрану (вперед)
        button:
            xfill True
            yfill True
            action If(idx < len(unlocked_imgs) - 1, SetScreenVariable("idx", idx + 1), Return())

        # Оверлей с текстом
        if item.name or current_desc:
            frame:
                align (0.5, 0.95)
                background Solid("#000000BB")
                padding (40, 20)
                vbox:
                    xalign 0.5
                    text item.name:
                        color "#ffaa00"
                        size 28
                        bold True
                        xalign 0.5
                    
                    if current_desc:
                        null height 5
                        text current_desc:
                            color "#eee"
                            size 24
                            italic True
                            xalign 0.5
                            text_align 0.5

        # Кнопки навигации
        if len(unlocked_imgs) > 1:
            if idx > 0:
                imagebutton:
                    idle Text("<", size=80, color="#fff", outlines=[(2,"#000")])
                    hover Text("<", size=80, color="#f00", outlines=[(2,"#000")])
                    align (0.02, 0.5)
                    action SetScreenVariable("idx", idx - 1)
            
            if idx < len(unlocked_imgs) - 1:
                imagebutton:
                    idle Text(">", size=80, color="#fff", outlines=[(2,"#000")])
                    hover Text(">", size=80, color="#f00", outlines=[(2,"#000")])
                    align (0.98, 0.5)
                    action SetScreenVariable("idx", idx + 1)

        textbutton "X":
            text_size 50
            text_color "#fff"
            text_outlines [(2, "#000")]
            align (0.98, 0.02)
            action Return()
    
    else:
        # На случай если список пуст (баг)
        textbutton "Ошибка: Нет картинок" action Return() align (0.5, 0.5)
        
    key "game_menu" action Return() # Правая кнопка мыши / Esc закрывает просмотр