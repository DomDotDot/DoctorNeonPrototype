label chapter_5_rpy:
    play sound "sfx/next-chapter.opus"
    call screen chapter_screen(_("Глава 5"), _("Предложение, от которого нельзя отказаться"), _("Продолжение Следует"))
    pause 2.0
    #call screen chapter_screen(_(""), _("2 Года спустя..."), _("Спустя инцидента Веритаса"))
    
    #call chapter5_start from _call_chapter5_start
    #call chapter5_exploration from _call_chapter5_exploration
    #call station_hub_menu from _call_station_hub_menu

    #call chapter5_introduction from _call_chapter5_introduction
    #call chapter5_start from _call_chapter5_start_1

return