init offset = -1

# Переменная для тестов: если True, открывает все картинки.
default persistent.unlock_gallery = False

init python:
    # Размеры миниатюры в меню
    gal_thumb_x = 384
    gal_thumb_y = 216

    gal_cols = 3
    gal_rows = 3
    # Сколько картинок на одной странице (3 * 2 = 6)
    gal_cells = gal_cols * gal_rows 
    
    class GalleryItem:
        def __init__(self, name, images_data, thumb=None):
            self.name = name
            self.images_data = []
            
            for item in images_data:
                # Передали ("имя", "описание")
                if isinstance(item, tuple):
                    self.images_data.append(item)
                # Если передали просто строку "cg-1_1"
                else:
                    self.images_data.append((item, "")) 
            

            # Логика миниатюры
            if thumb:
                self.thumb = thumb
            else:
                if len(self.images_data) > 0:
                    self.thumb = self.images_data[0][0]
                else:
                    self.thumb = None

        def is_unlocked(self):
            if persistent.unlock_gallery:
                return True
            for img_name, _ in self.images_data:
                if renpy.seen_image(img_name):
                    return True
            return False
                
            unlocked = []
            for img_name, desc in self.images_data:
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

    # Получить список для просмотра
        def get_unlocked_list(self):
            if persistent.unlock_gallery:
                return self.images_data
            return [(img, desc) for img, desc in self.images_data if renpy.seen_image(img)]

        # Главная оптимизация: метод возвращает Displayable
        # Если закрыто - возвращает легкий Solid/Image
        # Если открыто - возвращает картинку
        def get_thumbnail_displayable(self):
            if self.is_unlocked():
                # Возвращаем реальную картинку
                # Transform здесь нужен, чтобы закешировать размер
                # и не грузить фулл-сайз текстуру в память, если RenPy умный,
                # но лучше использовать заранее подготовленные маленькие файлы.
                return Transform(self.thumb, fit="cover", size=(gal_thumb_x, gal_thumb_y))
            else:
                # Возвращаем "общую" заглушку, не грузя файлы с диска
                return "gallery_locked_thumb"

        def get_count_text(self):
            total = len(self.images_data)
            unlocked = len(self.get_unlocked_list())
            return "{}/{}".format(unlocked, total)

    gallery_items = []

    def add_cg(name, images, thumb=None):
        gallery_items.append(GalleryItem(name, images, thumb))


# --- ОБЩИЙ РЕСУРС ЗАБЛОКИРОВАННОЙ КАРТИНКИ ---
# Создается один раз в памяти, используется везде. Супер-легкий.
image gallery_locked_thumb:
    Solid("#1a1a1a") # Темно-серый фон
    size(384, 216)
    Text("LOCKED", size=40, color="#444", align=(0.5, 0.5), outlines=[(2, "#000")])

image gallery_skeleton_thumb:
    Solid("#111111")
    size(384, 216)
    Text("...", size=60, color="#444", align=(0.5, 0.5), outlines=[(2, "#000")])



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

    add_cg(_("Цвета Белого снега и Черной Ночи"), [
        ("featured_cg-8_1", _("Холодная и отстраненная... как и я.")),
        ("featured_cg-8_2", _("'Давай сходим в Планетарий?'"))
    ])

    add_cg(_("Поездка"), [
        ("cg-9", _("GPS: Маршрут перестроен.")),
        ("cg-10", _("Фары разрезают тьму."))
        ])

    add_cg(_("Кошмар"), [
        ("cg-11_1-1", _("Ты - не Алекс.")),
        ("featured_cg-11_2", _("'Её' больше нет.")),
        ("featured_cg-11_3-1", _("Звук снова победил Тишину.")),
    ])

    add_cg(_("РАЗЫСКИВАЕТСЯ"), [
        ("cg-12_1", _("Кто это?")),
        ("cg-12_1-1", _("Мой фоторобот.")),
        ("featured_cg-12_2", _("Это же... моя подруга...")),
    ])

    add_cg(_("Уют дома"), [
        ("cg-13_1"),
        ("cg-13_2"),
    ])

    add_cg(_("Путь в Никуда"), [
        ("cg-14"),
        ("featured_cg-15_1"),
        ("featured_cg-15_2"),
    ])

    add_cg(_("Идиллия"), [
        ("cg-16", _("Кто все эти люди...?")),
    ])

    add_cg(_("Завод"), [
        ("cg-17"),
        ("featured_cg-18"),
    ])

    add_cg(_("Аномик-3"), [
        ("cg-19"),
        ("cg-20_1"),
        ("featured_cg-20_2", _("Я не могу бросить его... только не снова.")),
        ("featured_cg-20_3", _("Вы нас не видете.")),
    ])

    add_cg(_("Хрущевка"), [
        ("cg-22"),
        ("featured_cg-23", _("Я и мой Папа - Аргон!")),
    ])

    add_cg(_("Информационный Пузырь"), [
        ("featured_cg-24", _("Нам с Алекс также было весело...")),
        ("featured_cg-25"),
    ])

    add_cg(_("Непреступные Звезды"), [
        ("cg-26_1"),
        ("cg-26_2"),
        ("cg-26_3"),
        ("cg-26_4"),
        ("featured_cg-26_5", _("Селестия... Наконец-то я тебя нашла...")),
    ])

    add_cg(_("Ботанический сад"), [
        ("cg-27_1"),
        ("cg-27_2", _("Где же я видела похожий антураж?")),
        ("featured_cg-27_3", _("Она будто вышла из сказки.")),
    ])

    add_cg(_("Запретный Рай"), [
        ("cg-28_1", _("Гортензии")),
        ("featured_cg-28_2"),
        ("featured_cg-28_3", _("Ничто")),
        ("cg-28_4", _("Я испугала Тётю...")),
        ("cg-28_5", _("Такова моя природа")),
    ])

    add_cg(_("Созвездие"), [
        ("featured_cg-29", _("Возможно... возможно, я и правда смогу найти ее, и тогда... я увижу в этих созвездиях Селестию...")),
    ])

    add_cg(_("Кафе 'Сахарная Комета'"), [
        ("cg-30_1"),
        ("cg-30_2"),
        ("cg-30_3"),
        ("cg-30_4"),
    ])

    add_cg(_("Концерт"), [
        ("cg-31_1", _("Я смогу спеть... всё ради неё...")),
        ("featured_cg-31_2", _("...ради нашей мечты!")),
        ("featured_cg-31_3", _("Ну, что?! Веритас?! Готовы?!")),
        ("featured_cg-31_4", _("Готовы подарить свои сердца. Ради меня... Ради неё...?")),
    ])

    add_cg(_("Фан-встреча"), [
        ("cg-32_1"),
        ("featured_cg-32_2"),
        ("featured_cg-32_3", _("Я и мои фанатки!")),
    ])

    add_cg(_("Бог в обличии девы"), [
        ("featured_cg-32_4", _("Ой! Это только для платный подписчиков <3")),
        ("cg-32_5"),
        ("featured_cg-33_1", _("Нам сюда!")),
        ("featured_cg-33_2", _("Прости-Прости-Прости!")),
    ])

    add_cg(_("Золотой Час"), [
        ("featured_cg-33_4", _("Последнее, что я услышала - стук каблуков по кафелю, приближающийся из дальнего конца коридора.")),
    ])

    add_cg(_("Зависть"), [
        ("featured_cg-34", _("Мне бы больше чокер подошел...")),
        ("featured_cg-35_1", _("Незванка")),
        ("featured_cg-35_2", _("Это же моя гитара!")),
    ])

    add_cg(_("Идеальная Ученица"), [
        ("cg-36_1"),
        ("cg-36_2", _("Взгляд Ученицы")),
        ("featured_cg-36_3", _("Взгляд Куклы")),
    ])

    add_cg(_("Улей"), [
        ("featured_cg-36-1b"),
        ("cg-36-1a"),
    ])

    add_cg(_("Королева Школ"), [
        ("featured_1cg-2b"),
        ("featured_1cg-1"),
    ])

    add_cg(_("Твоя миссия..."), [
        ("2cg-4"),
        ("2cg-1"),
        ("featured_2cg-2"),
        ("featured_2cg-3", _("Форма Мертвеца")),
    ])

    add_cg(_("Академия Веритас"), [
        ("2cg-5", _("Всем привет. Моё имя - Неон Судзуки")),
        ("2cg-6", _("А какой твой любимый десерт?")),
        ("2cg-7", _("Не обращай внимания, она со всеми так.")),
        ("featured_3cg_2b"),
        ("featured_3cg-3"),
    ])

    add_cg(_("Спасение"), [
        ("4cg-1"),
        ("featured_4cg-2"),
        ("4cg-3"),
    ])

    add_cg(_("Взгляд Молящий"), [
        ("featured_4cg-4"),
        ("4cg-5"),
    ])

    add_cg(_("Актриса чужой Жизни"), [
        ("featured_5cg-1"),
        ("featured_5cg-2"),
        ("featured_5cg-3", _("Сделайте мне одолжение...")),
        ("5cg-4"),
        ("featured_5cg-5", _("Застрелите друг друга~")),
    ])

    add_cg(_("Полный Амбициями и Пустой Сосуд"), [
        ("6cg-1a"),
        ("featured_6cg-1b"),
        ("featured_6cg-2"),
        ("6cg-3"),
    ])


    add_cg(_("Дочь Луны"), [
        ("featured_6cg-4", _("Слезно заклинала до рассвета Луну. У нее просила повстречаться с милым, что не бросит её одну.")),
        ("featured_6cg-5", _("Да, получишь мужа ты, цыганка, что наполнит жизнь любовью яркой, но взамен же только первого ребенка отдаешь мне ты.")),
        ("featured_6cg-6", _("Буду я, качая, в нем души не чаять, - Говорила Луна.")),
        ("6cg-7"),
        ("6cg-8", _("Не находишь любви ты на своем пути. Ах, Луна золотая, что же делать будешь с ним.")),
        ("featured_6cg-9", _("Проклятая внешность. Он не мой, конечно! - Гнева полны очи.")),
    ])


    add_cg(_("Огонь, что во мне."), [
        ("7a-cg-1"),
        ("featured_7a-cg-2"),
        ("7a-cg-3"),
        ("7a-cg-4"),
        ("7a-cg-5", _("Она была права. Всё это время. Такова моя природа. Изначально")),
        ("featured_8cg-1"),
        ("featured_8cg-2", _("Взгляд Ребёнка")),
    ])

    add_cg(_("Кража Личности"), [
        ("featured_7b-cg-1"),
    ])

    add_cg(_("Психоз"), [
        ("8cg-3", _("Мастер в Гляделки")),
        ("8cg-4"),
        ("featured_8cg-5", _("Промокший Ангел")),
    ])

    add_cg(_("Сверкание во Тьме"), [
        ("8cg-5"),
        ("featured_8cg-6"),
    ])

    add_cg(_("Выстрел во Тьме"), [
        ("featured_8cg-7"),
    ])

    add_cg(_("Падший Ангел"), [
        ("featured_8cg-8e-1"),
        ("8cg-8e-2"),
        ("featured_8cg-8e-3"),
    ])

    add_cg(_("Увядший Цветок"), [
        ("featured_8cg-9"),
        ("featured_10cg-3-1"),
        ("featured_10cg-3-2"),
        ("10cg-3-3"),
        ("featured_11cg-1"),
    ])

    add_cg(_("Щит без Меча"), [
        ("featured_8cg-10-1"),
        ("featured_8cg-10-2"),
        ("8cg-11", _("Стань моим Щитом~")),
        ("featured_8cg-12"),
    ])

    add_cg(_("Буйное Увлечение"), [
        ("featured_10cg-1-1"),
        ("featured_10cg-1-2"),
        ("featured_10cg-2"),
    ])

    add_cg(_("Замысловатые Устремления"), [
        ("9cg-1"),
        ("featured_9cg-2"),
    ])

    add_cg(_("Промокший Ангел"), [
        ("featured_9cg-3"),
        ("featured_9cg-4", _("Заколка чужой Души")),
        ("featured_9cg-5b"),
        ("9cg-5"),
        ("featured_9cg-6"),
        ("featured_9cg-7b"),
        ("featured_9cg-8-1"),
        ("9cg-8-2"),
    ])

    add_cg(_("Cофиты"), [
        ("featured_9cg-9"),
        ("featured_9cg-10-1"),
        ("featured_9cg-10-2", _("Это... я врала зеркалам...")),
    ])

    add_cg(_("Выброшенный Мусор"), [
        ("featured_9cg-11"),
    ])

    add_cg(_("Веритас"), [
        ("featured_11cg-2"),
    ])

    add_cg(_("Королева Пчёл"), [
        ("12cg-2"),
    ])