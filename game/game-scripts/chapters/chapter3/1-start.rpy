label chapter3_part1_start:

    default hall_examined = False
    default locker_broken = False
    default has_motor_oil = False
    default factory_gate_open = False
    default inspected_gate_mechanism = False
    default tried_to_talk_to_thugs = False

    default provocation_count = 0
    default bouncer_talk_count = 0
    default thugs_listen_count = 0
    default knows_bouncer_secret = False

    # Новые переменные для пазла с кодом
    default has_keycard = False
    default inspected_keycard_barcode = False
    default found_code_clue = False
    default chemlab_door_unlocked = False

    # Неон в холле завода.
    # scene factory_hall_abandoned with Dissolve(1.0) # Фон: грязный, заброшенный холл завода
    # music "sounds/factory_oppressive_ambient.ogg" loop # Музыка: гнетущая, индустриальная, с гулом и скрипами
    # play sound "sounds/distant_machinery_groan.ogg" loop volume 0.3 # Звук: далекий скрежет и стоны старого завода

    narrator """
    Огромный холл. Высокие, закопченные потолки, с которых свисали обрывки проводов и ржавые цепи.

    Воздух был спертым, пахло сыростью, машинным маслом и пылью, которую не тревожили годами. Это место было мертвым, но его кости все еще стонали на ветру.

    Единственный выход – массивные двойные двери – был заблокирован. Не замком. Человеком.

    Он был огромен. Гора мышц в грязной майке, с лицом, которое, казалось, было высечено из гранита тупым зубилом.
    
    Он стоял, скрестив руки на груди, и молча смотрел в стену. Живая стена, преграждающая мне путь к свободе.
    """
    
    # Голос из интеркома
    # play sound "sounds/intercom_crackle.ogg"
    guts "Проснулась, ученая? Хорошо. Босс скоро будет. Жди здесь. И не делай глупостей."
    # play sound "sounds/intercom_crackle_off.ogg"

    narrator """
    Голос Гатса из старого динамика под потолком прозвучал как смертный приговор.

    'Жди здесь'. В этой клетке. Я знала, что это ловушка. Ожидание здесь означало конец. Мне нужно было действовать. И действовать сейчас.
    """
