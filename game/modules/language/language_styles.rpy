## Языки

# ЭКРАН ВЫБОРА ЯЗЫКА
screen language_selection_screen():
    modal True 
    zorder 150
    tag menu

    frame:
        style_prefix "language_select"
        xalign 0.5
        yalign 0.5
        background "#000a"
        padding (50, 50)

        vbox:
            xalign 0.5
            spacing 20

            text "Select Language / Выберите Язык:" xalign 0.5 size 30

            null height 10

            for name, code in LANGUAGE_LIST:
                # Action: 
                # 1. Language(code) - устанавливает и сохраняет язык в persistent.language
                # 2. Return() - закрывает экран, т.к. мы вызвали его через 'call screen'
                textbutton name action [Language(code), Return()]

style language_select_frame:
    background Frame("gui/frame.png", 25, 25)
    padding (40, 40)

style language_select_button:
    properties gui.button_properties("button")
    xalign 0.5
    size 28
 
style language_select_button_text:
    properties gui.text_properties("button_text")
    size 28

default persistent.language = None