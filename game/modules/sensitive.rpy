# Определяем картинку "bg bedroom"
image bg bedroom = ConditionSwitch(
    # Условие 1: Если режим 18+ включен
    "persistent.sensitive_mode == True", "images/backgrounds/bedroom_naked.jpg",
    
    # Условие 2: Во всех остальных случаях (True здесь значит "иначе")
    "True", "images/bg/bedroom_clean.jpg"
)

# То же самое для CG (персонажей)
image cg cg36-1 = ConditionSwitch(
    "persistent.sensitive_mode", "images/cg/cg cg36-1a.jpg",
    "True", "images/cg/cg cg-36-1b.jpg"
)