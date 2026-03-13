screen notification_center():
    tag menu
    modal True
    use main_menu_background

    frame:
        style "modern_panel"
        
        vbox:
            style "modern_vbox"
            
            # Шапка
            hbox:
                xfill True
                label _("Центр уведомлений") style "modern_title_label" align (0.0, 0.5)
                
                # Кнопка "Отметить все как прочитанные"
                if get_unread_count() > 0:
                    textbutton _("Прочитать все") action Function(mark_all_read) align (1.0, 0.5) text_size 18
            
            null height 10

            # --- СПИСОК (VIEWPORT) ---
            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True
                ysize 500
                
                vbox:
                    spacing 15
                    xfill True
                    
                    if not persistent.notifications:
                        text _("Уведомлений нет.") color "#888" xalign 0.5 yalign 0.5
                    
                    for note in persistent.notifications:
                        # Карточка одного уведомления
                        frame:
                            background Frame("gui/frame.png", 10, 10) # Замените на свой фон
                            xfill True
                            padding (20, 20)
                            
                            hbox:
                                spacing 20
                                
                                # Маркер непрочитанного (Красная точка или полоска)
                                if not note.is_read:
                                    frame:
                                        background Solid("#ffcc00")
                                        xsize 5 ysize 50
                                        yalign 0.5
                                else:
                                    null width 5

                                vbox:
                                    spacing 5
                                    xfill True
                                    
                                    # Заголовок и Дата
                                    hbox:
                                        xfill True
                                        text "[note.title!t]" bold True size 22 color ("#fff" if not note.is_read else "#aaa")
                                        # Кнопка удаления (крестик)
                                        textbutton "✕" action Function(delete_notification, note) text_color "#666" text_hover_color "#f00" align (1.0, 0.0)

                                    # Текст сообщения
                                    text "[note.message!t]" size 18 color ("#ddd" if not note.is_read else "#888")
                                    
                                    # ЕСЛИ ЭТО ОБНОВЛЕНИЕ - ПОКАЗЫВАЕМ КНОПКИ
                                    if note.version_tag:
                                        null height 10
                                        hbox:
                                            spacing 15
                                            if note.link_itch:
                                                textbutton _("Itch.io") action OpenURL(note.link_itch) style "button" text_size 16 padding (10,5)
                                            if note.link_github:
                                                textbutton _("GitHub") action OpenURL(note.link_github) style "button" text_size 16 padding (10,5)
                                            
                                            # Управление игнором
                                            if persistent.ignored_version == note.version_tag:
                                                textbutton _("Включить напоминание") action SetField(persistent, "ignored_version", None) text_size 14 text_color "#666" yalign 0.5
                                            else:
                                                textbutton _("Не напоминать") action SetField(persistent, "ignored_version", note.version_tag) text_size 14 text_color "#666" yalign 0.5
            
            # Подвал
            null height 20
            textbutton _("Назад") action [Function(mark_all_read), Return()] style "modern_back_button"