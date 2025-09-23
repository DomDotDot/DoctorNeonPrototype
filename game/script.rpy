label start:

        stop music fadeout 1.0
        stop sound fadeout 1.0
        stop ambience fadeout 1.0
        stop voice fadeout 1.0
    
        label chapter_0_prologue:
                call chapter_0_prologue_rpy



        label chapter_1:
                call chapter_1_rpy



        label chapter_2:
                call chapter_2_rpy



        label chapter_3:
                menu:
                        "Я знаю, что клиффхэнгеры могут расстраивать, поэтому сейчас я дам вам прочесть фрагмент третьей главы. Пожалуйста, обратите внимание, что глава 3 находится на ранней стадии разработки. Лучше воздержаться от начала игры."
                        
                        "Играть в Главу 3 (В РАЗРАБОТКЕ)":
                                call chapter_3_rpy
                        "Пока":
                                call end from _call_end



        label end:
                scene black with fade
                "Продолжение следует."
                $ MainMenu(confirm=False)()
        
return
