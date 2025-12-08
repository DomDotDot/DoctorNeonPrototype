init python:
    import requests
    import threading
    import json
    import time
    import re
    
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

    def _get_version_numbers(v_str):
        """
        Превращает "v0.5.3-stable" -> [0, 5, 3]
        Превращает "0.5.4-early"   -> [0, 5, 4]
        """
        # 1. Убираем 'v' в начале
        v_clean = v_str.lower().lstrip('v')
        
        # 2. Ищем с помощью RegEx только цифры и точки в начале строки
        # ^(\d+(?:\.\d+)*) означает: "Взять цифры с точками с самого начала"
        match = re.search(r'^(\d+(?:\.\d+)*)', v_clean)
        
        if match:
            # Получили строку "0.5.3", разбиваем её на список чисел
            version_str = match.group(1)
            return [int(x) for x in version_str.split('.')]
        
        return []
    
    def _version_compare(remote_ver, local_ver):
        """
        Сравнивает версии типа "v0.5.5" и "0.5.5".
        Возвращает True, если remote > local.
        """

        r_nums = _get_version_numbers(remote_ver)
        l_nums = _get_version_numbers(local_ver)

        print(f"UpdateCheck: Сравниваю сервер [{r_nums}] и локал [{l_nums}]")

        # Если удалось извлечь цифры из обеих версий
        if r_nums and l_nums:
            # Сравниваем списки математически:
            # [0, 5, 4] > [0, 5, 3] -> True
            # [0, 5, 3] > [0, 5, 3] -> False (даже если есть приписка -stable)
            return r_nums > l_nums
            
        # Если версии совсем странные (например "final-build" без цифр),
        # то сравниваем как строки, но это запасной вариант.
        return remote_ver != local_ver

    def _update_worker():
        global update_found, new_version_tag, update_check_done
        
        print(f"UpdateCheck: В persistent сейчас записано: {persistent.ignored_version}")
        print("UpdateCheck: Поток запущен...")

        try:

            headers = {'User-Agent': 'RenPy-Game-Client'}

            # Делаем запрос к API GitHub (таймаут 5 сек, чтобы не тупить)
            response = requests.get(GITHUB_API_URL, headers=headers, timeout=5, verify=False)
            
            if response.status_code == 200:
                data = response.json()
                remote_tag = data.get("tag_name", "0.0.0")
                
                # Сравниваем с текущей config.version
                if _version_compare(remote_tag, config.version):
                    new_version_tag = remote_tag
                    update_found = True
                    print(f"UpdateCheck: Найдена версия {new_version_tag}")

                    if persistent.ignored_version == new_version_tag:
                        print("UpdateCheck: Эта версия в игноре. Popup не должен появиться.")
                    else:
                        print("UpdateCheck: Эту версию еще не скрывали. Popup должен появиться.")
                else:
                    print("UpdateCheck: Версия актуальна.")
            else:
                print(f"UpdateCheck: Ошибка API: {response.text}")
                    
        except Exception as e:
            print(f"UpdateCheck Error: {e}")
        
        update_check_done = True

    def start_update_check():
        global update_found, update_check_done

        update_found = False
        update_check_done = False
        
        t = threading.Thread(target=_update_worker)
        t.daemon = True
        t.start()
        
    def ignore_current_update():
        # Запоминаем эту версию, чтобы больше не предлагать её
        persistent.ignored_version = new_version_tag