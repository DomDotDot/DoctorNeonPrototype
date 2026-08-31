init 1 python:
    # =========================================================================
    # РЕГИСТРАЦИЯ ВСЕХ ИГРОВЫХ ДОСТИЖЕНИЙ
    # =========================================================================

    # -------------------------------------------------------------------------
    # 1. ЯВНЫЕ (ОБЫЧНЫЕ) ДОСТИЖЕНИЯ
    # -------------------------------------------------------------------------
    
    register_achievement(Achievement(
        id="criminalist",
        name=_("Концептуализация: Cредне: Успех"),
        description=_("Внимательно изучите любой предмет в инвентаре через кнопку 'Осмотреть'."),
        icon=None,
        ach_type=ACH_TYPE_NORMAL
    ))

    register_achievement(Achievement(
        id="novice",
        name=_("Куда жать, чтобы победить?"),
        description=_("Откройте экран помощи и ознакомьтесь с управлением в визуальной новелле."),
        icon=None,
        ach_type=ACH_TYPE_NORMAL
    ))

    register_achievement(Achievement(
        id="mail_maniac",
        name=_("Почтовый маньяк"),
        description=_("Откройте Центр уведомлений и ознакомьтесь со всеми входящими сообщениями."),
        icon=None,
        ach_type=ACH_TYPE_NORMAL
    ))

    register_achievement(Achievement(
        id="behind_the_scenes",
        name=_("Взгляд за кулисы"),
        description=_("Загляните в раздел 'Об игре' и перейдите на страницу разработчиков."),
        icon=None,
        ach_type=ACH_TYPE_NORMAL
    ))

    # -------------------------------------------------------------------------
    # 2. СКРЫТЫЕ ДОСТИЖЕНИЯ
    # -------------------------------------------------------------------------

    register_achievement(Achievement(
        id="completionist_100",
        name=_("Комплеционист"),
        description=_("Получите абсолютно все остальные достижения в игре."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Откройте все секреты игры.")
    ))

    register_achievement(Achievement(
        id="concert_in_solitude",
        name=_("Концерт в одиночестве"),
        description=_("Дослушайте финальный трек в титрах 9-й главы до самой последней секунды без пропуска."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Проявите терпение в финале истории.")
    ))

    register_achievement(Achievement(
        id="absolute_silence",
        name=_("Абсолютная Тишина"),
        description=_("Пройдите любую главу истории в режиме 'Без звука'."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Погрузитесь в истинную тишину.")
    ))

    register_achievement(Achievement(
        id="frequency_resonance",
        name=_("Частота резонанса"),
        description=_("Проведите в воспоминании с Криптон более 7 минут до момента вспышки резонанса."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Не спешите покидать дорогой сердцу момент.")
    ))

    register_achievement(Achievement(
        id="midnight_shift",
        name=_("Спишь? — Нет, читаю ВН"),
        description=_("Запустите игру глубокой ночью."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Время для полуночных исследований.")
    ))

    register_achievement(Achievement(
        id="dont_rush",
        name=_("Куда ты спешишь?"),
        description=_("Пройдите главу истории быстрее чем за 10 минут, пропуская строки текста."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Не упускайте важные детали.")
    ))

    register_achievement(Achievement(
        id="without_blinking",
        name=_("Не моргай"),
        description=_("Пройдите главу истории на одном дыхании, ни разу не открывая меню паузы."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Полная концентрация на происходящем.")
    ))

    register_achievement(Achievement(
        id="thoughtful_reader",
        name=_("Буквально Я"),
        description=_("Остановитесь и проведите на одной реплике диалога более 3 минут без перелистывания и паузы."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Вдумайтесь в глубину слов.")
    ))

    register_achievement(Achievement(
        id="secret_cutscene_vol1",
        name=_("Страшно Вырубай"),
        description=_("Станьте свидетелем секретной кат-сцены в катакомбах города."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Откройте скрытый финал первого тома.")
    ))

    register_achievement(Achievement(
        id="pathological_interest",
        name=_("Патологический интерес"),
        description=_("Будучи с выключенным 18+ фильтром, включите его прямо во время сцены с ульем в комнате 404."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Проявите любопытство в самый неподходящий момент.")
    ))

    register_achievement(Achievement(
        id="nothing_wrong_ai",
        name=_("В этом нет ничего такого"),
        description=_("От начала до конца пройдите игру с включенным режимом ИИ-чувствительности (чёрный экран), ни разу его не выключая."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Доверьтесь восприятию на слух.")
    ))

    # --- ДОСТИЖЕНИЯ ГЛАВЫ 5 ---

    register_achievement(Achievement(
        id="mission_can_wait",
        name=_("Миссия подождёт"),
        description=_("В Главе 5 проведите в жилом блоке персонала (Дормы) более 10 внутриигровых минут."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Не торопитесь покидать уютную комнату.")
    ))

    register_achievement(Achievement(
        id="cultural_walk",
        name=_("Прогулка окультуривания"),
        description=_("В Главе 5 посетите Бар, Часовню и Библиотеку до того, как впервые ступите в зону Карго."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Изучите все общественные места второго уровня станции.")
    ))

    register_achievement(Achievement(
        id="bureaucracy",
        name=_("Давай по новой, Миша..."),
        description=_("В Отделе кадров успешно взломайте электронное табло, но подойдите к окну Автоматона с неверно выбранным запросом в талоне."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Прочувствуйте всю беспощадность космической бюрократии.")
    ))

    register_achievement(Achievement(
        id="seven_seven_seven_bulls",
        name=_("Три топора, три коровы, три быка"),
        description=_("В мини-игре 'Быки и Коровы' в Отделе кадров подберите 4-значный PIN-код за 7 ходов или меньше."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Проявите исключительную логику при взломе.")
    ))

    register_achievement(Achievement(
        id="fiasco_bro",
        name=_("Это фиаско, братан"),
        description=_("Сделать 15 или более попыток при подборе 4-значного PIN-кода в Отделе кадров."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Кажется, криптография — не ваша сильнейшая сторона.")
    ))

    register_achievement(Achievement(
        id="hal9000_sorry_neon",
        name=_("Мне жаль, Неон. Боюсь, я не могу этого сделать."),
        description=_("Попытаться запросить доступ у терминала СИВИЛЛЫ в Отделе исследований без чипа Администратора и получить отказ."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Даже самый дружелюбный ИИ не пустит вас без надлежащего пропуска.")
    ))

    register_achievement(Achievement(
        id="not_a_moron",
        name=_("Я НЕ ДУРАК!"),
        description=_("В Главе 5 пройдите все коридоры спутника Нексус (Alpha, Beta, Gamma) без единого сброса таймера перегрузки."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Докажите, что вы способны справиться с генераторами с первой попытки.")
    ))

    register_achievement(Achievement(
        id="second_before_midnight",
        name=_("За секунду до Полночи"),
        description=_("Завершите ввод шифра в последнем коридоре Gamma ровно за 1 секунду до критической перегрузки серверов."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Рискните всем на последних секундах отсчёта.")
    ))

    register_achievement(Achievement(
        id="sibyl_no_hints",
        name=_("Загадки Жака Фреско"),
        description=_("Ответьте на все 3 логические загадки СИВИЛЛЫ в Ядре ИИ, ни разу не допустив 3 ошибок и не активировав подсказку."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Решите загадки автономного интеллекта без чьей-либо помощи.")
    ))

    register_achievement(Achievement(
        id="scared_the_grandpa",
        name=_("Вы напугали деда"),
        description=_("Разозлите священника в Часовне, прочитайте книгу фольклора 'tears' в Библиотеке и вернитесь к пустой скамье."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Доведите спор о вере до конца и узнайте его последствия.")
    ))

    register_achievement(Achievement(
        id="sibyl_lore_name",
        name=_("Ты знаешь это имя"),
        description=_("При ответе на финальный вопрос СИВИЛЛЫ 'Кто вы?' введите одно из ключевых лорных имён вселенной."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Назовите имя, заставившее автономный интеллект вспомнить прошлое.")
    ))

    # --- ДОСТИЖЕНИЯ ГЛАВЫ 3 ---

    register_achievement(Achievement(
        id="bouncer_plead_useless",
        name=_("Ну и пожалуйста, ну и пошло всё в пи..."),
        description=_("В Главе 3 четырежды попытайтесь вежливо уговорить вышибалу открыть дверь, пока уговоры не станут бесполезными."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Проявите вежливость и упорство при общении с охраной.")
    ))

    register_achievement(Achievement(
        id="bouncer_daughter_game_over",
        name=_("Запретная тема"),
        description=_("В Главе 3 выведите вышибалу из себя упоминанием его дочери и сразу же попадитесь ему во время погони."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Некоторые слова стоят слишком дорого.")
    ))

    # -------------------------------------------------------------------------
    # 3. ТРЕКИНГ / ПРОГРЕССИВНЫЕ ДОСТИЖЕНИЯ
    # -------------------------------------------------------------------------

    register_achievement(Achievement(
        id="deep_analysis",
        name=_("Глубокий Анализ"),
        description=_("Изучите досье 10 персонажей в Глоссарии."),
        icon=None,
        ach_type=ACH_TYPE_TRACKING,
        max_progress=10
    ))

    register_achievement(Achievement(
        id="nostalgia",
        name=_("Ностальгия"),
        description=_("Просмотрите 25 уникальных иллюстраций в Галерее CG."),
        icon=None,
        ach_type=ACH_TYPE_TRACKING,
        max_progress=25
    ))

    register_achievement(Achievement(
        id="play_16_hours",
        name=_("Пора выйти на улицу"),
        description=_("Проведите в игре суммарно 16 часов."),
        icon=None,
        ach_type=ACH_TYPE_TRACKING,
        max_progress=16
    ))

    register_achievement(Achievement(
        id="dont_touch_logo",
        name=_("Не трогай меня!"),
        description=_("Нажмите на логотип игры в главном меню 10 раз."),
        icon=None,
        ach_type=ACH_TYPE_TRACKING,
        max_progress=10,
        hidden_desc=_("Скрытое достижение. Попробуйте взаимодействовать с меню.")
    ))
