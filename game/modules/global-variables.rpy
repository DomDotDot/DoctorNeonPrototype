# Переменные:

init python:
    oganesson_name_revealed = False

    if _preferences.language == "english_us":
        oganesson_display_name = _("Trustee")
    else:
        oganesson_display_name = _("Опекунша")


# Технические функции

label reveal_oganesson_name:
    $ oganesson_name_revealed = True

    if _preferences.language == "english_us":
        $ oganesson_display_name = _("Oganesson")
    else:
        $ oganesson_display_name = _("Оганесон")