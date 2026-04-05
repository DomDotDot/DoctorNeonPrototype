################################################################################
## Unified Modern GUI Styles (Glassmorphism & Dark Theme)
################################################################################

#
# Modern Panels (Sub-menus, PAUSE)
#
style modern_panel is frame:
    background Solid("#000000cc") # Glassmorphism dark background
    xalign 0.5
    yalign 0.5
    xsize 1000
    padding (50, 50)
    modal True

style modern_panel_wide is modern_panel:
    xsize 1200

#
# Common Layouts
#
style modern_vbox is vbox:
    xalign 0.5
    spacing 20

style main_menu_vbox is modern_vbox:
    xalign 0.5
    yalign 0.80
    yoffset 0
    spacing 15

#
# Titles
#
style modern_title_label is label:
    xalign 0.5
    bottom_margin 40

style modern_title_text is label_text:
    size 50
    color gui.accent_color
    text_align 0.5
    bold True

#
# Base Buttons
#
style modern_button is button:
    xsize 400
    ysize 65
    xalign 0.5
    yalign 0.5
    background Solid("#000000cc") 
    hover_background Solid("#222222cc")
    hover_sound "audio/sfx/cursor-hover.opus" 
    activate_sound "audio/sfx/button-click.opus"

style modern_button_text is button_text:
    size 28
    color "#e8e8e8"
    hover_color "#ffffff"
    selected_color "#ffffff"
    insensitive_color "#555555"
    xalign 0.5
    yalign 0.5
    bold True

#
# Specific Buttons
#
style main_menu_button is modern_button:
    xsize 350
    ysize 75

style main_menu_button_text is modern_button_text:
    size 32

style modern_back_button is modern_button:
    xsize 300
    ysize 50
    background None 
    hover_background Solid("#222222cc")
    xalign 0.5

style modern_back_button_text is modern_button_text:
    xalign 0.5
    text_align 0.5

#
# Settings Check/Sliders
#
style settings_check_label is label:
    xalign 0

style settings_check_label_text is label_text:
    size 24
    color "#cccccc"
    bottom_margin 5

style settings_check_button is button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"
    xsize 400

style settings_check_button_text is button_text:
    properties gui.text_properties("check_button")
    size 22

style settings_slider_label is settings_check_label:
    text_align 1

style settings_slider_label_text is settings_check_label_text:
    size 24
    color "#ffffff"
    bottom_margin 5

style settings_slider_bar is bar:
    xfill True 
    ysize 12
    left_bar Solid("#08608f")
    right_bar Solid("#333333")
    thumb Solid("#0f63c9")
    thumb_shadow None
    thumb_offset 6

style settings_test_button is button:
    xsize 100
    ysize 35
    left_margin 15
    background Solid("#ffffff10")
    hover_background Solid("#ffffff30")
    
style settings_test_button_text is button_text:
    size 20
    xalign 0.5
    yalign 0.5

#
# Chapter Buttons
#
style chapter_button is button:
    background Solid("#00000080")
    hover_background Solid("#ffffff20")
    xsize 335
    ysize 250

style chapter_title_text is text:
    size 22
    bold True
    color "#eba900"
    layout "subtitle"

style chapter_subtitle_text is text:
    size 16
    color "#cccccc"

#
# Danger / Safe Zones (Data Menu)
#
style danger_zone_frame:
    background Solid("#00000080") 
    xfill True
    ysize 110
    padding (20, 15)
    margin (0, 10)

style danger_zone_frame_red is danger_zone_frame:
    background Frame(Fixed(Solid("#b60205"), Solid("#000000", xmargin=2, ymargin=2), xysize=(100,100)), 4, 4)

style danger_zone_frame_green is danger_zone_frame:
    background Frame(Fixed(Solid("#2ea043"), Solid("#000000", xmargin=2, ymargin=2), xysize=(100,100)), 4, 4)

style danger_title_text:
    size 28
    bold True
    color "#ffffff"

style danger_desc_text:
    size 18
    color "#aaaaaa"

style danger_button is modern_button:
    background Solid("#b60205")
    hover_background Solid("#ff4444")
    xsize 200
    ysize 50
    xalign 1.0 
    yalign 0.5
    
style danger_button_text is modern_button_text:
    color "#ffffff"

style safe_button is danger_button:
    background Solid("#2ea043")
    hover_background Solid("#4ac260")

style neutral_button is danger_button:
    background Solid("#333333")
    hover_background Solid("#555555")
