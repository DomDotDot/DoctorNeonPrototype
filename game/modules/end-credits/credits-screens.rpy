init python:
    def get_images_from_dir(folder_path):
        img_list = []
        
        if not folder_path.endswith("/"):
            folder_path += "/"
         
        for file in renpy.list_files():
            if file.startswith(folder_path):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.avif', '.webp')):
                    img_list.append(file)
        
        # Сортируем по имени (чтобы cg1 шло перед cg2)
        img_list.sort()
        return img_list

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

screen end_credits(credits_list, image_list, track_duration, end_msg_offset, cg_time):
    modal True

    # --- ЛОГИКА ДВОЙНОГО СЛАЙДШОУ ---
    # idx_back - картинка, которая уже показана (фон)
    # idx_front - картинка, которая сейчас будет появляться (верхний слой)
    
    default idx_back = 0
    default idx_front = 0
    default timer_seed = 0 

    # Таймер срабатывает каждые cg_time секунды
    # 1. Мы копируем "переднюю" картинку на "задний план" (чтобы она осталась видна)
    # 2. Мы выбираем новую "переднюю" картинку

    if len(image_list) > 1:
        timer cg_time repeat True action [
            SetScreenVariable("idx_back", idx_front),                     # Текущую переднюю кидаем назад
            SetScreenVariable("idx_front", (idx_front + 1) % len(image_list)), # Выбираем следующую вперед
            SetScreenVariable("timer_seed", timer_seed + 1)               # Обновляем зерно уникальности
        ]
    
    
    # Логика пропуска (Клик или Пробел)
    key "dismiss" action Return("skipped")
    
    # Таймер, который завершит титры сам, когда музыка кончится
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
        
        # Контейнер с текстом, к которому применяем анимацию прокрутки
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
                    
                    # Имя (слева выровнено)
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

        # Контейнер фиксированного размера для картинок
        fixed:
            xsize 960 
            ysize 540
            
            if len(image_list) > 0:
                # 1. ЗАДНИЙ СЛОЙ (Предыдущая картинка)
                # Она просто висит статично, чтобы не было "черной дыры" при смене
                add image_list[idx_back]:
                    size (960, 540)
                
                # 2. ПЕРЕДНИЙ СЛОЙ (Новая картинка)
                # Она появляется поверх старой с анимацией
                # id "slide_..." нужен, чтобы RenPy понял, что это новый объект и перезапустил анимацию
                add image_list[idx_front]:
                    size (960, 540)
                    at slideshow_dissolve 
                    id "slide_[idx_front]_[timer_seed]" 
            else:
                null

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