screen notification_center():
    tag menu
    add gui.main_menu_background

    frame:
        xalign 0.5 yalign 0.5
        xsize 800 ysize 600
        padding (40, 40)
        
        vbox:
            spacing 20
            
            # Заголовок
            hbox:
                xalign 0.5
                text _("Центр уведомлений") size 40 bold True
            
            null height 20
            
            # --- СПИСОК УВЕДОМЛЕНИЙ ---
            viewport:
                scrollbars "vertical"
                mousewheel True
                ysize 400
                
                vbox:
                    spacing 15
                    
                    # 1. УВЕДОМЛЕНИЕ ОБ ОБНОВЛЕНИИ
                    if update_found:
                        frame:
                            background Frame("gui/frame.png", 10, 10) # Или Solid("#333")
                            xfill True
                            padding (20, 20)
                            
                            vbox:
                                spacing 10
                                hbox:
                                    text _("Доступна новая версия!") color "#ffcc00" bold True size 22
                                    if persistent.ignored_version == new_version_tag:
                                        # Пометка, что это скрытое обновление
                                        text " (Скрыто)" color "#888" size 18 yalign 1.0
                                
                                text _("Версия: [new_version_tag]") size 18
                                
                                hbox:
                                    spacing 20
                                    textbutton _("Скачать (Itch.io)") action OpenURL(LINK_ITCH) style "button" text_size 18
                                    textbutton _("Скачать (GitHub)") action OpenURL(LINK_GITHUB) style "button" text_size 18
                                    
                                    # Кнопка "Снять игнор" (Опционально)
                                    if persistent.ignored_version == new_version_tag:
                                        textbutton _("Включить напоминание") action SetField(persistent, "ignored_version", None) text_size 16 text_color "#aaa" yalign 0.5

                    # 2. ЗАГЛУШКА, ЕСЛИ ПУСТО
                    else:
                        text _("Нет новых уведомлений.") color "#888" xalign 0.5 yalign 0.5
            
            # Кнопка Назад
            textbutton _("Вернуться") action Return() xalign 0.5 yoffset 20