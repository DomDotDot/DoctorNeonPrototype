label chapter_7_rpy:
    play sound "sfx/next-chapter.opus"
    call screen chapter_screen(_("Глава 7"), _("Школьные… дни?"))
    pause 2.0
    
    call chapter8_drown

    call chapter8_school_days
    call chapter8_basketball
    call chapter8_infirmary

    call chapter8_search

    call chapter8_dream_cave

    call chapter8_letter
    call chapter8_mismatch

return