label chapter_5_rpy:
    play sound "sfx/next-chapter.opus"
    call screen chapter_screen(_("Глава 5"), _("Предложение, от которого нельзя отказаться"))
    pause 2.0
    
    call ch5_quest_init from _call_ch5_quest_init
    
    call chapter5_introduction from _call_chapter5_introduction
    call chapter5_start from _call_chapter5_start
    jump ch5_level2_main_hall_menu

    call chapter5_timer_and_brig from _call_chapter5_timer_and_brig
    call chapter5_breakout from _call_chapter5_breakout
    call chapter5_ghost_ship from _call_chapter5_ghost_ship

    call dream_sequence_japan_6 from _call_dream_sequence_japan_6

    call chapter5_bridge_and_katana from _call_chapter5_bridge_and_katana
    call chapter5_finale_sacrifice from _call_chapter5_finale_sacrifice

    call chapter5_epilogue_earth from _call_chapter5_epilogue_earth

return