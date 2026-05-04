label chapter_9_rpy:
    play sound "sfx/next-chapter.opus"
    call screen chapter_screen(_("Глава 9"), _("Резонирующий Диссонанс"))
    pause 2.0

    call chapter9_requiem
    call chapter9_redmist
    call chapter9_hall
    call chapter9_silence
    call chapter9_bell_toll
    call chapter9_epilogue
    
return