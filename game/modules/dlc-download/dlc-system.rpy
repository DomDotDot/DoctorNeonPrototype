init python:
    import os
    import zipfile
    import requests
    import threading
    import time

    # --- ГЛОБАЛЬНЫЕ НАСТРОЙКИ ---
    REPO_BASE_URL = "https://github.com/DomDotDot/DoctorNeonPrototype/releases/download"
    MAX_RETRIES = 5
    TIMEOUT_SEC = 10

    # --- ПЕРЕМЕННЫЕ СОСТОЯНИЯ (ГЛОБАЛЬНЫЕ) ---
    # Они общие для любой загрузки.
    dl_progress = 0.0
    dl_status = ""
    dl_done = False
    dl_error = None
    dl_should_cancel = False
    current_dlc_data = None 
    dl_queue_title = "" # Хранит заголовок с номером в очереди (Музыка (1/3))

    # ПЕРЕМЕННЫЕ ДЛЯ ОТСЛЕЖИВАНИЯ СОСТОЯНИЯ
    dl_phase = "init"        # init, connecting, downloading, unzipping, done
    dl_attempt_cur = 0       # Текущая попытка
    dl_attempt_max = 5       # Макс попыток
    dl_mb_cur = 0.0          # Скачано МБ
    dl_mb_tot = 0.0          # Всего МБ

    def _dlc_worker(url, zip_path, target_dir):
        global dl_progress, dl_status, dl_done, dl_error, dl_should_cancel
        global dl_phase, dl_attempt_cur, dl_attempt_max, dl_mb_cur, dl_mb_tot

        if not os.path.exists(os.path.dirname(zip_path)):
            os.makedirs(os.path.dirname(zip_path))

        print(f"DLC Loader: Start downloading {url}")

        attempt = 0
        success = False

        while attempt < MAX_RETRIES and not success and not dl_should_cancel:
            attempt += 1
            dl_attempt_cur = attempt

            try:
                dl_error = None
                dl_phase = "connecting"
                
                # Таймаут: 5 сек на коннект, 5 сек на ожидание байтов
                response = requests.get(url, stream=True, timeout=(5, TIMEOUT_SEC))

                if response.status_code == 404:
                    raise Exception(_("Файл не найден (404). Проверь версию!"))
                if response.status_code != 200:
                    raise Exception("HTTP Error: {}".format(response.status_code))

                total_length = response.headers.get('content-length')

                with open(zip_path, 'wb') as f:
                    if total_length is None:
                        f.write(response.content)
                    else:
                        dl = 0
                        total_length = int(total_length)
                        dl_mb_tot = total_length / 1024 / 1024

                        for data in response.iter_content(chunk_size=32768): # 32kb чанки
                            if dl_should_cancel: break
                            dl += len(data)
                            f.write(data)

                            dl_progress = float(dl) / total_length
                            # Cтатус: 15.4 / 120.0 MB
                            dl_mb_cur = dl / 1024 / 102

                if dl_should_cancel: return
                success = True

            except Exception as e:
                print(f"DLC Error: {e}")
                if attempt == MAX_RETRIES:
                    dl_error = str(e)
                else:
                    dl_phase = "waiting"
                    time.sleep(2)

        # Распаковка
        if success:
            try:
                dl_phase = "unzipping"
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(os.path.join(config.gamedir, current_dlc_data['folder']))
                
                if os.path.exists(zip_path):
                    os.remove(zip_path)

                dl_phase = "done"
                dl_done = True
            except Exception as e:
                dl_error = "Zip Error: " + str(e)
        elif not dl_error and not dl_should_cancel:
            dl_error = "Unknown download error."

    def start_download_current():
        global dl_progress, dl_status, dl_done, dl_error, dl_should_cancel, current_dlc_data
        global dl_phase, dl_mb_cur, dl_mb_tot
        
        # Сброс
        dl_progress = 0.0
        dl_phase = "init"
        dl_mb_cur = 0.0
        dl_mb_tot = 0.0
        dl_done = False
        dl_error = None
        dl_should_cancel = False
        
        # Сборка данных
        data = current_dlc_data
        filename = data['file']
        version = data['version']
        folder = data['folder']

        full_url = "{}/{}/{}".format(REPO_BASE_URL, version, filename)

        # Пути
        zip_path = os.path.join(config.gamedir, filename)
        target_dir = os.path.join(config.gamedir, data['folder'])
        
        t = threading.Thread(target=_dlc_worker, args=(full_url, zip_path, target_dir))
        t.daemon = True
        t.start()

# --- ЭКРАН ВЫБОРА ---
screen dlc_selection_screen(dlc_list):
    # dlc_list - это список словарей тех DLC, которые еще не установлены
    modal True

    # Переменная для хранения выбора игрока (id: True/False)
    # По умолчанию выбор всех доступные для скачивания
    default dlc_choices = {item['id']: True for item in dlc_list}

    frame:
        xalign 0.5 yalign 0.5
        xsize 900 ysize 700
        padding (40, 40)
        
        vbox:
            spacing 15
            
            text _("Дополнительный контент") size 40 bold True xalign 0.5
            text _("Выберите компоненты для установки:") size 22 xalign 0.5

            viewport:
                scrollbars "vertical"
                mousewheel True
                
                vbox:
                    spacing 10
                    for item in dlc_list:
                        hbox:
                            spacing 15

                            # Чекбокс
                            textbutton ("✓ " if dlc_choices[item['id']] else "☐ ") action SetDict(dlc_choices, item['id'], not dlc_choices[item['id']]) text_size 30
                            
                            vbox:
                                text "[item['title']!t]" size 24 bold True
                                text "[item['desc']!t]" size 20 color "#ccc"

            null height 20

            hbox:
                xalign 0.5 spacing 50
                
                # Кнопка СКАЧАТЬ -> возвращает список выбранных DLC
                textbutton _("Скачать выбранное") action Return([item for item in dlc_list if dlc_choices[item['id']]]) style "button" text_size 28
                
                # Кнопка ПРОПУСТИТЬ ВСЁ -> возвращает пустой список
                textbutton _("Пропустить всё") action Return([]) style "button" text_size 28


# --- ЭКРАН ПРОГРЕССА ---
screen dlc_progress_screen():
    modal True
    timer 0.05 repeat True action Function(renpy.restart_interaction)

    frame:
        xalign 0.5 yalign 0.5 padding (50, 50) xsize 800
        vbox:
            spacing 20
            text "[current_dlc_data['title']!t] ([dl_seq_current] / [dl_seq_total])" size 30 bold True xalign 0.5
            
            if dl_error:
                text _("ОШИБКА") color "#f00" size 26 xalign 0.5
                text "[dl_error!t]" size 18 xalign 0.5
                hbox:
                    xalign 0.5 spacing 30

                    textbutton _("Повторить") action Function(start_download_current)
                    textbutton _("Пропустить этот пак") action Return()
            else:
                if dl_phase == "init":
                    text _("Инициализация...") size 22 xalign 0.5
                
                elif dl_phase == "connecting":
                    # RenPy подставит числа в перевод строки "Попытка [dl_attempt_cur] из..."
                    text _("Попытка [dl_attempt_cur] из [dl_attempt_max]...") size 22 xalign 0.5

                elif dl_phase == "downloading":
                    # Форматируем числа до 1 знака после запятой через .1f
                    $ mb_c = "{:.1f}".format(dl_mb_cur)
                    $ mb_t = "{:.1f}".format(dl_mb_tot)
                    text _("[mb_c] / [mb_t] МБ") size 22 xalign 0.5
                
                elif dl_phase == "waiting":
                    text _("Сбой связи. Ждем...") size 22 xalign 0.5
                
                elif dl_phase == "unzipping":
                    text _("Распаковка архива...") size 22 xalign 0.5
                
                elif dl_phase == "done":
                    text _("Установка завершена!") size 22 xalign 0.5

                bar:
                    value dl_progress range 1.0 ysize 40
                
                if dl_done:
                    text _("Установка завершена. Переход к следующему файлу...") size 20 color "#888" xalign 0.5
                    timer 0.25 action Return()