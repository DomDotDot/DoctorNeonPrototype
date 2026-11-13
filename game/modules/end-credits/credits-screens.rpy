init python:
    import os
    import re

    def _natural_sort_key(path):
        """Натуральная сортировка: 1cg, 2cg, ..., 10cg вместо лексикографической."""
        return [int(tok) if tok.isdigit() else tok.lower() for tok in re.split(r'(\d+)', path)]

    def _is_fallback_key_cg(filename_no_ext):
        """Отбор ключевых CG первой вариации для папок без _featured-меток."""
        low = filename_no_ext.lower()
        if "_bg" in low or low.startswith("bg"):
            return False
        if "_v01" in low:
            # Исключаем вторичные слои _v01_b, оставляя _v01 или _v01_a
            if re.search(r'_v01(?:_a)?$', low):
                return True
            return False
        return False

    def get_images_from_dir(folder_path, featured_suffix="_featured", featured_prefix="featured_"):
        """Собирает и натурально сортирует все и избранные CG в каталоге тома.

        Для каждой подпапки главы отбираются файлы с суффиксом ``_featured``
        (или префиксом ``featured_``). Если в конкретной подпапке нет помеченных
        файлов (например, ``vol1/chapter1`` или ``vol2/chapter5``), выполняется
        автоматический фоллбэк на первые вариации CG (``_v01`` без ``_bg``).
        """
        all_images = []
        featured_images = []

        if not folder_path.endswith("/"):
            folder_path += "/"

        valid_exts = ('.png', '.jpg', '.jpeg', '.avif', '.webp')
        by_subdir = {}

        for file in renpy.list_files():
            if file.startswith(folder_path) and file.lower().endswith(valid_exts):
                all_images.append(file)
                subdir = os.path.dirname(file)
                by_subdir.setdefault(subdir, []).append(file)

        all_images.sort(key=_natural_sort_key)

        for subdir in sorted(by_subdir.keys(), key=_natural_sort_key):
            files = sorted(by_subdir[subdir], key=_natural_sort_key)
            marked = []
            for f in files:
                stem = os.path.splitext(os.path.basename(f))[0]
                if (featured_suffix and stem.endswith(featured_suffix)) or (featured_prefix and stem.startswith(featured_prefix)):
                    marked.append(f)

            if marked:
                featured_images.extend(marked)
            else:
                # Поглавный фоллбэк на первые вариации CG
                fallback = [f for f in files if _is_fallback_key_cg(os.path.splitext(os.path.basename(f))[0])]
                if not fallback:
                    fallback = [f for f in files if "_bg" not in os.path.basename(f).lower()]
                featured_images.extend(fallback)

        featured_images.sort(key=_natural_sort_key)
        return featured_images, all_images

    def calculate_credits_slide_timing(num_images, total_duration, fade_time=1.2, min_slide=2.4, max_slide=6.0):
        """Автоматически подбирает время показа одного CG под длину трека."""
        if num_images <= 0:
            return 4.0
        raw_cycle = float(total_duration) / float(num_images)
        slide_time = raw_cycle - float(fade_time)
        return round(max(min_slide, min(max_slide, slide_time)), 2)

    class CreditsSlideshow(renpy.Displayable):
        """Бесшовное полноэкранное слайдшоу без Dissolve-переходов и вложенных Transform.

        Рисует максимум два слайда одновременно напрямую с плоским Transform
        (fit='cover', blur=7.0, gl_mipmap=True, Image(mipmap=True), zoom, alpha), благодаря чему:
        - шейдер renpy.blur и аппаратные мипмапы работают на каждом кадре без сброса;
        - уходящий слайд продолжает свой Ken Burns зум без рывка st=0;
        - картинки любого разрешения строго центрируются в 1920x1080.
        """

        def __init__(self, images, slide_time, fade_time, use_gpu=True, **properties):
            super(CreditsSlideshow, self).__init__(**properties)
            self.images = list(images) if images else []
            self.slide_time = max(0.5, float(slide_time))
            self.fade_time = min(self.slide_time * 0.6, max(0.1, float(fade_time)))
            self.use_gpu = bool(use_gpu)
            self.curr_idx = 0

        def _get_image(self, img_path):
            img_cache = getattr(self, "_img_cache", None)
            if img_cache is None:
                img_cache = {}
                self._img_cache = img_cache
            img = img_cache.get(img_path)
            if img is None:
                img = renpy.display.im.Image(img_path, mipmap=True)
                img_cache[img_path] = img
            return img

        def _make_slide_transform(self, img_path, idx, age, alpha_val):
            sw = config.screen_width
            sh = config.screen_height

            if self.use_gpu:
                total_life = self.slide_time + self.fade_time
                p = min(1.0, max(0.0, age / total_life))
                if idx % 2 == 0:
                    z = 1.04 + 0.06 * p
                else:
                    z = 1.10 - 0.06 * p
            else:
                z = 1.04

            return Transform(
                self._get_image(img_path),
                fit="cover",
                xsize=sw,
                ysize=sh,
                xalign=0.5,
                yalign=0.5,
                zoom=z,
                blur=7.0,
                gl_mipmap=True,
                matrixcolor=BrightnessMatrix(-0.08),
                alpha=alpha_val,
                subpixel=True
            )

        def render(self, width, height, st, at):
            sw = config.screen_width
            sh = config.screen_height
            rv = renpy.display.render.Render(sw, sh)

            if not self.images:
                return rv

            n = len(self.images)
            if n == 1:
                disp = self._make_slide_transform(self.images[0], 0, st, 1.0)
                cr = renpy.display.render.render(disp, sw, sh, st, at)
                rv.subpixel_blit(cr, ((sw - cr.width) * 0.5, (sh - cr.height) * 0.5))
                if self.use_gpu:
                    renpy.display.render.redraw(self, 0)
                return rv

            idx = int(st // self.slide_time)
            local_t = st - idx * self.slide_time
            self.curr_idx = idx % n

            # Предзагружаем следующие слайды в фоновом потоке при смене индекса
            if getattr(self, "_last_preloaded_idx", -1) != idx:
                self._last_preloaded_idx = idx
                for offset in (1, 2):
                    next_img = self._get_image(self.images[(self.curr_idx + offset) % n])
                    renpy.display.im.cache.preload_image(next_img)

            # Уходящий слайд рисуется на заднем плане во время фазы кроссфейда
            if idx > 0 and local_t < self.fade_time:
                prev_idx = (idx - 1) % n
                prev_age = self.slide_time + local_t
                prev_disp = self._make_slide_transform(self.images[prev_idx], idx - 1, prev_age, 1.0)
                pr = renpy.display.render.render(prev_disp, sw, sh, st, at)
                rv.subpixel_blit(pr, ((sw - pr.width) * 0.5, (sh - pr.height) * 0.5))

                t_norm = min(1.0, max(0.0, local_t / self.fade_time))
                curr_alpha = t_norm * t_norm * (3.0 - 2.0 * t_norm)
            else:
                curr_alpha = 1.0

            curr_disp = self._make_slide_transform(self.images[self.curr_idx], idx, local_t, curr_alpha)
            cr = renpy.display.render.render(curr_disp, sw, sh, st, at)
            rv.subpixel_blit(cr, ((sw - cr.width) * 0.5, (sh - cr.height) * 0.5))

            renpy.display.render.redraw(self, 0)
            return rv

        def visit(self):
            if not self.images:
                return []
            # Возвращаем только ближайшее окно слайдов, чтобы не перегружать кэш текстур
            n = len(self.images)
            window = []
            for offset in range(3):
                window.append(self._get_image(self.images[(self.curr_idx + offset) % n]))
            return window

        def predict_one(self):
            if not self.images:
                return
            n = len(self.images)
            for offset in range(3):
                img = self._get_image(self.images[(self.curr_idx + offset) % n])
                renpy.display.predict.displayable(img)

    def create_slideshow(images, slide_time, fade_time, total_duration=None):
        """Создаёт полноэкранный заблюренный слайдшоу 1920x1080 без скачков и lowres."""
        if not images:
            return Solid("#000000")

        use_gpu = not getattr(persistent, "disable_gpu_animations", False)
        return CreditsSlideshow(images, slide_time, fade_time, use_gpu=use_gpu)

# ---------------------------------------------
# ТРАНСФОРМАЦИИ (Анимация)
# ---------------------------------------------

# Плавная субпиксельная прокрутка всего блока титров строго по высоте контента
transform credits_scroll_up(scroll_duration):
    subpixel True
    yanchor 0.0
    ypos 1.0
    linear scroll_duration yanchor 1.0 ypos 0.0

# Появление в начале и плавный увод правого затемнения / логотипа перед финальной надписью
transform credits_side_ui_fade(fade_out_at):
    subpixel True
    alpha 0.0
    easein 1.2 alpha 1.0
    pause max(0.0, fade_out_at - 1.2)
    easeout 1.5 alpha 0.0

# Появление финальной надписи строго по центру экрана
transform thanks_center_appear(wait_time):
    subpixel True
    alpha 0.0
    yoffset 16
    pause max(0.0, wait_time)
    easein 2.0 alpha 1.0 yoffset 0

# Плавное появление / скрытие подсказки двухшагового пропуска
transform skip_prompt_fade:
    subpixel True
    on show:
        alpha 0.0
        yoffset 8
        easein 0.25 alpha 1.0 yoffset 0
    on hide:
        easeout 0.25 alpha 0.0 yoffset 8

# ---------------------------------------------
# ЭКРАН ТИТРОВ
# ---------------------------------------------

screen end_credits(credits_list, slideshow_obj, track_duration, end_msg_offset):

    modal True
    zorder 200

    default skip_ready = False
    default skip_prompt_active = False

    $ phase2_time = max(2.0, float(track_duration) - float(end_msg_offset))
    $ scroll_duration = max(5.0, phase2_time - 1.5)

    # Защита от случайного клика по инерции в первую секунду после диалога
    timer 1.0 action SetScreenVariable("skip_ready", True)

    # Автоматическое завершение по окончании музыкального трека
    timer track_duration action Return("finished")

    # Авто-скрытие подсказки пропуска, если игрок не подтвердил пропуск за 4 секунды
    if skip_prompt_active:
        timer 4.0 action SetScreenVariable("skip_prompt_active", False)

    # Двухшаговый пропуск с клавиатуры (Пробел / Enter / Esc)
    key "dismiss" action If(
        skip_ready,
        If(skip_prompt_active, Return("skipped"), SetScreenVariable("skip_prompt_active", True)),
        NullAction()
    )
    key "game_menu" action If(
        skip_ready,
        If(skip_prompt_active, Return("skipped"), SetScreenVariable("skip_prompt_active", True)),
        NullAction()
    )

    # 1. Базовый чёрный фон
    add Solid("#000000")

    # 2. Полноэкранный заблюренный слайдшоу CG (1920x1080)
    add slideshow_obj id "credits_slideshow"

    # 3. Атмосферная виньетка из главного меню
    add "gui/main_menu/vignette.png" alpha 0.55

    # 4. Перехватчик кликов мыши по экрану (двухшаговый пропуск)
    button:
        style "empty"
        xfill True
        yfill True
        action If(
            skip_ready,
            If(skip_prompt_active, Return("skipped"), SetScreenVariable("skip_prompt_active", True)),
            NullAction()
        )

    # 5. Плавное затемнение правой части экрана (уходит перед финалом)
    add "gui/main_menu/credits_right_gradient.png":
        xsize config.screen_width
        ysize config.screen_height
        at credits_side_ui_fade(phase2_time)

    # 6. Чистый логотип слева-сверху (уходит перед финалом)
    add "gui/main_menu/logo3.png":
        xpos 55
        ypos 35
        zoom 0.65
        subpixel True
        at credits_side_ui_fade(phase2_time)

    # 7. Правая колонка бегущих титров
    fixed:
        xpos 1080
        ypos 0
        xsize 790
        ysize config.screen_height
        clipping True

        vbox at credits_scroll_up(scroll_duration):
            spacing 28
            xfill True

            for role, name in credits_list:
                if role == "---":
                    null height 32
                elif role != "" and name == "":
                    # Заголовок секции
                    null height 18
                    vbox:
                        xalign 0.5
                        spacing 8

                        text _(role):
                            font "WDXLLubrifontTC-Regular.ttf"
                            size 36
                            color "#00e5ff"
                            xalign 0.5
                            text_align 0.5
                            outlines [(2, "#000000aa", 0, 0)]

                        add Solid("#00e5ff66"):
                            xsize 260
                            ysize 2
                            xalign 0.5
                    null height 6
                elif role == "" and name != "":
                    # Одиночная строка списка
                    text _(name):
                        font "WDXLLubrifontTC-Regular.ttf"
                        size 30
                        color "#e6eef8"
                        xalign 0.5
                        text_align 0.5
                        outlines [(2, "#000000aa", 0, 0)]
                else:
                    # Двухколоночная пара: Роль — Имя
                    hbox:
                        spacing 28
                        xalign 0.5

                        text _(role):
                            font "WDXLLubrifontTC-Regular.ttf"
                            size 28
                            color "#9bb0c9"
                            xsize 340
                            text_align 1.0
                            yalign 0.5
                            outlines [(2, "#000000aa", 0, 0)]

                        text _(name):
                            font "WDXLLubrifontTC-Regular.ttf"
                            size 30
                            color "#ffffff"
                            xsize 380
                            text_align 0.0
                            yalign 0.5
                            outlines [(2, "#000000aa", 0, 0)]

            null height 180

    # 8. Финальная надпись ровно по центру всего экрана (после ухода бокового UI)
    text _("И тебе. Спасибо за игру!") at thanks_center_appear(phase2_time):
        font "WDXLLubrifontTC-Regular.ttf"
        align (0.5, 0.5)
        text_align 0.5
        size 52
        color "#ffffff"
        outlines [(3, "#000000cc", 0, 0)]

    # 9. Подсказка подтверждения пропуска (появляется только после первого нажатия)
    if skip_prompt_active:
        button at skip_prompt_fade:
            align (0.5, 0.93)
            background Solid("#080c16cc")
            hover_background Solid("#141e32dd")
            padding (32, 12)
            action Return("skipped")

            text _("Нажмите Пробел или Клик ещё раз для пропуска"):
                font "WDXLLubrifontTC-Regular.ttf"
                size 22
                color "#cfe2ff"
                hover_color "#ffffff"
                align (0.5, 0.5)

# ---------------------------------------------
# ПОДМЕНЮ ПОВТОРНОГО ПРОСМОТРА ТИТРОВ (ВОСПОМИНАНИЯ)
# ---------------------------------------------

screen credits_recollection_menu():
    tag menu
    modal True
    zorder 25
    use main_menu_background

    key "game_menu" action ShowMenu("memory_recollection")

    $ vol1_open = persistent.unlock_gallery or getattr(persistent, "credits_vol1_unlocked", False) or getattr(persistent, "cutcene_vol_1_end_unlocked", False) or getattr(persistent, "chapter_5_unlocked", False)
    $ vol2_open = persistent.unlock_gallery or getattr(persistent, "credits_vol2_unlocked", False) or getattr(persistent, "main_menu_level", 0) >= 7

    frame:
        style "modern_panel"
        vbox:
            style "modern_vbox"
            label _("Титры") style "modern_title_label"

            vbox:
                xalign 0.5
                spacing 25

                textbutton (_("Том 1 — Синяя Ворона") if vol1_open else _("Том 1 — Закрыто")):
                    sensitive vol1_open
                    action Replay("credits_replay_vol1", locked=False)
                    style "modern_button"
                    xsize 560

                textbutton (_("Том 2 — Резонирующий Диссонанс") if vol2_open else _("Том 2 — Закрыто")):
                    sensitive vol2_open
                    action Replay("credits_replay_vol2", locked=False)
                    style "modern_button"
                    xsize 560

            null height 30
            textbutton _("Назад") action ShowMenu("memory_recollection") style "modern_back_button"
