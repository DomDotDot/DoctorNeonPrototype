label chapter_2_rpy:
        play sound "sfx/next-chapter.mp3"
        call screen chapter_screen(_("Глава 2"), _("В поисках подруги"))
        call krypton_firstmeet_flashback from _call_krypton_firstmeet_flashback

        call chapter2_act1_false_memories from _call_chapter2_act1_false_memories
        call chapter2_act2_long_night from _call_chapter2_act2_long_night

        call nightmare_sequence from _call_nightmare_sequence
        
        call chapter2_act3_facing_reality from _call_chapter2_act3_facing_reality
        call chapter2_act4_desperate_measures from _call_chapter2_act4_desperate_measures
        
        call chapter2_act5_journey_to_anomic from _call_chapter2_act5_journey_to_anomic

        # --- Глава 2, Акт 5: Сон о Японии ---
        call dream_sequence_japan_1 from _call_dream_sequence_japan_1
        # --- Конец сна о Японии ---

        call chapter2_act5_anomic_arrival from _call_chapter2_act5_anomic_arrival
return