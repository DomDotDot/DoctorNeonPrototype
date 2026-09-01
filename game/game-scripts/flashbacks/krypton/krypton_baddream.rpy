label chapter1_krypton_baddream:

    scene black with Fade(0.5, 0.0, 0.5)
    stop music fadeout 2.0

    narrator """
    Тьма под сомкнутыми веками дышала весенней оттепелью: сырой землей, первыми цветами, нагретым солнцем гранитом.
    
    Сквозь темноту проступили мягкие акварельные пятна, собираясь в до боли знакомый силуэт.
    
    Пышные пряди — черные и ослепительно белые, переплетенные, словно клавиши рояля. Снег и полночь.
    
    Она обернулась ко мне.
    """

    show krypton smile with Dissolve(2.0)
    play sound "sfx/sfx_zurich-bells.opus" fadein 10.0 loop volume 0.25

    "???" "Неон! Ну где ты ходишь?"
    
    narrator "Ее голос звучал кристально чисто, без единой помехи."

    "???" "Слышишь колокола? Лекции закончились! Идем в парк, пожалуйста?"

    neon "{=thoughts}В парк... С тобой — хоть на край света.{/thoughts}"

    show krypton gratitude

    "???" "На улице такое солнце... Я так тебя ждала."

    narrator """
    Она протянула мне раскрытую ладонь.
    
    Я подалась вперед, пальцы почти коснулись её тепла...
    """

    stop sound fadeout 10.0
    #show krypton gratitude at Glitch(_fps=6.0, glitch_strength=.03125, color_range1="#00000000", color_range2="#00000000")
    $ renpy.pause(0.125, hard=True)
    hide krypton gratitude with Fade(2.5, 5.0, 2.5)

    $ persistent.flashback_krypton_2_unlocked = True
return