init python:
    def slow_punctuation(str_to_test):
        return (str_to_test
            .replace("... ", ".{w=0.5}.{w=0.5}.{w=0.5} ")
            .replace(", ", ",{w=0.5} ")
            .replace(". ", ".{w=1.0} ")
            .replace("! ", "!{w=1.0} ")
            .replace("? ", "?{w=1.0} ")
            .replace(": ", ":{w=0.5} ")
            .replace("— ", "—{w=0.5} ")
            .replace(" —", " —{w=0.5}")
            .replace("-", "-{w=0.33}")
            )
    config.say_menu_text_filter = slow_punctuation