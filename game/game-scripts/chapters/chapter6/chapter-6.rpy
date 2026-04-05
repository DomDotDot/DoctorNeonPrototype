label chapter_6_rpy:
    play sound "sfx/next-chapter.opus"
    call screen chapter_screen(_("Глава 6"), _("Первый ряд, Пятое место"))
    pause 2.0
    
    call chapter6_alley_valley from _call_chapter6_alley_valley

    call chapter6_spire from _call_chapter6_spire
    call chapter6_tradingcenter from _call_chapter6_tradingcenter
    call chapter6_encounter from _call_chapter6_encounter

    call chapter6_ceo from _call_chapter6_ceo

    call chapter6_krypton from _call_chapter6_krypton

return