label chapter_3_rpy:
    play sound "sfx/next-chapter.mp3"
    call screen chapter_screen(_("Глава 3"), _("Эскапизм"))
    
    call chapter3_part1_start from _call_chapter3_part1_start
    call ch3_hall_explore from _call_ch3_hall_explore

    call ch3_briefing_scene from _call_ch3_briefing_scene
    call ch3_path_to_station from _call_ch3_path_to_station
    call chapter3_the_heist_start from _call_chapter3_the_heist_start
    call chapter3_breather from _call_chapter3_breather
    
    call chapter3_on_train from _call_chapter3_on_train


return