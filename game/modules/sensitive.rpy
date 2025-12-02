# Определяем картинку "bg bedroom"
image bg bedroom = ConditionSwitch(
    # Условие 1: Если режим 18+ включен
    "persistent.sensitive_mode == True", "images/backgrounds/bedroom_naked.webp",
    
    # Условие 2: Во всех остальных случаях (True здесь значит "иначе")
    "True", "images/bg/bedroom_clean.webp"
)

# То же самое для CG (персонажей)
image cg cg36-1 = ConditionSwitch(
    "persistent.sensitive_mode", "images/cg/cg cg36-1a.webp",
    "True", "images/cg/cg cg-36-1b.webp"
)