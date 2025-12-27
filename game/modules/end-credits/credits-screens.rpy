init python:
    def get_images_from_dir(folder_path, featured_prefix="featured_"):
        all_images = []
        featured_images = []
        
        if not folder_path.endswith("/"):
            folder_path += "/"
         
        for file in renpy.list_files():
            if file.startswith(folder_path):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.avif', '.webp')):
                    if featured_prefix and featured_prefix in file:
                        featured_images.append(file)
                    all_images.append(file)
        
        all_images.sort()
        featured_images.sort()

        return featured_images, all_images
        
        img_list.sort()
        return img_list

    def create_slideshow(images, slide_time, fade_time):

        if not images:
            return Null()
    
        if len(images) == 1:
            return images[0]

        # Порядок должен быть строго: Картинка, Пауза, Переход...
        args = []
        for img in images:
            args.append(img)          # 1. Показ
            args.append(slide_time)   # 2. Сколько висит картинка (сек)
            args.append(Dissolve(fade_time)) # 3. С каким эффектом меняется на СЛЕДУЮЩУЮ
            
        return anim.TransitionAnimation(*args)

# ---------------------------------------------
# ТРАНСФОРМАЦИИ (Анимация)
# ---------------------------------------------

# Трансформация для плавного появления картинки
transform slideshow_dissolve:
    alpha 0.0
    linear 1.0 alpha 1.0

# Анимация для смены картинок
transform slideshow_fade_in:

    on show:
        alpha 0.0
        easein 1.0 alpha 1.0
    on replace:
        alpha 0.0
        easein 1.0 alpha 1.0

# Анимация прокрутки титров снизу вверх
transform credits_scroll_up(t_duration):
    ypos 1.1
    linear t_duration ypos -1.5

# Анимация появления финальной надписи
transform thanks_appear(wait_time):
    alpha 0.0
    pause wait_time
    easein 2.0 alpha 1.0

# ---------------------------------------------
# ЭКРАН ТИТРОВ
# ---------------------------------------------

screen end_credits(credits_list, slideshow_obj, track_duration, end_msg_offset):

    modal True
    
    # Логика пропуска (Клик или Пробел)
    key "dismiss" action Return("skipped")
    
    timer track_duration action Return("finished")

    # --- ФОН ---
    add "#000"

    # --- ТЕКСТ ТИТРОВ (СЛЕВА) ---
    frame:
        background None
        xalign 0.1
        yalign 0.5
        xsize 800
        ysize config.screen_height
        
        vbox at credits_scroll_up(track_duration):
            spacing 40
            
            for role, name in credits_list:
                hbox:
                    spacing 20

                    text role:
                        font "WDXLLubrifontTC-Regular.ttf"
                        size 30
                        color "#aaa"
                        xsize 350
                        text_align 1.0

                    text name:
                        font "WDXLLubrifontTC-Regular.ttf"
                        size 32
                        color "#fff"

            null height 300

    # --- ОКОШКО С CG (СПРАВА) ---
    frame:
        background "#222"
        padding (5, 5)
        xalign 0.9
        yalign 0.4

        add slideshow_obj:
            size (960, 540)
            xalign 0.5
            yalign 0.5


    # --- ФИНАЛЬНАЯ НАДПИСЬ ---
    # Появляется за end_msg_offset секунд до конца
    text "И тебе. Спасибо за игру!" at thanks_appear(track_duration - end_msg_offset):
        xalign 0.5
        yalign 0.9
        size 40
        color "#fff"
    
    # --- ИНСТРУКЦИЯ ПО ПРОПУСКУ ---
    text "Нажмите Пробел или Клик для пропуска" :
        yalign 0.95
        xalign 0.5
        size 15
        color "#555"