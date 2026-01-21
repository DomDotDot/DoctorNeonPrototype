label chapter_5_rpy:
    play sound "sfx/next-chapter.opus"
    call screen chapter_screen(_("Глава 5"), _("Предложение, от которого нельзя отказаться"), _("Продолжение Следует"))

    pause 2.0

    call screen chapter_screen(_(""), _("2 Года спустя..."), _("Спустя инцидента Веритаса"))
    
    call chapter5_start
    call chapter5_exploration
    call station_hub_menu

return