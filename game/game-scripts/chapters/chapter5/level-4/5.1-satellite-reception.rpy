# --- ГЛОБАЛЬНЫЙ ТАЙМЕР НЕКСУСА ---
init python:
    def ch5_check_timer_and_jump():
        if store.ch5_satellite_timer_active:
            elapsed = renpy.time.time() - store.ch5_satellite_timer_start
            if elapsed >= store.ch5_satellite_timer_duration:
                renpy.hide_screen("global_satellite_timer_screen")
                renpy.jump("ch5_satellite_timer_expired")

    def ch5_render_timer_text(st, at):
        if store.ch5_satellite_timer_active:
            elapsed = renpy.time.time() - store.ch5_satellite_timer_start
            remaining = max(0.0, store.ch5_satellite_timer_duration - elapsed)
            return Text("ВРЕМЯ ДО ПЕРЕГРУЗКИ: {} сек.".format(int(remaining)), color="#ff3333", size=30, outlines=[(2, "#000", 0, 0)], bold=True), 0.1
        return Text(""), None

screen global_satellite_timer_screen():
    zorder 100
    if ch5_satellite_timer_active:
        timer 0.1 action Function(ch5_check_timer_and_jump) repeat True
        
        vbox:
            xalign 0.5
            yalign 0.05
            add DynamicDisplayable(ch5_render_timer_text)

# --- СПУТНИК НЕКСУС: РЕСЕПШЕН ---
label ch5_satellite_reception:
    scene bg space_station_maintenance_tunnel with fade
    stop music fadeout 2.0
    play ambient "ambient/derelict_hum_wind.opus" loop fadein 3.0
    
    narrator """
        Ресепшен Нексуса.
        
        Запылённая круглая комната, освещённая мерцающими аварийными лампами. Пол покрыт тонким слоем металлической пыли. Воздух был затхлым и холодным.
        
        В центре — старая стойка регистрации с потрескавшимся голоэкраном. На стенах — блёклые указатели.
    """

label ch5_satellite_reception_menu:
    
    menu:
        "Осмотреть стойку регистрации" if not ch5_satellite_reception_examined:
            narrator """
                Я подошла к стойке. Голоэкран мигал, пытаясь загрузить интерфейс, но застревал на экране приветствия.
                
                На столе под слоем пыли я нашла планшет одного из техников. Большая часть данных была повреждена, но кое-что удалось прочитать:
            """
            
            narrator """
                Запись от инженера Такахаши, дата повреждена:
                
                'Протокол активации сервером Нексуса:
                Сервера в коридорах A, B и C питают энергетический затвор Ядра.
                Активация строго последовательная — A, затем B, затем C.
                
                ВНИМАНИЕ: после выполнения верификации в коридоре B запускается отсчёт мощности. Сервера перегрузятся через 90 секунд. Этого должно хватить на прохождение коридора C и открытие Ядра.
                
                Если не успеете — всё придётся начинать заново.'
            """
            
            $ ch5_satellite_reception_examined = True
            
            neon "{=thoughts}Последовательно: A, B, C. И таймер на 90 секунд со второго коридора. Нужно действовать быстро.{/thoughts}"
            jump ch5_satellite_reception_menu
        
        "Осмотреть указатели на стенах":
            narrator """
                Выцветшие указатели на стенах:
                
                ← Коридор A — 'Модуль Паттернов' 
                ↑ Коридор B — 'Модуль Логики'
                → Коридор C — 'Модуль Шифрования'
                ↓ Коридор D — 'Ядро Коммуникации''
            """
            jump ch5_satellite_reception_menu
        
        "Осмотреть доску на стене":
            narrator """
                На стене, рядом со стойкой, висела старая информационная доска. Среди пожелтевших объявлений и расписаний я заметила рукописный листок, приколотый канцелярской кнопкой:
                
                'Для новеньких — не запоминайте коды. Запоминайте стихи.
                
                Истина скрыта в первых словах,
                Каждая строчка — часть ключа.
                Ответ в начале каждой строки,
                Разум откроет путь — смотри.'
            """
            
            neon "{=thoughts}Первые буквы строк... И-К-О-Р... 'ИКОР'? Нет, это подсказка к загадке в одном из коридоров. Нужно запомнить.{/thoughts}"
            jump ch5_satellite_reception_menu
        
        "Пойти в Коридор A (Модуль Паттернов)":
            jump ch5_corridor_alpha
        
        "Пойти в Коридор B (Модуль Логики)" if ch5_corridor_alpha_solved:
            jump ch5_corridor_beta
        
        "Пойти в Коридор C (Модуль Контекста)" if ch5_corridor_beta_solved:
            jump ch5_corridor_gamma
        
        "Пойти в Коридор D (Ядро Коммуникации)" if ch5_core_corridor_open:
            jump ch5_corridor_core
        
        "Вернуться к монорельсу" if ch5_ai_core_complete:
            jump ch5_monorail_entrance