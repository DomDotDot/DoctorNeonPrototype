init python:
    def flashback_delayed_thumb(st, at, item, delay):
        if st < delay:
            return renpy.displayable("gallery_skeleton_thumb"), delay - st
        return item.get_thumbnail_displayable(), None

screen flashback_thumbnail_button(item, delay_time=0.05):
    button:
        xysize (384, 216)
        background Solid("#333")
        
        if item.is_unlocked():
            add DynamicDisplayable(flashback_delayed_thumb, item=item, delay=delay_time)
                
            action Replay(item.label, locked=False)
            hover_foreground Solid("#ffffff22")
            hovered Play("audio", "audio/sfx/cursor-hover.wav")

            # Label
            frame:
                background Solid("#00000099")
                xfill True
                yalign 1.0
                padding (10, 5)
                text item.name size 18 color "#fff" align (0.0, 0.5)
        else:
            add item.get_thumbnail_displayable()
            action NullAction()
            foreground Text("?", size=80, align=(0.5, 0.5), color="#555")

# --- FLASHBACK GALLERY SCREEN ---
screen flashback_gallery():
    tag menu
    add gui.main_menu_background

    default page = 0
    default has_paginated = False
    $ fb_rows = 3
    $ fb_cols = 3
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

                    for i, item in enumerate(current_items):
                        $ delay_val = i * 0.05 if has_paginated else 0.0
                        use flashback_thumbnail_button(item, delay_val) id ("fb_thumb_p" + str(page) + "_" + item.name.replace(" ", "_"))

                    # Fill empty cells
                    for i in range(fb_cells - len(current_items)):
                        null width 384 height 216

                # Pagination
                hbox:
                    xalign 0.5
                    spacing 50
                    
                    textbutton "<":
                        action [SetScreenVariable("page", max(0, page - 1)), SetScreenVariable("has_paginated", True)]
                        sensitive (page > 0)
                        text_size 40
                        
                    text "Страница [page+1] / [max_page+1]" yalign 0.5 color "#fff"
                    
                    textbutton ">":
                        action [SetScreenVariable("page", min(max_page, page + 1)), SetScreenVariable("has_paginated", True)]
                        sensitive (page < max_page)
                        text_size 40

            null height 40
            textbutton _("Назад") action ShowMenu("memory_recollection") style "modern_back_button"
