init python:
    import json
    import os
    import hashlib

    def generate_dlc_manifest(target_filename="dlc_manifest.json", source_folders=None):
        """
        Сканирует source_folders (относительно game/) и создает target_filename
        в корне игры.
        """
        if source_folders is None:
            source_folders = ["audio"] # Дефолт

        manifest = {}
        base_dir = config.gamedir
        
        files_list = []

        for d in source_folders:
            full_path = os.path.join(base_dir, d)
            if not os.path.exists(full_path):
                print(f"Skipping missing folder: {full_path}")
                continue
                
            for root, dirs, files in os.walk(full_path):
                # Игнорируем папки с названием Unused (любой регистр)
                dirs[:] = [d for d in dirs if d.lower() != "unused"]
                
                for file in files:
                    if file.endswith((".rpy", ".rpyc", ".rpym", ".rpymc", ".py", ".pyc")):
                        continue # Пропускаем скрипты
                    if file.endswith(".DS_Store") or file.endswith("thumbs.db"):
                        continue
                        
                    # Получаем относительный путь
                    abs_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_path, base_dir).replace("\\", "/")
                    
                    files_list.append(rel_path)

        manifest["files"] = files_list
        manifest["version"] = config.version
        
        # Сортируем для красоты
        files_list.sort()
        
        manifest_path = os.path.join(base_dir, target_filename)
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=4)
            
        print(f"Manifest Generated: {target_filename} ({len(files_list)} files)")
        return files_list

    def verify_dlc_manifest(manifest_filename="dlc_manifest.json"):
        """
        Проверяет наличие всех файлов из манифеста.
        Возвращает True, если ВСЕ файлы на месте.
        """
        manifest_path = os.path.join(config.gamedir, manifest_filename)
        
        if not os.path.exists(manifest_path):
            return False
            
        try:
            with open(manifest_path, "r") as f:
                data = json.load(f)
                
            files = data.get("files", [])
            if not files:
                return False # Пустой манифест - считаем как нет DLC
                
            for rel_path in files:
                full_path = os.path.join(config.gamedir, rel_path)
                if not os.path.exists(full_path):
                    return False # Хоть одного нет - fail
            
            return True
            
        except Exception as e:
            print("Manifest Check Error: " + str(e))
            return False
