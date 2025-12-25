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

        def get_unlocked_list(self):
            if persistent.unlock_gallery:
                return self.images_data
                
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
    add_cg(_("Кафетерия Гелиос"), [
        ("featured_cg-1", _("В этот день кофе был особенно горьким.")),
    ])

    add_cg(_("Доклад"), [
        ("cg-2_1", _("Начало доклада.")),
        ("cg-2_3"),
        ("cg-2_4", _("Критические данные.")),
        ("featured_cg-2_5", _("Конец записи.")),
    ])

    add_cg(_("Цюрих"), [
        ("cg-3_1"),
    ])

    add_cg(_("Звездочка"), [
        ("cg-4_1", _("Я помню этот свет...")),
    ])

    add_cg(_("Разгромлен"), [
        ("featured_cg-5_1", _("Первый удар.")),
        ("cg-5_2", _("Посторонний шум.")),
        ("featured_cg-5_3", _("Крах и Триумф."))
    ])

    add_cg(_("Воспоминания 1"), [
        ("cg-6_1"),
        ("featured_cg-6_2", _("'Такова её природа'")),
        ("cg-6_3"),
    ])

    add_cg(_("Побег"), [
        ("cg-7_1", _("Беги!")),
        ("cg-7_2"),
        ("cg-7_3", _("Хвост.")), 
        ("cg-7_5_1", _("Блокада.")),
        ("cg-7_5"),
        ("cg-7_6"),
        ("featured_cg-7_8", _("Почти у цел-")),
        ("featured_cg-7_9", _("Свет в конце тоннеля."))
    ])

    add_cg(_("Цвета Белого снега и Черной Ночи"), [
        ("featured_cg-8_1", _("Холодная и отстраненная... как я.")),
        ("featured_cg-8_2", _("Давай сходим в Планетарий?"))
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