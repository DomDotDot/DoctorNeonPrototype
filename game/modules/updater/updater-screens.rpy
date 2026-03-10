screen updater_prompt_screen():
    modal True
    zorder 300
    
    frame:
        style "modern_panel"
        xsize 700
        
        vbox:
            style "modern_vbox"
            
            label _("Доступно обновление!") style "modern_title_label"
            
            text _("Найдена новая версия игры: ") + "[updater_state['new_version']!t]" size 26 color "#ffffff" xalign 0.5 bold True
            text _("Хотите скачать и установить её сейчас?") size 22 color "#cccccc" xalign 0.5     
            
            null height 30
            
            hbox:
                xalign 0.5 spacing 30
                textbutton _("Обновить") action Return("update") style "safe_button" text_style "danger_button_text" xsize 250 xalign 0.5 text_xalign 0.5
                textbutton _("Позже") action Return("cancel") style "neutral_button" text_style "modern_button_text" xsize 250 xalign 0.5 text_xalign 0.5

screen updater_catalog_screen():
    modal True
    zorder 300

    timer 0.1 repeat True action Function(renpy.restart_interaction)
    
    frame:
        style "modern_panel_wide"
        xsize 1100
        ysize 800
        
        vbox:
            style "modern_vbox"
            
            if updater_state["status"] in ["downloading", "running", "error"]:
                label _("Обновление игры до версии [updater_state['new_version']]") style "modern_title_label"
                
                null height 50
                if updater_state["status"] == "downloading":
                    $ cur_fmt = "{:.1f}".format(updater_state['mb_cur'])
                    $ tot_fmt = "{:.1f}".format(updater_state['mb_total'])
                    text _("Загрузка установщика: [cur_fmt] из [tot_fmt] МБ") xalign 0.5 size 26 color "#e8e8e8"
                    
                    null height 10
                    
                    # Стилизованная полоса прогресса аналогично настройкам или кастомная
                    bar:
                        value updater_state['progress']
                        range 1.0
                        ysize 25
                        xsize 700
                        xalign 0.5
                        left_bar Solid("#0f63c9")
                        right_bar Solid("#333333")
                        thumb None
                        
                    null height 50
                    textbutton _("Отмена загрузки") action [Function(cancel_update), Return("cancel")] style "danger_button" text_style "danger_button_text" xsize 350 xalign 0.5 text_xalign 0.5
                    
                elif updater_state["status"] == "running":
                    text _("Запуск мастера установки...") xalign 0.5 color "#4ac260" size 30 bold True
                    text _("Сейчас игра будет автоматически закрыта.") xalign 0.5 size 22 color "#aaaaaa"
                    timer 1.5 action Quit(confirm=False)
                    
                elif updater_state["status"] == "error":
                    text _("ОШИБКА ОБНОВЛЕНИЯ") color "#ff3333" xalign 0.5 size 36 bold True
                    text "[updater_state['error_msg']!t]" size 20 xalign 0.5 color "#cccccc"
                    
                    null height 40
                    textbutton _("Закрыть") action Return("cancel") style "neutral_button" text_style "modern_button_text" xsize 300 xalign 0.5 text_xalign 0.5
                    
            else:
                label _("Доступные версии игры") style "modern_title_label" bottom_margin 10
                text _("Выберите версию для скачивания и установки.") size 22 color "#cccccc" xalign 0.5
                
                hbox:
                    xalign 0.5 spacing 30
                    $ is_stable = updater_state["selected_track"] == "stable"
                    $ is_early = updater_state["selected_track"] == "early"
                    
                    button:
                        xsize 300 ysize 60
                        background (Solid("#4ac260cc") if is_stable else Solid("#222222cc"))
                        hover_background (Solid("#4ac260") if is_stable else Solid("#444444cc"))
                        action SetDict(updater_state, "selected_track", "stable")
                        text _("Stable Releases") xalign 0.5 yalign 0.5 size 24 color ("#ffffff" if is_stable else "#aaaaaa") bold is_stable
                        
                    button:
                        xsize 300 ysize 60
                        background (Solid("#0f63c9cc") if is_early else Solid("#222222cc"))
                        hover_background (Solid("#0f63c9") if is_early else Solid("#444444cc"))
                        action SetDict(updater_state, "selected_track", "early")
                        text _("Early Access") xalign 0.5 yalign 0.5 size 24 color ("#ffffff" if is_early else "#aaaaaa") bold is_early
                        
                null height 15

                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    ysize 380
                    xsize 900
                    xalign 0.5
                    
                    vbox:
                        spacing 15
                        xalign 0.5
                        $ rel_list = updater_state["releases"].get(updater_state["selected_track"], [])
                        
                        if not rel_list:
                            null height 100
                            text _("В этом канале нет доступных версий.") xalign 0.5 color "#aaaaaa" size 26
                            
                        for item in rel_list:
                            $ is_sel = (updater_state["selected_release"] == item)
                            $ has_exe = item["exe_url"] is not None
                            $ bg_col = Solid("#444444cc") if is_sel else Solid("#00000080")
                            
                            button:
                                action SetDict(updater_state, "selected_release", item)
                                xsize 850
                                padding (25, 20)
                                background bg_col
                                hover_background Solid("#555555cc")
                                
                                hbox:
                                    spacing 20
                                    vbox:
                                        text "[item['name']!t]" size 26 bold True color ("#ffffff" if is_sel else "#cccccc")
                                        text _("Версия: [item['version']]") size 20 color "#aaaaaa"
                                        
                                    frame:
                                        xalign 1.0 yalign 0.5 background None
                                        if has_exe:
                                            text _("Установщик доступен") color "#4ac260" size 20 bold True
                                        else:
                                            text _("Нет установщика") color "#ff3333" size 20 bold True
                                            
                null height 20
                
                hbox:
                    xalign 0.5 spacing 40
                    
                    $ sel_item = updater_state.get("selected_release")
                    $ can_install = sel_item and sel_item.get("exe_url")
                    
                    textbutton _("Установить"):
                        action If(can_install, true=Function(start_game_update, sel_item), false=None)
                        style ("safe_button" if can_install else "neutral_button")
                        text_style ("danger_button_text" if can_install else "modern_button_text")
                        xsize 400
                        xalign 0.5
                        text_xalign 0.5
                        
                    textbutton _("Закрыть") action Return("close") style "neutral_button" text_style "modern_button_text" xsize 300 xalign 0.5 text_xalign 0.5

label show_updater_prompt:
    call screen updater_prompt_screen()
    $ res = _return
    if res == "update":
        call screen updater_catalog_screen()
    return
