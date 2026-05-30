# --- ГЕНЕТИКА ---
label ch5_level3_genetics:
    scene bg space_station_genetics with dissolve
    
    narrator "Отдел Генетики. Ряды секвенаторов ДНК тихо гудели в темноте."
    
    if not hasattr(store, 'ch5_genetics_looted') or not ch5_genetics_looted:
        narrator "На одном из столов я заметила открытый кейс с химикатами."
        menu:
            "Осмотреть кейс":
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