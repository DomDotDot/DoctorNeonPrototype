# --- Слушатель клавиши M ---
screen inventory_listener():
    # Работает всегда, но открывает инвентарь только если inventory_allowed == True
    key "K_m" action If(inventory_allowed, ToggleScreen("inventory_screen"), Notify(_("Инвентарь недоступен")))

# --- Основной экран Инвентаря ---
screen inventory_screen():
    modal True # Блокирует взаимодействие с игрой под инвентарем
    add Solid("#000000AA") # Полупрозрачный фон

    # Основная рамка
    frame:
        align (0.5, 0.5)
        xysize (800, 600)
        padding (20, 20)
        
        vbox:
            spacing 20
            
            text _("Инвентарь") size 40 align (0.5, 0.0)

            # Сетка предметов (Gridset)
            vpgrid:
                cols 5
                rows 4
                spacing 15
                draggable True
                mousewheel True
                scrollbars "vertical"
                xysize (760, 450)

                for item in inventory_list:
                    # Кнопка с иконкой предмета, с автоматическим ресайзом под слот
                    imagebutton:
                        idle Transform(item.icon, fit="contain", xysize=(100, 100), zoom=1.0)
                        hover Transform(item.icon, fit="contain", xysize=(100, 100), zoom=1.1)
                        action SetVariable("selected_item", item)
                        xysize (100, 100) # Размер слота
                        
                # Заполняем пустые слоты (опционально, для красоты сетки)
                for i in range(20 - len(inventory_list)):
                    frame:
                        background Solid("#333")
                        xysize (100, 100)

            textbutton _("Закрыть (M)") action [SetVariable("selected_item", None), Hide("inventory_screen")] align (0.5, 1.0)
    
    # Подгружаем контекстное меню, если выбран предмет
    if selected_item:
        use item_context_menu(selected_item)

# --- Контекстное меню предмета (Осмотреть, Использовать, Закрыть) ---
screen item_context_menu(item):
    modal True
    # Закрытие меню при клике мимо
    button:
        yfill True
        xfill True
        action SetVariable("selected_item", None)
        
    frame:
        align (0.5, 0.5)
        padding (30, 30)
        background Solid("#222")
        
        vbox:
            align (0.5, 0.5)
            spacing 20
            
            text _(item.name) size 30 bold True xalign 0.5
            
            # Ячейка (контейнер) для зума картинки
            frame:
                xalign 0.5
                xysize (500, 500)
                background Solid("#111")
                add Transform(item.icon, fit="contain", xysize=(500, 500)) align (0.5, 0.5)
            
            hbox:
                spacing 10
                xalign 0.5
                
                # Кнопка ОСМОТРЕТЬ (показывает описание)
                textbutton _("Осмотреть") action [Show("item_description", i=item), Function(track_item_inspected, item.id)]
                
                # Кнопка ИСПОЛЬЗОВАТЬ (если есть функция)
                if item.use_func:
                    textbutton _("Использовать") action Function(use_current_item)
                else:
                    textbutton _("Использовать") action Notify(_("Это нельзя использовать здесь.")) text_color "#888"

                # Кнопка ЗАКРЫТЬ
                textbutton _("Отмена") action SetVariable("selected_item", None)

# --- Экран описания (всплывает при "Осмотреть") ---
screen item_description(i):
    modal True
    frame:
        align (0.5, 0.5)
        padding (30,30)
        vbox:
            spacing 20
            text _(i.name) size 30
            text _(i.description)
            textbutton _("OK") action Hide("item_description") xalign 0.5