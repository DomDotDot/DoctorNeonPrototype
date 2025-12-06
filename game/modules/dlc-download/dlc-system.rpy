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
    # Хранит инфо о текущем DLC (для экрана прогресса)
    current_dlc_data = None 
    # Хранит заголовок с номером в очереди (Музыка (1/3))
    dl_queue_title = ""

    # Внутренние переменные для ретрая (храним параметры текущей задачи)
    _current_task = {} 

    def _dlc_worker(url, zip_path, target_dir):
        global dl_progress, dl_status, dl_done, dl_error, dl_should_cancel

        if not os.path.exists(os.path.dirname(zip_path)):
            os.makedirs(os.path.dirname(zip_path))

        print(f"DLC Loader: Start downloading {url}")

        attempt = 0
        success = False

        while attempt < MAX_RETRIES and not success and not dl_should_cancel:
            attempt += 1
            try:
                dl_error = None
                dl_status = "Попытка {} из {}...".format(attempt, MAX_RETRIES)
                
                # Таймаут: 5 сек на коннект, 5 сек на ожидание байтов
                response = requests.get(url, stream=True, timeout=(5, TIMEOUT_SEC))

                if response.status_code == 404:
                    raise Exception("Файл не найден (404). Проверь версию!")
                if response.status_code != 200:
                    raise Exception("HTTP Error: {}".format(response.status_code))

                total_length = response.headers.get('content-length')

                with open(zip_path, 'wb') as f:
                    if total_length is None:
                        f.write(response.content)
                    else:
                        dl = 0
                        total_length = int(total_length)
                        for data in response.iter_content(chunk_size=32768): # 16kb чанки
                            if dl_should_cancel: break
                            dl += len(data)
                            f.write(data)
                            
                            # Обновляем прогресс
                            dl_progress = float(dl) / total_length
                            # Красивый статус: 15.4 / 120.0 MB
                            mb_cur = dl / 1024 / 1024
                            mb_tot = total_length / 1024 / 1024
                            dl_status = "{:.1f} / {:.1f} MB".format(mb_cur, mb_tot)

                if dl_should_cancel: return
                success = True

            except Exception as e:
                print(f"DLC Error: {e}")
                if attempt == MAX_RETRIES:
                    dl_error = str(e)
                else:
                    dl_status = "Сбой связи. Ждем..."
                    time.sleep(2)

        # Распаковка
        if success:
            try:
                dl_status = "Распаковка архива..."
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(os.path.join(config.gamedir, current_dlc_data['folder']))
                
                if os.path.exists(zip_path):
                    os.remove(zip_path)

                dl_status = "Установка завершена!"
                dl_done = True
            except Exception as e:
                dl_error = "Ошибка архива: " + str(e)
        elif not dl_error and not dl_should_cancel:
            dl_error = "Неизвестная ошибка загрузки."

    def start_download_current():
        global dl_progress, dl_status, dl_done, dl_error, dl_should_cancel, current_dlc_data
        
        # Сброс
        dl_progress = 0.0
        dl_status = "Инициализация..."
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

screen dlc_selection_screen(dlc_list):
    # dlc_list - это список словарей тех DLC, которые еще не установлены
    modal True

    # Переменная для хранения выбора игрока (id: True/False)
    # По умолчанию выбираем все доступные для скачивания
    default dlc_choices = {item['id']: True for item in dlc_list}

    frame:
        xalign 0.5 yalign 0.5
        xsize 900 ysize 700
        padding (40, 40)
        
        vbox:
            spacing 15
            
            text "Дополнительный контент" size 40 bold True xalign 0.5
            text "Выберите компоненты для установки:" size 22 xalign 0.5
            
            # Область с прокруткой, если DLC много
            viewport:
                scrollbars "vertical"
                mousewheel True
                
                vbox:
                    spacing 10
                    # Цикл по всем доступным DLC
                    for item in dlc_list:
                        hbox:
                            spacing 15
                            # Чекбокс
                            textbutton ("✓ " if dlc_choices[item['id']] else "☐ ") action SetDict(dlc_choices, item['id'], not dlc_choices[item['id']]) text_size 30
                            
                            vbox:
                                # Название и описание
                                text item['title'] size 24 bold True
                                text item['desc'] size 20 color "#ccc"

            null height 20

            hbox:
                xalign 0.5 spacing 50
                
                # Кнопка СКАЧАТЬ -> возвращает список выбранных DLC
                textbutton "Скачать выбранное" action Return([item for item in dlc_list if dlc_choices[item['id']]]) style "button" text_size 28
                
                # Кнопка ПРОПУСТИТЬ ВСЁ -> возвращает пустой список
                textbutton "Пропустить всё" action Return([]) style "button" text_size 28

# --- ОБНОВЛЕННЫЙ ЭКРАН ПРОГРЕССА ---
screen dlc_progress_screen():
    modal True
    timer 0.05 repeat True action Function(renpy.restart_interaction)

    frame:
        xalign 0.5 yalign 0.5 padding (50, 50) xsize 800
        vbox:
            spacing 20
            
            # Используем новый заголовок с номером в очереди
            text "[dl_queue_title]" size 30 bold True xalign 0.5
            
            if dl_error:
                text "ОШИБКА" color "#f00" size 26 xalign 0.5
                text "[dl_error]" size 18 xalign 0.5
                hbox:
                    xalign 0.5 spacing 30
                    # Повторяем только текущую проваленную загрузку
                    textbutton "Повторить" action Function(start_download_current)
                    # Пропускаем текущую и идем к следующей в очереди
                    textbutton "Пропустить этот пак" action Return()
            else:
                text "[dl_status]" size 22 xalign 0.5
                bar:
                    value dl_progress range 1.0 ysize 40
                
                # Кнопка "Далее" появляется, когда текущий файл скачан.
                # Нажатие на нее вернет нас в цикл для скачивания следующего файла.
                if dl_done:
                    # Вместо кнопки мы показываем текст (опционально)
                    text "Установка завершена. Переход к следующему файлу..." size 20 color "#888" xalign 0.5
                    
                    # И запускаем таймер на 1.0 секунду (чтобы игрок успел увидеть 100%)
                    # После чего экран закроется сам, и цикл перейдет к следующему файлу
                    timer 0.25 action Return()