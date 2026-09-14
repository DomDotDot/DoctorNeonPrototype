################################################################################
## Система выхода из игры и GPU-шейдер синего пламени
## Doctor Neon Prototype - Cinematic Blue Flame Screen Burn Exit System
################################################################################

init 5 python:
    # =========================================================================
    # GPU Шейдер синего пламени (Hardware GLSL Burn Shader)
    # Сжигает экран снизу-справа и сверху-слева навстречу друг другу
    # с использованием кастомной органической маски burn_mask.png:
    # 1. Непрогоревшая область: прозрачная (виден экран игры)
    # 2. Предпламенная область: неоновое бирюзовое свечение и дымка
    # 3. Фронт пламени: яркий синий огонь, белый центр, языки пламени и искры
    # 4. Обугленный край: коричневатый нагар, угли и пепел
    # 5. Сожжённая область: абсолютно чёрный фон (#000000)
    # =========================================================================
    renpy.register_shader("custom.blue_flame_burn",
        variables="""
            uniform sampler2D tex0;
            uniform float u_progress;
            uniform float u_time;
            attribute vec2 a_tex_coord;
            varying vec2 v_tex_coord;
        """,
        vertex_300="""
            v_tex_coord = a_tex_coord;
        """,
        fragment_300="""
            // Сэмплирование кастомной маски сгорания (сверху-слева и снизу-справа)
            float mask = texture2D(tex0, v_tex_coord.xy).r;
            
            // Живое микро-мерцание пламени вдоль органического контура
            float flicker = sin(u_time * 22.0 + v_tex_coord.y * 35.0 + v_tex_coord.x * 25.0) * 0.008;
            
            // Порог сжигания: плавно распространяется от углов к центру
            // При progress 0.0 threshold = 1.05 (ни один пиксель ещё не горит)
            // При progress 1.0 threshold = -0.20 (100% экрана сожжено в чистый чёрный фон)
            float threshold = 1.05 - (u_progress * 1.25);
            float dist = (mask + flicker) - threshold;
            
            if (dist < -0.040) {
                // Зона до огня: полностью прозрачная (отображается экран игры)
                gl_FragColor = vec4(0.0, 0.0, 0.0, 0.0);
            } else if (dist < 0.0) {
                // Предпламенная зона: неоновая бирюзовая дымка / тепловой ореол
                float t = (dist + 0.040) / 0.040;
                gl_FragColor = vec4(0.02 * t, 0.75 * t, 1.0 * t, t * 0.70);
            } else if (dist < 0.060) {
                // ФРОНТ СИНЕГО ПЛАМЕНИ
                float t = dist / 0.060;
                if (t < 0.40) {
                    // Ядро пламени: ослепительный электрик-циан + белые искры
                    float f = t / 0.40;
                    float spark = sin(v_tex_coord.x * 150.0 + v_tex_coord.y * 130.0 - u_time * 20.0);
                    float spark_val = step(0.88, spark) * 0.35;
                    gl_FragColor = vec4(0.60 + 0.40 * f + spark_val, 0.90 + 0.10 * f, 1.0, 1.0);
                } else {
                    // Тело пламени: насыщенный синий переходит в глубокий ультрамарин
                    float f = (t - 0.40) / 0.60;
                    vec3 blue_flame = mix(vec3(0.55, 0.88, 1.0), vec3(0.02, 0.25, 0.95), f);
                    gl_FragColor = vec4(blue_flame, 1.0);
                }
            } else if (dist < 0.140) {
                // ОБУГЛЕННЫЙ КРАЙ (коричневатость, угли, нагар)
                float t = (dist - 0.060) / 0.080;
                float falloff = (1.0 - t) * (1.0 - t);
                // Градиент коричневатости: от тёплых тлеющих углей к чёрному
                vec3 scorch = vec3(0.48 * falloff, 0.18 * falloff, 0.05 * falloff);
                gl_FragColor = vec4(scorch, 1.0);
            } else {
                // СОЖЖЁННАЯ ОБЛАСТЬ (абсолютный чёрный фон)
                gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
            }
        """
    )


init -1 python:
    # =========================================================================
    # Проверка типа подтверждения (выход из игры или другое действие)
    # =========================================================================
    def is_quit_confirmation(message):
        if message is None:
            return False
        if message == layout.QUIT:
            return True
        try:
            msg_str = str(_(message)).lower()
        except:
            msg_str = str(message).lower()
        return ("выйти" in msg_str or "quit" in msg_str or "выход" in msg_str or "exit" in msg_str)


    # =========================================================================
    # Контроллер обновления прогресса сгорания экрана (ATL Updater)
    # =========================================================================
    class ExitBurnUpdater(object):
        def __init__(self, duration=2.4):
            self.duration = float(duration)

        def __call__(self, trans, st, at):
            # st - количество секунд с момента старта анимации
            progress = min(1.0, st / self.duration)
            trans.u_progress = progress
            trans.u_time = st

            if progress >= 1.0:
                # Экран полностью покрыт чёрным, производим чистый выход из игры
                renpy.quit(relaunch=False, status=0)
                return None
            return 0

    def exit_burn_func(duration=2.4):
        return ExitBurnUpdater(duration)


    # =========================================================================
    # Ren'Py Action: Запуск процесса выхода с анимацией синего пламени
    # =========================================================================
    class StartExitBurn(Action):
        def __init__(self, duration=2.4):
            self.duration = duration

        def __call__(self):
            # 1. Закрываем окно подтверждения
            renpy.hide_screen("confirm")

            if getattr(persistent, "disable_gpu_animations", False):
                renpy.quit()
                return

            # 2. Плавно затухаем музыку
            try:
                renpy.music.stop(channel="music", fadeout=1.5)
            except:
                pass

            # 3. Воспроизводим звуки возгорания

            try:
                renpy.sound.play("audio/sfx/fire-burn.mp3", channel="ui_sfx1")
            except:
                pass

            # 4. Показываем полноэкранный оверлей сгорания
            renpy.show_screen("game_exit_burn_screen", duration=self.duration)
            renpy.restart_interaction()


transform exit_burn_tf(duration):
    mesh True
    shader "custom.blue_flame_burn"
    function exit_burn_func(duration)


# =============================================================================
# Экран кинематографичного сгорания игры синим пламенем
# =============================================================================
screen game_exit_burn_screen(duration=2.4):
    modal True
    zorder 999999

    # Блокируем абсолютно любой пользовательский ввод во время сгорания экрана
    key "game_menu" action NullAction()
    key "dismiss" action NullAction()
    key "button_select" action NullAction()

    # Полотно кастомной органической маски с наложенным GPU-шейдером синего пламени
    add "gui/burn_mask.png":
        xsize config.screen_width
        ysize config.screen_height
        at exit_burn_tf(duration)

    # Страховочный таймер для гарантированного выхода
    timer (duration + 0.15) action Quit(confirm=False)
