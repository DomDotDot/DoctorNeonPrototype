init 1 python:
    # =========================================================================
    # РЕГИСТРАЦИЯ ВСЕХ ИГРОВЫХ ДОСТИЖЕНИЙ
    # =========================================================================

    # -------------------------------------------------------------------------
    # 1. ЯВНЫЕ (ОБЫЧНЫЕ) ДОСТИЖЕНИЯ
    # -------------------------------------------------------------------------
    
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
        description=_("Откройте Центр уведомлений, когда в нём есть хотя бы одно входящее сообщение."),
        icon="images/achievements/pipebomb.png",
        ach_type=ACH_TYPE_NORMAL
    ))

    register_achievement(Achievement(
        id="behind_the_scenes",
        name=_("Взгляд за кулисы"),
        description=_("Перейдите по ссылке на страницу разработчика в разделе 'Титры'."),
        icon="images/achievements/backrooms.png",
        ach_type=ACH_TYPE_NORMAL
    ))

    register_achievement(Achievement(
        id="completionist_100",
        name=_("Комплеционист"),
        description=_("Разгадайте абсолютно все секреты и соберите все фрагменты этой истории."),
        icon="images/achievements/100.png",
        ach_type=ACH_TYPE_NORMAL,
    ))

    # -------------------------------------------------------------------------
    # 2. СКРЫТЫЕ ДОСТИЖЕНИЯ
    # -------------------------------------------------------------------------

    register_achievement(Achievement(
        id="concert_in_solitude",
        name=_("Концерт в одиночестве"),
        description=_("Дослушайте финальный трек в титрах 9-й главы до самой последней секунды без пропуска."),
        icon="images/achievements/lastfeather.png",
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Настоящие ценители не покидают зал, пока финальная композиция не отзвучит до самой последней секунды.")
    ))

    register_achievement(Achievement(
        id="absolute_silence",
        name=_("Абсолютная Тишина"),
        description=_("Пройдите любую главу истории в режиме 'Без звука'."),
        icon="images/achievements/absolutesilence.png",
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. В космосе никто не услышит твой крик... особенно если полностью заглушить все звуки.")
    ))

    register_achievement(Achievement(
        id="frequency_resonance",
        name=_("Частота резонанса"),
        description=_("Проведите в воспоминании с Криптон более 7 минут до момента вспышки резонанса."),
        icon="images/achievements/grossmunster.png",
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Время относительно, когда рядом дорогой человек.")
    ))

    register_achievement(Achievement(
        id="midnight_shift",
        name=_("Спишь? — Нет, читаю ВН"),
        description=_("Запустите игру глубокой ночью."),
        icon="images/achievements/yousleeping.png",
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. В этот глухой час спят даже кибернетические андроиды. Но настоящие детективы выходят на связь только ночью.")
    ))

    register_achievement(Achievement(
        id="dont_rush",
        name=_("Куда ты спешишь?"),
        description=_("Пройдите главу истории быстрее чем за 10 минут, пропуская строки текста."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Зачем читать сюжет новеллы, если можно вдавить клавишу пропуска в пол?")
    ))

    register_achievement(Achievement(
        id="without_blinking",
        name=_("Не моргай"),
        description=_("Пройдите главу истории на одном дыхании, ни разу не открывая меню паузы."),
        icon="images/achievements/dontblink.png",
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Моргнёшь — и ты труп. Никаких пауз, никаких остановок: только вы и разворачивающееся повествование.")
    ))

    register_achievement(Achievement(
        id="thoughtful_reader",
        name=_("Буквально Я"),
        description=_("Остановитесь и проведите на реплике Неон более 3 минут без перелистывания и паузы."),
        icon="images/achievements/literallyme.png",
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Стоять под неоновым дождём, слушать синтвейв и молча смотреть на экран целых три минуты... Она — буквально ты.")
    ))

    register_achievement(Achievement(
        id="secret_cutscene_vol1",
        name=_("Страшно Вырубай"),
        description=_("Станьте свидетелем секретной кат-сцены в катакомбах города."),
        icon="images/achievements/redscarf.png",
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Некоторые двери в городских катакомбах лучше было оставить запертыми. Но любопытство взяло верх...")
    ))

    register_achievement(Achievement(
        id="pathological_interest",
        name=_("Патологический интерес"),
        description=_("Будучи с выключенным 18+ фильтром, включите его прямо во время сцены с ульем в комнате 404."),
        icon="images/achievements/scaredeye.png",
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Вспомнить о правилах приличия в самый неподходящий и кошмарный момент. Что с вами не так?")
    ))

    register_achievement(Achievement(
        id="nothing_wrong_ai",
        name=_("В этом нет ничего такого"),
        description=_("От начала до конца пройдите игру с включенным режимом ИИ-чувствительности (чёрный экран), ни разу его не выключая."),
        icon="images/achievements/nothinghere.png",
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("В этом действительно нет ничего такого.")
    ))

    # --- ДОСТИЖЕНИЯ ГЛАВЫ 5 ---

    register_achievement(Achievement(
        id="mission_can_wait",
        name=_("Миссия подождёт"),
        description=_("В Главе 5 проведите в жилом блоке персонала более 10 внутриигровых минут."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Внештатная ситуация на станции подождёт, пока в жилом блоке так спокойно и тихо.")
    ))

    register_achievement(Achievement(
        id="cultural_walk",
        name=_("Прогулка окультуривания"),
        description=_("В Главе 5 посетите Бар, Часовню и Библиотеку до того, как впервые ступите в зону Карго."),
        icon="images/achievements/culture.png",
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Истинный эстет не спешит, пока не прикоснётся ко всему возвышенному.")
    ))

    register_achievement(Achievement(
        id="bureaucracy",
        name=_("Пропуск А-38"),
        description=_("В Отделе кадров успешно взломайте электронное табло, но подойдите к окну Автоматона с неверно выбранным запросом в талоне."),
        icon="images/achievements/againneon.png",
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Чтобы получить пропуск, вам понадобится формуляр из окна 'Два'.")
    ))

    register_achievement(Achievement(
        id="seven_seven_seven_bulls",
        name=_("Три топора, три коровы, три быка"),
        description=_("В мини-игре 'Быки и Коровы' в Отделе кадров подберите 4-значный PIN-код за 7 ходов или меньше."),
        icon="images/achievements/777.png",
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Даже сложнейший шифр спасует перед дедуктивным гением менее чем за 8 ходов.")
    ))

    register_achievement(Achievement(
        id="fiasco_bro",
        name=_("Это фиаско, братан"),
        description=_("Сделать 15 или более попыток при подборе 4-значного PIN-кода в Отделе кадров."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Когда даже терминал устал наблюдать за бесконечными попытками угадать 4 цифры.")
    ))

    register_achievement(Achievement(
        id="hal9000_sorry_neon",
        name=_("Мне жаль, Неон. Боюсь, я не могу этого сделать."),
        description=_("Трижды попытаться запросить доступ у терминала СИВИЛЛЫ в Отделе исследований без чипа Администратора."),
        icon="images/achievements/sorrydave.png",
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. «Открой створки шлюза, СИВИЛЛА...» Настойчивость перед лицом бесстрастной машины порой творит чудеса.")
    ))

    register_achievement(Achievement(
        id="not_a_moron",
        name=_("Я НЕ ДУРАК!"),
        description=_("В Главе 5 пройдите все коридоры спутника Нексус (Alpha, Beta, Gamma) без единого сброса таймера перегрузки."),
        icon="images/achievements/moron.png",
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. «Я НЕ ДУРАК! Мог бы дурак перезагрузить все три сектора генераторов без единого сбоя таймера?!» — Докажите это зазнавшимся машинам.")
    ))

    register_achievement(Achievement(
        id="second_before_midnight",
        name=_("За секунду до Полночи"),
        description=_("Завершите ввод шифра в последнем коридоре Gamma ровно за 1 секунду до критической перегрузки серверов."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. В настоящих блокбастерах провод всегда перерезают на самом последнем делении таймера.")
    ))

    register_achievement(Achievement(
        id="sibyl_no_hints",
        name=_("Загадки Жака Фреско"),
        description=_("Ответьте на все 3 логические загадки СИВИЛЛЫ в Ядре ИИ, ни разу не допустив 3 ошибок и не активировав подсказку."),
        icon="images/achievements/sibyl.png",
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. На размышление даётся 30 секунд. Решите все головоломки автономного интеллекта без единой подсказки.")
    ))

    register_achievement(Achievement(
        id="scared_the_grandpa",
        name=_("Вы напугали деда"),
        description=_("Разозлите священника в Часовне, прочитайте книгу фольклора 'tears' в Библиотеке и вернитесь к пустой скамье."),
        icon="images/achievements/warning.png",
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Один дерзкий спор, подкреплённый цитатой из древнего библиотечного фолианта, способен обратить в бегство даже служителя культа.")
    ))

    register_achievement(Achievement(
        id="sibyl_lore_name",
        name=_("Ты знаешь это имя"),
        description=_("При ответе на финальный вопрос СИВИЛЛЫ 'Кто вы?' введите одно из ключевых лорных имён вселенной."),
        icon="images/achievements/yourname.png",
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. «Назови моё имя». В недрах памяти СИВИЛЛЫ дремлют имена тех, кто правил островами и зажигал звёзды. Сумеете ли вы вспомнить хоть одно?")
    ))

    # --- ДОСТИЖЕНИЯ ГЛАВЫ 3 ---

    register_achievement(Achievement(
        id="bouncer_plead_useless",
        name=_("Ну и пожалуйста, ну и пошло всё в пи..."),
        description=_("В Главе 3 четырежды попытайтесь вежливо уговорить вышибалу открыть дверь, пока уговоры не станут бесполезными."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. «Ты не пройдёшь!» — но вежливый следователь упрямо продолжает здороваться со стеной раз за разом...")
    ))

    register_achievement(Achievement(
        id="bouncer_daughter_game_over",
        name=_("Запретная тема"),
        description=_("В Главе 3 выведите вышибалу из себя упоминанием его дочери и сразу же попадитесь ему во время погони."),
        icon="images/achievements/bodyshadow.png",
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Премия Дарвина достаётся тому, кто сначала заденет громилу за самое живое, а потом попытается сбежать по прямой.")
    ))

    # --- НОВЫЕ СКРЫТЫЕ ДОСТИЖЕНИЯ ---

    register_achievement(Achievement(
        id="protocol_error_profanity",
        name=_("Штраф за нарушение морального кодекса"),
        description=_("При вопросе СИВИЛЛЫ 'Кто вы?' попытайтесь ввести запрещённое слово или оскорбление."),
        icon=None,
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Искусственный интеллект обучен миллионам страниц вежливости. А вот ваш словарный запас при знакомстве оставляет желать лучшего.")
    ))

    register_achievement(Achievement(
        id="backup_plan",
        name=_("Определение безумия"),
        description=_("Попробуйте применить неподходящий или бесполезный предмет из инвентаря 5 раз."),
        icon="images/achievements/neonthinking.png",
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Безумие — это точное повторение одного и того же действия в надежде на результат. Например, упорные попытки применить неподходящий предмет снова и снова.")
    ))

    register_achievement(Achievement(
        id="painful_doubts",
        name=_("Красная или синяя?"),
        description=_("Проведите на экране выбора важного решения более 2 минут без действия."),
        icon="images/achievements/argondoubt.png",
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Даже сверхмощный процессор перегреется, если слишком долго взвешивать варианты. Замереть на развилке судьбы на пару минут — тоже выбор.")
    ))

    register_achievement(Achievement(
        id="detective_intuition",
        name=_("Хан стрелял первым"),
        description=_("Сделайте сюжетный выбор менее чем за 1.5 секунды после появления меню выборов."),
        icon="images/achievements/fastdecision.png",
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. В неоновых переулках секунда промедления стоит жизни. Доверьтесь рефлексам и сделайте сюжетный выбор молниеносно, не читая варианты.")
    ))

    register_achievement(Achievement(
        id="polyglot",
        name=_("Вавилонская рыбка"),
        description=_("Смените язык игры прямо во время прохождения истории."),
        icon="images/achievements/radon.png",
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Чтобы понимать чужую речь, Артур Дент использовал маленькую рыбку. А вам достаточно заглянуть в системные настройки прямо посреди диалога.")
    ))

    register_achievement(Achievement(
        id="cinema_mode",
        name=_("Попкорн не входит в стоимость"),
        description=_("Прочитайте 100 строк диалога подряд в режиме Авточтения (Auto Forward)."),
        icon="images/achievements/argontv.png",
        ach_type=ACH_TYPE_HIDDEN,
        hidden_desc=_("Скрытое достижение. Уберите руки от мышки и клавиатуры. Позвольте сотне строк текста проплыть перед глазами в режиме авточтения.")
    ))

    # -------------------------------------------------------------------------
    # 3. ТРЕКИНГ / ПРОГРЕССИВНЫЕ ДОСТИЖЕНИЯ
    # -------------------------------------------------------------------------

    register_achievement(Achievement(
        id="bookworm",
        name=_("Книжный Червь"),
        description=_("Изучите все 4 архивные статьи в терминале Библиотеки Орбитали."),
        icon="images/achievements/xenon.png",
        ach_type=ACH_TYPE_TRACKING,
        max_progress=4
    ))

    register_achievement(Achievement(
        id="failure_chronicles",
        name=_("Хроники неудач"),
        description=_("Столкнитесь с 3 различными ситуациями неудач, перезагрузок или гибели."),
        icon="images/achievements/todo.png",
        ach_type=ACH_TYPE_TRACKING,
        max_progress=3
    ))

    register_achievement(Achievement(
        id="save_scummer",
        name=_("Синдром Сохранения"),
        description=_("Сделайте 50 ручных сохранений игры."),
        icon=None,
        ach_type=ACH_TYPE_TRACKING,
        max_progress=50
    ))

    register_achievement(Achievement(
        id="criminalist",
        name=_("Криминалист"),
        description=_("Внимательно изучите все доступные предметы в игре хотя бы один раз."),
        icon="images/achievements/neondetective.png",
        ach_type=ACH_TYPE_TRACKING,
        max_progress=13
    ))

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
        icon="images/achievements/16hours.png",
        ach_type=ACH_TYPE_TRACKING,
        max_progress=16
    ))

    register_achievement(Achievement(
        id="dont_touch_logo",
        name=_("Не трогай меня!"),
        description=_("Нажмите на логотип игры в главном меню 10 раз."),
        icon="images/achievements/dontclick.png",
        ach_type=ACH_TYPE_TRACKING,
        max_progress=10,
        hidden_desc=_("Скрытое достижение. Любопытство сгубило не одного сотрудника Корпорации. Нажатие на запретные объекты никогда не приводит к добру.")
    ))
