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

style chapter_subtitle_style:
    color "#CCCCCC"  # Чуть сероватый или белый, как хотите
    size 30          # Размер меньше основного заголовка
    xalign 0.5
    top_margin 10    # Отступ сверху от названия главы
    italic True      # Можно сделать курсивом (опционально)

# Определение самого экрана
# Он принимает два параметра: chapter_text и title_text
screen chapter_screen(chapter_text, title_text, subtitle_text=None):
 
    # modal True делает экран модальным. Это значит, что игрок не сможет
    # взаимодействовать с элементами под этим экраном (например, прокликивать диалог).
    modal True
    

    # on "show" определяет действие, которое выполнится при показе экрана.
    # Здесь мы запускаем таймер на 5 секунды.
    # По истечении времени экран скроется с анимацией растворения (dissolve).
    #on "show":
    timer 5.0 action [Hide('chapter_screen', transition=dissolve), Return()]
    
    # Добавляем сплошной черный фон на весь экран
    frame:
        xfill True      # Заполнить ширину (если нужен фон на весь экран)
        yfill True      # Заполнить высоту
        background "#000000" # Черный фон (или "#000000cc" для прозрачности)
        padding (50, 50)

    # vbox - это контейнер, который располагает элементы вертикально.
    # Мы центрируем его по горизонтали и вертикали.
    vbox:
        align (0.5, 0.5)

        # Первый текст, использующий параметр chapter_text и свой стиль
        text chapter_text style "chapter_number_style"

        # Второй текст, использующий параметр title_text и свой стиль
        text title_text style "chapter_title_style"

        if subtitle_text:
                text subtitle_text style "chapter_subtitle_style"