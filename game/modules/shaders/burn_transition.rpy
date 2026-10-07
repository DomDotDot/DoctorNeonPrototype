################################################################################
## GPU-шейдер и переход сгорания сцены (Cinematic Screen Burn Transition)
## Doctor Neon Prototype - In-game Scene Burn Transition using burn_mask.png
################################################################################

init -10 python:
    # =========================================================================
    # Регистрация аппаратного GPU-шейдера сгорания сцены
    # tex0 = маска сгорания (gui/burn_mask.png)
    # tex1 = уходящая сцена (старый кадр)
    # tex2 = проявляющаяся сцена (новый кадр, например scene black или новая локация)
    # =========================================================================
    renpy.register_shader("custom.burn_transition",
        variables="""
            uniform float u_lod_bias;
            uniform sampler2D tex0;
            uniform sampler2D tex1;
            uniform sampler2D tex2;
            uniform float u_burn_progress;
            uniform float u_burn_time;
            uniform float u_burn_mode;
            attribute vec2 a_tex_coord;
            varying vec2 v_tex_coord;
        """,
        vertex_200="""
            v_tex_coord = a_tex_coord;
        """,
        fragment_200="""
            vec2 uv = v_tex_coord.xy;
            vec4 old_scene = texture2D(tex1, uv, u_lod_bias);
            vec4 new_scene = texture2D(tex2, uv, u_lod_bias);
            float mask = texture2D(tex0, uv, u_lod_bias).r;

            // 1. Органическая турбулентность и мерцание фронта пламени
            float flame_flicker = sin(u_burn_time * 26.0 + uv.y * 45.0 + uv.x * 35.0) * 0.012;
            float heat_wave = cos(u_burn_time * 18.0 - uv.y * 30.0) * 0.007;
            float organic_mask = mask + flame_flicker + heat_wave;

            // 2. Порог сгорания: распространяется от углов/контура маски
            // При progress 0.0 -> threshold = 1.06 (вся старая сцена цела)
            // При progress 1.0 -> threshold = -0.22 (вся сцена полностью сожжена, видна новая)
            float threshold = 1.06 - (u_burn_progress * 1.28);
            float dist = organic_mask - threshold;

            if (dist < -0.045) {
                // ЗОНА 1: ДО ОГНЯ — старая сцена цела и не тронута
                gl_FragColor = old_scene;
            } else if (dist < 0.0) {
                // ЗОНА 2: ПРЕДПЛАМЕННЫЙ ТЕПЛОВОЙ ОРЕОЛ И ИСКАЖЕНИЕ СТАРОЙ СЦЕНЫ
                float heat_factor = (dist + 0.045) / 0.045; // 0.0 -> 1.0

                // Тепловое преломление (дисторшн горячего воздуха) на текстуре старой сцены
                vec2 heat_distortion = vec2(
                    sin(u_burn_time * 30.0 + uv.y * 55.0) * 0.004 * heat_factor,
                    cos(u_burn_time * 25.0 + uv.x * 55.0) * 0.004 * heat_factor
                );
                vec4 distorted_old = texture2D(tex1, clamp(uv + heat_distortion, 0.0, 1.0), u_lod_bias);

                // Тепловое неоновое свечение перед возгоранием
                vec3 preheat_glow;
                if (u_burn_mode < 0.5) {
                    // Режим 0: Фирменный синий неон Doctor Neon (бирюзовый жар)
                    preheat_glow = vec3(0.04, 0.72, 1.0) * heat_factor * 0.85;
                } else {
                    // Режим 1: Классическое тёплое пламя (тлеющий оранжевый жар)
                    preheat_glow = vec3(1.0, 0.45, 0.05) * heat_factor * 0.85;
                }
                gl_FragColor = vec4(distorted_old.rgb + preheat_glow, distorted_old.a);
            } else if (dist < 0.070) {
                // ЗОНА 3: ФРОНТ ПЛАМЕНИ (бушующая стена огня)
                float f = dist / 0.070; // 0.0 на кромке -> 1.0 внутри пламени

                // Живые искры вдоль фронта горения
                float spark_seed = sin(uv.x * 160.0 + uv.y * 140.0 - u_burn_time * 24.0);
                float spark = step(0.86, spark_seed) * 0.40;

                vec3 flame_col;
                if (u_burn_mode < 0.5) {
                    // Синее неоновое пламя
                    if (f < 0.35) {
                        // Раскалённое ядро: ослепительный электрик-циан + белый центр
                        float core_t = f / 0.35;
                        flame_col = mix(vec3(1.0, 1.0, 1.0) + spark, vec3(0.35, 0.92, 1.0), core_t);
                    } else {
                        // Тело пламени: насыщенный синий ультрамарин
                        float body_t = (f - 0.35) / 0.65;
                        flame_col = mix(vec3(0.35, 0.92, 1.0), vec3(0.02, 0.22, 0.96), body_t);
                    }
                } else {
                    // Тёплый классический огонь
                    if (f < 0.35) {
                        // Бело-жёлтое раскалённое ядро
                        float core_t = f / 0.35;
                        flame_col = mix(vec3(1.0, 1.0, 1.0) + spark, vec3(1.0, 0.90, 0.25), core_t);
                    } else {
                        // Огненно-оранжевый и багровый язык пламени
                        float body_t = (f - 0.35) / 0.65;
                        flame_col = mix(vec3(1.0, 0.85, 0.15), vec3(0.96, 0.18, 0.02), body_t);
                    }
                }
                gl_FragColor = vec4(flame_col, 1.0);
            } else if (dist < 0.150) {
                // ЗОНА 4: ОБУГЛЕННЫЙ КРАЙ, ПЕПЕЛ И ТЛЕЮЩИЕ УГЛИ
                float ash_t = (dist - 0.070) / 0.080; // 0.0 -> 1.0
                float char_falloff = (1.0 - ash_t) * (1.0 - ash_t);

                // Мерцание тлеющих углей в пепле
                float ember_noise = fract(sin(dot(uv * 90.0, vec2(12.9898, 78.233)) + u_burn_time * 12.0) * 43758.5453);
                float ember_pulse = step(0.92, ember_noise) * (1.0 - ash_t) * 0.75;

                vec3 char_col;
                if (u_burn_mode < 0.5) {
                    // Тёмно-угольный край с неоновыми голубыми угольками
                    char_col = vec3(0.02, 0.05, 0.12) * char_falloff + vec3(0.12, 0.65, 1.0) * ember_pulse;
                } else {
                    // Обугленный нагар с огненно-красными искрами
                    char_col = vec3(0.20, 0.06, 0.02) * char_falloff + vec3(1.0, 0.35, 0.0) * ember_pulse;
                }

                // Плавное перетекание обугленного края в открывающуюся новую сцену
                gl_FragColor = mix(vec4(char_col, 1.0), new_scene, ash_t);
            } else {
                // ЗОНА 5: ПОЛНОСТЬЮ СГОРЕЛО — видна новая сцена
                gl_FragColor = new_scene;
            }
        """
    )


init -5 python:
    class FlameBurnTransition(renpy.display.transition.Transition):
        """
        Полноэкранный кинематографичный переход сгорания текущей сцены.
        Использует GPU-шейдер и маску burn_mask.png, обнажая новую сцену
        сквозь языки пламени, тепловые искажения и обугленный край.
        """
        def __init__(self, time=2.5, mask="gui/burn_mask.png", sound="audio/sfx/fire-burn.mp3", mode="blue", old_widget=None, new_widget=None, **properties):
            super(FlameBurnTransition, self).__init__(time, **properties)
            self.time = float(time)
            self.mask_path = mask
            self.sound = sound
            self.mode = mode.lower() if isinstance(mode, str) else "blue"
            self.old_widget = old_widget
            self.new_widget = new_widget
            self.events = False
            self.sound_played = False

            # Создаём контейнер и displayable для маски с фиксированным разрешением экрана игры
            self.control = renpy.display.layout.Fixed()
            mask_d = Transform(
                renpy.easy.displayable(mask),
                xsize=config.screen_width,
                ysize=config.screen_height
            )
            self.control.add(mask_d)

        def visit(self):
            v = super(FlameBurnTransition, self).visit()
            if self.control is not None:
                v.append(self.control)
            return v

        def render(self, width, height, st, at):
            # Если переход завершился — возвращаем финальный новый экран
            if st >= self.time:
                self.events = True
                if self.new_widget is not None:
                    return renpy.display.render.render(self.new_widget, width, height, st, at)
                return renpy.display.render.Render(width, height)

            # Воспроизведение звука возгорания при старте перехода
            if self.sound and not self.sound_played:
                self.sound_played = True
                try:
                    renpy.sound.play(self.sound, channel="sound")
                except Exception:
                    pass

            # Fallback: если игрок отключил GPU-анимации в настройках игры
            if getattr(persistent, "disable_gpu_animations", False):
                complete = min(1.0, max(0.0, st / self.time))
                old_w = self.old_widget or renpy.display.layout.Null()
                new_w = self.new_widget or renpy.display.layout.Null()
                bottom = renpy.display.render.render(old_w, width, height, st, at)
                top = renpy.display.render.render(new_w, width, height, st, at)

                w = max(bottom.width, top.width, width)
                h = max(bottom.height, top.height, height)
                rv = renpy.display.render.Render(w, h)

                rv.mesh = True
                rv.add_shader("renpy.dissolve")
                rv.add_uniform("u_renpy_dissolve", complete)
                rv.blit(bottom, (0, 0), focus=False, main=False)
                rv.blit(top, (0, 0), focus=True, main=True)
                renpy.display.render.redraw(self, 0)
                return rv

            # Аппаратный рендеринг GPU-шейдера сгорания
            old_w = self.old_widget or renpy.display.layout.Null()
            new_w = self.new_widget or renpy.display.layout.Null()

            bottom = renpy.display.render.render(old_w, width, height, st, at)
            top = renpy.display.render.render(new_w, width, height, st, at)
            mask_r = renpy.display.render.render(self.control, width, height, st, at)

            w = max(bottom.width, top.width, mask_r.width, width)
            h = max(bottom.height, top.height, mask_r.height, height)

            rv = renpy.display.render.Render(w, h)
            complete = min(1.0, max(0.0, st / self.time))

            rv.mesh = True
            rv.add_shader("custom.burn_transition")
            rv.add_uniform("u_burn_progress", complete)
            rv.add_uniform("u_burn_time", st)
            rv.add_uniform("u_burn_mode", 0.0 if self.mode == "blue" else 1.0)

            # Порядок текстур для GLSL:
            # tex0 = mask_r (маска горения)
            # tex1 = bottom (сгорающая старая сцена)
            # tex2 = top (проявляющаяся новая сцена)
            rv.blit(mask_r, (0, 0), focus=False, main=False)
            rv.blit(bottom, (0, 0), focus=False, main=False)
            rv.blit(top, (0, 0), focus=True, main=True)

            renpy.display.render.redraw(self, 0)
            return rv

    # Фабрика каррирования для использования как 'with FlameBurn(...)'
    FlameBurn = renpy.curry(FlameBurnTransition)
    BurnTransition = FlameBurn

    # Готовые пресеты переходов для использования в сценах (.rpy):
    #   scene black with flame_burn
    #   scene my_cg with flame_burn_orange
    #   scene next_bg with flame_burn_fast

    # Фирменное синее неоновое сгорание Doctor Neon (2.5 сек, со звуком огня)
    flame_burn = FlameBurn(2.5, mode="blue")
    flame_burn_blue = FlameBurn(2.5, mode="blue")

    # Классический огненный переход (тёплое оранжево-красное пламя)
    flame_burn_orange = FlameBurn(2.5, mode="orange")
    fire_burn = FlameBurn(2.5, mode="orange")

    # Быстрый переход сгорания (1.5 сек)
    flame_burn_fast = FlameBurn(1.5, mode="blue")
    fire_burn_fast = FlameBurn(1.5, mode="orange")

    # Драматичный медленный переход сгорания (3.5 сек)
    flame_burn_slow = FlameBurn(3.5, mode="blue")
    fire_burn_slow = FlameBurn(3.5, mode="orange")

    # Беззвучный переход сгорания (звук отключен)
    flame_burn_silent = FlameBurn(2.5, mode="blue", sound=None)
    fire_burn_silent = FlameBurn(2.5, mode="orange", sound=None)

