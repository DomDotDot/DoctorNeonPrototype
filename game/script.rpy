label start:
        
        # Переменная, которая будет храниться между прохождениями.
        # 0 - стандартное меню
        # 1 - первый этап
        # 2 - второй этап
        # и т.д

        default persistent.main_menu_level = 0
        
        # По умолчанию False (выключено/цензура).
        default persistent.sensitive_mode = False

        image main_menu_logo = "gui/main_menu/logo2.avif"

        image main_menu_bg_default = "gui/main_menu/background_default.avif"
        image main_menu_bg_unlocked_1 = "gui/main_menu/background_unlocked_1.avif"
        image main_menu_bg_unlocked_2 = "gui/main_menu/background_unlocked_2.avif"
        image main_menu_bg_unlocked_3 = "gui/main_menu/background_unlocked_3.avif"
        image main_menu_bg_unlocked_4 = "gui/main_menu/background_unlocked_4.avif"

        define main_menu_music_default = "audio/music/BGM/NightMare.opus"
        define main_menu_music_unlocked_1 = "audio/music/BGM/FearForUnreal.opus"
        define main_menu_music_unlocked_2 = "audio/music/BGM/WitheredFlower.opus"
        define main_menu_music_unlocked_3 = "audio/music/BGM/Sorrowless.opus"
        define main_menu_music_unlocked_4 = "audio/music/BGM/BuzzingGoodbye.opus"


        stop music fadeout 1.0
        stop sound fadeout 1.0
        stop ambient fadeout 1.0
        stop voice fadeout 1.0


    
        label chapter_0_prologue:
                call chapter_0_prologue_rpy from _call_chapter_0_prologue_rpy



        label chapter_1:
                call chapter_1_rpy from _call_chapter_1_rpy
                $ persistent.main_menu_level = 1



        label chapter_2:
                call chapter_2_rpy from _call_chapter_2_rpy
                $ persistent.main_menu_level = 2



        label chapter_3:
                call chapter_3_rpy from _call_chapter_3_rpy


        
        label chapter_4:
                call chapter_4_rpy from _call_chapter_4_rpy
                $ persistent.main_menu_level = 3



        label chapter_4_5:
                call chapter_4_5_rpy from _call_chapter_4_5_rpy
                $ persistent.main_menu_level = 4

        label chapter_5:
                call chapter_5_rpy from _call_chapter_5_rpy



        label end:
                scene black with fade
                "Продолжение следует."
                $ MainMenu(confirm=False)()
        
return
