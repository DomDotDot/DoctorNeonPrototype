screen update_notification_screen():
    modal True
    zorder 2000
    
    frame:
        xalign 0.5 yalign 0.5
        xsize 600
        padding (40, 40)
        
        vbox:
            spacing 20
            xalign 0.5
            
            text _("Доступно обновление!") size 40 bold True color "#ffcc00" xalign 0.5
            
            text _("Текущая версия: [config.version!t]") size 18 color "#888" xalign 0.5
            text _("Новая версия: [new_version_tag!t]") size 24 color "#fff" xalign 0.5
            
            null height 20
            
            text _("Где скачать?") size 22 bold True xalign 0.5
            
            hbox:
                spacing 30 xalign 0.5
                
                # Кнопка ITCH.IO
                textbutton _("Itch.io") action OpenURL(LINK_ITCH) style "button" text_size 28 padding (15, 10)
                
                # Кнопка GITHUB
                textbutton _("GitHub") action OpenURL(LINK_GITHUB) style "button" text_size 28 padding (15, 10)

            null height 30
            
            # Кнопки управления окном
            vbox:
                spacing 10 xalign 0.5

                # Просто закрыть (напомнит при следующем запуске)
                textbutton "Напомнить позже" action [SetVariable("update_found", False), Hide("update_notification_screen")] xalign 0.5 text_color "#aaa"
                
                # Запомнить и не показывать для ЭТОЙ версии
                textbutton "Пропустить эту версию" action [
                    SetField(persistent, "ignored_version", new_version_tag),
                    Function(renpy.save_persistent), 
                    SetVariable("update_found", False), 
                    Hide("update_notification_screen")
                ] xalign 0.5 text_color "#aaa"