screen content_warning():

    tag menu

    frame:

        align(0.5, 0.5)
        xmargin 50
        xpadding 100

        vbox:
            
            align(0.5, 0.5)
            spacing 50
            # xfill True
            style_prefix "presplash"

            label _("Дисклеймер") xalign 0.5

            text _("Привет, дорогой игрок!") text_align 0.5 xalign 0.5

            null height 20

            text _("""Спасибо, что решили познакомиться с моей историей. Прежде чем вы окунетесь в этот мир, я хочу быть с вами полностью честным.

Я не художник, а в первую очередь рассказчик.

У меня в голове родилась история с персонажами, которых я полюбил, и мне безумно хотелось поделиться ею с кем-то ещё. Визуальная новелла показалась мне идеальным форматом для этого.

Чтобы «оживить» мир и героев, я использовал современные технологии - все фоны, спрайты персонажей и иллюстрации (CG) были созданы с помощью нейросетей (AI). Это стало для меня тем самым мостиком, который позволил визуализировать то, что я придумал.

При этом всё остальное - сюжет, диалоги, характеры персонажей и сама идея - это полностью моя авторская работа, в которую я вложил душу.

Также хочу отметить, что в игре используется музыка, распространяемая по лицензии Royalty-Free, за что я безмерно благодарен её создателям.

Эта новелла не является коммерческим проектом и создана исключительно из любви к историям.""") text_align 0.5 xalign 0.5 size 20

            null height 40

            text _("Спасибо за ваше понимание! Надеюсь, вам понравится путешествие, которое вас ждёт.") text_align 0.5 xalign 0.5

            textbutton _("Подтвердить") action Return() xalign 0.5 text_align 0.5 text_size 55
    


## Splashscreen Settings##################################
##
## A custom screen that tells players to adjust their settings in the Preferences
## Screen. Edited so you don't have to keep track of two different pages.

screen splash_settings():

    tag menu

    frame:

        align(0.5, 0.5)
        xmargin 50
        xpadding 100

        vbox:
            
            align(0.5, 0.5)
            spacing 50
            # xfill True
            style_prefix "presplash"

            label _("Установите настройки") xalign 0.5

            text _("В следующем меню вы можете задать настройки игры. Эти параметры можно изменить в любое время в меню.") text_align 0.5 xalign 0.5

            textbutton _("Подтвердить") action Return() xalign 0.5 text_align 0.5 text_size 55



style presplash_label:
    top_margin gui.pref_spacing
    bottom_margin 3
    text_align 0.5

style presplash_label_text:
    yalign 1.0
    size 100