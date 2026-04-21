# ---------------------------------------------------------
# 1. ПАЛИТРА ЦВЕТОВ
# ---------------------------------------------------------
init python:
    # Ключевые
    c_neon      = "#1f4bc4"
    c_argon     = "#457632" # Борис
    c_radon     = "#c04547" # Нари, Серафина
    c_helium    = "#ffffffff"
    c_xenon     = "#1f90c4"
    c_krypton   = "#b41f1f"
    c_marcus    = "#967230"
    c_alex      = "#b41f5d"
    
    # Опекуны и семья
    c_oganesson = "#663399" # Опекунша
    c_ogan_young= "#390482" # Тетя-гостья
    c_akane     = "#e87a90" # Мама
    c_father    = "#5a7a8d"
    
    # Второстепенные и Эпизодические
    c_celeste   = "#7f9ae4ff"
    c_lily      = "#c16a19"
    c_seraphina = "#F2DBBB"
    c_hans      = "#7a7a7a"
    c_ceo       = "#305a96"
    c_cro       = "#753636"
    c_anna      = "#d96411"
    c_sophie    = "#d1c682"
    c_headteach = "#808080"
    c_guts      = "#8b4513"
    c_rico      = "#a56a44"
    c_boss      = "#b22222"
    
    # Студенты
    c_student1  = "#d4ad4b" # Amy / Student1
    c_student2  = "#33dad4" # Carol / Student2
    c_student3  = "#d1289e" # Mika / Student3
    c_student4  = "#bc040d" # Clara / Student4
    
    # Учителя и прочие
    c_meryl     = "#e87a90" # Мэрил Кендрик
    c_akari     = "#1885c8" # Убрал 'fd' на конце, hex д.б. 6 или 8 символов
    c_kai       = "#5d19c9" # Кай Ито
    c_nari      = "#863b97"
    
    # Интерфейс / Неизвестные
    c_white     = "#ffffff"
    c_fcs       = "#a30e0e"



# ---------------------------------------------------------
# 2. ШАБЛОНЫ (НАСЛЕДОВАНИЕ)
# ---------------------------------------------------------

# Базовый шаблон для ВСЕХ персонажей (обычные диалоги)
define base = Character(None,
    ctc="ctc_blink",
    ctc_position="nestled",
    what_slow_cps_multiplier=1.0,
    callback=name_callback
)

# Шаблон для ключевых персонажей (пока пуст)
define main = Character(kind=base,
)



# --- ЭЛЕМЕНТЫ ---

define neon = Character(_('Неон'),
    kind=base,
    image="neon",
    color=c_neon, 
    ctc="ctc_neon",
    cb_name="neon"
)

default argon_display_name = "???"
define argon = Character("[argon_display_name!t]", 
    kind=base, 
    image="argon", 
    color=c_argon, 
    what_slow_cps_multiplier=0.65, 
    cb_name="argon"
)

default oganesson_display_name = "Опекунша"
define oganesson = Character("[oganesson_display_name!t]",
    kind=base,
    image="oganesson",
    color=c_oganesson, 
    what_slow_cps_multiplier=0.75,
    ctc="ctc_oganesson",
    cb_name="oganesson"
)
define oganesson_young = Character(_('Тетя-гостья'),
    kind=base,
    image="oganesson",
    color=c_ogan_young, 
    what_slow_cps_multiplier=0.80,
    ctc="ctc_oganesson",
    cb_name="oganesson"
)

define radon = Character(_('Радон'),
    kind=base,
    image="nari",
    color=c_radon,
    cb_name="nari"
)

define helium = Character(_('Гелий'),
    kind=base,
    image="helium",
    color=c_helium,
    cb_name="helium"
)

define krypton = Character(_('Криптон'),
    kind=base,
    image="krypton",
    color=c_krypton,
    cb_name="krypton"
)

define xenon = Character(_('Ксенон'),
    kind=base,
    image="xenon",
    color=c_xenon,
    cb_name="xenon"
)



# --- Ключевые ---

# --- Семья и Близкие ---

define akane = Character(_('Мама'),
    kind=base,
    image="akane",
    color=c_akane,
    cb_name="akane"
)

define celeste = Character(_('Селестия'),
    kind=base,
    image="celeste",
    color=c_celeste,
    ctc="ctc_celeste",
    cb_name="celeste"
)

# --- Гелиос ---

define marcus = Character(_('Маркус'), 
    kind=base,
    image="marcus",
    color=c_marcus, 
    what_slow_cps_multiplier=0.85,
    cb_name="marcus"
)

define alex = Character(_('Алекс'),
    kind=base,
    image="alex",
    color=c_alex, 
    what_slow_cps_multiplier=1.11,
    cb_name="alex"
)
    
# --- Веритас-сити ---

define lily = Character(_('Лили'),
    kind=base,
    image="lily",
    color=c_lily,
    cb_name="lily"
)

define seraphina = Character(_('Серафина'),
    kind=base,
    image="seraphina",
    color=c_seraphina, 
    what_slow_cps_multiplier=1.11,
    ctc="ctc_seraphina",
    cb_name="seraphina"
)

define nari = Character(_('Нари'),
    kind=base,
    image="nari",
    color=c_nari,
    ctc="ctc_nari",
    cb_name="nari"
)



# --- Вспомогательные и Сюжетные ---

# --- Семья и Опекуны ---
define father = Character(_('Папа'), kind=base, color=c_father)

# --- Гелиос и Цюрих ---
define hans = Character(_('Ханс'), kind=base, image="hans", color=c_hans, cb_name="hans")
define anna = Character(_('Анна'), kind=base, image="anna", color=c_anna, cb_name="anna")
define sophie = Character(_('Софи'), kind=base, image="sophie", color=c_sophie, cb_name="sophie")

define ceo = Character(_('Г-н Бауманн'), kind=base, image="ceo_boss", color=c_ceo)
define cro = Character(_('Д-р Грубенманн'), kind=base, image="cro_boss", color=c_cro)

define headteacher = Character(_('Завуч'), kind=base, image="headteacher", color=c_headteach)

# --- Веритас-сити ---
define meryl = Character(_('Мэрил Кендрик'), kind=base, image="meryl", color=c_meryl, cb_name="meryl")
define akari = Character(_('Учительница Акари'), kind=base, image="akari", color=c_akari, cb_name="akari")
define kai = Character(_('Кай'), kind=base, image="kai", color=c_kai, cb_name="kai")
define illusion = Character(_('Сущность'), kind=base, image="ilusion", color=c_nari, cb_name="ilusion")


# --- Студенты ---
define student1 = Character(_('Студентка 1'), kind=base, image="amy", color=c_student1, cb_name="amy")
define amy = Character(_('Эми'), kind=base, image="amy", color=c_student1, cb_name="amy")

define student2 = Character(_('Студентка 2'), kind=base, image="carol", color=c_student2, cb_name="carol")
define carol = Character(_('Кэрол'), kind=base, image="carol", color=c_student2, cb_name="carol")

define clara = Character(_('Клара'), kind=base, image="clara", color=c_student4, cb_name="clara")

default mika_display_name = "Мика"
define mika = Character(_("[mika_display_name!t]"), kind=base, image="mika", color=c_student3, cb_name="mika")

# --- Аномик ---
define guts = Character(_('Гатс'), kind=base, image="guts", color=c_guts, what_slow_cps_multiplier=0.70, cb_name="guts")
define rico = Character(_('Рико'), kind=base, color=c_rico)
define boss = Character(_('Босс'), kind=base, color=c_boss)


# --- Системные и Неизвестные ---
define narrator = Character(None, kind=base, what_size=27.5, cb_name=None)
define narrator_nvl = Character(None, kind=nvl)

define unknown = Character(_('Неизвестный'), kind=base, color=c_white)
define unknown_f = Character(_('Неизвестная'), kind=base, color=c_white)
define unknown_char = Character("???", kind=base, color=c_white)
define fcs = Character(_('АБСУ'), color=c_fcs, voice_tag="fcs")

init python:
    def fix_chapter_names(chap_num):
        global argon_display_name, oganesson_display_name, mika_display_name
        
        if chap_num >= 4:
            argon_display_name = "Аргон"
        else:
            argon_display_name = "???"

        if chap_num >= 4.6:
            mika_display_name = "Мика Китамура"
        else:
            mika_display_name = "Мика"

        if chap_num >= 6:
            oganesson_display_name = "Оганессон"
        else:
            oganesson_display_name = "Опекунша"

# Fix names on loading old saves
label after_load:
    python:
        ret_stack = renpy.get_return_stack()
        if "_call_chapter_5_rpy" in ret_stack:
            fix_chapter_names(5)
        elif "_call_chapter_4_5_rpy_act2" in ret_stack:
            fix_chapter_names(4.6)
        elif "_call_chapter_4_5_rpy_act1" in ret_stack:
            fix_chapter_names(4.5)
        elif "_call_chapter_4_rpy" in ret_stack:
            fix_chapter_names(4)
        elif "_call_chapter_3_rpy" in ret_stack:
            fix_chapter_names(3)
        elif "_call_chapter_2_rpy" in ret_stack:
            fix_chapter_names(2)
        elif "_call_chapter_1_rpy" in ret_stack:
            fix_chapter_names(1)
    return
