label chapter_4_rpy:
    $ persistent.chapter_4_unlocked = True
    play sound "sfx/next-chapter.opus"
    call screen chapter_screen(_("Глава 4.0"), _("Ковчег на мели"))

    call dream_sequence_japan_2 from _call_dream_sequence_japan_2

    call chapter4_0_train_dream from _call_chapter4_0_train_dream
    call chapter4_0_arkaground from _call_chapter4_0_arkaground
    call chapter4_0_academy from _call_chapter4_0_academy
    call chapter4_0_24syndrome from _call_chapter4_0_24syndrome
    call chapter4_0_garden from _call_chapter4_0_garden

return