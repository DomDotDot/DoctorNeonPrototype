label chapter_1_rpy:
    play sound "sfx/next-chapter.opus"
    call screen chapter_screen(_("Глава 1"), _("Синяя Ворона"))


    call chapter1_lab_night from _call_chapter1_lab_night

    call chapter1_krypton_baddream from _call_chapter1_krypton_baddream

    call chapter1_lab_morning from _call_chapter1_lab_morning
    call chapter1_lab_noon from _call_chapter1_lab_noon


    call chapter1_lab_noon_library from _call_chapter1_lab_noon_library
    call zurich_university_flashback_1 from _call_zurich_university_flashback_1
    call chapter1_lab_noon_library_desk from _call_chapter1_lab_noon_library_desk


    call chapter1_meeting_start from _call_chapter1_meeting_start

    call oganesson_school_flashback_1
    
    call chapter1_meeting_aftermath_hallway from _call_chapter1_meeting_aftermath_hallway


    call chapter1_security_post_scene from _call_chapter1_security_post_scene
    call chapter1_confrontation_path
    call chapter1_marcus_attack_scene

    call chapter1_escape

return