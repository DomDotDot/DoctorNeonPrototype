init python:
    import re

    def slow_punctuation(str_to_test):
        # Пропуск, если текст пустой или скорость текста установлена на "Мгновенно" (CPS = 0)
        if not str_to_test or getattr(preferences, "text_cps", 1) == 0:
            return str_to_test

        # Не добавляем паузы при скипе текста, чтобы не блокировать быструю перемотку
        if renpy.is_skipping():
            return str_to_test

        # Не добавляем паузы в кнопки меню выборов (screen choice)
        if renpy.get_screen("choice") is not None:
            return str_to_test

        # Проверка пользовательского тумблера доступности
        if getattr(persistent, "slow_punctuation", True) is False:
            return str_to_test
            
        # Try to translate the string first, so that the translation matches the unmodified string.
        # config.say_menu_text_filter runs before string translation for menus.
        try:
            # __() is the Ren'Py built-in for immediate translation.
            str_to_test = __(str_to_test)
        except Exception:
            pass
            
        # Split string to isolate tags like {color=#fff} and interpolations like [player_name]
        # Even indices (0, 2, 4...) are plain text; odd indices are tags.
        parts = re.split(r'(\{[^\}]+\}|\[[^\]]+\])', str_to_test)
        
        for i in range(0, len(parts), 2):
            text = parts[i]
            if not text:
                continue
                
            # Replace ellipsis first for a nice stuttered wait effect
            text = text.replace("...", ".{w=0.45}.{w=0.45}.{w=0.45}") 
            text = text.replace("…", "…{w=1.35}")
            
            # Regex replaces punctuation only if followed by a space or end-of-line.
            # \1 puts the matched punctuation back before the {w} tag.
            text = re.sub(r'([.?!]+)(?=\s|$)', r'\1{w=0.75}', text)  # Sentence ends
            text = re.sub(r'(,)(?=\s|$)', r'\1{w=0.5}', text)      # Commas
            text = re.sub(r'(:|;)(?=\s|$)', r'\1{w=0.5}', text)     # Colons/Semicolons
            text = re.sub(r'(—|-{2,})(?=\s|$)', r'\1{w=0.5}', text) # Em dashes
            
            parts[i] = text
            
        return "".join(parts)

    config.say_menu_text_filter = slow_punctuation