init python:
    # Функция полного сброса сюжетного прогресса
    def hard_reset_progress():
        persistent.main_menu_level = 0
        
        # Сброс открытых глав
        # (Лучше пройтись циклом, если у тебя их много, или перечислить вручную)
        persistent.chapter_1_unlocked = False
        persistent.chapter_2_unlocked = False
        persistent.chapter_3_unlocked = False
        persistent.chapter_4_unlocked = False
        persistent.chapter_4_5a_unlocked = False
        persistent.chapter_4_5b_unlocked = False
        persistent.chapter_5_unlocked = False
        
        # Сброс галереи
        if hasattr(persistent, "_seen_images"):
            persistent._seen_images.clear()
            
        # Очистка списка виденного аудио
        if hasattr(persistent, "_seen_audio"):
            persistent._seen_audio.clear()
            
        # Очистка списка "когда-либо виденного" (для пропуска текста)
        if hasattr(persistent, "_seen_ever"):
            persistent._seen_ever.clear()
        
        renpy.save_persistent()
        
        renpy.notify("Сюжетный прогресс сброшен.")
        renpy.restart_interaction()

    # Функция удаления всех сохранений
    def delete_all_saves():
        try:
            all_saves = renpy.list_saved_games(fast=True)
            for save_item in all_saves:
                renpy.unlink_save(save_item[0])
        except:
            pass

        # Список папок для зачистки
        folders_to_clean = []

        # А) Папка AppData (Основная для релиза)
        if config.savedir:
            folders_to_clean.append(config.savedir)

            sync_path = os.path.join(config.savedir, "sync")
            if os.path.exists(sync_path):
                folders_to_clean.append(sync_path)

        # Б) Папка game/saves (Локальная для разработки)
        if config.gamedir:
            local_saves_path = os.path.join(config.gamedir, "saves")
            if os.path.exists(local_saves_path):
                folders_to_clean.append(local_saves_path)

        # Удаление
        for folder in folders_to_clean:
            try:
                if not os.path.exists(folder):
                    continue
                    
                file_list = os.listdir(folder)
                
                for filename in file_list:
                    file_path = os.path.join(folder, filename)
                    
                    if "persistent" in filename:
                        continue
                    
                    if filename.endswith(".save") or filename.endswith(".png") or filename.endswith(".extra"):
                        try:
                            os.remove(file_path)
                        except Exception as e:
                            print("Не удалось удалить: " + str(filename))
                            
            except Exception as e:
                print("Ошибка доступа к папке " + folder + ": " + str(e))

            

        # Полный сброс кеша
        renpy.loadsave.save_cache = {} 
        
        renpy.notify("Все сохранения безвозвратно удалены.")
        renpy.restart_interaction()

    # Чит-код: Открыть всё.
    def unlock_everything():
        persistent.main_menu_level = 4
        persistent.chapter_1_unlocked = True
        persistent.chapter_2_unlocked = True
        persistent.chapter_3_unlocked = True
        persistent.chapter_4_unlocked = True
        persistent.chapter_4_5a_unlocked = True
        persistent.chapter_4_5b_unlocked = True
        persistent.chapter_5_unlocked = True
        persistent.unlock_gallery = True

        unlock_all_chars_full()
        
        renpy.notify("Весь контент разблокирован.")
        renpy.restart_interaction()
        


    # Сброс настроек (Preferences)
    def reset_preferences_to_default():
        # Сброс громкости
        renpy.music.set_volume(1, channel='main')
        renpy.music.set_volume(0.5, channel='main')
        renpy.music.set_volume(0.5, channel='music')
        renpy.music.set_volume(0.5, channel='sfx')
        renpy.music.set_volume(0.5, channel='voice')
        renpy.music.set_volume(0.5, channel='ambient')
        
        # Сбрас текстовых настройек
        preferences.text_cps = 35    # Скорость текста (0-100 или больше)
        preferences.afm_time = 15    # Время авточтения
    
        preferences.fullscreen = False 
        
        # Сбрас пропускка
        preferences.skip_unseen = False
        preferences.skip_after_choices = False
        
        renpy.notify("Настройки восстановлены по умолчанию.")
        renpy.restart_interaction()

screen data_settings_screen():
    tag menu
    modal True
    use main_menu_background
    key "game_menu" action ShowMenu("settings_menu")

    frame:
        style "modern_panel"

        vbox:
            style "modern_vbox"
            label _("Управление данными") style "modern_title_label"
            viewport:
                mousewheel True
                draggable True
                scrollbars "vertical"
                xsize 900
                ysize 600
                xalign 0.5
                
                vbox:
                    spacing 10
                    xfill True

                    # --- СЕКЦИЯ: НАСТРОЙКИ ---
                    label _("Общие") text_size 24 text_color "#888" xoffset 5

                    # Карточка: Сброс настроек
                    frame:
                        style "danger_zone_frame"
                        background Frame(Fixed(Solid("#555"), Solid("#000000", xmargin=2, ymargin=2), xysize=(100,100)), 4, 4)
                        
                        hbox:
                            yalign 0.5
                            xfill True
                            
                            # Текст слева
                            vbox:
                                yalign 0.5
                                text _("Сброс настроек") style "danger_title_text"
                                text _("Вернуть громкость, скорость текста и пропуск к значениям по умолчанию.") style "danger_desc_text"

                            # Кнопка справа
                            button:
                                style "neutral_button"
                                text _("Сбросить") style "danger_button_text"
                                action Confirm(_("Сбросить все настройки звука и текста?"), yes=Function(reset_preferences_to_default))


                    null height 20

                    # --- СЕКЦИЯ: ОПАСНАЯ ЗОНА ---
                    label _("Danger Zone") text_size 24 text_color "#b60205" xoffset 5

                    # Карточка: Сброс сюжета
                    frame:
                        style "danger_zone_frame_red"
                        
                        hbox:
                            yalign 0.5
                            xfill True 
                            
                            vbox:
                                yalign 0.5
                                text _("Сбросить прогресс сюжета") style "danger_title_text" color "#ffaaaa"
                                text _("Закроет все главы и вернет главное меню в начальное состояние.") style "danger_desc_text"

                            button:
                                style "danger_button"
                                text _("Сбросить") style "danger_button_text"
                                action Confirm(_("Вы уверены? Это обнулит ваш прогресс."), yes=Function(hard_reset_progress))

                    # Карточка: Удаление сейвов
                    frame:
                        style "danger_zone_frame_red"
                        
                        hbox:
                            yalign 0.5
                            xfill True 
                            
                            vbox:
                                yalign 0.5
                                text _("Удалить ВСЕ сохранения") style "danger_title_text" color "#ffaaaa"
                                text _("Безвозвратно удаляет все файлы сохранений с диска.") style "danger_desc_text"

                            button:
                                style "danger_button"
                                text _("Удалить все") style "danger_button_text"
                                action Confirm(_("Это действие нельзя отменить. Удалить все сохранения?"), yes=Function(delete_all_saves))


                    null height 20

                    # --- СЕКЦИЯ: ЧИТЫ / ТЕСТЫ ---
                    if config.developer or True: #TODO True до релиза
                        label _("Разработка") text_size 24 text_color "#2ea043" xoffset 5

                        # Карточка: Unlock All
                        frame:
                            style "danger_zone_frame_green"
                            
                            hbox:
                                yalign 0.5
                                xfill True 
                                
                                vbox:
                                    yalign 0.5
                                    text _("Разблокировать контент") style "danger_title_text" color "#aaffaa"
                                    text _("Открывает все главы, музыку и фоны меню. (Чит)") style "danger_desc_text"

                                button:
                                    style "safe_button"
                                    text _("Открыть всё") style "danger_button_text"
                                    action Confirm(_("Открыть весь контент?"), yes=Function(unlock_everything))

                        # Карточка: Unlock Characters
                        frame:
                            style "danger_zone_frame_green"
                            
                            hbox:
                                yalign 0.5
                                xfill True 
                                
                                vbox:
                                    yalign 0.5
                                    text _("Разблокировать всех пероснажей") style "danger_title_text" color "#aaffaa"
                                    text _("Открывает всех персонажей из Глоссария") style "danger_desc_text"

                                button:
                                    style "safe_button"
                                    text _("Открыть всё") style "danger_button_text"
                                    action Confirm(_("Открыть всех персонажей в Глоссарий?"), yes=Function(unlock_all_chars_full))

            # Кнопка НАЗАД (внизу)
            null height 20
            textbutton _("Назад") action ShowMenu("settings_menu") style "modern_back_button"
