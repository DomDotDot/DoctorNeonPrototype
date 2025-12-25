# Для BG
#image bg bedroom = ConditionSwitch(
    # Условие 1: Если режим 18+ включен
#    "persistent.sensitive_mode == True", "images/backgrounds/bedroom_naked.avif",
    
    # Условие 2: Во всех остальных случаях (True здесь значит "иначе")
#    "True", "images/bg/bedroom_clean.avif"
#)

# для CG
image cg-36-1 = ConditionSwitch(
    "persistent.sensitive_mode", "images/cg/vol1/cg-36-1a.avif",
    "True", "images/cg/vol1/cg--36-1b.avif"
)