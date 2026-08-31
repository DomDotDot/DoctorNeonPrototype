
style chapter_number_style:
    color "#FFFFFF"
    size 40
    xalign 0.5
    bottom_margin 20

style chapter_title_style:
    color "#FFFFFF"
    size 60
    xalign 0.5

style chapter_subtitle_style:
    color "#CCCCCC"
    size 30
    xalign 0.5
    top_margin 10
    italic True

# Определение экрана
screen chapter_screen(chapter_text, title_text, subtitle_text=None):
    modal True

    on "show" action Function(start_chapter_tracking)
    timer 5.0 action [Hide('chapter_screen', transition=dissolve), Return()]
    
    frame:
        xfill True
        yfill True
        background "#000000" # ("#000000cc" для прозрачности)
        padding (50, 50)

    vbox:
        align (0.5, 0.5)

        text chapter_text style "chapter_number_style"
        text title_text style "chapter_title_style"

        if subtitle_text:
                text subtitle_text style "chapter_subtitle_style"