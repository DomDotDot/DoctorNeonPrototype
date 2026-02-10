init -999 python:
    import os
    import zipfile
    import threading
    import time
    
    # === КОНФИГУРАЦИЯ ===
    DLC_REPO_URL = "https://github.com/DomDotDot/DoctorNeonPrototype/releases/download"
    
    # Список DLC
    # id: уникальный код
    # file: имя архива
    # folder: куда распаковать (относительно папки game/)
    # check_file: файл для проверки наличия (теперь используется manifest)
    dlc_catalog = [
        {
            "id": "assets",
            "file": "assets.zip",
            "version": config.version, # Автоматически синхронизируем с версией игры
            "url_version": "v" + config.version, # Для GitHub Releases нужен тег с 'v'
            "folder": ".", # Распаковываем в корень game/
            "manifest": "dlc_manifest.json",
            "title": _("Полный пакет ресурсов"),
            "desc": _("Звуки, музыка и озвучка (включает все предыдущие пакеты)."),
            # --- СЕКЦИЯ СБОРКИ (DEV ONLY) ---
            # Указываем папки, которые нужно упаковать в этот DLC.
            # Билдер сам найдет файлы, создаст манифест и архив.
            "build_sources": ["audio", "tl/english_us/audio"] 
        }
    ]

    # === ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ СОСТОЯНИЯ ===
    dlc_state = {
        "progress": 0.0,
        "mb_cur": 0.0,
        "mb_total": 0.0,
        "phase": "init", # init, connecting, downloading, unzipping, done, error
        "error_msg": None,
        "should_cancel": False,
        "current_item": None,
        "is_done": False
    }

    IS_WEB = renpy.variant("web")
    if not IS_WEB:
        import requests
    else:
        requests = None

    # === ЛОГИКА ===

    def is_dlc_installed(dlc_item):
        """Проверяет наличие файлов через манифест."""
        # Если есть поле manifest - проверяем через него
        if "manifest" in dlc_item:
             return verify_dlc_manifest(dlc_item["manifest"])
        
        # Fallback на старую логику для совместимости (если вдруг пригодится)
        if "check_file" in dlc_item:
             full_path = os.path.join(config.gamedir, dlc_item['check_file'])
             return os.path.exists(full_path)
             
        return False

    def get_dlc_url(dlc_item):
        # Если в конфиге DLC явно указано какую версию использовать в URL (например "v0.6.6")
        version = dlc_item.get("url_version", dlc_item['version'])
        return "{}/{}/{}".format(DLC_REPO_URL, version, dlc_item['file'])

    def _dlc_thread_worker(url, zip_path, target_dir):
        global dlc_state
        
        # Папку для zip
        try:
            os.makedirs(os.path.dirname(zip_path))
        except:
            pass
            
        # Целевая папка
        try:
            os.makedirs(target_dir)
        except:
            pass

        attempt = 0
        max_retries = 5
        success = False

        while attempt < max_retries and not success and not dlc_state["should_cancel"]:
            attempt += 1
            dlc_state["phase"] = "connecting"
            dlc_state["error_msg"] = None
            
            try:
                # Таймаут: 5 сек на коннект, 10 на чтение
                with requests.get(url, stream=True, timeout=(5, 10)) as response:
                    if response.status_code != 200:
                        raise Exception("HTTP Code: {}".format(response.status_code))
                    
                    total_length = response.headers.get('content-length')
                    
                    if total_length:
                        dlc_state["mb_total"] = int(total_length) / 1048576.0 # Делим на 1024*1024
                    else:
                        dlc_state["mb_total"] = 0.0

                    dlc_state["phase"] = "downloading"
                    
                    downloaded_bytes = 0
                    
                    with open(zip_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=65536): # 64KB chunk
                            if dlc_state["should_cancel"]: 
                                break
                            
                            if chunk:
                                f.write(chunk)
                                downloaded_bytes += len(chunk)
                                
                                # Обновляем прогресс
                                dlc_state["mb_cur"] = downloaded_bytes / 1048576.0
                                if total_length:
                                    dlc_state["progress"] = float(downloaded_bytes) / int(total_length)
                    
                    if not dlc_state["should_cancel"]:
                        success = True

            except Exception as e:
                print("DLC Download Error: " + str(e))
                if attempt == max_retries:
                    dlc_state["phase"] = "error"
                    dlc_state["error_msg"] = str(e)
                else:
                    dlc_state["phase"] = "waiting"
                    time.sleep(1.5)

        # Распаковка
        if success and not dlc_state["should_cancel"]:
            try:
                dlc_state["phase"] = "unzipping"
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(target_dir)
                
                if os.path.exists(zip_path):
                    os.remove(zip_path)
                
                dlc_state["phase"] = "done"
                dlc_state["is_done"] = True
                
            except Exception as e:
                dlc_state["phase"] = "error"
                dlc_state["error_msg"] = "Unzip Error: " + str(e)

    def start_download_dlc(dlc_item):
        global dlc_state
        
        if IS_WEB:
            return

        # Сброс состояния
        dlc_state["progress"] = 0.0
        dlc_state["mb_cur"] = 0.0
        dlc_state["mb_total"] = 0.0
        dlc_state["phase"] = "init"
        dlc_state["error_msg"] = None
        dlc_state["should_cancel"] = False
        dlc_state["is_done"] = False
        dlc_state["current_item"] = dlc_item

        url = get_dlc_url(dlc_item)
        zip_path = os.path.join(config.gamedir, dlc_item['file'])
        target_dir = os.path.join(config.gamedir, dlc_item['folder'])

        t = threading.Thread(target=_dlc_thread_worker, args=(url, zip_path, target_dir))
        t.daemon = True
        t.start()

    def cancel_download():
        global dlc_state
        dlc_state["should_cancel"] = True

    def get_dlc_initial_selection(dlc_list, first_run):
        """
        Генерирует словарь {id: True/False} для галочек по умолчанию.
        """
        res = {}
        for item in dlc_list:
            if first_run:
                # При первом запуске: ставим галочку, если DLC НЕ установлено
                is_installed = is_dlc_installed(item)
                res[item['id']] = not is_installed
            else:
                # Если открыли меню вручную: галочки сняты
                res[item['id']] = False
        return res