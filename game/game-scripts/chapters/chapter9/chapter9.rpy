label chapter_9_rpy:
    play sound "sfx/next-chapter.opus"
    call screen chapter_screen(_("Глава 9"), _("Резонирующий Диссонанс"))
    pause 2.0

    call chapter9_requiem from _call_chapter9_requiem
    call chapter9_redmist from _call_chapter9_redmist
    call chapter9_hall from _call_chapter9_hall
    call chapter9_silence from _call_chapter9_silence
    call chapter9_bell_toll from _call_chapter9_bell_toll

    $ renpy.pause(5.0, hard=True)

    play music "music/BGM/Celestia_Piano_Theme_Slow.opus" fadein 2.0

    show text "{size=40}The Brightest Neon - Semitone Resonance{/size}" at truecenter with dissolve
    $ renpy.pause(3.0, hard=True)

    hide text with Dissolve(3.0)

    # ВЫЗОВ ТИТРОВ ДЛЯ ТОМА 2
    call credits_sequence(2) from _call_credits_sequence_1

    if _return == "secret_scene":
        call chapter9_epilogue from _call_chapter9_epilogue

return