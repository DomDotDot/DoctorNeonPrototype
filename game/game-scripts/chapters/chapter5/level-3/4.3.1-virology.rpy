# --- ВИРУСОЛОГИЯ ---
label ch5_level3_virology:
    scene bg space_station_virology with dissolve
    
    narrator "Сектор Вирусологии. Желтые предупреждающие знаки биологической опасности."
    
    if not hasattr(store, 'ch5_virology_looted') or not ch5_virology_looted:
        narrator "В одном из охладителей мигала красная лампочка."
        menu:
            "Осмотреть охладитель":
                narrator "Внутри находилась капсула 'Цито-В'."
                neon "Базовый биоматериал. Может пригодиться."
                $ add_item(Item_ReagentA)
                $ ch5_virology_looted = True
                jump ch5_level3_virology
            "Уйти":
                jump ch5_level3_medbay_menu
    else:
        narrator "Охладители пусты. Больше ничего ценного."
        jump ch5_level3_medbay_menu