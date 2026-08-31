screen language_selection_screen():
    modal True 
    zorder 150
    tag menu
    add "#000c" 

    frame:
        style_prefix "lang_panel"
        xalign 0.5 yalign 0.5
        xsize 1000 ysize 700
        padding (40, 40)
        
        vbox:
            spacing 20
            
            text "SELECT LANGUAGE / ВЫБЕРИТЕ ЯЗЫК" size 40 bold True xalign 0.5 color "#fff"

            null height 20

            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True
                ysize 500
                
                vpgrid:
                    cols 2
                    spacing 30
                    xalign 0.5
                    
                    for lang in LANGUAGE_LIST:
                        $ code = lang['code']
                        $ percent = get_lang_progress(code)
                        $ is_active = (_preferences.language == code)
                        
                        button:
                            style "lang_button"
                            action [Language(code), Function(check_polyglot_on_lang_change), Return()]
                            

            
                            if is_active:

                                background Frame("gui/button/choice_hover_background.png", 10, 10)
                            
                            else:
                            
                                background Frame("gui/button/choice_idle_background.png", 10, 10)
                            
                            hbox:
                                spacing 20
                                yalign 0.5
                                xfill True

                                # 1. Флаг (с проверкой на существование файла)
                                if renpy.loadable(lang['flag']):
                                    add lang['flag'] yalign 0.5 xsize 64 ysize 64 fit "contain"
                                else:
                                    # Заглушка, если флага нет
                                    text "?" size 40 bold True yalign 0.5 xsize 64 xalign 0.5

                                # 2. Инфо
                                vbox:
                                    yalign 0.5
                                    text lang['name'] size 30 bold True color ("#ffaa00" if is_active else "#fff")
                                    
                                    # Полоска прогресса (если не 100%)
                                    if percent < 100:
                                        null height 5
                                        hbox:
                                            spacing 10
                                            bar:
                                                value percent 
                                                range 100 
                                                xsize 150 ysize 10
                                                yalign 0.5
                                                style "lang_progress_bar"
                                            
                                            text f"{percent}%" size 16 color "#aaa" yalign 0.5
                                    else:
                                        text "Готово / Ready" size 16 color "#8f8"

# --- СТИЛИ ---

style lang_panel_frame:
    background Frame("gui/frame.png", 40, 40)

style lang_button:
    xsize 420
    ysize 110
    hover_background Frame("gui/button/choice_hover_background.png", 10, 10)

style lang_progress_bar:
    left_bar Frame("gui/bar/left.png", 4, 4)
    right_bar Frame("gui/bar/right.png", 4, 4)
    thumb None