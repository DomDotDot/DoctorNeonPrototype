# 1. Переменная-переключатель
default persistent.ai_sensitive_mode = False

# 2. Экран-перехватчик
screen ai_sensitive_overlay():
    zorder -10
    
    # Слушаем нажатие клавиши (английская 'H' - Hide)

    key "h" action ToggleField(persistent, "ai_sensitive_mode")

    if persistent.ai_sensitive_mode:
        add Solid("#000000") 
        text "AI SENSITIVE MODE" size 14 color "#333" align (0.99, 0.01)

# 3. Автозапуск экрана
# Это значит, что Ren'Py будет показывать его всегда, когда идет игровой процесс,
# но автоматически скроет при выходе в Главное Меню.
init python:
    config.overlay_screens.append("ai_sensitive_overlay")