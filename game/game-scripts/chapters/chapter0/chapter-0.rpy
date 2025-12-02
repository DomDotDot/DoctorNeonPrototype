label chapter_0_prologue_rpy:
    play sound "sfx/next-chapter.opus"
    call screen chapter_screen(_("Глава 0"), _("Пролог"))

    call prologue from _call_prologue

return