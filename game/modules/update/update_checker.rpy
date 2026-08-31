init python:
    if not renpy.variant("web"):
        import requests
    import threading
    import json
    import time
    import re
    
    # --- НАСТРОЙКИ ---
    GITHUB_API_URL = "https://api.github.com/repos/DomDotDot/DoctorNeonPrototype/releases/latest"
    
    LINK_ITCH = "https://dotprod.itch.io/bright-neon-semitone-resonance#download"
    LINK_GITHUB = "https://github.com/DomDotDot/DoctorNeonPrototype/releases/latest"
    # LINK_STEAM = "..." 

    update_check_done = False

    def _get_version_numbers(v_str):
        """
        Превращает "vx.y.z-stable" -> [x, y, z]
        Превращает "x.y.z-early"   -> [x, y, z]
        """
        # 1. Убираем 'v' в начале
        v_clean = v_str.lower().lstrip('v')
        
        # 2. RegEx только цифры и точки в начале строки
        # ^(\d+(?:\.\d+)*) означает: "Взять цифры с точками с самого начала"
        match = re.search(r'^(\d+(?:\.\d+)*)', v_clean)
        
        if match:
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
            # Сравнение списков математически:
            # [0, 5, 4] > [0, 5, 3] -> True
            # [0, 5, 3] > [0, 5, 3] -> False (даже если есть приписка -stable)
            return r_nums > l_nums
            
        # Если версии совсем странные (например "final-build" без цифр),
        # то сравниваем как строки, но это запасной вариант.
        return remote_ver != local_ver

    def _update_worker():

        if renpy.variant("web"):
            return

        global update_check_done
        
        print(f"UpdateCheck: В persistent сейчас записано: {persistent.ignored_version}")
        print("UpdateCheck: Поток запущен...")

        try:

            headers = {'User-Agent': 'RenPy-Game-Client'}

            # Делаем запрос к API GitHub (таймаут 5 сек, чтобы не тупить)
            response = requests.get(GITHUB_API_URL, headers=headers, timeout=5, verify=False)
            
            if response.status_code == 200:
                data = response.json()
                remote_tag = data.get("tag_name", "0.0.0")
                body_text = data.get("body", "") # Описание релиза с Гитхаба
                
                
                # Сравниваем с текущей config.version
                if _version_compare(remote_tag, config.version):
                    print(f"UpdateCheck: Найдена новая версия {remote_tag}")
                    
                    # Формируем ID, чтобы не добавлять одно и то же 100 раз
                    notif_id = f"update_{remote_tag}"

                    title = f"Доступно обновление: {remote_tag}"
                    message = "Вышла новая версия игры!\n\n" + body_text[:200]
                    if len(body_text) > 200: message += "..."
                    
                    # Проверяем, игнорировал ли игрок эту версию
                    should_popup = True
                    if persistent.ignored_version == remote_tag:
                        should_popup = False
                        title += _(" (Скрыто)")
                        print("UpdateCheck: Версия в игноре, только добавляем в список.")

                    if hasattr(renpy, "invoke_in_main_thread"):
                        renpy.invoke_in_main_thread(
                            add_notification, 
                            notif_id, title, message, LINK_ITCH, LINK_GITHUB, remote_tag, should_popup
                        )
                    else:
                        # Старый способ (может вызвать конфликты, но обычно работает)
                        add_notification(
                            notif_id,
                            title,
                            message,
                            LINK_ITCH,
                            LINK_GITHUB,
                            remote_tag,
                            should_popup
                        )

                    # ДОБАВЛЯЕМ В МЕНЕДЖЕР
                    add_notification(
                        notif_id=notif_id,
                        title=title,
                        message=message,
                        link_itch=LINK_ITCH,
                        link_github=LINK_GITHUB,
                        version_tag=remote_tag,
                        force_popup=should_popup # Покажем попап, только если не в игноре
                    )

                else:
                    print("UpdateCheck: Версия актуальна.")
            else:
                print(f"UpdateCheck: Ошибка API {response.status_code}")
                    
        except Exception as e:
            print(f"UpdateCheck Error: {e}")
        
        update_check_done = True

    def start_update_check():

        if renpy.variant("web"):
            return
            
        global update_check_done
        update_check_done = False
        
        if not update_check_done:
            t = threading.Thread(target=_update_worker)
            t.daemon = True
            t.start()