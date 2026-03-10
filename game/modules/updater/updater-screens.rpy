screen updater_prompt_screen():
    modal True
    zorder 300
    
    frame:
        xalign 0.5 yalign 0.5
        xsize 600 padding (40, 40)
        
        vbox:
            spacing 20
            
            text _("Доступно обновление!") size 36 bold True xalign 0.5
            
            text _("Найдена новая версия игры: ") + "[updater_state['new_version']!t]" size 24 xalign 0.5
            text _("Хотите скачать и установить её сейчас?") size 22 color "#ccc" xalign 0.5
            
            null height 20
            
            hbox:
                xalign 0.5 spacing 50
                textbutton _("Обновить") action Return("update") style "button" text_size 28 padding (15, 10)
                textbutton _("Позже") action Return("cancel") style "button" text_size 28 padding (15, 10)

screen updater_catalog_screen():
    modal True
    zorder 300

    timer 0.1 repeat True action Function(renpy.restart_interaction)
    
    frame:
        xalign 0.5 yalign 0.5 padding (40, 40) xsize 1000 ysize 700
        background "#000000dd"
        
        vbox:
            spacing 20
            
            if updater_state["status"] in ["downloading", "running", "error"]:
                text _("Обновление игры до версии [updater_state['new_version']]") size 30 bold True xalign 0.5
                
                null height 50
                if updater_state["status"] == "downloading":
                    $ cur_fmt = "{:.1f}".format(updater_state['mb_cur'])
                    $ tot_fmt = "{:.1f}".format(updater_state['mb_total'])
                    text _("Загрузка установщика: [cur_fmt] из [tot_fmt] МБ") xalign 0.5 size 24
                    
                    bar:
                        value updater_state['progress']
                        range 1.0
                        ysize 30
                        left_bar Frame("gui/bar/left.png", 4, 4)
                        right_bar Frame("gui/bar/right.png", 4, 4)
                        
                    null height 20
                    textbutton _("Отмена") action [Function(cancel_update), Return("cancel")] xalign 0.5
                    
                elif updater_state["status"] == "running":
                    text _("Запуск мастера установки...") xalign 0.5 color "#0f0"
                    text _("Сейчас игра будет автоматически закрыта.") xalign 0.5 size 20
                    timer 1.5 action Quit(confirm=False)
                    
                elif updater_state["status"] == "error":
                    text _("ОШИБКА ОБНОВЛЕНИЯ") color "#f00" xalign 0.5 size 30
                    text "[updater_state['error_msg']!t]" size 18 xalign 0.5
                    
                    null height 20
                    textbutton _("Закрыть") action Return("cancel") xalign 0.5
                    
            else:
                text _("Доступные версии игры") size 36 bold True xalign 0.5
                text _("Выберите версию для скачивания и установки.") size 20 color "#ccc" xalign 0.5
                
                hbox:
                    xalign 0.5 spacing 50
                    $ is_stable = updater_state["selected_track"] == "stable"
                    $ is_early = updater_state["selected_track"] == "early"
                    
                    textbutton _("Stable Releases"):
                        action SetDict(updater_state, "selected_track", "stable")
                        background ("#444" if is_stable else "#222") padding (15, 10)
                        
                    textbutton _("Early Access"):
                        action SetDict(updater_state, "selected_track", "early")
                        background ("#444" if is_early else "#222") padding (15, 10)
                        
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    ysize 350
                    
                    vbox:
                        spacing 10
                        $ rel_list = updater_state["releases"].get(updater_state["selected_track"], [])
                        
                        if not rel_list:
                            null height 50
                            text _("В этом канале нет доступных версий.") xalign 0.5 color "#aaa"
                            
                        for item in rel_list:
                            $ is_sel = (updater_state["selected_release"] == item)
                            $ has_exe = item["exe_url"] is not None
                            $ bg_col = "#333" if is_sel else "#111"
                            
                            button:
                                action SetDict(updater_state, "selected_release", item)
                                xfill True padding (15, 15) background bg_col
                                
                                hbox:
                                    spacing 20
                                    vbox:
                                        text "[item['name']!t]" size 24 bold True color "#fff"
                                        text _("Версия: [item['version']]") size 18 color "#ccc"
                                        
                                    frame:
                                        xalign 1.0 background None
                                        if has_exe:
                                            text _("Установщик доступен") color "#0f0" size 18
                                        else:
                                            text _("Нет установщика") color "#f00" size 18
                                            
                null height 20
                
                hbox:
                    xalign 0.5 spacing 50
                    
                    $ sel_item = updater_state.get("selected_release")
                    $ can_install = sel_item and sel_item.get("exe_url")
                    
                    textbutton _("Загрузить и установить"):
                        action If(can_install, true=Function(start_game_update, sel_item), false=None)
                        style "button" text_size 28 padding (20, 10)
                        
                    textbutton _("Закрыть") action Return("close") style "button" text_size 28 padding (20, 10)

label show_updater_prompt:
    call screen updater_prompt_screen()
    $ res = _return
    if res == "update":
        call screen updater_catalog_screen()
    return
