label chapter5_start:

    # Переменные для отслеживания исследования
    default visited_bar = False
    default visited_chapel = False
    default visited_library = False
    default hacking_tool = True # У нас есть "отмычка" от Мэрил

    # --- СЦЕНА: РАЗДЕЛЕНИЕ ---
    scene bg space_station_corridor_main with fade
    play music "music/BGM/Space_Station_Atmosphere.opus" fadein 2.0 loop volume 0.3
    play ambient "ambient/station_hum_ventilation.opus" fadein 2.0 loop

    show neon operative_neutral at right with dissolve
    show argon operative_glasses at left with dissolve

    argon "{=whisper}Помни легенду. Елена Кеттлер. Ты здесь, чтобы проверить калибровку сенсоров в Научном крыле."

    neon "{=whisper}Я помню, Аргон. Я делала это сотню раз за последние два года."

    argon "{=whisper}И каждый раз я волнуюсь. Эта станция... она другая. Здесь слишком тихо для торгового хаба. И слишком много красных мундиров."

    narrator """
        Он поправил воротник моего комбинезона, словно заботливый отец, поправляющий шарф перед школой.
        
        Это движение было таким привычным и таким неуместным здесь, в логове корпоративного монстра.
    """

    argon "{=whisper}Если что-то пойдет не так — сразу на частоту 'Омега'. Я брошу Карго и буду у тебя через три минуты."

    neon "Иди, Аргон. Я справлюсь. Встретимся у шлюза."

    hide argon with dissolve

    narrator """
        Он неохотно кивнул и растворился в потоке техников, направляясь к грузовым лифтам.
        
        Я осталась одна. В огромном металлическом чреве 'Орбитали'.
        
        Моя цель — Серверная в Научном секторе. Но у меня есть немного времени, чтобы осмотреться. Информация — это тоже оружие.
    """
return