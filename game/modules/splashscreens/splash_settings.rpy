screen splash_settings():

    tag menu

    frame:
        style "modern_panel"

        vbox:
            style "modern_vbox"

            label _("Установите настройки") style "modern_title_label"

            text _("В следующем меню вы можете задать настройки игры. Эти параметры можно изменить в любое время в меню.") text_align 0.5 xalign 0.5 size 24 color "#cccccc"

            null height 30

            textbutton _("Подтвердить") action Return() style "main_menu_button"
