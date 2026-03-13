# --- СТИЛИ И ТРАНСФОРМАЦИИ ---
transform gal_thumb_hover:
    zoom 1.05
    ease 0.2 zoom 1.05

image gallery_locked_thumb:
    Solid("#000")
    size(384, 216) # Размер как в конфиге
    Text("?", size=60, color="#555", align=(0.5, 0.5))

init python:
    def gallery_delayed_thumb(st, at, item, delay):
        if st < delay:
            return renpy.displayable("gallery_skeleton_thumb"), delay - st
        return item.get_thumbnail_displayable(), None

screen gallery_thumbnail_button(item, delay_time=0.25):
    button:
        xysize (gal_thumb_x, gal_thumb_y)
        background Solid("#333")

        if item.is_unlocked():
            add DynamicDisplayable(gallery_delayed_thumb, item=item, delay=delay_time)
                    
            action Show("gallery_view", item=item)
            hover_foreground Solid("#ffffff22")
            hovered Play("audio", "audio/sfx/cursor-hover.wav")
            
            # Название и счетчик
            frame:
                background Solid("#00000099")
                xfill True
                yalign 1.0
                padding (10, 5)
                hbox:
                    xfill True
                    text "[item.name!t]" size 18 color "#fff" align (0.0, 0.5)
                    text item.get_count_text() size 16 color "#aaa" align (1.0, 0.5)
        else:
            add item.get_thumbnail_displayable()
            action NullAction()

        # Если картинка не найдена/битая, этот текст будет виден поверх серого фона
        if not renpy.loadable(item.thumb) and not renpy.has_image(item.thumb):
            text _("Нет файла:\n[item.thumb]"):
                size 14 
                color "#f00" 
                align (0.5, 0.5) 
                text_align 0.5


# --- ЭКРАН МЕНЮ ГАЛЕРЕИ ---
screen gallery():
    tag menu
    add gui.main_menu_background

    # Переменная текущей страницы
    default page = 0
    default has_paginated = False
    
    # Вычисляем макс. страниц
    $ max_page = (len(gallery_items) - 1) // gal_cells if len(gallery_items) > 0 else 0
    
    # Срезаем список, чтобы получить только нужные элементы (ОПТИМИЗАЦИЯ)
    $ start_index = page * gal_cells
    $ end_index = min(start_index + gal_cells, len(gallery_items))
    $ current_items = gallery_items[start_index:end_index]

    frame:
        style "modern_panel_wide"

        vbox:
            style "modern_vbox"

            label _("Галерея CG") style "modern_title_label"

            if len(gallery_items) == 0:
                text _("Пока нет открытых CG.") align (0.5, 0.5)
            else:
                grid gal_cols gal_rows:
                    spacing 30
                    xalign 0.5
                
                    for i, item in enumerate(current_items):
                        $ delay_val = i * 0.05 if has_paginated else 0.0
                        use gallery_thumbnail_button(item, delay_val) id ("gal_thumb_p" + str(page) + "_" + item.name.replace(" ", "_"))

                    # Если на последней странице элементов меньше, чем ячеек, заполняем пустотой
                    for i in range(gal_cells - len(current_items)):
                        null width gal_thumb_x height gal_thumb_y

                # Навигация по страницам
                hbox:
                    xalign 0.5
                    spacing 50
                    
                    textbutton "<":
                        action [SetScreenVariable("page", max(0, page - 1)), SetScreenVariable("has_paginated", True)]
                        sensitive (page > 0)
                        text_size 40
                        
                    text _("Страница [page+1] / [max_page+1]") yalign 0.5 color "#fff"
                        
                    textbutton ">":
                        action [SetScreenVariable("page", min(max_page, page + 1)), SetScreenVariable("has_paginated", True)]
                        sensitive (page < max_page)
                        text_size 40

            null height 40
            textbutton _("Назад") action ShowMenu("memory_recollection") style "modern_back_button"



# --- ЭКРАН ПРОСМОТРА (СЛАЙДШОУ) ---
screen gallery_view(item):
    modal True
    tag menu
    $ unlocked_imgs = item.get_unlocked_list()
    default idx = 0

    add "#000"
    
    # Данные текущей картинки
    if unlocked_imgs:
        $ current_img, current_desc = unlocked_imgs[idx]

        # Само изображение
        add current_img:
            fit "contain"
            xalign 0.5
            yalign 0.5
            at transform:
                alpha 0.0
                ease 0.25 alpha 1.0

        button:
            xfill True
            yfill True
            action If(idx < len(unlocked_imgs) - 1, SetScreenVariable("idx", idx + 1), ShowMenu("gallery"))

        # Оверлей с текстом
        if item.name or current_desc:
            frame:
                align (0.5, 0.95)
                background Solid("#000000BB")
                padding (40, 20)
                vbox:
                    xalign 0.5
                    text "[item.name!t]":
                        color "#ffaa00"
                        size 28
                        bold True
                        xalign 0.5
                    
                    if current_desc:
                        null height 5
                        text "[current_desc!t]":
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
            action ShowMenu("gallery")
    
    else:
        textbutton _("Ошибка: Нет картинок") action ShowMenu("gallery") align (0.5, 0.5)
        
    key "game_menu" action ShowMenu("gallery")