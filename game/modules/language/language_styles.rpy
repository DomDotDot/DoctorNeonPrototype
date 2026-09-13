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
                    
                    $ current_active_langs = get_active_languages()
                    for lang in current_active_langs:
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
                                    text ("🌐" if not lang.get("official", True) else "?") size 36 bold True yalign 0.5 xsize 64 xalign 0.5

                                # 2. Инфо
                                vbox:
                                    yalign 0.5
                                    hbox:
                                        spacing 10
                                        text lang['name'] size 26 bold True color ("#ffaa00" if is_active else "#fff")
                                        if not lang.get("official", True):
                                            text _("[[МОД]]") substitute False size 16 color "#39ff14" yalign 0.5
                                    
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
                                        text _("Готово / Ready") size 16 color "#8f8"

            null height 10
            if not getattr(persistent, "community_content_enabled", False):
                text _("💡 Сторонние коммьюнити-переводы можно включить в: Настройки -> Коммьюнити Контент") size 16 color "#888" xalign 0.5
            else:
                text _("🧩 Режим коммьюнити-контента активен") size 16 color "#39ff14" xalign 0.5

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