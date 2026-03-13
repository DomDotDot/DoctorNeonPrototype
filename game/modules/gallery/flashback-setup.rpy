default persistent.flashback_zurich_1_unlocked = False
default persistent.flashback_zurich_2_unlocked = False

default persistent.flashback_krypton_1_unlocked = False
default persistent.flashback_krypton_2_unlocked = False
default persistent.flashback_krypton_3_unlocked = False

default persistent.flashback_oganesson_1_unlocked = False

default persistent.flashback_dream_1_unlocked = False
default persistent.flashback_dream_2_unlocked = False
default persistent.flashback_dream_3_unlocked = False
default persistent.flashback_dream_4_unlocked = False
default persistent.flashback_dream_5_unlocked = False
default persistent.flashback_dream_6_unlocked = False

default persistent.prestory_nari_unlocked = False
default persistent.prestory_kai_unlocked = False
default persistent.prestory_lily_unlocked = False
default persistent.prestory_penthouse_unlocked = False
default persistent.prestory_seraphina_unlocked = False

default persistent.cutcene_vol_1_end_unlocked = False

init python:

    class FlashbackItem:
        def __init__(self, name, label, thumb=None, condition=None):
            self.name = name
            self.label = label
            self.thumb = thumb
            self.condition = condition 

        def is_unlocked(self):
            if persistent.unlock_gallery:
                return True
            if self.condition:
                return getattr(persistent, self.condition, False)
            return False

        def get_thumbnail_displayable(self):
            if self.is_unlocked():
                if self.thumb:
                    return Transform(self.thumb, fit="cover", size=(384, 216))
                else:
                    return renpy.displayable("gallery_locked_thumb")
            else:
                return renpy.displayable("gallery_locked_thumb")

    flashback_items = []

    def add_flashback(name, label, thumb=None, condition=None):
        flashback_items.append(FlashbackItem(name, label, thumb, condition))

    # --- DEFINITION OF FLASHBACKS ---
    # Add flashbacks here
    
    # Example:
    # add_flashback(_("Zurich University"), "zurich_university_flashback_1", condition="flashback_zurich_1_unlocked")
    
    add_flashback(
        _("Университет в Цюрихе"), 
        "zurich_university_flashback_1", 
        thumb="ch01_cg16_v02",
        condition="flashback_zurich_1_unlocked"
    ),

    add_flashback(
        _("Концерт в Цюрихе"), 
        "zurich_university_flashback_2", 
        thumb="7a-cg-5",
        condition="flashback_zurich_2_unlocked"
    ),

    add_flashback(
        _("Концерт для Одной"), 
        "krypton_concert_flashback", 
        thumb="ch01_cg05_v01",
        condition="flashback_krypton_1_unlocked"
    ),

    add_flashback(
        _("Колокола"), 
        "chapter1_krypton_baddream", 
        thumb="ch01_cg06_v01",
        condition="flashback_krypton_2_unlocked"
    ),

    add_flashback(
        _("Несдержанное Обещание"), 
        "krypton_firstmeet_flashback", 
        thumb="ch01_cg09_v01",
        condition="flashback_krypton_3_unlocked"
    ),

    add_flashback(
        _("Школа"), 
        "oganesson_school_flashback_1", 
        thumb="ch01_cg23_v01",
        condition="flashback_oganesson_1_unlocked"
    ),

    add_flashback(
        _("Фрагмент 1"), 
        "dream_sequence_japan_1", 
        thumb="cg-16",
        condition="flashback_dream_1_unlocked"
    ),

    add_flashback(
        _("Фрагмент 2"), 
        "dream_sequence_japan_2", 
        thumb="cg-28_1",
        condition="flashback_dream_2_unlocked"
    ),

    add_flashback(
        _("Фрагмент 3"), 
        "dream_sequence_japan_3", 
        thumb="cg-28_4",
        condition="flashback_dream_3_unlocked"
    ),

    add_flashback(
        _("Фрагмент 4"), 
        "dream_sequence_japan_4", 
        thumb="featured_7a-cg-2",
        condition="flashback_dream_4_unlocked"
    ),

    add_flashback(
        _("Фрагмент 5"), 
        "dream_sequence_japan_5", 
        thumb="7a-cg-5",
        condition="flashback_dream_5_unlocked"
    ),

    add_flashback(
        _("Фрагмент 6"), 
        "dream_sequence_japan_6", 
        thumb="7a-cg-5",
        condition="flashback_dream_6_unlocked"
    ),

    add_flashback(
        _("Предыстория Нари"), 
        "chapter4_5_nari_flashback", 
        thumb="featured_cg-34",
        condition="prestory_nari_unlocked"
    ),

    add_flashback(
        _("Предыстория Кая"), 
        "chapter4_5_kai_ito_interlude", 
        thumb="7a-cg-5",
        condition="prestory_kai_unlocked"
    ),

    add_flashback(
        _("Предыстория Лили"), 
        "chapter4_5_lily_flashback", 
        thumb="featured_10cg-1-1",
        condition="prestory_lily_unlocked"
    ),

    add_flashback(
        _("Пентхаус"), 
        "chapter4_5_seraphina_penthouse", 
        thumb="featured_5cg-3",
        condition="prestory_penthouse_unlocked"
    ),

    add_flashback(
        _("Предыстория Лже-Серафины"), 
        "chapter4_5_seraphina_flashback", 
        thumb="10cg-3-3",
        condition="prestory_seraphina_unlocked"
    ),

    add_flashback(
        _("Развороченный Улей"), 
        "secret_scene_vol1", 
        thumb="12cg-2",
        condition="cutcene_vol_1_end_unlocked"
    ),