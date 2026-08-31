# --- MEMORY RECOLLECTION HUB SCREEN ---
screen memory_recollection():
    tag menu
    modal True
    zorder 25
    use main_menu_background
    key "game_menu" action (ShowMenu("main_menu") if main_menu else Return())

    frame:
        style "modern_panel"
        vbox:
            style "modern_vbox"
            label _("Воспоминания") style "modern_title_label"
            
            vbox:
                xalign 0.5
                spacing 25
                
                textbutton _("Галерея CG"):
                    action ShowMenu("gallery")
                    style "modern_button"
                    
                textbutton _("Флешбеки"):
                    action ShowMenu("flashback_gallery")
                    style "modern_button"

                if renpy.has_screen("achievements_screen"):
                    textbutton _("Достижения"):
                        action ShowMenu("achievements_screen")
                        style "modern_button"

            null height 30
            textbutton _("Назад") action (ShowMenu("main_menu") if main_menu else Return()) style "modern_back_button"


