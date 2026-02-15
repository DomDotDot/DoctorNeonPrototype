# --- MEMORY RECOLLECTION HUB SCREEN ---
screen memory_recollection():
    tag menu
    add "gui/main_menu.png" # Using standard background

    use game_menu(_("Memory Recollection")):
        
        vbox:
            align (0.5, 0.5)
            spacing 40
            
            textbutton _("Галерея CG"):
                action ShowMenu("gallery")
                text_size 60
                xalign 0.5
                text_idle_color "#aaaaaa"
                text_hover_color "#ffffff"
                
            textbutton _("Воспоминания"):
                action ShowMenu("flashback_gallery")
                text_size 60
                xalign 0.5
                text_idle_color "#aaaaaa"
                text_hover_color "#ffffff"




# --- CUSTOM GAME MENU WRAPPER FOR NAVIGATION ---
screen memory_game_menu(title, scroll=None, yinitial=0.0, spacing=0, return_action=Return()):
    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:
            # Navigation placeholder
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":
                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True
                        side_yfill True
                        vbox:
                            spacing spacing
                            transclude
                elif scroll == "vpgrid":
                     vpgrid:
                        cols 1
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True
                        side_yfill True
                        spacing spacing
                        transclude
                else:
                    transclude

    use navigation

    textbutton _("Вернуться"):
        style "return_button"
        action return_action

    label title

    if main_menu:
        key "game_menu" action return_action
