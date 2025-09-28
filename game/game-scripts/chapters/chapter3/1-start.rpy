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
    default can_provoke = False

    default has_torn_sheet = False
    default has_keycard = False
    default inspected_keycard_barcode = False
    default found_code_clue = False
    default chemlab_door_unlocked = False
    default has_sugar = False
    default has_yeast = False
    default has_equipment_idea = False

            

    $ hall_examined = False
    $ locker_broken = False
    $ has_motor_oil = False
    $ factory_gate_open = False
    $ inspected_gate_mechanism = False
    $ tried_to_talk_to_thugs = False

    $ provocation_count = 0
    $ bouncer_talk_count = 0
    $ thugs_listen_count = 0
    $ knows_bouncer_secret = False
    $ can_provoke = False

    $ has_torn_sheet = False
    $ has_keycard = False
    $ inspected_keycard_barcode = False
    $ found_code_clue = False
    $ chemlab_door_unlocked = False
    $ has_sugar = False
    $ has_yeast = False
    $ has_equipment_idea = False


    # Неон в холле завода.
    scene bg chapter_3_start-mainhall with Dissolve(5.0) # Фон: грязный, заброшенный холл завода
    queue music "music/BGM/Revpad.ogg" fadein 5.0 loop volume 0.5
    show neon neutral at right with dissolve

    narrator """
    Огромный холл. Высокие, закопченные потолки, с которых свисали обрывки проводов и ржавые цепи.

    Воздух был спертым, пахло сыростью, машинным маслом и пылью, которую не тревожили годами. Это место было мертвым, но его кости все еще стонали на ветру.

    Единственный выход – массивные двойные двери – был заблокирован. Не замком. Человеком.

    Он был огромен. Гора мышц в грязной майке, с лицом, которое, казалось, было высечено из гранита тупым зубилом.
    
    Он стоял, скрестив руки на груди, и молча смотрел в стену. Живая стена, преграждающая мне путь к свободе.
    """
    
    show guts neutral at left with dissolve
    guts "Осмотрелась, ученая? Хорошо. Босс скоро будет."
    
    neon "Здесь... своеобразная атмосфера..."

    guts "Ничего. Мы привыкали и ты привыкнешь. Если доживешь. Жди здесь до следующих приказов. И не делай глупостей."

    narrator """
    Голос Гатса прозвучал как смертный приговор.

    Гатс вскоре обернулся и ушел за какую-то металлическую дверь, открыв её ключ-карточкой, оставив меня одну с этим исполином.
    """

    hide guts neutral with dissolve

    narrator """
    'Жди здесь'. В этой клетке. Я знала, что это ловушка.
    
    Ожидание здесь означало конец. Мне нужно было действовать. И действовать сейчас.
    """
return