default persistent.ai_sensitive_mode = False

screen ai_sensitive_overlay():
    zorder -10

    if persistent.ai_sensitive_mode:
        add Solid("#000000") 
        text "AI SENSITIVE MODE | TURN OFF SETTING TO UNCOVER" size 45 color "#333" align (0.99, 0.01)

# Автозапуск экрана
# Это значит, что Ren'Py будет показывать его всегда, когда идет игровой процесс,
# но автоматически скроет при выходе в Главное Меню.
init python:
    config.overlay_screens.append("ai_sensitive_overlay")