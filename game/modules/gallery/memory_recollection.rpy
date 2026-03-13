# --- MEMORY RECOLLECTION HUB SCREEN ---
screen memory_recollection():
    tag menu
    modal True
    zorder 25
    use main_menu_background
    key "game_menu" action Return()

    frame:
        style "modern_panel"
        vbox:
            style "modern_vbox"
            label _("Воспоминания") style "modern_title_label"
            
            vbox:
                xalign 0.5
                spacing 40
                
                textbutton _("Галерея CG"):
                    action ShowMenu("gallery")
                    style "modern_button"
                    
                textbutton _("Флешбеки"):
                    action ShowMenu("flashback_gallery")
                    style "modern_button"

            null height 30
            textbutton _("Назад") action Return() style "modern_back_button"


