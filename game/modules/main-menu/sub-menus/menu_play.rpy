# --- ЛОГИКА ГЛАВ ---
init python:
    class ChapterItem:
        def __init__(self, label_start, title, subtitle, image, condition_var):
            self.label_start = label_start
            self.title = title
            self.subtitle = subtitle
            self.image = image
            self.condition_var = condition_var

        def is_unlocked(self):
            return getattr(persistent, self.condition_var, False)

    chapter_items = []
    def add_chapter(label_start, title, subtitle, image, condition_var):
        chapter_items.append(ChapterItem(label_start, title, subtitle, image, condition_var))

    def GetMostRecentSave():
        # Находим самый свежий сейв (включая авто)
        newest = renpy.newest_slot()
        if newest:
            return newest
        return None

# Инициализация списка глав
init 1 python:
    chapter_items = []
    # add_chapter("chapter_0", _("Глава 0"), _("Пролог"), "images/bg_prologue.avif", "chapter_0_unlocked")
    add_chapter("chapter_1", _("Глава 1"), _("Синяя Ворона"), "images/backgrounds/bg chapter_1_lab_corridor_1.avif", "chapter_1_unlocked")
    add_chapter("chapter_2", _("Глава 2"), _("В поисках подруги"), "images/backgrounds/bg chapter_2_false_memories-alex_call.avif", "chapter_2_unlocked")
    add_chapter("chapter_3", _("Глава 3"), _("Эскапизм"), "images/backgrounds/bg chapter_3_sorting-station-start.avif", "chapter_3_unlocked")
    add_chapter("chapter_4", _("Глава 4.0"), _("Ковчег на мели"), "images/backgrounds/bg chapter_4_ark-aground-veritas-station.avif", "chapter_4_unlocked")
    add_chapter("chapter_4_5a", _("Глава 4.5 - Акт I"), _("Из Изгнанницы В Созвездие"), "images/backgrounds/bg chapter_4_garden-bonatic-interior.avif", "chapter_4_5a_unlocked")
    add_chapter("chapter_4_5b", _("Глава 4.5 - Акт II"), _("Из Изгнанницы В Созвездие"), "images/backgrounds/bg chapter_4_academy-veritas-central.avif", "chapter_4_5b_unlocked")

default persistent.chapter_1_unlocked = True

################################################################################
## Саб-меню "Играть"
################################################################################

screen play_menu():
    tag menu
    zorder 25
    modal True

    use main_menu_background
    key "game_menu" action ShowMenu("main_menu")

    frame:
        style "sub_menu_frame"
        vbox:
            style "sub_menu_vbox"
            label _("Режим игры") style "sub_menu_label"

            textbutton _("Новая игра") action Start() style "sub_menu_button"

            if renpy.newest_slot():
                textbutton _("Продолжить") action FileLoad(renpy.newest_slot()) style "sub_menu_button"
            else:
                textbutton _("Продолжить") action None style "sub_menu_button" text_color "#888"

            textbutton _("Выбор сохранения") action ShowMenu("load") style "sub_menu_button"
            textbutton _("Выбор глав") action ShowMenu("chapter_select") style "sub_menu_button"

            null height 30
            textbutton _("Назад") action ShowMenu("main_menu") style "sub_menu_button"

################################################################################
## Экран Выбора Глав
################################################################################

screen chapter_select():
    tag menu
    zorder 30
    modal True
    
    add "gui/main_menu.png" # Фон
    key "game_menu" action ShowMenu("play_menu")

    textbutton _("Назад") action ShowMenu("play_menu") align (0.05, 0.05) style "main_menu_button" xsize 200

    vpgrid:
        cols 3
        spacing 30
        draggable True
        mousewheel True
        scrollbars "vertical"
        xalign 0.5
        yalign 0.6
        xsize 1200
        ysize 800

        for item in chapter_items:
            if item.is_unlocked():
                button:
                    style "chapter_button"
                    action Start(item.label_start)
                    tooltip item.title

                    vbox:
                        add item.image:
                            fit "cover"
                            xysize (320, 180)
                        
                        frame:
                            background None
                            xsize 320
                            padding (5, 10)
                            vbox:
                                text item.title style "chapter_title_text"
                                text item.subtitle style "chapter_subtitle_text"