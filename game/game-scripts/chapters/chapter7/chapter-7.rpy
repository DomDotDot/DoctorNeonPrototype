label chapter_7_rpy:
    play sound "sfx/next-chapter.opus"
    call screen chapter_screen(_("Глава 7"), _("Туман Войны"))
    pause 2.0
    
    call chapter7_library
    call chapter7_apartments
    call chapter7_decay

return