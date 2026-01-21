init python:
    # 1. Класс Предмета
    class Item:
        def __init__(self, id, name, description, icon, use_func=None):
            self.id = id
            self.name = name
            self.description = description
            self.icon = icon
            # use_func - это имя label или python-функции, вызываемой при использовании из инвентаря
            self.use_func = use_func 

    # 2. Переменные состояния
    inventory_list = [] # Список предметов
    selected_item = None # Текущий выбранный предмет (для контекстного меню)
    inventory_allowed = False # Глобальный переключатель (можно ли открывать инвентарь)

    # 3. Методы управления
    def add_item(item):
        if item not in inventory_list:
            inventory_list.append(item)
            renpy.notify(f"Получено: {item.name}")

    def remove_item(item_id):
        global inventory_list
        # Удаляем предмет по ID, создавая новый список без него
        inventory_list = [i for i in inventory_list if i.id != item_id]
        # Сбрасываем выделение, если удалили выбранный предмет
        global selected_item
        if selected_item and selected_item.id == item_id:
            selected_item = None

    def has_item(item_id):
        # Проверка наличия предмета для меню выборов
        for i in inventory_list:
            if i.id == item_id:
                return True
        return False
        
    # Функция использования предмета (из GUI инвентаря)
    def use_current_item():
        global selected_item
        if selected_item and selected_item.use_func:
            func = selected_item.use_func
            # Если это имя лейбла, прыгаем туда (закрыв инвентарь)
            if renpy.has_label(func):
                renpy.hide_screen("inventory_screen")
                renpy.call_in_new_context(func)
            else:
                # Если это просто python-код или notify
                renpy.notify(func)
                
            # Если предмет одноразовый, можно раскомментировать строку ниже:
            # remove_item(selected_item.id) 
            
            selected_item = None