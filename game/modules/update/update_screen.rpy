screen update_popup_screen(note):
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
            text "[note.title!t]" size 24 xalign 0.5

            text _("Новая версия доступна в центре уведомлений.") size 18 color "#aaa" xalign 0.5 text_align 0.5
            
            hbox:
                spacing 30 xalign 0.5
                
                # Кнопка "Посмотреть сейчас"
                textbutton _("Подробнее") action [Hide("update_popup_screen"), ShowMenu("notification_center")] style "button" padding (20, 10)
                
                # Кнопка "Позже"
                textbutton _("Позже") action Hide("update_popup_screen") style "button" padding (20, 10)