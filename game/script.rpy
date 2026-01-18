label start:

        stop music fadeout 1.0
        stop sound fadeout 1.0
        stop ambient fadeout 1.0
        stop voice fadeout 1.0


    
        #label chapter_0_prologue:
                #call chapter_0_prologue_rpy from _call_chapter_0_prologue_rpy

        $ persistent.chapter_1_unlocked = True

        label chapter_1:
                call chapter_1_rpy from _call_chapter_1_rpy
                $ persistent.chapter_2_unlocked = True
                $ persistent.main_menu_level = 1



        label chapter_2:
                call chapter_2_rpy from _call_chapter_2_rpy
                $ persistent.chapter_3_unlocked = True
                $ persistent.main_menu_level = 2



        label chapter_3:
                call chapter_3_rpy from _call_chapter_3_rpy
        
        label chapter_4:
                $ persistent.chapter_4_unlocked = True
                call chapter_4_rpy from _call_chapter_4_rpy
                $ persistent.chapter_4_5a_unlocked = True
                $ persistent.main_menu_level = 3



        label chapter_4_5a:
                call chapter_4_5_rpy_act1 from _call_chapter_4_5_rpy_act1

        label chapter_4_5b:
                $ persistent.chapter_4_5b_unlocked = True
                call chapter_4_5_rpy_act2 from _call_chapter_4_5_rpy_act2
                $ persistent.chapter_5_unlocked = True
                $ persistent.main_menu_level = 4

        label chapter_5:
                call chapter_5_rpy from _call_chapter_5_rpy



        label end:
                scene black with fade
                "Продолжение следует."
                $ MainMenu(confirm=False)()
        
return
