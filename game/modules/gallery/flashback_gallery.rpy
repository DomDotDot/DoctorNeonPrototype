# --- FLASHBACK GALLERY SCREEN ---
screen flashback_gallery():
    tag menu
    add gui.main_menu_background

    default page = 0
    $ fb_rows = 2
    $ fb_cols = 2
    $ fb_cells = fb_rows * fb_cols
    
    $ max_page = (len(flashback_items) - 1) // fb_cells if len(flashback_items) > 0 else 0
    $ start_index = page * fb_cells
    $ end_index = min(start_index + fb_cells, len(flashback_items))
    $ current_items = flashback_items[start_index:end_index]

    frame:
        style "modern_panel_wide"

        vbox:
            style "modern_vbox"

            label _("Флешбеки") style "modern_title_label"

            if len(flashback_items) == 0:
                text _("Пока нет воспоминаний.") align (0.5, 0.5)
            else:
                grid fb_cols fb_rows:
                    spacing 30
                    xalign 0.5

                    for item in current_items:
                        button:
                            xysize (400, 250)
                            background Solid("#333")
                            hover_foreground Solid("#ffffff22")

                            # Thumbnail
                            add item.get_thumbnail() fit "cover" size (400, 250)

                            # Label
                            frame:
                                align (0.5, 1.0)
                                xfill True
                                background Solid("#000000AA")
                                text item.name size 20 align (0.5, 0.5) color "#fff"

                            if item.is_unlocked():
                                action Replay(item.label, locked=False)
                            else:
                                action NullAction()
                                foreground Text("?", size=80, align=(0.5, 0.5), color="#555")

                    # Fill empty cells
                    for i in range(fb_cells - len(current_items)):
                        null width 400 height 250

                # Pagination
                hbox:
                    xalign 0.5
                    spacing 50
                    
                    textbutton "<":
                        action SetScreenVariable("page", max(0, page - 1))
                        sensitive (page > 0)
                        text_size 40
                        
                    text "Страница [page+1] / [max_page+1]" yalign 0.5 color "#fff"
                    
                    textbutton ">":
                        action SetScreenVariable("page", min(max_page, page + 1))
                        sensitive (page < max_page)
                        text_size 40

            null height 40
            textbutton _("Назад") action ShowMenu("memory_recollection") style "modern_back_button"
