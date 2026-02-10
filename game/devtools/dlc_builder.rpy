init python:
    import zipfile
    import os

    def build_all_dlc_packages():
        """
        Создает ZIP архивы для DLC из папок игры.
        Архивы будут лежать в корне проекта (рядом с папкой game).
        """
        
        # Базовая директория (папка проекта, где лежит папка game)
        base_dir = config.basedir 
        game_dir = config.gamedir
        
        print("\n--- НАЧАЛО СБОРКИ DLC (v{}) ---".format(config.version))
        
        # Получаем каталог DLC (он определен в dlc-config-new.rpy)
        # Так как это init python, dlc_catalog должен быть доступен в store
        catalog = getattr(store, "dlc_catalog", [])
        
        if not catalog:
            print("!! ОШИБКА: dlc_catalog не найден или пуст.")
            renpy.notify("Ошибка: dlc_catalog пуст!")
            return

        for item in catalog:
            # Проверяем, есть ли инструкции для сборки
            if "build_sources" not in item:
                continue
                
            dlc_id = item["id"]
            zip_name = item["file"]
            sources = item["build_sources"]
            manifest_name = item.get("manifest", "dlc_manifest.json")
            
            print(f"\n[Обработка DLC: {dlc_id}]")
            
            # 1. Генерируем манифест
            print(f" -> Генерация манифеста: {manifest_name}")
            # Вызываем функцию из files_manifest.rpy
            file_list = generate_dlc_manifest(target_filename=manifest_name, source_folders=sources)
            
            # 2. Создаем архив
            zip_filename = os.path.join(base_dir, zip_name)
            print(f" -> Архивация в: {zip_filename}")
            
            try:
                with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    # Добавляем манифест в корень архива
                    manifest_path = os.path.join(game_dir, manifest_name)
                    if os.path.exists(manifest_path):
                        zipf.write(manifest_path, manifest_name) # В архиве будет лежать как dlc_manifest.json
                    else:
                        print("!! ВНИМАНИЕ: Манифест не найден после генерации!")

                    # Добавляем файлы из манифеста
                    for rel_path in file_list:
                        full_path = os.path.join(game_dir, rel_path)
                        if not os.path.exists(full_path):
                            print(f"!! Пропуск (не найден): {rel_path}")
                            continue
                        
                        # В архиве сохраняем структуру (например audio/music/track.opus)
                        # Важно: файлы из game/ должны лежать в корне архива (или в game/?).
                        # По логике распаковки в dlc_download: folder="." -> распаковка в game/
                        # Значит, в архиве файлы должны лежать как audio/...
                        # А манифест как dlc_manifest.json
                        zipf.write(full_path, rel_path)
                        
                print(f" -> Готово: {zip_name}")

            except Exception as e:
                print(f"!! ОШИБКА при сборке {zip_name}: {e}")

        print("\n--- СБОРКА ЗАВЕРШЕНА ---")
        renpy.notify("DLC Архивы обновлены!")

# Кнопка для вызова (добавь в screens.rpy в developer menu или просто временный экран)
screen dlc_builder_tool():
    frame:
        xalign 0.95 yalign 0.05
        textbutton "СОЗДАТЬ DLC АРХИВЫ" action Function(build_all_dlc_packages) text_size 20 style "button"