# Определение персонажей игры.
    # Ключевые персонажи
define neon = Character(_('Неон'), color="#1f4bc4", image="neon", ctc="ctc_neon", ctc_position="nestled", callback = name_callback, cb_name = "neon")
layeredimage neon:
    at sprite_highlight('neon')


define argon = Character("[argon_display_name]", color="#457632", image="argon", dynamic=True, what_slow_cps_multiplier=0.65, ctc="ctc_blink", ctc_position="nestled", callback = name_callback, cb_name = "argon")

define marcus = Character(_('Маркус'), color="#967230", image="marcus", what_slow_cps_multiplier=0.85, ctc="ctc_blink", ctc_position="nestled", callback = name_callback, cb_name = "marcus")
layeredimage marcus:
    at sprite_highlight('marcus')


define alex = Character(_('Алекс'), color="#b41f5d", image="alex", what_slow_cps_multiplier=1.25, ctc="ctc_blink", ctc_position="nestled")

define oganesson_display_name = _("Опекунша")
define oganesson = Character("[oganesson_display_name]", color="#663399", image="oganesson", dynamic=True, what_slow_cps_multiplier=0.75, ctc="ctc_blink", ctc_position="nestled")
define oganesson_young = Character(_('Тетя-гостья'), color="#390482", image="oganesson", what_slow_cps_multiplier=0.80, ctc="ctc_blink", ctc_position="nestled") # Имя скрыто для Неон

    # Вспомогательные персонажи
define narrator = Character(None, what_size=25, ctc="ctc_blink", ctc_position="nestled", callback = name_callback, cb_name = None)
define narrator_nvl = Character(None, kind=nvl)
define dashboard = Character(_('Приборная Панель') , image="fuel_warning")

define unknown = Character(_('Неизвестный'), color="#ffffff", ctc="ctc_blink", ctc_position="nestled")
define unknown_f = Character(_('Неизвестная'), color="#ffffff", ctc="ctc_blink", ctc_position="nestled")
define unknown_char = Character("???", color="#ffffff")
define fcs = Character(_('АБСУ'), color="#a30e0e", voice_tag="fcs")

    # Второстепенные персонажи
define hans = Character(_('Ханс'), color="#7a7a7a", image="hans", ctc="ctc_blink", ctc_position="nestled")

define ceo = Character(_('Г-н Бауманн'), color="#305a96", image="ceo_boss", ctc="ctc_blink", ctc_position="nestled") # Генеральный директор
define cro = Character(_('Д-р Грубенманн'), color="#753636", image="cro_boss", ctc="ctc_blink", ctc_position="nestled") # Руководитель исследований

define anna = Character(_('Анна'), color="#d96411", image="anna", ctc="ctc_blink", ctc_position="nestled")
define sophie = Character(_('Софи'), color="#d1c682", image="sophie", ctc="ctc_blink", ctc_position="nestled")

define headteacher = Character(_('Завуч'), color="#808080", image="headteacher", ctc="ctc_blink", ctc_position="nestled")

define guts = Character(_('Гатс'), color="#8b4513", image="guts", what_slow_cps_multiplier=0.70, ctc="ctc_blink", ctc_position="nestled")
define rico = Character(_('Рико'), color="#a56a44")
define boss = Character(_('Босс'), color="#b22222")

define akane = Character(_('Мама'), color="#e87a90", image="akane", ctc="ctc_blink", ctc_position="nestled")
define father = Character(_('Папа'), color="#5a7a8d", ctc="ctc_blink", ctc_position="nestled")
