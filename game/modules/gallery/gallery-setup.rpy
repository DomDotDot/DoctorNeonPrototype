init offset = -1

# Переменная для тестов: если True, открывает все картинки.
default persistent.unlock_gallery = False

init python:
    # Размеры миниатюры в меню
    gal_thumb_x = 384
    gal_thumb_y = 216
    
    class GalleryItem:
        def __init__(self, name, images_data, thumb=None):
            self.name = name
            self.images_data = []
            
            # Разбираем входные данные
            for item in images_data:
                # Если передали кортеж ("имя", "описание")
                if isinstance(item, tuple):
                    self.images_data.append(item)
                # Если передали просто строку "cg cg1_1"
                else:
                    self.images_data.append((item, "")) 
            
            # Логика миниатюры
            if thumb:
                self.thumb = thumb
            else:
                if len(self.images_data) > 0:
                    self.thumb = self.images_data[0][0]
                else:
                    self.thumb = None # Защита от пустых списков

        def get_unlocked_list(self):
            """Возвращает список (картинка, описание), которые игрок видел."""
            if persistent.unlock_gallery:
                return self.images_data
                
            unlocked = []
            for img_name, desc in self.images_data:
                # renpy.seen_image отлично работает с авто-именами
                if renpy.seen_image(img_name):
                    unlocked.append((img_name, desc))
            return unlocked

        def is_visible(self):
            if persistent.unlock_gallery:
                return True
            for img_name, _ in self.images_data:
                if renpy.seen_image(img_name):
                    return True
            return False
            
        def num_unlocked(self):
            return len(self.get_unlocked_list())
        
        def num_total(self):
            return len(self.images_data)

    gallery_items = []

    def add_cg(name, images, thumb=None):
        gallery_items.append(GalleryItem(name, images, thumb))


# --- ЗАПОЛНЕНИЕ ГАЛЕРЕИ (ПРИМЕР) ---
init python:
    # Пример 1: Просто список картинок (без описаний)
    # "cg_escape_1" - это имя image, определенное в script.rpy
    #add_cg("Побег", ["cg_escape_1", "cg_escape_2", "cg_escape_3"])

    # Пример 2: С описаниями для каждой вариации
#   add_cg("Воспоминание о лете", [
#     ("cg_summer_1", "Это был теплый день."),
#      ("cg_summer_2", "Она улыбнулась мне."),
#       ("cg_summer_kiss", "Наш первый поцелуй.")
#    ], thumb="images/thumbs/summer_thumb.png") # Кастомная миниатюра

        # Пример 2: С описаниями для каждой вариации
    add_cg("Кафетерия", [
        ("cg cg1", "В этот день кофе был особенно горьким."),
    ])

    add_cg("Доклад", [
        ("cg cg2_1", "Начало доклада."),
        ("cg cg2_3"),
        ("cg cg2_4", "Критические данные."),
        ("cg cg2_5", "Конец записи."),
    ])

    add_cg("Цюрих", [
        ("cg cg3_1"),
    ])

    add_cg("Звездочка", [
        ("cg cg4_1", "Я помню этот свет..."),
    ])

    add_cg("Уничтожен", [
        ("cg cg5_1", "Первый удар."),
        ("cg cg5_2", "Посторонний шум."),
        ("cg cg5_3", "Крах и Триумф.")
    ])

    add_cg("Воспоминания 1", [
        ("cg cg6_1"),
        ("cg cg6_2", "'Такова её природа'"),
        ("cg cg6_3"),
    ])

    add_cg("Побег", [
        ("cg cg7_1", "Беги!"),
        ("cg cg7_2", ""),
        ("cg cg7_3", "Хвост."), 
        ("cg cg7_5_1", "Блокада."),
        ("cg cg7_5", ""),
        ("cg cg7_6", ""),
        ("cg cg7_8", "Почти у цел-"),
        ("cg cg7_9", "Свет в конце тоннеля.")
    ])

    add_cg("Селестия", [
        ("cg cg8_1", "Холодная и отстраненная... как я."),
        ("cg cg8_2", "Давай сходим в Планетарий?")
    ])

    add_cg("Поездка", [
        ("cg cg9", "GPS: Маршрут перестроен."),
        ("cg cg10", "Фары разрезают тьму.")
        ])

    add_cg("Кошмар", [
        ("cg cg11_1-1", "Ты - не Алекс."),
        ("cg cg11_2", "'Её' больше нет."),
        ("cg cg11_3-1", "Звук снова победил Тишину."),
    ])

    add_cg("РАЗЫСКИВАЕТСЯ", [
        ("cg cg12_1", "Кто это?"),
        ("cg cg12_1-1", "Мой фоторобот."),
        ("cg cg12_2", "Это же... моя подруга..."),
    ])

    add_cg("Уют дома", [
        ("cg cg13_1"),
        ("cg cg13_2"),
    ])

    add_cg("Путь в Никуда", [
        ("cg cg14"),
        ("cg cg15_1"),
        ("cg cg15_2"),
    ])

    add_cg("Идиллия", [
        ("cg cg16", "Кто все эти люди...?"),
    ])

    add_cg("Завод", [
        ("cg cg17"),
        ("cg cg18"),
    ])

    add_cg("Аномик-3", [
        ("cg cg19"),
        ("cg cg20_1"),
        ("cg cg20_2", "Я не могу бросить его... только не снова."),
        ("cg cg20_3", "Вы нас не видете."),
    ])

    add_cg("Хрущевка", [
        ("cg cg22"),
        ("cg cg23", "Я и мой Папа - Аргон!"),
    ])

    add_cg("Информационный Пузырь", [
        ("cg cg24", "Нам с Алекс также было весело..."),
        ("cg cg25"),
    ])

    add_cg("Непреступные Звезды", [
        ("cg cg26_1"),
        ("cg cg26_2"),
        ("cg cg26_3"),
        ("cg cg26_4"),
        ("cg cg26_5", "Селестия... Наконец-то я тебя нашла..."),
    ])

    add_cg("Ботанический сад", [
        ("cg cg27_1"),
        ("cg cg27_2", "Где же я видела похожий антураж?"),
        ("cg cg27_3", "Она будто вышла из сказки."),
    ])

    add_cg("Запретный Рай", [
        ("cg cg28_1", "Гортензии"),
        ("cg cg28_2", "Где же я видела похожий антураж?"),
        ("cg cg28_3", "Она будто вышла из сказки."),
        ("cg cg28_4", "Я испугала Тётю..."),
        ("cg cg28_5", "Такова моя природа"),
    ])

    add_cg("Созвездие", [
        ("cg cg29", "Возможно... возможно, я и правда смогу найти ее, и тогда... я увижу в этих созвездиях Селестию..."),
    ])

    add_cg("Кафе 'Сахарная Комета'", [
        ("cg cg30_1"),
        ("cg cg30_2"),
        ("cg cg30_3"),
        ("cg cg30_4"),
    ])

    add_cg("Концерт", [
        ("cg cg31_1", "Я смогу спеть... всё ради неё..."),
        ("cg cg31_2", "...ради нашей мечты!"),
        ("cg cg31_3", "Ну, что?! Веритас?! Готовы?!"),
        ("cg cg31_4", "Готовы подарить свои сердца. Ради меня... Ради неё...?"),
    ])

    add_cg("Фан-встреча", [
        ("cg cg32_1"),
        ("cg cg32_2"),
        ("cg cg32_3", "Я и мои фанатки!"),
    ])

    add_cg("Бог в обличии девы", [
        ("cg cg32_4", "Ой! Это только для платный подписчиков <3"),
        ("cg cg32_5"),
        ("cg cg33_1", "Нам сюда!"),
        ("cg cg33_2", "Прости-Прости-Прости!"),
    ])

    add_cg("Золотой Час", [
        ("cg cg33_4", "Последнее, что я услышала - стук каблуков по кафелю, приближающийся из дальнего конца коридора."),
    ])

    add_cg("Зависть", [
        ("cg cg34", "Мне бы больше чокер подошел..."),
        ("cg cg35_1", "Незванка"),
        ("cg cg35_2", "Это же моя гитара!"),
    ])

    add_cg("Идеальная Ученица", [
        ("cg cg36_1"),
        ("cg cg36_2", "Взгляд Ученицы"),
        ("cg cg36_3", "Взгляд Куклы"),
    ])

    add_cg("Улей", [
        ("cg cg-36-1b"),
        ("cg cg36-1a"),
    ])