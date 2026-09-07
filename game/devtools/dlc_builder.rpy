init python:
    import zipfile
    import os
    import threading

    def _build_dlc_worker():
        base_dir = config.basedir 
        game_dir = config.gamedir
        
        print("\n--- НАЧАЛО СБОРКИ DLC (v{}) ---".format(config.version))
        
        catalog = getattr(store, "dlc_catalog", [])
        if not catalog:
            print("!! ОШИБКА: dlc_catalog не найден или пуст.")
            renpy.notify(_("Ошибка: dlc_catalog пуст!"))
            return

        has_errors = False
        built_count = 0

        for item in catalog:
            if "build_sources" not in item:
                continue
                
            dlc_id = item["id"]
            zip_name = item["file"]
            sources = item["build_sources"]
            manifest_name = item.get("manifest", "dlc_manifest.json")
            
            print(f"\n[Обработка DLC: {dlc_id}]")
            
            try:
                # 1. Генерируем манифест
                print(f" -> Генерация манифеста: {manifest_name}")
                file_list = generate_dlc_manifest(target_filename=manifest_name, source_folders=sources)
                
                # 2. Создаем архив
                zip_filename = os.path.join(base_dir, zip_name)
                print(f" -> Архивация в: {zip_filename}")
                
                with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    manifest_path = os.path.join(game_dir, manifest_name)
                    if os.path.exists(manifest_path):
                        zipf.write(manifest_path, manifest_name)
                    else:
                        print("!! ВНИМАНИЕ: Манифест не найден после генерации!")

                    for rel_path in file_list:
                        full_path = os.path.join(game_dir, rel_path)
                        if not os.path.exists(full_path):
                            print(f"!! Пропуск (не найден): {rel_path}")
                            continue
                        zipf.write(full_path, rel_path)
                        
                print(f" -> Готово: {zip_name}")
                built_count += 1

            except Exception as e:
                has_errors = True
                print(f"!! ОШИБКА при сборке {zip_name}: {e}")

        print("\n--- СБОРКА ЗАВЕРШЕНА ---")
        if has_errors:
            renpy.notify(_("Сборка DLC завершена с ошибками! См. консоль."))
        elif built_count > 0:
            renpy.notify(_("DLC Архивы успешно обновлены!"))
        else:
            renpy.notify(_("Нет пакетов DLC для сборки."))

    def build_all_dlc_packages():
        """
        Создает ZIP архивы для DLC из папок игры в фоновом потоке.
        Архивы будут лежать в корне проекта (рядом с папкой game).
        """
        renpy.notify(_("Сборка DLC запущена в фоновом режиме..."))
        thread = threading.Thread(target=_build_dlc_worker, daemon=True)
        thread.start()

# Кнопка для вызова (добавь в screens.rpy в developer menu или просто временный экран)
screen dlc_builder_tool():
    frame:
        xalign 0.95 yalign 0.05
        textbutton "СОЗДАТЬ DLC АРХИВЫ" action Function(build_all_dlc_packages) text_size 20 style "button"