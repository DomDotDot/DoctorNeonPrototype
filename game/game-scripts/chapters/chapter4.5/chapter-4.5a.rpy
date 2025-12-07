label chapter_4_5_rpy_act1:
    $ persistent.chapter_4_5a_unlocked = True
    play sound "sfx/next-chapter.opus"
    call screen chapter_screen(_("Глава 4.5"), _("Из Изгнанницы В Созвездие"), _("Акт I - Не сотвори себе кумира"))

    call chapter4_5_garden_aftermath from _call_chapter4_5_garden_aftermath
    call chapter4_5_cafe_scene from _call_chapter4_5_cafe_scene

    call chapter4_5_concert_start from _call_chapter4_5_concert_start
    call chapter4_5_concert_mid from _call_chapter4_5_concert_mid
    call chapter4_5_concert_end from _call_chapter4_5_concert_end

    call chapter4_5_nari_flashback from _call_chapter4_5_nari_flashback

    call chapter4_5_argon_rescue from _call_chapter4_5_argon_rescue

    call chapter4_5_kai_ito_interlude from _call_chapter4_5_kai_ito_interlude

    call chapter4_5_dorm_way from _call_chapter4_5_dorm_way

return