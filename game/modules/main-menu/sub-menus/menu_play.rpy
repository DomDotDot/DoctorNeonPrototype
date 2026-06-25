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
        SubchapterItem("chapter4_0_arkaground", _("2. Ковчег на мели"), _("Что скрывает Ковчег?"), _("Сюжет")),
        SubchapterItem("chapter4_0_academy", _("3. Академия"), _("Путь в Академию Веритас"), _("Сюжет")),
        SubchapterItem("chapter4_0_24syndrome", _("4. Синдром 24"), _("Расследование загадочных исчезновениях"), _("Сюжет")),
        SubchapterItem("chapter4_0_garden", _("5. Сад"), _("Неожиднная Встреча"), _("Сюжет")),
    ]
    
    ch4_5a_subchapters = [
        SubchapterItem("chapter4_5_garden_aftermath", _("1. Последствия в саду"), _("После тяжелого дня"), _("Сюжет")),
        SubchapterItem("chapter4_5_cafe_scene", _("2. Кафе"), _("Подготовка к концерту."), _("Сюжет")),
        SubchapterItem("chapter4_5_concert_start", _("3. Концерт: Начало"), _("Большое выступление начинается"), _("Сюжет")),
        SubchapterItem("chapter4_5_concert_mid", _("4. Встреча с фанатами"), _("Общение за кулисами"), _("Сюжет")),
        SubchapterItem("chapter4_5_concert_end", _("5. Завершение концерта"), _("Встреча с Серафиной"), _("Сюжет")),
        SubchapterItem("chapter4_5_argon_rescue", _("6. Спасение Аргоном"), _("И всепожирающая зависть"), _("Сюжет")),
        SubchapterItem("chapter4_5_dorm_way", _("7. Спальная Сары"), _("В тенях комнаты"), _("Сюжет")),
    ]

    ch4_5b_subchapters = [
        SubchapterItem("chapter4_5_boulevard_night", _("1. Бульвар Мечтателей"), _("Блуждающий огонёк с красным шарфом"), _("Сюжет")),
        SubchapterItem("chapter4_5_morning_after", _("2. Внедрение в Академию"), _("Большой секрет Акари-сенсей"), _("Сюжет")),
        SubchapterItem("chapter4_5_akari_arrest", _("3. Арест Акари"), _("Пойман с поличным"), _("Сюжет")),
        SubchapterItem("chapter4_5_lily_cafe", _("4. Спасение Лили"), _("Этот цветок уже не спасти"), _("Сюжет")),
        SubchapterItem("chapter4_5_awakening_and_finale", _("5. Пробуждение Вакуума"), _("Огонь, тот что во мне"), _("Сюжет")),
        SubchapterItem("chapter4_5_finale", _("6. Самопровозглашенный Ангел"), _("В ней не было ничего святого"), _("Сюжет")),
        SubchapterItem("chapter4_5_epilogue", _("7. Эпилог Веритаса"), _("Иллюзии были развеяны"), _("Сюжет")),
    ]

    ch5_subchapters = [
        SubchapterItem("chapter5_introduction", _("1. Прибытие на Орбиталь"), _("С моей семьёй"), _("Сюжет")),
        SubchapterItem("chapter5_start", _("2. Начало миссиии"), _("Уровень 1"), _("Квест")),
        SubchapterItem("ch5_level3_main_hall", _("3. Отделение Медбея"), _("Уровень 2"), _("Квест")),
        SubchapterItem("ch5_monorail_entrance", _("4. Монорельс Нексус"), _("Уровень 3"), _("Квест")),
        SubchapterItem("station_server_room_entry", _("5. Серверная"), _("Огонь, тот что во мне"), _("Сюжет")),
        SubchapterItem("chapter5_timer_and_brig", _("6. Бриг"), _("Отдел Охраны"), _("Сюжет")),
        SubchapterItem("chapter5_breakout", _("7. Пермабриг"), _("Компания позаботиться о вас"), _("Сюжет")),
        SubchapterItem("chapter5_ghost_ship", _("8. Эреб"), _("Идеально ровный срез"), _("Сюжет")),
        SubchapterItem("chapter5_bridge_and_katana", _("9. Мостик"), _("Бойня"), _("Сюжет")),
        SubchapterItem("chapter5_finale_sacrifice", _("10. Отец"), _("Жертвенное искупление"), _("Сюжет")),
        SubchapterItem("chapter5_epilogue_earth", _("11. Падение"), _("Второй ковчег пал."), _("Сюжет")),
    ]

    ch6_subchapters = [
        SubchapterItem("chapter6_alley_valley", _("1. Запределье"), _("Холод алого тумана и тьма желтого"), _("Сюжет")),
        SubchapterItem("chapter6_spire", _("2. Шпиль"), _("Таинственная фигура на вершине города"), _("Сюжет")),
        SubchapterItem("chapter6_tradingcenter", _("3. ТЦ 'Оазис'"), _("Примерка новой жизни"), _("Сюжет")),
        SubchapterItem("chapter6_encounter", _("4. Грация..."), _("Встреча с той, кто искал"), _("Сюжет")),
        SubchapterItem("chapter6_ceo", _("5. Хладнокровная Месть"), _("Блюдо, которое подают холодным"), _("Сюжет")),
        SubchapterItem("chapter6_krypton", _("6. Скрытые Георгини"), _("Запах Формалина"), _("Сюжет")),
    ]

    ch7_subchapters = [
        SubchapterItem("chapter7_library", _("1. Библиотека"), _("Не суди книгу по обложке"), _("Сюжет")),
        SubchapterItem("chapter7_apartments", _("2. Начало миссиии"), _("Уровень 1"), _("Сюжет")),
        SubchapterItem("chapter7_decay", _("3. Распад"), _("Самый тяжелый элемент"), _("Сюжет")),
    ]

    ch8_subchapters = [
        SubchapterItem("chapter8_drown", _("1. Пробуждение"), _("Шум прибоя"), _("Сюжет")),
        SubchapterItem("chapter8_school_days", _("2. Самое обычное Утро"), _("Мир, где нет угроз"), _("Сюжет")),
        SubchapterItem("chapter8_locker_room", _("3. Раздевалка"), _("Чрезмерная Опека"), _("Сюжет")),
        SubchapterItem("chapter8_basketball", _("4. Вышибалы"), _("Слишком эмоциональная игра"), _("Сюжет")),
        SubchapterItem("chapter8_infirmary", _("5. Школьный медпункт"), _("Поцелуй"), _("Сюжет")),
        SubchapterItem("chapter8_search", _("6. Поиски на Острове"), _("Поиски того, кого уже нет"), _("Сюжет")),
        SubchapterItem("chapter8_dream_cave", _("7. Пещера"), _("Обещание, которого не было"), _("Сюжет")),
        SubchapterItem("chapter8_letter", _("8. Письмо'"), _("Оповещение постфактум"), _("Сюжет")),
        SubchapterItem("chapter8_mismatch", _("9. Несовместимые"), _("Её не исправить"), _("Сюжет")),
        SubchapterItem("chapter8_morning_incident", _("10. Утреннее происшествие"), _("Рациональнвя логика от того, от кого её не ожидали"), _("Сюжет")),
        SubchapterItem("chapter8_invitation", _("11. Приглашение"), _("Музыкальный Клуб"), _("Сюжет")),
        SubchapterItem("chapter8_new_classmate", _("12. Новый Одноклассник"), _("...Аристократичность"), _("Сюжет")),
        SubchapterItem("chapter8_club", _("13. Музыкальный Клуб"), _("Собрались все музыкальные люди"), _("Сюжет")),
        SubchapterItem("chapter8_lost_key", _("14. Нет Ключей"), _("Кто же их взял?"), _("Сюжет")),
        SubchapterItem("chapter8_date", _("15. Свидание"), _("Свидание под соусом 'дружбы'"), _("Сюжет")),
        SubchapterItem("chapter8_tide", _("16. Мученичество"), _("Культ мученика никогда не приводит к хорошим результатам"), _("Сюжет")),
        SubchapterItem("chapter8_loneless", _("17. Океан Пустоты"), _("Никого больше нет"), _("Сюжет")),
        SubchapterItem("chapter8_memory_sea", _("18. Океан Воспоминаний"), _("Воспоминания, которые не хотят умирать"), _("Сюжет")),
        SubchapterItem("chapter8_boundless", _("19. Океан Бездны"), _("Если долго смотреть в бездну, то бездна начинает смотреть на тебя"), _("Сюжет")),
        SubchapterItem("chapter8_helium", _("20. Гелий"), _("Самый Легкий газ"), _("Сюжет")),
        SubchapterItem("chapter8_dream", _("21. Сон"), _("То, чего не было и было одновременно"), _("Сюжет")),
    ]

    ch9_subchapters = [
        SubchapterItem("chapter9_requiem", _("1. Реквием"), _("Для мечты"), _("Сюжет")),
        SubchapterItem("chapter9_redmist", _("2. Красный Туман"), _("Усилитель и Трансляция Боли"), _("Квест")),
        SubchapterItem("chapter9_hall", _("3. Дух прошлого"), _("Разум настоящего"), _("Квест")),
        SubchapterItem("chapter9_silence", _("4. Абсолютная Тишина"), _("Никто из нас не монстр"), _("Квест")),
        SubchapterItem("chapter9_bell_toll", _("5. Звон"), _("Слышишь звонок? Пары закончились"), _("Сюжет")),
        SubchapterItem("chapter9_epilogue", _("6. Упокоение"), _("Конец для Элементов, Начало для Человечества"), _("Сюжет")),
    ]


    # add_chapter("chapter_0", _("Глава 0"), _("Пролог"), "images/bg_prologue.avif", "chapter_0_unlocked")
    add_chapter("chapter_1", _("Глава 1"), _("Синяя Ворона"), "images/cg/vol1/chapter1/ch01_cg23_v01.avif", "chapter_1_unlocked", ch1_subchapters)
    add_chapter("chapter_2", _("Глава 2"), _("В поисках подруги"), "images/cg/vol1/chapter2/featured_cg-8_2.avif", "chapter_2_unlocked", ch2_subchapters)
    add_chapter("chapter_3", _("Глава 3"), _("Эскапизм"), "images/backgrounds/bg chapter_3_sorting-station-start.avif", "chapter_3_unlocked", ch3_subchapters)
    add_chapter("chapter_4", _("Глава 4.0"), _("Ковчег на мели"), "images/cg/vol1/chapter4-0/featured_cg-29.avif", "chapter_4_unlocked", ch4_subchapters)
    add_chapter("chapter_4_5a", _("Глава 4.5 - Акт I"), _("Из Изгнанницы В Созвездие"), "images/cg/vol1/chapter4-5a/featured_cg-31_2.avif", "chapter_4_5a_unlocked", ch4_5a_subchapters)
    add_chapter("chapter_4_5b", _("Глава 4.5 - Акт II"), _("Из Изгнанницы В Созвездие"), "images/cg/vol1/chapter4-5b/featured_7a-cg-2.avif", "chapter_4_5b_unlocked", ch4_5b_subchapters)
    add_chapter("chapter_5", _("Глава 5"), _("Предложение, от которого нельзя отказаться"), "images/cg/vol1/chapter5/ch05_cg01_v01.avif", "chapter_5_unlocked", ch5_subchapters)
    add_chapter("chapter_6", _("Глава 6"), _("Первый ряд, Пятое место"), "images/cg/vol1/chapter4-5b/7a-cg-5.avif", "chapter_6_unlocked", ch6_subchapters)
    add_chapter("chapter_7", _("Глава 7"), _("Туман Войны"), "images/cg/vol1/chapter4-5b/7a-cg-5.avif", "chapter_7_unlocked", ch7_subchapters)
    add_chapter("chapter_8", _("Глава 8"), _("Школьные… дни?"), "images/cg/vol1/chapter4-5b/7a-cg-5.avif", "chapter_8_unlocked", ch8_subchapters)
    add_chapter("chapter_9", _("Глава 9"), _("Резонирующий Диссонанс"), "images/cg/vol1/chapter4-5b/7a-cg-5.avif", "chapter_9_unlocked", ch9_subchapters)

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
                                # action SetScreenVariable("selected_chapter", item) # Выключено: саб-чаптеры не работают стабильно с flow менеджером
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
