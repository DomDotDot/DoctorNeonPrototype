default active_bio_char = None # Текущий выбранный персонаж в меню

# ОГАНЕСОН
default oga_bio = CharBio(
    id="oga",
    name="Опекунша",
    real_name="Оганессон (Oganesson)",
    gender="♀",
    height="180cm",
    age="33",
    role="Antagonist, Head of Sect, Politician",
    element="Element No. 118 (Oganesson)",
    hair="Black, Hime Cut, Long",
    eyes="Violet",
    clothes="Formal Shirt, Trench Coat",
    personality="Ambitious, Cold-hearted, Idealist",
    aliases=["Тетя", "Опекунша", "{color=#c0392b}Trustee{/color}"],
    engages_in=["Arson", "Kidnapping", "{color=#c0392b}Murder{/color}", "Memory Alteration"],
    desc_stages=[
        "Теневая фигура, стоящая за событиями в жизни Неона.", # Уровень 1
        "Представитель древнего 'Клана Завоевателей'. Обладает железной волей.", # Уровень 2
        "Организовала похищение Неона. Её цель — использовать 'Вакуум' для стабилизации Тумана." # Уровень 3
    ],
    image_tag="oga_prof_img"
)

# СЕРАФИНА
default sera_bio = CharBio(
    id="sera",
    name="Идол",
    real_name="Серафина (Seraphina)",
    gender="♀ (⚥)",
    height="169cm",
    age="Unknown",
    role="Idol, Singer, Virtual Avatar",
    element="Element No. 86 (Radon)",
    hair="Blond, Twin Tails",
    eyes="Glowing Red",
    clothes="Choker, Corset, Dress",
    personality="Energetic, Charismatic, {color=#c0392b}Yandere{/color}",
    aliases=["Sera", "Star"],
    engages_in=["Stalking", "Hypnotism", "{color=#c0392b}Attempted Murder{/color}"],
    desc_stages=[
        "Супер-популярный идол города Veritas. Сияющая и добрая звезда.",
        "Проявляет странный, одержимый интерес к Неону.",
        "На самом деле... (тут раскрывается спойлер)."
    ],
    image_tag="sera_prof_img"
)

#TODO Аргон
default argon_bio = CharBio(
    id="sera",
    name="Идол",
    real_name="Серафина (Serafina)",
    gender="♂ (⚥)",
    height="169cm",
    age="Unknown",
    role="Idol, Singer, Virtual Avatar",
    element="Element No. 86 (Radon)",
    hair="Blond, Twin Tails",
    eyes="Glowing Red",
    clothes="Choker, Corset, Dress",
    personality="Energetic, Charismatic, {color=#c0392b}Yandere{/color}",
    aliases=["Sera", "Star"],
    engages_in=["Stalking", "Hypnotism", "{color=#c0392b}Attempted Murder{/color}"],
    desc_stages=[
        "Супер-популярный идол города Veritas. Сияющая и добрая звезда.",
        "Проявляет странный, одержимый интерес к Неону.",
        "На самом деле... (тут раскрывается спойлер)."
    ],
    image_tag="sera_prof_img"
)

# Список всех профилей
default all_bios = [oga_bio, sera_bio]