# --- ГЕНЕТИКА ---
label ch5_level3_genetics:
    scene ch05_cg36_v01 with dissolve
    
    narrator "Отдел Генетики. Ряды секвенаторов ДНК тихо гудели в темноте."
    
    if not hasattr(store, 'ch5_genetics_looted') or not ch5_genetics_looted:
        narrator "На одном из столов я заметила открытый кейс с химикатами."
        menu:
            "Осмотреть кейс":
                if not getattr(store, 'ch5_monorail_terminal_seen', False) or not getattr(store, 'ch5_medbay_empty_spray_taken', False):
                    neon "{=thoughts}Синяя жидкость в ампуле... Кажется, это 'Ген-Связь'. Но сейчас мне это не нужно.{/thoughts}"
                    jump ch5_level3_medbay_fwd_corridor
                narrator "Синяя жидкость в ампуле 'Ген-Связь'."
                neon "Протеиновый коннектор для ДНК. Беру."
                $ add_item(Item_ReagentB)
                $ ch5_genetics_looted = True
                jump ch5_level3_genetics
            "Уйти":
                jump ch5_level3_medbay_fwd_corridor
    else:
        narrator "Лаборатория уже обыскана."
        jump ch5_level3_medbay_fwd_corridor