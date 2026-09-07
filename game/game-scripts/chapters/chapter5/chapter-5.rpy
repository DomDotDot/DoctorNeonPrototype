label chapter_5_rpy:

    call screen chapter_screen(_("Глава 5"), _("Предложение, от которого нельзя отказаться"))
    pause 2.0
    
    call ch5_quest_init from _call_ch5_quest_init
    
    call chapter5_introduction from _call_chapter5_introduction

    $ inventory_allowed = True
    # Откат намеренно отключен на время квеста для предотвращения сейв-скама
    $ _rollback = False

    call chapter5_start from _call_chapter5_start
    jump ch5_level2_main_hall_menu

    label chapter5_after_quest:

        $ inventory_allowed = False
        # Восстановление возможности отката после завершения квестовой части
        $ _rollback = True

        call station_server_room_entry from _call_station_server_room_entry

        call chapter5_cargo_dead_end from _call_chapter5_cargo_dead_end
        call chapter5_bridge_overload from _call_chapter5_bridge_overload

        call dream_sequence_japan_6 from _call_dream_sequence_japan_6

        call chapter5_rescue from _call_chapter5_rescue
        call chapter5_finale_sacrifice from _call_chapter5_finale_sacrifice

        call dream_sequence_japan_5 from _call_dream_sequence_japan_5

        call chapter5_wasteland from _call_chapter5_wasteland
        call chapter5_oganesson from _call_chapter5_oganesson
    return