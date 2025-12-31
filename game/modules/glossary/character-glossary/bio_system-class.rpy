init python:
    class CharBio:
        def __init__(self, id, name, real_name, gender, height, age, role, element="Нет", 
                    hair="-", eyes="-", clothes="-", personality="-", 
                    aliases=None, engages_in=None, 
                    desc_stages=None, image_tag=None):
            
            self.id = id
            self.name = name            # Отображаемое имя в списке (может быть "???")
            self.real_name = real_name  # Настоящее имя (для заголовка)
            self.gender = gender        # Пол (символ или текст)
            self.role = role
            
            # Физические параметры
            self.height = height
            self.age = age
            self.element = element
            self.hair = hair
            self.eyes = eyes
            self.clothes = clothes
            self.personality = personality
            
            # Списки (Алиасы и "В чем замешан")
            self.aliases = aliases if aliases else []
            self.engages_in = engages_in if engages_in else []
            
            # Описание (список строк, открывающихся по очереди)
            self.desc_stages = desc_stages if desc_stages else []
            
            # Спрайт для профиля
            self.image_tag = image_tag if image_tag else id
            
            # --- СОСТОЯНИЕ (ПРОГРЕСС) ---
            self.seen = True           # Видел ли игрок персонажа
            self.name_known = True     # Знает ли игрок настоящее имя
            self.gender_known = True   # Раскрыт ли пол (для Серафины)
            self.desc_level = 0         # Сколько абзацев описания открыто
            self.extra_info_known = True # Раскрыты ли спойлерные теги (engages_in)

        # Метод для проверки: показывать данные или "???"
        def get_display_name(self):
            return self.real_name if self.name_known else "???"

        def get_display_gender(self):
            if not self.gender_known:
                return "?" 
            return self.gender

        # Метод для "Опасных" красных тегов
        # Если extra_info_known = False, мы скрываем самые страшные грехи
        def get_engages_list(self):
            if not self.extra_info_known:
                # Возвращаем только безопасные или ставим заглушку
                return ["???"]
            return self.engages_in

    # 1. Функция полного открытия ОДНОГО персонажа по его ID
    def unlock_char_full(target_id):
        # Ищем персонажа в списке
        target = None
        for char in all_bios:
            if char.id == target_id:
                target = char
                break
            
        if target:
            target.seen = True              # Персонаж виден в списке
            target.name_known = True        # Имя раскрыто
            target.gender_known = True      # Пол раскрыт
            target.extra_info_known = True  # Спойлерные теги (грехи) раскрыты
            target.desc_level = len(target.desc_stages) # Открываем все доступные абзацы
                
            renpy.notify(f"Данные {target.real_name} полностью расшифрованы.")
        else:
            renpy.notify(f"Ошибка: ID '{target_id}' не найден.")

    # 2. Функция открытия ВСЕХ персонажей (Режим Бога / Галерея открыта)
    def unlock_all_chars_full():
        for char in all_bios:
            char.seen = True
            char.name_known = True
            char.gender_known = True
            char.extra_info_known = True
            char.desc_level = len(char.desc_stages)
                
        renpy.notify("Глоссарий: Все персонажи разблокированы")
            
    # 3. (Опционально) Просто "встретить" всех, но не спойлерить
    def meet_all_chars():
        for char in all_bios:
            char.seen = True
        renpy.notify("Все профили персонажей добавлены в список.")