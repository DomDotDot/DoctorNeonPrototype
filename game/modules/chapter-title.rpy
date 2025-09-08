# Определяем стили для нашего текста, чтобы легко менять его вид
style chapter_number_style:
    # Белый цвет, размер 40, выравнивание по центру
    color "#FFFFFF"
    size 40
    xalign 0.5
    # Отступ снизу, чтобы отделить от названия главы
    bottom_margin 20

style chapter_title_style:
    # Белый цвет, размер 60 (крупнее), выравнивание по центру
    color "#FFFFFF"
    size 60
    xalign 0.5

# Определение самого экрана
# Он принимает два параметра: chapter_text и title_text
screen chapter_screen(chapter_text, title_text):
 
    # modal True делает экран модальным. Это значит, что игрок не сможет
    # взаимодействовать с элементами под этим экраном (например, прокликивать диалог).
    modal True
    

    # on "show" определяет действие, которое выполнится при показе экрана.
    # Здесь мы запускаем таймер на 4 секунды.
    # По истечении времени экран скроется с анимацией растворения (dissolve).
    #on "show":
    timer 5.0 action [Hide('chapter_screen', transition=dissolve), Return()]
    
    # Добавляем сплошной черный фон на весь экран
    frame:
        xalign 0.5
        yalign 0.5
        background "#000000ff" # Слегка прозрачный фон
        padding (50, 50)

    # vbox - это контейнер, который располагает элементы вертикально.
    # Мы центрируем его по горизонтали и вертикали.
    vbox:
        xalign 0.5
        yalign 0.5

        # Первый текст, использующий параметр chapter_text и свой стиль
        text chapter_text style "chapter_number_style"

        # Второй текст, использующий параметр title_text и свой стиль
        text title_text style "chapter_title_style"