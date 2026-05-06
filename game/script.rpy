label start:

        stop music fadeout 1.0
        stop sound fadeout 1.0
        stop ambient fadeout 1.0
        stop voice fadeout 1.0


    
        #label chapter_0_prologue:
                #call chapter_0_prologue_rpy from _call_chapter_0_prologue_rpy

        $ persistent.chapter_1_unlocked = True

        label chapter_1:
                $ fix_chapter_names(1)
                call chapter_1_rpy from _call_chapter_1_rpy
                $ persistent.chapter_2_unlocked = True
                $ persistent.main_menu_level = 1



        label chapter_2:
                $ fix_chapter_names(2)
                call chapter_2_rpy from _call_chapter_2_rpy
                $ persistent.chapter_3_unlocked = True
                $ persistent.main_menu_level = 2



        label chapter_3:
                $ fix_chapter_names(3)
                call chapter_3_rpy from _call_chapter_3_rpy
        
        label chapter_4:
                $ persistent.chapter_4_unlocked = True
                $ fix_chapter_names(4)
                call chapter_4_rpy from _call_chapter_4_rpy
                $ persistent.chapter_4_5a_unlocked = True
                $ persistent.main_menu_level = 3



        label chapter_4_5a:
                $ fix_chapter_names(4.5)
                call chapter_4_5_rpy_act1 from _call_chapter_4_5_rpy_act1

        label chapter_4_5b:
                $ persistent.chapter_4_5b_unlocked = True
                $ fix_chapter_names(4.6)
                call chapter_4_5_rpy_act2 from _call_chapter_4_5_rpy_act2

                $ persistent.chapter_5_unlocked = True
                $ persistent.main_menu_level = 4

        label volume_1_end:
                call screen chapter_screen(_("Конец Первого Тома"), _("Спасибо за игру!"))
                $ MainMenu(confirm=False)()

        label chapter_5:
                $ fix_chapter_names(5)
                call chapter_5_rpy from _call_chapter_5_rpy

                $ persistent.chapter_6_unlocked = True

        label chapter_6:
                $ fix_chapter_names(6)
                call chapter_6_rpy from _call_chapter_6_rpy

                $ persistent.chapter_7_unlocked = True
        
        label chapter_7:
                $ fix_chapter_names(7)
                call chapter_7_rpy from _call_chapter_7_rpy

                $ persistent.chapter_8_unlocked = True

        label chapter_8:
                $ fix_chapter_names(8)
                call chapter_8_rpy from _call_chapter_8_rpy

                $ persistent.chapter_9_unlocked = True

        label chapter_9:
                $ fix_chapter_names(9)
                call chapter_9_rpy from _call_chapter_9_rpy

                $ persistent.end_unlocked = True

        label volume_2_end:
                call screen chapter_screen(_("Конец Второго Тома"), _("Спасибо за игру!"))
                $ MainMenu(confirm=False)()

        label end:
                scene black with fade
                # "Продолжение следует."
                $ MainMenu(confirm=False)()
        
return
