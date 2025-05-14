# Определение персонажей игры.
    # Ключевые персонажи
define neon = Character('Неон', color="#1f4bc4", image="neon")
define mark = Character('Марк', color="#967230", image="mark")
define alex = Character('Алекс', color="#b41f5d", image="alex")

    # Вспомогательные персонажи
define narrator = Character(None, what_size=15)
define narrator_nvl = Character(None, kind=nvl)

define unknown = Character('Неизвестный', color="#ffffff")
define unknown_f = Character('Неизвестная', color="#ffffff")
define fcs = Character('Система Управление Полётом', color="#a30e0e")

define petrovich = Character('Петрович', color="#7a7a7a", image="petrovich")

define ceo = Character('Господин Бауманн (CEO)', color="#305a96", image="ceo_boss") # Генеральный директор
define cro = Character('Доктор Захаров (CRO)', color="#753636", image="cro_boss") # Руководитель исследований

define bully1 = Character('Задира 1', color="#b32424", image="bully")
define bully2 = Character('Задира 2', color="#b32424", image="bully")


# Кастомные стили
style thoughts:
    italic True
style yell:
    size 40

init:
    transform flip:
        xzoom -1.0
    transform restore_flip:
        xzoom 1.0