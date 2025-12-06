default active_speaker = None

init python:
    # Явно импортируем Матрицу, чтобы избежать путаницы
    # -----------------------------------------------------------
    # 1. ЛОГИКА ПОДСВЕТКИ (Та же, что и раньше)
    # -----------------------------------------------------------

    def name_callback(event, interact=True, **kwargs):
        if not interact: return
        if event == "begin":
            store.active_speaker = kwargs.get("name")

# Трансформация: если active_speaker совпадает с char_name -> ярко, иначе -> темно

    class Dimmer:
        def __init__(self, char_name):
            self.char_name = char_name
            
            if store.active_speaker == char_name:
                self.current_value = 1.0
            else:
                self.current_value = 0.5
            
        def __call__(self, trans, st, at):
            # Определяем целевую яркость:
            # Если говорит этот персонаж - 1.0 (ярко), иначе 0.5 (темно)
            if store.active_speaker == self.char_name:
                target = 1.0
            else:
                target = 0.5
            
            # Если яркость уже правильная, проверяем реже (оптимизация)
            if self.current_value == target:
                return 0.1
            
            # Плавная анимация (ручной 'ease')
            step = 0.05
            
            if self.current_value < target:
                self.current_value = min(target, self.current_value + step)
            else:
                self.current_value = max(target, self.current_value - step)

            v = self.current_value
            
            # Создаем матрицу масштабирования цвета (то же самое, что TintMatrix)
            # Формат: [R, 0,0,0, 0,G,0,0, 0,0,B,0, 0,0,0,Alpha]
            m = Matrix([
                v, 0, 0, 0,
                0, v, 0, 0,
                0, 0, v, 0,
                0, 0, 0, 1
            ])
            
            trans.matrixcolor = m
            
            # Повторяем часто для плавности
            return 0.01


    # -----------------------------------------------------------
    # 2. АВТОМАТИЧЕСКИЙ ПОИСК И РЕГИСТРАЦИЯ СПРАЙТОВ
    # -----------------------------------------------------------

    import os
    SPRITE_DIR = "images/sprites/"

    def register_auto_sprites():
        # Получаем список файлов
        files = renpy.list_files()
        
        for path in files:
            if path.startswith(SPRITE_DIR) and path.lower().endswith((".png", ".webp", ".jpg", ".avif")):
                filename = os.path.basename(path)
                name_no_ext = os.path.splitext(filename)[0]

                parts = name_no_ext.split()
                
                if parts:
                    char_tag = parts[0]
                    # Здесь мы привязываем класс Dimmer к картинке
                    renpy.image(name_no_ext, At(path, auto_dim(char_tag)))

            
# -----------------------------------------------------------
# БЛОК 3: Трансформация и Запуск (Ren'Py Script)
# -----------------------------------------------------------

# Сама трансформация теперь очень простая, она просто вызывает наш класс
transform auto_dim(char_name):
    function Dimmer(char_name)

# Запускаем поиск спрайтов при инициализации
init 1 python:
    register_auto_sprites()