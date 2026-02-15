default persistent.flashback_zurich_1_unlocked = False

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

        def get_thumbnail(self):
            if self.is_unlocked():
                if self.thumb:
                    return self.thumb
                else:
                    return "gallery_locked_thumb" # Usage of generic thumb if specific not provided
            else:
                return "gallery_locked_thumb"

    flashback_items = []

    def add_flashback(name, label, thumb=None, condition=None):
        flashback_items.append(FlashbackItem(name, label, thumb, condition))

    # --- DEFINITION OF FLASHBACKS ---
    # Add flashbacks here
    
    # Example:
    # add_flashback(_("Zurich University"), "zurich_university_flashback_1", condition="flashback_zurich_1_unlocked")
    
    add_flashback(_("Университет в Цюрихе"), "zurich_university_flashback_1", condition="flashback_zurich_1_unlocked")
