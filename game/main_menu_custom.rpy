# Файл: main_menu_custom.rpy

init python:
    def play_main_menu_music():
        if persistent.main_menu_level == 0:
            renpy.music.play(main_menu_music_default, fadein=1.0)
        elif persistent.main_menu_level == 1:
            renpy.music.play(main_menu_music_unlocked_1, fadein=1.0)
        elif persistent.main_menu_level == 2:
            renpy.music.play(main_menu_music_unlocked_2, fadein=1.0)
        elif persistent.main_menu_level == 3:
            renpy.music.play(main_menu_music_unlocked_3, fadein=1.0)
        elif persistent.main_menu_level == 4:
            renpy.music.play(main_menu_music_unlocked_4, fadein=1.0)

################################################################################
## 1. Главное меню (Полная замена стандартного)
################################################################################

screen main_menu():
    tag menu
    zorder 10

    # Логика смены фона и музыки при показе экрана
    on "show" action Function(play_main_menu_music)

    # Отображение фона в зависимости от прогресса
    if persistent.main_menu_level == 0:
        add "main_menu_bg_default"
    elif persistent.main_menu_level == 1:
        add "main_menu_bg_unlocked_1"
    elif persistent.main_menu_level == 2:
        add "main_menu_bg_unlocked_2"
    elif persistent.main_menu_level == 3:
        add "main_menu_bg_unlocked_3"
    elif persistent.main_menu_level == 4:
        add "main_menu_bg_unlocked_4"
    
    # Баннер-логотип сверху
    add "main_menu_logo" xalign 0.5 ypos 25

    # Основной блок навигации
    vbox:
        style "main_menu_vbox"

        textbutton _("Начать") action Start() style "main_menu_button"
        textbutton _("Продолжить") action ShowMenu("load") style "main_menu_button"
        textbutton _("Настройки") action ShowMenu("settings_menu") style "main_menu_button"
        
        # Показываем галерею, только если она доступна
        if renpy.has_screen("gallery"):
            textbutton _("Галерея CG") action ShowMenu("gallery") style "main_menu_button"

        textbutton _("Об игре") action ShowMenu("about_menu") style "main_menu_button"
        textbutton _("Выход") action Quit(confirm=True) style "main_menu_button"


################################################################################
## 2. Саб-меню "Настройки"
################################################################################

screen settings_menu():
    tag menu
    zorder 25
    modal True # Делает фон неактивным

    # Используем экран main_menu как фон, чтобы не было "скачка"
    use main_menu

    # Затемняющая рамка для фокуса на саб-меню
    frame:
        style "sub_menu_frame"

        vbox:
            style "sub_menu_vbox"
            label _("Настройки") style "sub_menu_label"

            textbutton _("Текст/Графика") action ShowMenu("graphics_settings_screen") style "sub_menu_button"
            textbutton _("Звук") action ShowMenu("sound_settings_screen") style "sub_menu_button"
            textbutton _("Язык") action ShowMenu("language_selection_screen") style "sub_menu_button"
            textbutton _("DLC Контент") action Start("dlc_manager_flow") style "sub_menu_button"

            null height 30 # Отступ

            textbutton _("Назад") action ShowMenu("main_menu") style "sub_menu_button"

# Экран выбора языка (если у вас его еще нет)
    #screen language_selection_screen():
        #modal True
        #tag menu
        
        #use game_menu(_("Выбор языка")):
            #vbox:
                #xalign 0.5
                #yalign 0.5
                #spacing 15

                # Пример:
                #textbutton "Русский" action [Language(None), Return()]
                #textbutton "English" action [Language("english_us"), Return()]


################################################################################
## 3. Саб-меню "Об игре"
################################################################################

screen about_menu():
    tag menu
    zorder 25
    modal True

    use main_menu

    frame:
        style "sub_menu_frame"

        vbox:
            style "sub_menu_vbox"
            label _("Об игре") style "sub_menu_label"

            textbutton _("Управление") action ShowMenu("help") style "sub_menu_button"
            textbutton _("Лицензия") action ShowMenu("license_screen") style "sub_menu_button"
            textbutton _("Титры") action ShowMenu("credits_screen") style "sub_menu_button"
            textbutton _("Обновление") action ShowMenu("update_screen") style "sub_menu_button"

            null height 30

            textbutton _("Назад") action ShowMenu("main_menu") style "sub_menu_button"


################################################################################
## 4. Конечные экраны для раздела "Об игре"
## Они используют стандартный фрейм `game_menu` для единообразия
################################################################################

screen license_screen():
    tag menu
    zorder 25
    use game_menu(_("Лицензия"), scroll="viewport"):
        vbox:
            style_prefix "about" # Используем стили от стандартного экрана about
            spacing 20

            label _("Музыка")
            text "ksho - Purge Protocol\n{a=https://www.youtube.com/watch?v=BecKecHBOdc}Источник{/a}"
            text "Factorio - Swell Pad\n{a=https://www.youtube.com/watch?v=2C8-u0IkQVk}Источник{/a}\n"
            text "Rewrite - Potted One\n{a=https://www.youtube.com/watch?v=2C8-u0IkQVk}Источник{/a}\n"
            text "Rewrite - Sorrowless\n{a=https://www.youtube.com/watch?v=rIwl2cDwStw}Источник{/a}\n"
            text "Rewrite - Rememberance\n{a=}Источник{/a}\n"
            text "Rewrite - Reply\n{a=}Источник{/a}\n"
            text "PRESSURE - One Way Trip\n{a=https://www.youtube.com/watch?v=8yFUzUmWe4M}Источник{/a}\n"
            text "PRESSURE - First Theme\n{a=}Источник{/a}\n"
            text "Steins;Gate - Self Affirmation\n{a=}Источник{/a}\n"
            text "Steins;Gate - Quiet Air\n{a=}Источник{/a}\n"
            text "Occultic;Nine - OVERCAST-EYES\n{a=}Источник{/a}\n"
            text "CHAOS;HEAD - Colors\n{a=}Источник{/a}\n"
            text "Shadows of Doubt - Revpad\n{a=}Источник{/a}\n"
            text "Shadows of Doubt - LD Celts\n{a=}Источник{/a}\n"
            text "Shadows of Doubt - FM Modul\n{a=}Источник{/a}\n"
            text "Intravenous - Initiation (Inactive)\n{a=}Источник{/a}\n"
            text "Avery Alexander - HRT\n{a=https://www.youtube.com/watch?v=7OpLRMyiueY}Источник{/a}\n"



            label _("Музыка в меню")
            text "1 - NightMare\n"
            text "2 - FearForUnreal\n"
            text "3 - Sorrowless\n"
            text "4 - BuzzingGoodbye\n"
            # ... и так далее

screen credits_screen():
    tag menu
    use game_menu(_("Титры"), scroll="viewport"):
        vbox:
            style_prefix "about"
            spacing 15
            
            text "Спасибо за игру в этот прототип. Это моя первая визуальная новелла, и я многому научился в процессе её создания. Я надеюсь, что вам понравится история и персонажи, и я с нетерпением жду возможности поделиться с вами остальной частью истории в будущем."
            text "Автор и Разработчик: {a=https://dotprod.itch.io/}Dot{/a}\n"
            text "Тестировщик и Вдохновитель: Overhappy_Avali\n"
            # ... и так далее

screen update_screen():
    tag menu
    use game_menu(_("Обновление")):
        vbox:
            style_prefix "about"
            xalign 0.5
            yalign 0.5

            text "Текущая версия: [config.version]\n"
            text "\nСписок изменений:\n- Добавлена новая система меню."


# Добавьте этот код в конец файла main_menu_custom.rpy

################################################################################
## 5. НОВЫЕ ЭКРАНЫ НАСТРОЕК И ИХ СТИЛИ
################################################################################

## Экран настроек Текста и Графики
screen graphics_settings_screen():
    tag menu
    zorder 50
    modal True

    # Используем главный экран как фон для бесшовного перехода
    use main_menu

    # Основное окно настроек
    frame:
        style "settings_frame"

        # Контейнер для всего содержимого
        vbox:
            # Заголовок
            label _("Текст и Графика") style "settings_title"

            # Основной контент в виде сетки для аккуратного выравнивания
            grid 2 1:
                xalign 0.5
                xsize 900 # Задаем общую ширину для сетки
                spacing 80  # Увеличиваем расстояние между колонками

                # --- Левая колонка ---
                vbox:
                    style_prefix "settings_check"
                    spacing 15
                    
                    label _("Режим экрана")
                    textbutton _("Оконный") action Preference("display", "window")
                    textbutton _("Полный") action Preference("display", "fullscreen")

                    null height 20

                    label _("Пропуск")
                    textbutton _("Непрочитанного текста") action Preference("skip", "toggle")
                    textbutton _("После выборов") action Preference("after choices", "toggle")
                    textbutton _("Переходов") action InvertSelected(Preference("transitions", "toggle"))

                # --- Правая колонка ---
                vbox:
                    style_prefix "settings_check" # Используем тот же стиль кнопок
                    spacing 15 # Расстояние такое же, как слева

                    label _("Контент")
                    
                    # Кнопка-тумблер. Она будет подсвечена, если режим ВКЛЮЧЕН.
                    textbutton _("Включение Чувствительнного контента (18+)"):
                        action ToggleField(persistent, "sensitive_mode")
                        tooltip _("Включает отображение откровенных сцен.")


                    null height 20

                    # label _("")
                    #bar value Preference("text speed")

                    # label _("")
                    #bar value Preference("auto-forward time")
            
            # Отступ перед кнопкой "Назад"
            null yfill True

            # Кнопка "Назад", которая ведет в саб-меню настроек
            textbutton _("Назад") action ShowMenu("settings_menu") style "settings_back_button"


## Экран настроек Звука
screen sound_settings_screen():
    tag menu
    zorder 50
    modal True
    
    use main_menu

    frame:
        style "settings_frame"
        vbox:
            label _("Звук") style "settings_title"
            
            # Контейнер для слайдеров
            vbox:
                style_prefix "settings_slider"
                xalign 0.5
                spacing 15

                if config.has_music:
                    label _("Громкость музыки")
                    hbox:
                        bar value Preference("music volume")
                        textbutton "Тест" action Play("music", config.sample_sound) style "settings_test_button"

                if config.has_sound:
                    label _("Громкость звуков")
                    hbox:
                        bar value Preference("sound volume")
                        if config.sample_sound:
                            textbutton _("Тест") action Play("sound", config.sample_sound) style "settings_test_button"

                if config.has_voice:
                    label _("Громкость голоса")
                    hbox:
                        bar value Preference("voice volume")
                        if config.sample_voice:
                            textbutton _("Тест") action Play("voice", config.sample_voice) style "settings_test_button"
            
            null height 30

            # Кнопка Mute
            textbutton _("Без звука"):
                action Preference("all mute", "toggle")
                style "settings_check_button"
                xalign 0.5

            null height 30
            textbutton _("Назад") action ShowMenu("settings_menu") style "settings_back_button"