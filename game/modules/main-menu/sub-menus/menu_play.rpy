# --- ЛОГИКА ГЛАВ ---
init python:
    class SubchapterItem:
        def __init__(self, label_start, title, description, category):
            self.label_start = label_start
            self.title = title
            self.description = description
            self.category = category

    class ChapterItem:
        def __init__(self, label_start, title, subtitle, image, condition_var, subchapters=None):
            self.label_start = label_start
            self.title = title
            self.subtitle = subtitle
            self.image = image
            self.condition_var = condition_var
            if subchapters:
                self.subchapters = subchapters
            else:
                self.subchapters = [SubchapterItem(label_start, title, subtitle, _("Сюжет"))]

        def is_unlocked(self):
            return getattr(persistent, self.condition_var, False)

    chapter_items = []
    def add_chapter(label_start, title, subtitle, image, condition_var, subchapters=None):
        chapter_items.append(ChapterItem(label_start, title, subtitle, image, condition_var, subchapters))

    def GetMostRecentSave():
        newest = renpy.newest_slot()
        if newest:
            return newest
        return None

# Инициализация списка глав
init 1 python:
    chapter_items = []
    
    ch1_subchapters = [
        SubchapterItem("chapter1_lab_night", _("1. Ночь в лаборатории"), _("Начало истории"), _("Сюжет")),
        SubchapterItem("chapter1_lab_morning", _("2. Утро в лаборатории"), _("Первые лучи солнца и новые улики в комнате"), _("Сюжет")),
        SubchapterItem("chapter1_lab_noon", _("3. День"), _("Размышления"), _("Сюжет")),
        SubchapterItem("chapter1_lab_noon_library", _("4. Библиотека"), _(""), _("Сюжет")),
        SubchapterItem("chapter1_meeting_start", _("5. Встреча с Маркусом"), _("Важный разговор, меняющий ход расследования"), _("Сюжет")),
        SubchapterItem("chapter1_confrontation_path", _("6. Противостояние"), _("Столкновение интересов и принятие решений"), _("Сюжет")),
        SubchapterItem("chapter1_escape_sequence_start", _("7. Побег"), _("Динамичная сцена побега из опасной зоны"), _("Сюжет")),
    ]
    
    ch2_subchapters = [
        SubchapterItem("chapter2_act1_false_memories", _("1. Ложные воспоминания"), _("Что из этого реально, а что — плод воображения?"), _("Сюжет")),
        SubchapterItem("chapter2_act2_long_night", _("2. Длинная ночь"), _("Ночные поиски и неожиданные открытия в городе"), _("Сюжет")),
        SubchapterItem("nightmare_sequence", _("3. Кошмар"), _("Знакомое лицо"), _("Сюжет")),
        SubchapterItem("chapter2_act3_facing_reality", _("4. Лицом к реальности"), _("Трудные истины, которые приходится признать"), _("Сюжет")),
        SubchapterItem("chapter2_act4_desperate_measures", _("5. Отчаянные меры"), _("Когда не остается выбора, приходится рисковать"), _("Сюжет")),
        SubchapterItem("chapter2_act5_journey_to_anomic", _("6. Путь в Аномик"), _("Путешествие в таинственный сектор Аномик"), _("Сюжет")),
        SubchapterItem("chapter2_act5_anomic_arrival", _("7. Прибытие в Аномик"), _("Первые шаги на новой неизведанной территории"), _("Сюжет")),
    ]
    
    ch3_subchapters = [
        SubchapterItem("chapter3_part1_start", _("1. Начало пути"), _("Погружение в новые тайны и подготовка плана"), _("Квест")),
        SubchapterItem("chapter3_breather", _("2. Брифинг"), _("Информация о задании"), _("Сюжет")),
        SubchapterItem("ch3_path_to_station", _("3. Ограбление"), _("Проникновение на сортировочную станцию"), _("Сюжет")),
        SubchapterItem("chapter3_escape", _("4. Апартаменты"), _("Подготовка к к побегу из Аномика"), _("Сюжет")),
        SubchapterItem("chapter3_on_train", _("5. В поезде"), _("В пути, В Веритас"), _("Сюжет")),
    ]
    
    ch4_subchapters = [
        SubchapterItem("chapter4_0_train_dream", _("1. Сон в поезде"), _("Странные видения на пути к Ковчегу"), _("Сюжет")),
        SubchapterItem("chapter4_0_arkaground", _("2. Ковчег на мели"), _("Исследование застрявшего Ковчега"), _("Сюжет")),
        SubchapterItem("chapter4_0_academy", _("3. Академия"), _("Встреча с преподавателями и студентами"), _("Квест")),
        SubchapterItem("chapter4_0_24syndrome", _("4. Синдром 24"), _("Расследование загадочной болезни"), _("Квест")),
        SubchapterItem("chapter4_0_garden", _("5. Сад"), _("Прогулка по саду Академии"), _("Игровая часть")),
    ]
    
    ch4_5a_subchapters = [
        SubchapterItem("chapter4_5_garden_aftermath", _("1. Последствия в саду"), _("Разбор произошедших событий"), _("Сюжет")),
        SubchapterItem("chapter4_5_cafe_scene", _("2. Кафе"), _("Разговор в спокойной обстановке"), _("Сюжет")),
        SubchapterItem("chapter4_5_concert_start", _("3. Концерт: Начало"), _("Большое выступление начинается"), _("Игровая часть")),
        SubchapterItem("chapter4_5_concert_mid", _("4. Встреча с фанатами"), _("Общение за кулисами"), _("Сюжет")),
        SubchapterItem("chapter4_5_concert_end", _("5. Завершение концерта"), _("Встреча с Серафиной"), _("Сюжет")),
    ]

    # add_chapter("chapter_0", _("Глава 0"), _("Пролог"), "images/bg_prologue.avif", "chapter_0_unlocked")
    add_chapter("chapter_1", _("Глава 1"), _("Синяя Ворона"), "images/cg/vol1/chapter1/ch01_cg23_v01.avif", "chapter_1_unlocked", ch1_subchapters)
    add_chapter("chapter_2", _("Глава 2"), _("В поисках подруги"), "images/cg/vol1/chapter2/featured_cg-8_2.avif", "chapter_2_unlocked", ch2_subchapters)
    add_chapter("chapter_3", _("Глава 3"), _("Эскапизм"), "images/backgrounds/bg chapter_3_sorting-station-start.avif", "chapter_3_unlocked", ch3_subchapters)
    add_chapter("chapter_4", _("Глава 4.0"), _("Ковчег на мели"), "images/cg/vol1/chapter4-0/featured_cg-29.avif", "chapter_4_unlocked", ch4_subchapters)
    add_chapter("chapter_4_5a", _("Глава 4.5 - Акт I"), _("Из Изгнанницы В Созвездие"), "images/cg/vol1/chapter4-5a/featured_cg-31_2.avif", "chapter_4_5a_unlocked", ch4_5a_subchapters)
    add_chapter("chapter_4_5b", _("Глава 4.5 - Акт II"), _("Из Изгнанницы В Созвездие"), "images/cg/vol1/chapter4-5b/featured_7a-cg-2.avif", "chapter_4_5b_unlocked")
    add_chapter("chapter_5", _("Глава 5"), _("Предложение, от которого нельзя отказаться"), "images/cg/vol1/chapter5/ch05_cg01_v01.avif", "chapter_5_unlocked")
    add_chapter("chapter_6", _("Глава 6"), _("Первый ряд, Пятое место"), "images/cg/vol1/chapter4-5b/7a-cg-5.avif", "chapter_6_unlocked")
    add_chapter("chapter_7", _("Глава 7"), _("Туман Войны"), "images/cg/vol1/chapter4-5b/7a-cg-5.avif", "chapter_7_unlocked")
    add_chapter("chapter_8", _("Глава 8"), _("Школьные… дни?"), "images/cg/vol1/chapter4-5b/7a-cg-5.avif", "chapter_8_unlocked")
    add_chapter("chapter_9", _("Глава 9"), _("Резонирующий Диссонанс"), "images/cg/vol1/chapter4-5b/7a-cg-5.avif", "chapter_9_unlocked")

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
        style "modern_panel"
        vbox:
            style "modern_vbox"
            label _("Режим игры") style "modern_title_label"

            textbutton _("Новая игра") action Start() style "modern_button"

            if renpy.newest_slot():
                textbutton _("Продолжить") action Continue() style "modern_button"
            else:
                textbutton _("Продолжить") action None style "modern_button" text_color "#888"

            textbutton _("Выбор сохранения") action ShowMenu("load") style "modern_button"
            textbutton _("Выбор глав") action ShowMenu("chapter_select") style "modern_button"

            null height 30
            textbutton _("Назад") action ShowMenu("main_menu") style "modern_back_button"

################################################################################
## Экран Выбора Глав
################################################################################

screen chapter_select():
    tag menu
    zorder 30
    modal True
    
    default selected_chapter = None
    
    use main_menu_background
    key "game_menu" action (If(selected_chapter is None, ShowMenu("play_menu"), SetScreenVariable("selected_chapter", None)))

    frame:
        style "modern_panel_wide"
        
        if selected_chapter is None:
            vbox:
                style "modern_vbox"
                label _("Выбор глав") style "modern_title_label"

                vpgrid:
                    cols 3
                    spacing 30
                    draggable True
                    mousewheel True
                    scrollbars "vertical"
                    xalign 0.5
                    xsize 1100
                    ysize 600

                    for item in chapter_items:
                        if item.is_unlocked():
                            button:
                                style "chapter_button"
                                action SetScreenVariable("selected_chapter", item)
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

                null height 20
                textbutton _("Назад") action ShowMenu("play_menu") style "modern_back_button"
        else:
            vbox:
                style "modern_vbox"
                
                # Заголовок главы
                label "[selected_chapter.title] — [selected_chapter.subtitle]" style "modern_title_label"
                
                hbox:
                    spacing 40
                    xalign 0.5
                    
                    # Левая колонка: Кадр главы в рамке
                    frame:
                        background Solid("#ffffff10")
                        padding (10, 10)
                        xysize (480, 290)
                        yalign 0.0
                        
                        add selected_chapter.image:
                            fit "cover"
                            xysize (460, 270)
                            align (0.5, 0.5)
                            
                    # Правая колонка: Список подглав
                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        xsize 580
                        ysize 400
                        yalign 0.0
                        
                        vbox:
                            spacing 15
                            xsize 560
                            
                            for sub in selected_chapter.subchapters:
                                button:
                                    style "subchapter_button"
                                    action Start(sub.label_start)
                                    
                                    vbox:
                                        spacing 4
                                        xfill True
                                        
                                        hbox:
                                            spacing 10
                                            yalign 0.5
                                            
                                            text sub.category style "subchapter_category_text" yalign 0.5
                                            text sub.title style "subchapter_title_text" yalign 0.5
                                            
                                        text sub.description style "subchapter_desc_text"

            null height 20
            textbutton _("Назад") action SetScreenVariable("selected_chapter", None) style "modern_back_button"


style subchapter_button is button:
    background Solid("#ffffff0a")
    hover_background Solid("#ffffff1a")
    xfill True
    padding (15, 10)
    activate_sound "audio/sfx/button-click.opus"
    hover_sound "audio/sfx/cursor-hover.opus"

style subchapter_title_text is text:
    size 20
    bold True
    color "#ffffff"

style subchapter_desc_text is text:
    size 14
    color "#bbbbbb"

style subchapter_category_text is text:
    size 13
    bold True
    color gui.accent_color
