init python:
    import requests
    import threading
    import json
    
    # --- НАСТРОЙКИ ---
    # Ссылка на API твоего репо (замени USER и REPO)
    # Это НЕ ссылка на файл, это API, оно возвращает текст о релизе
    GITHUB_API_URL = "https://api.github.com/repos/DomDotDot/DoctorNeonPrototype/releases/latest"
    
    # Ссылки, куда вести игрока
    LINK_ITCH = "https://dotprod.itch.io/bright-neon-semitone-resonance#download"
    LINK_GITHUB = "https://github.com/DomDotDot/DoctorNeonPrototype/releases/latest"
    # LINK_STEAM = "..." 

    # Переменные состояния
    update_found = False
    new_version_tag = ""
    update_check_done = False
    
    def _version_compare(remote_ver, local_ver):
        """
        Сравнивает версии типа "v0.5.5" и "0.5.5".
        Возвращает True, если remote > local.
        """
        # Убираем 'v' и лишние пробелы
        r_clean = remote_ver.lower().replace('v', '').strip()
        l_clean = local_ver.lower().replace('v', '').strip()
        
        # Разбиваем на цифры: "0.6.1" -> [0, 6, 1]
        try:
            r_parts = [int(x) for x in r_clean.split('.')]
            l_parts = [int(x) for x in l_clean.split('.')]
            return r_parts > l_parts
        except:
            # Если версии кривые (типа "beta-2"), просто сравниваем строки
            return r_clean != l_clean

    def _update_worker():
        global update_found, new_version_tag, update_check_done
        
        try:
            # Делаем запрос к API GitHub (таймаут 3 сек, чтобы не тупить)
            response = requests.get(GITHUB_API_URL, timeout=3)
            
            if response.status_code == 200:
                data = response.json()
                remote_tag = data.get("tag_name", "0.0.0")
                
                # Проверяем, не нажал ли игрок "Больше не напоминать об ЭТОЙ версии"
                if persistent.ignored_version == remote_tag:
                    update_check_done = True
                    return

                # Сравниваем с текущей config.version
                if _version_compare(remote_tag, config.version):
                    new_version_tag = remote_tag
                    update_found = True
                    
        except Exception as e:
            print(f"Update Check Fail: {e}")
        
        update_check_done = True

    def start_update_check():
        t = threading.Thread(target=_update_worker)
        t.daemon = True
        t.start()
        
    def ignore_current_update():
        # Запоминаем эту версию, чтобы больше не предлагать её
        persistent.ignored_version = new_version_tag