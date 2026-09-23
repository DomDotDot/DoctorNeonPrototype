init offset = 1 # Force this to load after standard screens

# Переопределяем экран, вызываемый по ESC (game_menu)
# Обычно это "save", но мы меняем на наше новое "pause_menu"
define _game_menu_screen = "pause_menu"

# =============================================================================
# GPU-шейдер эффекта срыва кассетного видео (VHS Tape Tearing Glitch)
# =============================================================================

init -5 python:
    renpy.register_shader("custom.vhs_tape_glitch",
        variables="""
            uniform sampler2D tex0;
            uniform float u_vhs_time;
            attribute vec2 a_tex_coord;
            varying vec2 v_tex_coord;
        """,
        vertex_300="""
            v_tex_coord = a_tex_coord;
        """,
        fragment_300="""
            vec2 uv = v_tex_coord;

            // 1. Полосы срыва синхронизации трекинга (Tracking tear wave)
            float wave1 = sin(uv.y * 7.0 + u_vhs_time * 3.5);
            float wave2 = sin(uv.y * 23.0 - u_vhs_time * 6.0);
            float tear_trigger = step(0.65, sin(uv.y * 3.0 + u_vhs_time * 5.0));

            // Высокочастотный псевдослучайный строчный джиттер (Jitter)
            float line_seed = floor(uv.y * 240.0) + floor(u_vhs_time * 20.0);
            float line_rand = fract(sin(line_seed * 91.3458) * 47453.5453);
            float jitter = (line_rand - 0.5) * step(0.85, line_rand) * 0.035;

            // Суммарный горизонтальный сдвиг ленты
            float shift_x = (wave1 * wave2 * 0.04 * tear_trigger + jitter);

            // 2. Нижняя полоса переключения видеоголовок (Head-switching noise at bottom)
            if (uv.y > 0.93) {
                float head_noise = sin(uv.y * 60.0 + u_vhs_time * 45.0) * 0.05;
                shift_x += head_noise;
            }

            // 3. Хроматический сдвиг RGB (расслоение каналов магнитной плёнки)
            float r_offset = shift_x + 0.005;
            float b_offset = shift_x - 0.005;

            vec2 uv_r = vec2(clamp(uv.x + r_offset, 0.0, 1.0), uv.y);
            vec2 uv_g = vec2(clamp(uv.x + shift_x, 0.0, 1.0), uv.y);
            vec2 uv_b = vec2(clamp(uv.x + b_offset, 0.0, 1.0), uv.y);

            float col_r = texture2D(tex0, uv_r).r;
            float col_g = texture2D(tex0, uv_g).g;
            float col_b = texture2D(tex0, uv_b).b;
            float alpha = texture2D(tex0, uv_g).a;

            vec3 col = vec3(col_r, col_g, col_b);

            // 4. Тонкие линии строчной развертки аналогового ТВ (Scanlines)
            float scanline = sin(uv.y * 600.0 * 3.14159) * 0.06;
            col -= vec3(scanline);

            // 5. Зерно и искры шума магнитной ленты (Tape noise sparkle)
            float noise = fract(sin(dot(uv + vec2(u_vhs_time * 17.0, u_vhs_time * 11.0), vec2(12.9898, 78.233))) * 43758.5453);
            if (noise > 0.985) {
                col += vec3(0.25);
            }

            // Легкое приглушение цвета для кинематографичности кассетного архива
            col = mix(col, vec3(dot(col, vec3(0.299, 0.587, 0.114))), 0.15);

            gl_FragColor = vec4(col, alpha);
        """
    )

    class VHSTapeUpdater(object):
        def __call__(self, trans, st, at):
            if getattr(persistent, "disable_gpu_animations", False):
                trans.u_vhs_time = 0.0
                return 0.2
            trans.u_vhs_time = st
            return 0

    def vhs_tape_func():
        return VHSTapeUpdater()


transform vhs_tape_glitch_tf:
    mesh True
    shader "custom.vhs_tape_glitch"
    function vhs_tape_func()


# =============================================================================
# Анимации элементов экрана паузы
# =============================================================================

transform pause_backdrop_fade:
    alpha 0.0
    easein 0.25 alpha 1.0

transform pause_card_entrance:
    alpha 0.0 zoom 0.95
    easein 0.22 alpha 1.0 zoom 1.0

transform pause_badge_pulse:
    alpha 0.4
    ease 0.8 alpha 1.0
    ease 0.8 alpha 0.4
    repeat


# =============================================================================
# Стили элементов интерфейса паузы
# =============================================================================

style pause_frame is frame:
    background Solid("#070d1cf2")
    xalign 0.5
    yalign 0.5
    xsize 480
    padding (32, 28)

style pause_action_button is button:
    xfill True
    ysize 46
    xalign 0.5
    yalign 0.5
    background Solid("#0f172a99")
    hover_background Solid("#1e293bcc")
    padding (20, 8)
    hover_sound "audio/sfx/cursor-hover.opus"
    activate_sound "audio/sfx/button-click.opus"

style pause_action_button_text is button_text:
    size 16
    color "#cbd5e1"
    hover_color "#38bdf8"
    bold True
    xalign 0.5
    yalign 0.5


# =============================================================================
# Экран паузы (ESC во время игры)
# =============================================================================

screen pause_menu():
    tag menu
    modal True

    # Воспроизведение звука колокола паузы, учёт достижения и запуск аудио паузы
    on "show" action [Function(mark_pause_opened), Function(enter_pause_audio), Play("sound", "audio/sfx/bell-ring.mp3")]
    on "replace" action [Function(mark_pause_opened), Function(enter_pause_audio), Play("sound", "audio/sfx/bell-ring.mp3")]
    on "hide" action Function(exit_pause_audio)

    # Горячая клавиша ESC для снятия паузы
    key "game_menu" action [Function(exit_pause_audio), Return()]

    # 1. Захваченный кадр игры со срывом кассетного видео (VHS Tape Glitch)
    add FileCurrentScreenshot(empty=Solid("#070d1a")):
        xsize config.screen_width
        ysize config.screen_height
        if not getattr(persistent, "disable_gpu_animations", False):
            at vhs_tape_glitch_tf

    # 2. Мягкое полупрозрачное затемнение поверх рвущегося кадра для читаемости меню
    add Solid("#03071288") at pause_backdrop_fade

    # 3. Верхняя статусная панель HUD
    frame:
        align (0.5, 0.0)
        xfill True
        ysize 36
        padding (30, 0)
        background Solid("#020617ea")
        hbox:
            xfill True
            yalign 0.5
            hbox:
                spacing 10
                yalign 0.5
                text "●" size 13 color "#1347a8" at (pause_badge_pulse if not getattr(persistent, "disable_gpu_animations", False) else None) yalign 0.5
            hbox:
                xalign 1.0
                yalign 0.5
                text _("[config.version!t]") size 11 bold True color "#475569" yalign 0.5

    # 4. Нижняя информационная плашка
    frame:
        align (0.5, 1.0)
        xfill True
        ysize 34
        padding (30, 0)
        background Solid("#020617ea")
        hbox:
            xfill True
            yalign 0.5
            text _("[[ESC]] — ВОЗОБНОВИТЬ ИГРУ  •  АВТОСОХРАНЕНИЕ ДОСТУПНО В МЕНЮ") substitute False size 11 color "#64748b" yalign 0.5
            hbox:
                xalign 1.0
                yalign 0.5
                text _("RESONANCE // MEMORY ARCHIVE") size 11 bold True color "#475569" yalign 0.5

    # 5. Центральная модальная панель управления
    frame:
        style "pause_frame"
        at (pause_card_entrance if not getattr(persistent, "disable_gpu_animations", False) else None)

        vbox:
            spacing 12
            xfill True

            # Заголовок с неоновой иконкой
            vbox:
                xalign 0.5
                spacing 2
                hbox:
                    xalign 0.5
                    spacing 10
                    text "⏸" size 26 bold True color "#38bdf8" yalign 0.5
                    text _("ПАУЗА") size 24 bold True color "#f8fafc" yalign 0.5

            # Разделитель
            frame:
                xfill True
                ysize 1
                background Solid("#38bdf833")

            null height 4

            # Меню действий
            textbutton _("▶  Продолжить"):
                action [Function(exit_pause_audio), Return()]
                style "pause_action_button"

            textbutton _("💾  Сохранить"):
                action ShowMenu("save")
                style "pause_action_button"

            textbutton _("📂  Загрузить"):
                action ShowMenu("load")
                style "pause_action_button"

            textbutton _("⚙️  Настройки"):
                action ShowMenu("settings_menu")
                style "pause_action_button"

            textbutton _("🌸  Главное меню"):
                action [Function(exit_pause_audio), MainMenu()]
                style "pause_action_button"

            textbutton _("🚪  Выход"):
                action Quit()
                style "pause_action_button"
