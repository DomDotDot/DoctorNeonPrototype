init python:
    import zipfile
    import os

    def build_all_dlc_packages():
        """
        Создает ZIP архивы для DLC из папок игры.
        Архивы будут лежать в корне проекта (рядом с папкой game).
        """
        
        # --- НАСТРОЙКИ: СПИСОК DLC ---
        # Формат: ("Имя_Архива.zip", "Папка_ИСТОЧНИК", "Папка_ВНУТРИ_АРХИВА")
        
        # Параметры
        # 1. music.zip - имя файла
        # 2. game/audio/music - что берем
        # 3. music - как папка будет называться внутри ZIP. 
        #    (Чтобы при распаковке в game/audio она стала game/audio/music)
        
        tasks = [

            # Музыка
            {
                "zip": "music.zip", 
                "src": "game/audio/music", 
                "arcname": "music" 
            },

            # Эмбиент
            {
                "zip": "ambient.zip", 
                "src": "game/audio/ambient", 
                "arcname": "ambient"
            },

            # SFX
            {
                "zip": "sfx.zip", 
                "src": "game/audio/sfx", 
                "arcname": "sfx"
            },

            # Озвучка RU
            {
                "zip": "voice_ru.zip", 
                "src": "game/audio/voice", 
                "arcname": "voice"
            },

            # Озвучка EN
            {
                "zip": "voice_en.zip", 
                "src": "game/tl/english_us/audio/voice", 
                "arcname": "voice"
            },
        ]

        # Базовая директория (папка проекта, где лежит папка game)
        base_dir = config.basedir 
        
        print("\n--- НАЧАЛО СБОРКИ DLC ---")
        
        for task in tasks:
            zip_filename = os.path.join(base_dir, task["zip"])
            source_dir = os.path.join(base_dir, task["src"])
            arc_root = task["arcname"]
            
            print(f"Архивация: {task['zip']}...")
            
            # Проверяем, существует ли папка
            if not os.path.exists(source_dir):
                print(f"!! ОШИБКА: Папка не найдена: {source_dir}")
                continue

            try:
                # Создаем ZIP (сжатие DEFLATED - стандартное)
                with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    # Обходим все файлы в папке
                    for root, dirs, files in os.walk(source_dir):
                        for file in files:
                            # Полный путь к файлу на диске
                            file_path = os.path.join(root, file)
                            
                            # Вычисляем путь внутри архива
                            # Например: source_dir = .../music
                            # file_path = .../music/track1.opus
                            # rel_path = track1.opus
                            rel_path = os.path.relpath(file_path, source_dir)
                            
                            # Итоговый путь в zip: music/track1.opus
                            zip_path = os.path.join(arc_root, rel_path)
                            
                            zipf.write(file_path, zip_path)
                            
                print(f"-> Готово: {zip_filename}")
                
            except Exception as e:
                print(f"!! ОШИБКА при создании {task['zip']}: {e}")

        print("--- СБОРКА ЗАВЕРШЕНА ---\n")
        renpy.notify("DLC Архивы созданы! Проверьте папку проекта.")

# Кнопка для вызова (добавь в screens.rpy в developer menu или просто временный экран)
screen dlc_builder_tool():
    frame:
        xalign 0.95 yalign 0.05
        textbutton "СОЗДАТЬ DLC АРХИВЫ" action Function(build_all_dlc_packages) text_size 20 style "button"