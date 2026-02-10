init python:
    import json
    import os
    import hashlib

    def generate_dlc_manifest():
        """
        Сканирует папку game/audio (и другие если надо) и создает dlc_manifest.json
        в корне игры.
        """
        manifest = {}
        base_dir = config.gamedir
        
        # Папки для сканирования (относительно game/)
        scan_dirs = ["audio", "tl/english_us/audio"] 
        
        files_list = []

        for d in scan_dirs:
            full_path = os.path.join(base_dir, d)
            if not os.path.exists(full_path):
                continue
                
            for root, dirs, files in os.walk(full_path):
                for file in files:
                    if file.endswith((".rpy", ".rpyc", ".rpym", ".rpymc", ".py", ".pyc")):
                        continue # Пропускаем скрипты
                        
                    # Получаем относительный путь
                    abs_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_path, base_dir).replace("\\", "/")
                    
                    files_list.append(rel_path)

        manifest["files"] = files_list
        manifest["version"] = config.version
        
        manifest_path = os.path.join(base_dir, "dlc_manifest.json")
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=4)
            
        renpy.notify("Manifest Generated: {} files".format(len(files_list)))

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
