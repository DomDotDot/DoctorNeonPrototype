label chapter_8_rpy:
    play sound "sfx/next-chapter.opus"
    call screen chapter_screen(_("Глава 8"), _("Школьные… дни?"))
    pause 2.0
    
    call chapter8_drown

    call chapter8_school_days
    call chapter8_basketball
    call chapter8_infirmary

    call chapter8_search

    call chapter8_dream_cave

    call chapter8_letter
    call chapter8_mismatch

    call chapter8_morning_incident
    call chapter8_invitation
    call chapter8_new_classmate
    call chapter8_club

    call chapter8_lost_key
    call chapter8_date
    call chapter8_tide

    call chapter8_loneless
    call chapter8_memory_sea

    call chapter8_boundless
    call chapter8_helium
    call chapter8_dream
return