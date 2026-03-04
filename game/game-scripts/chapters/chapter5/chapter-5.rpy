label chapter_5_rpy:
    play sound "sfx/next-chapter.opus"
    call screen chapter_screen(_("Глава 5"), _("Предложение, от которого нельзя отказаться"), _("Продолжение Следует"))
    pause 2.0
    
    call ch5_quest_init
    
    call chapter5_introduction
    call chapter5_start
    jump ch5_level2_main_hall_menu

    call chapter5_timer_and_brig
    call chapter5_breakout
    call chapter5_ghost_ship

    call chapter5_bridge_and_katana
    call chapter5_finale_sacrifice

return