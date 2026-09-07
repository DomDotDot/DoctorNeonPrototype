label chapter_7_rpy:

    call screen chapter_screen(_("Глава 7"), _("Туман Войны"))
    pause 2.0
    
    call chapter7_library from _call_chapter7_library
    call chapter7_apartments from _call_chapter7_apartments
    call chapter7_decay from _call_chapter7_decay

    call chapter7_penance from _call_chapter7_penance

return