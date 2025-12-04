init -1 python:
    # -----------------------------------------------------------
    # 1. ЛОГИКА ПОДСВЕТКИ (Та же, что и раньше)
    # -----------------------------------------------------------
    default active_speaker = None

    def name_callback(event, interact=True, **kwargs):
        if not interact: return
        if event == "begin":
            store.active_speaker = kwargs.get("cb_name")

# Трансформация: если active_speaker совпадает с char_name -> ярко, иначе -> темно
transform auto_dim(char_name):
    matrixcolor TintMatrix(1.0)
    block:
        if active_speaker == char_name:
            ease 0.2 matrixcolor TintMatrix(1.0)
        else:
            ease 0.2 matrixcolor TintMatrix(0.5) # Насколько затемнять (0.5 = 50%)
        pause 0.1
        repeat

init python:
    # -----------------------------------------------------------
    # 2. АВТОМАТИЧЕСКИЙ ПОИСК И РЕГИСТРАЦИЯ СПРАЙТОВ
    # -----------------------------------------------------------
    import os

    # Укажите папку, где лежат спрайты персонажей (относительно папки game)
    SPRITE_DIR = "images/sprites/"

    # Проходимся по всем файлам игры
    for path in renpy.list_files():
        
        # Ищем только файлы в папке спрайтов
        if path.startswith(SPRITE_DIR):
            
            # Проверяем расширения (картинки)
            if path.lower().endswith((".png", ".webp", ".jpg")):
                
                # Получаем имя файла без пути: "marcus lab_neutral.webp"
                filename = os.path.basename(path)
                
                # Убираем расширение: "marcus lab_neutral"
                name_no_ext = os.path.splitext(filename)[0]
                
                # Разбиваем имя на части: ["marcus", "lab_neutral"]
                parts = name_no_ext.split()
                
                if parts:
                    # Первое слово считаем "тегом" персонажа (marcus)
                    char_tag = parts[0]
                    
                    # Регистрируем изображение в Ren'Py
                    # Это аналог строки: image marcus lab_neutral = At("...", auto_dim("marcus"))
                    renpy.image(name_no_ext, At(path, auto_dim(char_tag)))