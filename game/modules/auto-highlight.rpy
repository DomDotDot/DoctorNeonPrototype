default active_speaker = None

init python:

    # -----------------------------------------------------------
    # ЛОГИКА ПОДСВЕТКИ
    # -----------------------------------------------------------

    # Глобальный кеш яркости — переживает пересоздание Dimmer
    # (при show/смене выражения/позиции не теряем текущую яркость)
    _dimmer_brightness = {}

    def name_callback(event, interact=True, **kwargs):
        if not interact:
            return
        if event == "begin":
            store.active_speaker = kwargs.get("name") or "narrator"
        elif event == "end":
            # Сбрасываем говорящего → между репликами все яркие
            # (анимации сцены не затемняют персонажей)
            store.active_speaker = None


    class Dimmer:
        def __init__(self, char_name):
            self.char_name = char_name

            # Восстанавливаем из кеша (при show/смене выражения/позиции)
            if char_name in _dimmer_brightness:
                self.current_value = _dimmer_brightness[char_name]
            elif store.active_speaker is None:
                # Никто не говорит → все яркие
                self.current_value = 1.0
            elif store.active_speaker == char_name:
                self.current_value = 1.0
            else:
                self.current_value = 0.5

        def __call__(self, trans, st, at):

            # Никто не говорит → все яркие (1.0)
            if store.active_speaker is None:
                target = 1.0
            elif store.active_speaker == self.char_name:
                target = 1.0
            else:
                target = 0.5

            # Сохраняем в кеш
            _dimmer_brightness[self.char_name] = self.current_value

            # Если яркость уже правильная, проверка реже (оптимизация)
            if self.current_value == target:
                return 0.1

            # Ручной 'ease'
            step = 0.05

            if self.current_value < target:
                self.current_value = min(target, self.current_value + step)
            else:
                self.current_value = max(target, self.current_value - step)

            v = self.current_value
            _dimmer_brightness[self.char_name] = v

            # Матрицу масштабирования цвета
            m = Matrix([
                v, 0, 0, 0,
                0, v, 0, 0,
                0, 0, v, 0,
                0, 0, 0, 1
            ])

            trans.matrixcolor = m
            return 0.01


    # -----------------------------------------------------------
    # АВТОМАТИЧЕСКИЙ ПОИСК И РЕГИСТРАЦИЯ СПРАЙТОВ
    # -----------------------------------------------------------

    import os
    SPRITE_DIR = "images/sprites/"

    def register_auto_sprites():
        files = renpy.list_files()
        
        for path in files:
            if path.startswith(SPRITE_DIR) and path.lower().endswith((".png", ".webp", ".jpg", ".avif")):
                filename = os.path.basename(path)
                name_no_ext = os.path.splitext(filename)[0]

                parts = name_no_ext.split()
                
                if parts:
                    char_tag = parts[0]
                    renpy.image(name_no_ext, At(path, auto_dim(char_tag)))

            
# -----------------------------------------------------------
# Трансформация и Запуск
# -----------------------------------------------------------

transform auto_dim(char_name):
    function Dimmer(char_name)

init 1 python:
    register_auto_sprites()