import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# Фиксируем seed для красивой и предсказуемой генерации цветов
random.seed(42)

# Конфигурация из Ren'Py
SCREEN_W, SCREEN_H = 1920, 1080
TEXTBOX_W = 1560
TEXTBOX_H = 260
TEXTBOX_YALIGN = 0.92

# Рендерим в 2x разрешении для идеального сглаживания (Supersampling)
SCALE = 2
W = TEXTBOX_W * SCALE
H = TEXTBOX_H * SCALE


def get_stylized_frame_polygon(x1, y1, x2, y2, s=SCALE):
    """
    Создаёт непрямоугольный контур диалогового окна:
    гранёные боковые крылья, вогнутые резные углы и фигурные выступы.
    """
    mid_y = (y1 + y2) / 2.0
    cut = 28 * s        # скос угла
    wing = 22 * s       # боковой выступ по центру
    step = 10 * s       # декоративная ступенька
    dip = 6 * s         # плавный изгиб верхней грани

    pts = [
        # Верхняя грань (с декоративными уступами по краям)
        (x1 + cut, y1 + step),
        (x1 + cut * 2.2, y1 + step),
        (x1 + cut * 2.6, y1),
        ((x1 + x2) / 2, y1 + dip),
        (x2 - cut * 2.6, y1),
        (x2 - cut * 2.2, y1 + step),
        (x2 - cut, y1 + step),

        # Правый верхний резной угол и боковое крыло
        (x2 - cut * 0.4, y1 + cut * 0.6),
        (x2, y1 + cut * 1.2),
        (x2 + wing, mid_y),

        # Правый нижний угол
        (x2, y2 - cut * 1.2),
        (x2 - cut * 0.4, y2 - cut * 0.5),
        (x2 - cut, y2 - step * 0.6),
        (x2 - cut * 2.2, y2 - step * 0.6),
        (x2 - cut * 2.6, y2),

        # Нижняя грань
        (x1 + cut * 2.6, y2),
        (x1 + cut * 2.2, y2 - step * 0.6),
        (x1 + cut, y2 - step * 0.6),

        # Левый нижний угол и левое боковое крыло
        (x1 + cut * 0.4, y2 - cut * 0.5),
        (x1, y2 - cut * 1.2),
        (x1 - wing, mid_y),
        (x1, y1 + cut * 1.2),
        (x1 + cut * 0.4, y1 + cut * 0.6),
    ]
    return pts


def draw_frame_background(w, h):
    """Создаёт фигурную основу диалогового окна с градиентом и филигранной рамкой."""
    base = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    # Отступы внутри 1560x260, чтобы свисающие цветы и боковые крылья не обрезались
    margin_x = 78 * SCALE
    margin_top = 34 * SCALE
    margin_bottom = 18 * SCALE
    x1, y1 = margin_x, margin_top
    x2, y2 = w - margin_x, h - margin_bottom

    outer_poly = get_stylized_frame_polygon(x1, y1, x2, y2, SCALE)
    inner_poly = get_stylized_frame_polygon(
        x1 + 7 * SCALE, y1 + 7 * SCALE, x2 - 7 * SCALE, y2 - 7 * SCALE, SCALE
    )

    # 1. Мягкая внешняя тень-свечение
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.polygon(outer_poly, fill=(8, 18, 42, 210))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10 * SCALE))
    base = Image.alpha_composite(base, shadow)

    # 2. Градиентная заливка окна (глубокий ночной сапфир -> полупрозрачный индиго)
    grad = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(grad)
    for y in range(int(y1), int(y2) + 1):
        t = (y - y1) / max(1, (y2 - y1))
        r = int(12 + 16 * (1 - t) + 8 * math.sin(t * math.pi))
        g = int(24 + 28 * (1 - t) + 14 * math.sin(t * math.pi))
        b = int(52 + 46 * (1 - t) + 20 * math.sin(t * math.pi))
        alpha = int(218 + 20 * t)
        g_draw.line([(x1 - 30 * SCALE, y), (x2 + 30 * SCALE, y)], fill=(r, g, b, alpha))

    # Маска по фигурному многоугольнику
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).polygon(outer_poly, fill=255)

    frame_fill = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    frame_fill.paste(grad, (0, 0), mask)

    # 3. Нежное внутреннее боке / свечение по краям внутри окна
    bokeh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(bokeh)
    for _ in range(45):
        bx = random.randint(int(x1 + 20 * SCALE), int(x2 - 20 * SCALE))
        by = random.randint(int(y1 + 10 * SCALE), int(y2 - 10 * SCALE))
        br = random.randint(8 * SCALE, 32 * SCALE)
        b_draw.ellipse(
            (bx - br, by - br, bx + br, by + br),
            fill=(110, 175, 255, random.randint(8, 22)),
        )
    bokeh = bokeh.filter(ImageFilter.GaussianBlur(6 * SCALE))
    frame_fill_masked = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    frame_fill_masked.paste(Image.alpha_composite(frame_fill, bokeh), (0, 0), mask)
    base = Image.alpha_composite(base, frame_fill_masked)

    # 4. Двойная декоративная рамка (серебристо-голубая и жемчужная филигрань)
    border_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d_draw = ImageDraw.Draw(border_layer)

    # Внешний контур
    d_draw.line(outer_poly + [outer_poly[0]], fill=(150, 205, 255, 245), width=3 * SCALE, joint="curve")
    # Внутренний тонкий контур
    d_draw.line(inner_poly + [inner_poly[0]], fill=(210, 232, 255, 140), width=1 * SCALE, joint="curve")

    # Декоративные ромбы на боковых крыльях и внизу
    mid_y = (y1 + y2) / 2.0
    for cx_orn in [x1 - 8 * SCALE, x2 + 8 * SCALE]:
        r_d = 6 * SCALE
        diamond = [(cx_orn, mid_y - r_d), (cx_orn + r_d, mid_y), (cx_orn, mid_y + r_d), (cx_orn - r_d, mid_y)]
        d_draw.polygon(diamond, fill=(195, 228, 255, 230), outline=(90, 150, 230, 255))

    base = Image.alpha_composite(base, border_layer)
    return base, (x1, y1, x2, y2)


def draw_hydrangea_leaf(draw, cx, cy, angle, size, dark=False):
    """Рисует зубчатый лист гортензии с прожилками."""
    pts = []
    steps = 28
    for i in range(steps + 1):
        t = -math.pi / 2 + (math.pi * i / steps)
        u = math.cos(t)
        # Зубчики по краю листа
        serration = 1.0 + 0.08 * math.sin(i * 4.5) if 2 < i < steps - 2 else 1.0
        px = size * (u ** 0.75)
        py = size * 0.48 * math.sin(t) * (u ** 0.4) * serration

        rx = cx + px * math.cos(angle) - py * math.sin(angle)
        ry = cy + px * math.sin(angle) + py * math.cos(angle)
        pts.append((rx, ry))

    if dark:
        fill_col = (22, 62, 68, 240)
        outline_col = (14, 42, 48, 255)
        vein_col = (45, 100, 102, 190)
    else:
        fill_col = (36, 94, 92, 245)
        outline_col = (20, 58, 62, 255)
        vein_col = (78, 148, 140, 200)

    draw.polygon(pts, fill=fill_col, outline=outline_col)

    # Центральная прожилка
    tip_x = cx + size * 0.92 * math.cos(angle)
    tip_y = cy + size * 0.92 * math.sin(angle)
    draw.line([(cx, cy), (tip_x, tip_y)], fill=vein_col, width=max(1, int(1.2 * SCALE)))


def draw_hydrangea_floret(draw, cx, cy, size, rotation, shade="mid"):
    """
    Рисует отдельный цветок синей гортензии (4 характерных чашелистика + бутон в центре).
    """
    palettes = {
        "deep": (
            (42, 82, 185, 250),   # основной цвет лепестка
            (65, 112, 215, 255),  # внутренний блик
            (25, 50, 130, 255),   # контур и прожилки
        ),
        "mid": (
            (74, 134, 238, 252),
            (115, 175, 252, 255),
            (45, 90, 185, 255),
        ),
        "light": (
            (118, 182, 255, 255),
            (175, 218, 255, 255),
            (72, 130, 215, 255),
        ),
        "violet_blue": (
            (88, 112, 235, 250),
            (132, 158, 252, 255),
            (55, 72, 175, 255),
        ),
    }
    base_col, inner_col, line_col = palettes[shade]

    # 4 лепестка гортензии
    for k in range(4):
        pet_angle = rotation + k * (math.pi / 2.0) + random.uniform(-0.08, 0.08)
        pet_size = size * random.uniform(0.92, 1.06)

        outer_pts = []
        inner_pts = []
        steps = 16
        for i in range(steps + 1):
            t = -math.pi / 2 + (math.pi * i / steps)
            u = max(0.0, math.cos(t))
            # Форма лепестка гортензии (округло-заострённая на конце)
            lx = pet_size * (0.10 + 0.90 * (u ** 0.65))
            ly = pet_size * 0.64 * math.sin(t) * (u ** 0.32)

            rx = cx + lx * math.cos(pet_angle) - ly * math.sin(pet_angle)
            ry = cy + lx * math.sin(pet_angle) + ly * math.cos(pet_angle)
            outer_pts.append((rx, ry))

            # Внутренний мягкий градиентный слой лепестка
            ix = cx + (lx * 0.68) * math.cos(pet_angle) - (ly * 0.62) * math.sin(pet_angle)
            iy = cy + (lx * 0.68) * math.sin(pet_angle) + (ly * 0.62) * math.cos(pet_angle)
            inner_pts.append((ix, iy))

        draw.polygon(outer_pts, fill=base_col, outline=line_col)
        draw.polygon(inner_pts, fill=inner_col)

        # Тонкая прожилка по центру лепестка
        vein_end_x = cx + pet_size * 0.72 * math.cos(pet_angle)
        vein_end_y = cy + pet_size * 0.72 * math.sin(pet_angle)
        draw.line([(cx, cy), (vein_end_x, vein_end_y)], fill=line_col, width=max(1, int(0.8 * SCALE)))

    # Центр цветка (маленькая бусинка-соцветие)
    r_shadow = size * 0.19
    draw.ellipse((cx - r_shadow, cy - r_shadow, cx + r_shadow, cy + r_shadow), fill=line_col)
    r_core = size * 0.12
    draw.ellipse((cx - r_core, cy - r_core, cx + r_core, cy + r_core), fill=(225, 242, 255, 255))


def draw_hydrangea_cluster(draw, cx, cy, rx, ry, count=36):
    """Рисует пышную шапку синей гортензии с объёмом от темных нижних к светлым верхним цветкам."""
    pts = []
    for _ in range(count):
        ang = random.uniform(0, 2 * math.pi)
        dist = math.sqrt(random.uniform(0, 1))
        px = cx + math.cos(ang) * rx * dist
        py = cy + math.sin(ang) * ry * dist
        pts.append((px, py, dist))

    # Сортируем от краёв к центру, чтобы центральные светлые соцветия лежали поверх
    pts.sort(key=lambda item: item[2], reverse=True)

    for px, py, dist in pts:
        if dist > 0.72:
            shade = random.choice(["deep", "violet_blue"])
            f_size = random.uniform(11, 14) * SCALE
        elif dist > 0.38:
            shade = random.choice(["mid", "violet_blue", "mid"])
            f_size = random.uniform(12, 16) * SCALE
        else:
            shade = random.choice(["light", "mid"])
            f_size = random.uniform(13, 17) * SCALE

        draw_hydrangea_floret(draw, px, py, f_size, random.uniform(0, math.pi), shade)


def draw_hanging_garland(draw, start_x, start_y, length, sway_dir=1):
    """
    Рисует свисающую вниз ветвь гортензии (гирлянду из соцветий, бутонов и листьев).
    """
    steps = 12
    spine = []
    for i in range(steps + 1):
        t = i / steps
        # Изгиб свисающей лозы
        x = start_x + sway_dir * math.sin(t * math.pi * 1.15) * (12 * SCALE)
        y = start_y + t * length
        spine.append((x, y))

    # Стебель
    draw.line(spine, fill=(32, 78, 76, 235), width=int(2.2 * SCALE), joint="curve")

    # Листья вдоль свисающей ветви
    for i in range(1, steps, 2):
        sx, sy = spine[i]
        t = i / steps
        leaf_size = (18 * (1.0 - 0.45 * t)) * SCALE
        side = 1 if (i % 4 == 1) else -1
        leaf_angle = math.pi / 2 + side * 0.65
        draw_hydrangea_leaf(draw, sx, sy, leaf_angle, leaf_size, dark=(i % 3 == 0))

    # Каскад цветов гортензии, уменьшающихся к кончику свисающей лозы
    for i in range(1, steps + 1):
        sx, sy = spine[i]
        t = i / steps
        sub_count = max(1, int(5 * (1.0 - t * 0.75)))
        spread = (18 * (1.0 - t * 0.65)) * SCALE

        for _ in range(sub_count):
            fx = sx + random.uniform(-spread, spread)
            fy = sy + random.uniform(-spread * 0.5, spread * 0.5)
            f_size = (14.5 * (1.0 - t * 0.45)) * SCALE
            shade = random.choice(["deep", "mid", "light", "violet_blue"])
            draw_hydrangea_floret(draw, fx, fy, f_size, random.uniform(0, math.pi), shade)

    # Маленькие свисающие капли росы / бутоны в самом низу лозы
    end_x, end_y = spine[-1]
    for k in range(1, 3):
        by = end_y + k * 8 * SCALE
        r_bud = (4.5 - k * 1.1) * SCALE
        draw.ellipse(
            (end_x - r_bud, by - r_bud, end_x + r_bud, by + r_bud),
            fill=(150, 205, 255, 240),
            outline=(55, 105, 195, 255),
        )


def generate_dialogue_box():
    # 1. Рисуем фигурное диалоговое окно
    canvas, (x1, y1, x2, y2) = draw_frame_background(W, H)

    # 2. Слой для листвы и свисающих соцветий синей гортензии
    floral_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    f_draw = ImageDraw.Draw(floral_layer)

    # --- Фоновые крупные листья по углам и сверху ---
    leaf_configs = [
        # Левый верхний угол и бок
        (x1 + 10 * SCALE, y1 + 8 * SCALE, math.pi * 0.85, 38 * SCALE, True),
        (x1 + 35 * SCALE, y1 + 4 * SCALE, -math.pi * 0.12, 34 * SCALE, False),
        (x1 + 85 * SCALE, y1 + 2 * SCALE, -math.pi * 0.05, 30 * SCALE, True),
        (x1 - 5 * SCALE, y1 + 35 * SCALE, math.pi * 0.62, 34 * SCALE, False),
        # Правый верхний угол и бок
        (x2 - 10 * SCALE, y1 + 8 * SCALE, math.pi * 0.15, 38 * SCALE, True),
        (x2 - 35 * SCALE, y1 + 4 * SCALE, -math.pi * 0.88, 34 * SCALE, False),
        (x2 - 85 * SCALE, y1 + 2 * SCALE, -math.pi * 0.95, 30 * SCALE, True),
        (x2 + 5 * SCALE, y1 + 35 * SCALE, math.pi * 0.38, 34 * SCALE, False),
    ]
    for lx, ly, lang, lsize, ldark in leaf_configs:
        draw_hydrangea_leaf(f_draw, lx, ly, lang, lsize, dark=ldark)

    # --- Свисающие вниз гирлянды (слева и справа по краям окна) ---
    # Левый каскад (3 свисающие ветви разной длины)
    draw_hanging_garland(f_draw, x1 - 8 * SCALE, y1 + 22 * SCALE, length=185 * SCALE, sway_dir=-1)
    draw_hanging_garland(f_draw, x1 + 22 * SCALE, y1 + 28 * SCALE, length=155 * SCALE, sway_dir=1)
    draw_hanging_garland(f_draw, x1 + 58 * SCALE, y1 + 14 * SCALE, length=95 * SCALE, sway_dir=-1)

    # Правый каскад (симметрично-живописный)
    draw_hanging_garland(f_draw, x2 + 8 * SCALE, y1 + 22 * SCALE, length=185 * SCALE, sway_dir=1)
    draw_hanging_garland(f_draw, x2 - 22 * SCALE, y1 + 28 * SCALE, length=155 * SCALE, sway_dir=-1)
    draw_hanging_garland(f_draw, x2 - 58 * SCALE, y1 + 14 * SCALE, length=95 * SCALE, sway_dir=1)

    # --- Пышные основные шапки синей гортензии на верхних углах ---
    # Левая угловая композиция
    draw_hydrangea_cluster(f_draw, x1 + 16 * SCALE, y1 + 16 * SCALE, rx=42 * SCALE, ry=28 * SCALE, count=34)
    draw_hydrangea_cluster(f_draw, x1 + 72 * SCALE, y1 + 10 * SCALE, rx=32 * SCALE, ry=20 * SCALE, count=22)
    draw_hydrangea_cluster(f_draw, x1 + 122 * SCALE, y1 + 8 * SCALE, rx=22 * SCALE, ry=14 * SCALE, count=12)

    # Правая угловая композиция
    draw_hydrangea_cluster(f_draw, x2 - 16 * SCALE, y1 + 16 * SCALE, rx=42 * SCALE, ry=28 * SCALE, count=34)
    draw_hydrangea_cluster(f_draw, x2 - 72 * SCALE, y1 + 10 * SCALE, rx=32 * SCALE, ry=20 * SCALE, count=22)
    draw_hydrangea_cluster(f_draw, x2 - 122 * SCALE, y1 + 8 * SCALE, rx=22 * SCALE, ry=14 * SCALE, count=12)

    # 3. Мягкая тень от цветов на само диалоговое окно (для 3D-объёма)
    flower_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    alpha_mask = floral_layer.split()[3]
    black_img = Image.new("RGBA", (W, H), (5, 12, 30, 150))
    flower_shadow.paste(black_img, (3 * SCALE, 5 * SCALE), alpha_mask)
    flower_shadow = flower_shadow.filter(ImageFilter.GaussianBlur(5 * SCALE))

    canvas = Image.alpha_composite(canvas, flower_shadow)
    canvas = Image.alpha_composite(canvas, floral_layer)

    # Уменьшаем в 2 раза до целевого размера 1560x260 с премиальным сглаживанием LANCZOS
    resample_mode = getattr(Image, "Resampling", Image).LANCZOS
    final_textbox = canvas.resize((TEXTBOX_W, TEXTBOX_H), resample=resample_mode)
    return final_textbox


def create_renpy_preview(textbox_img):
    """Создаёт превью 1920x1080 с размещением окна по gui.textbox_yalign = 0.92."""
    preview = Image.new("RGBA", (SCREEN_W, SCREEN_H), (18, 26, 44, 255))
    p_draw = ImageDraw.Draw(preview)

    # Atmospheric фон для демонстрации прозрачности
    for y in range(SCREEN_H):
        t = y / SCREEN_H
        r = int(20 + 25 * t)
        g = int(32 + 38 * t)
        b = int(58 + 55 * t)
        p_draw.line([(0, y), (SCREEN_W, y)], fill=(r, g, b, 255))

    # Вычисляем координаты в Ren'Py при xalign=0.5 и yalign=0.92
    pos_x = int((SCREEN_W - TEXTBOX_W) * 0.5)
    pos_y = int((SCREEN_H - TEXTBOX_H) * TEXTBOX_YALIGN)

    preview.alpha_composite(textbox_img, (pos_x, pos_y))

    # Пример текста внутри окна
    try:
        font_name = ImageFont.truetype("arialbd.ttf", 30)
        font_text = ImageFont.truetype("arial.ttf", 26)
    except IOError:
        font_name = ImageFont.load_default()
        font_text = ImageFont.load_default()

    text_x = pos_x + 150
    text_y = pos_y + 52
    p_draw.text((text_x, text_y), "Айрис", fill=(155, 210, 255, 255), font=font_name)
    p_draw.text(
        (text_x, text_y + 48),
        "«Синие гортензии расцветают даже в самую тихую дождливую ночь...»",
        fill=(235, 244, 255, 255),
        font=font_text,
    )

    return preview


if __name__ == "__main__":
    print("Генерация диалогового окна с синей гортензией...")
    textbox = generate_dialogue_box()
    textbox.save("textbox.png")
    print("Сохранено: textbox.png (1560x260, прозрачный фон)")

    preview = create_renpy_preview(textbox)
    preview.save("preview_1920x1080.png")
    print("Сохранено: preview_1920x1080.png (превью на экране 1920x1080)")