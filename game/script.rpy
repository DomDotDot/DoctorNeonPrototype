label start:

        stop music fadeout 1.0
        stop sound fadeout 1.0
        stop ambience fadeout 1.0
        stop voice fadeout 1.0
    
        label chapter_0_prologue:
                call chapter_0_prologue_rpy from _call_chapter_0_prologue_rpy



        label chapter_1:
                call chapter_1_rpy from _call_chapter_1_rpy



        label chapter_2:
                call chapter_2_rpy from _call_chapter_2_rpy



        label chapter_3:
                call chapter_3_rpy from _call_chapter_3_rpy


        
        label chapter_4:
                call chapter_4_rpy from _call_chapter_4_rpy




        label end:
                scene black with fade
                "Продолжение следует."
                $ MainMenu(confirm=False)()
        
return
