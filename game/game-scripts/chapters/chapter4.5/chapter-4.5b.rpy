label chapter_4_5_rpy_act2:
    $ persistent.chapter_4_5b_unlocked = True
    call screen chapter_screen(_("Глава 4.5"), _("Из Изгнанницы В Созвездие"), _("Акт II - И никакого изображения того, что на небе вверху"))

    call chapter4_5_boulevard_night from _call_chapter4_5_boulevard_night

    call chapter4_5_morning_after from _call_chapter4_5_morning_after
    call chapter4_5_akari_arrest from _call_chapter4_5_akari_arrest

    call chapter4_5_seraphina_penthouse from _call_chapter4_5_seraphina_penthouse
    
    call chapter4_5_lily_cafe from _call_chapter4_5_lily_cafe

    call dream_sequence_japan_4 from _call_dream_sequence_japan_4
    call chapter4_5_awakening_and_finale from _call_chapter4_5_awakening_and_finale

    call chapter4_5_finale from _call_chapter4_5_finale
    call chapter4_5_epilogue from _call_chapter4_5_epilogue

    $ add_notification("msg_end", _("Спасибо за игру!"), _("Я рад, что вы прошли её. Это ещё не конец, а лишь первая часть истории (Первый Том) История о Селестии только начинается. Сможет ли Неон найти своих подруг? Найти своё прошлое?"))
    
    # ВЫЗОВ ТИТРОВ ДЛЯ ТОМА 1
    call credits_sequence(1) from _call_credits_sequence

    if _return == "secret_scene":
        jump secret_scene_vol1
    
    return # В главное меню

return