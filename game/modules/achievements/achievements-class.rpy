init -2 python:
    import time
    import datetime

    # =========================================================================
    # КОНСТАНТЫ ТИПОВ ДОСТИЖЕНИЙ
    # =========================================================================
    ACH_TYPE_NORMAL = "normal"      # 1. Явный (обычный): видна иконка, имя, описание.
    ACH_TYPE_HIDDEN = "hidden"      # 2. Скрытый: до получения видны только иконка и имя (описание скрыто).
    ACH_TYPE_TRACKING = "tracking"  # 3. Трекинг: пошаговый прогресс (0 / max_progress), авто-анлок.

    # =========================================================================
    # БЕЗОПАСНАЯ ИНИЦИАЛИЗАЦИЯ PERSISTENT
    # =========================================================================
    def _safe_init_achievements_persistent():
        if getattr(persistent, "achievements", None) is None:
            persistent.achievements = {}
        if getattr(persistent, "achievements_progress", None) is None:
            persistent.achievements_progress = {}
        if getattr(persistent, "total_playtime_seconds", None) is None:
            persistent.total_playtime_seconds = 0
        if getattr(persistent, "seen_gallery_cg_set", None) is None:
            persistent.seen_gallery_cg_set = set()
        if getattr(persistent, "seen_glossary_chars_set", None) is None:
            persistent.seen_glossary_chars_set = set()
        if getattr(persistent, "inspected_items_set", None) is None:
            persistent.inspected_items_set = set()
        if getattr(persistent, "ai_mode_full_run_valid", None) is None:
            persistent.ai_mode_full_run_valid = False

    _safe_init_achievements_persistent()

    def _safe_restart_interaction():
        try:
            renpy.restart_interaction()
        except:
            pass

    # =========================================================================
    # КЛАСС ДОСТИЖЕНИЯ
    # =========================================================================
    class Achievement(object):
        def __init__(self, id, name, description, icon=None, ach_type=ACH_TYPE_NORMAL, 
                     max_progress=1, hidden_desc=None, category=None):
            self.id = str(id)
            self.name = name
            self.description = description
            self.icon = icon
            self.ach_type = ach_type
            self.max_progress = max(1, int(max_progress))
            self.hidden_desc = hidden_desc if hidden_desc is not None else _("Скрытое достижение. Разблокируйте, чтобы узнать подробности.")
            self.category = category

        def is_unlocked(self):
            _safe_init_achievements_persistent()
            return self.id in persistent.achievements

        def get_progress(self):
            _safe_init_achievements_persistent()
            if self.is_unlocked():
                return self.max_progress
            val = persistent.achievements_progress.get(self.id, 0)
            return min(self.max_progress, max(0, val))

        def get_progress_fraction(self):
            if self.max_progress <= 0:
                return 1.0 if self.is_unlocked() else 0.0
            return float(self.get_progress()) / float(self.max_progress)

        def get_display_name(self):
            return renpy.translate_string(self.name)

        def get_display_description(self):
            if self.ach_type == ACH_TYPE_HIDDEN and not self.is_unlocked():
                return renpy.translate_string(self.hidden_desc)
            return renpy.translate_string(self.description)

        def get_icon_displayable(self):
            if self.icon and (renpy.loadable(self.icon) or renpy.has_image(self.icon)):
                return self.icon
            if self.is_unlocked():
                return "ach_default_icon_unlocked"
            return "ach_default_icon_locked"

        def get_unlock_time_string(self):
            if not self.is_unlocked():
                return ""
            _safe_init_achievements_persistent()
            info = persistent.achievements.get(self.id)
            if isinstance(info, dict) and "timestamp" in info:
                try:
                    t = time.localtime(info["timestamp"])
                    return time.strftime("%d.%m.%Y %H:%M", t)
                except:
                    pass
            return renpy.translate_string(_("Получено"))

        def unlock(self, notify=True):
            _safe_init_achievements_persistent()

            if self.id not in persistent.achievements:
                persistent.achievements[self.id] = {
                    "unlocked": True,
                    "timestamp": time.time()
                }
                persistent.achievements_progress[self.id] = self.max_progress
                renpy.save_persistent()

                if notify:
                    show_achievement_notification(self)
                
                _safe_restart_interaction()

                if self.id != "completionist_100":
                    check_platinum_achievement()
            return None

        def add_progress(self, amount=1, notify=True):
            _safe_init_achievements_persistent()

            if self.is_unlocked() or amount <= 0:
                return None

            current = persistent.achievements_progress.get(self.id, 0)
            new_val = current + amount
            persistent.achievements_progress[self.id] = new_val
            renpy.save_persistent()

            if new_val >= self.max_progress:
                self.unlock(notify=notify)
            else:
                _safe_restart_interaction()
            return None

        def set_progress(self, value, notify=True):
            _safe_init_achievements_persistent()

            if self.is_unlocked():
                return None

            val = max(0, int(value))
            current = persistent.achievements_progress.get(self.id, 0)
            if current == val:
                return None # Значение не изменилось

            persistent.achievements_progress[self.id] = val
            renpy.save_persistent()

            if val >= self.max_progress:
                self.unlock(notify=notify)
            else:
                _safe_restart_interaction()
            return None

    # =========================================================================
    # РЕЕСТР И МЕТОДЫ УПРАВЛЕНИЯ
    # =========================================================================
    achievements_list = []
    achievements_map = {}

    def register_achievement(ach):
        global achievements_list, achievements_map
        if ach.id in achievements_map:
            achievements_list = [a for a in achievements_list if a.id != ach.id]
        achievements_list.append(ach)
        achievements_map[ach.id] = ach
        return ach

    def get_achievement(ach_id):
        return achievements_map.get(str(ach_id), None)

    def grant_achievement(ach_id, notify=True):
        ach = get_achievement(ach_id)
        if ach:
            ach.unlock(notify=notify)
        else:
            _safe_init_achievements_persistent()
            if str(ach_id) not in persistent.achievements:
                persistent.achievements[str(ach_id)] = {
                    "unlocked": True,
                    "timestamp": time.time()
                }
                renpy.save_persistent()
                if notify:
                    prefix = renpy.translate_string(_("Достижение получено: {}"))
                    renpy.notify(prefix.format(ach_id))
                _safe_restart_interaction()
        return None

    def unlock_achievement(ach_id, notify=True):
        return grant_achievement(ach_id, notify=notify)

    def add_achievement_progress(ach_id, amount=1, notify=True):
        ach = get_achievement(ach_id)
        if ach:
            ach.add_progress(amount=amount, notify=notify)
        else:
            _safe_init_achievements_persistent()
            current = persistent.achievements_progress.get(str(ach_id), 0)
            persistent.achievements_progress[str(ach_id)] = current + amount
            renpy.save_persistent()
            _safe_restart_interaction()
        return None

    def set_achievement_progress(ach_id, value, notify=True):
        ach = get_achievement(ach_id)
        if ach:
            ach.set_progress(value=value, notify=notify)
        else:
            _safe_init_achievements_persistent()
            val = max(0, int(value))
            current = persistent.achievements_progress.get(str(ach_id), 0)
            if current != val:
                persistent.achievements_progress[str(ach_id)] = val
                renpy.save_persistent()
                _safe_restart_interaction()
        return None

    def has_achievement(ach_id):
        ach = get_achievement(ach_id)
        if ach:
            return ach.is_unlocked()
        _safe_init_achievements_persistent()
        return str(ach_id) in persistent.achievements

    def get_achievement_progress(ach_id):
        ach = get_achievement(ach_id)
        if ach:
            return (ach.get_progress(), ach.max_progress)
        _safe_init_achievements_persistent()
        return (persistent.achievements_progress.get(str(ach_id), 0), 1)

    def get_achievements_stats():
        total = len(achievements_list)
        if total == 0:
            return (0, 0, 0)
        unlocked = sum(1 for a in achievements_list if a.is_unlocked())
        percent = int((float(unlocked) / float(total)) * 100)
        return (unlocked, total, percent)

    def show_achievement_notification(ach):
        try:
            sound_path = "audio/sfx/keycard-accepted.opus"
            if renpy.loadable(sound_path):
                renpy.sound.play(sound_path, channel="sfx")
        except:
            pass
        renpy.show_screen("achievement_popup_toast", ach=ach)

    def check_platinum_achievement():
        plat_ach = get_achievement("completionist_100")
        if plat_ach and not plat_ach.is_unlocked():
            other_achs = [a for a in achievements_list if a.id != "completionist_100"]
            if other_achs and all(a.is_unlocked() for a in other_achs):
                plat_ach.unlock(notify=True)

    def unlock_all_achievements(notify=False):
        for ach in achievements_list:
            ach.unlock(notify=notify)
        renpy.save_persistent()
        renpy.notify(_("Все достижения разблокированы!"))
        _safe_restart_interaction()
        return None

    def reset_all_achievements():
        persistent.achievements = {}
        persistent.achievements_progress = {}
        persistent.total_playtime_seconds = 0
        persistent.seen_gallery_cg_set = set()
        persistent.seen_glossary_chars_set = set()
        renpy.save_persistent()
        renpy.notify(_("Прогресс достижений сброшен."))
        _safe_restart_interaction()
        return None

    # =========================================================================
    # ВСПОМОГАТЕЛЬНЫЕ ХУКИ ДЛЯ ИГРОВЫХ АЧИВОК
    # =========================================================================

    _current_chapter_start_time = None
    _current_chapter_paused = False

    def is_audio_muted():
        try:
            if preferences.get_mute("all") or preferences.get_mute("music"):
                return True
            vol_m = preferences.volumes.get("music", 1.0)
            vol_s = preferences.volumes.get("sfx", 1.0)
            if vol_m == 0.0 and vol_s == 0.0:
                return True
        except:
            pass
        return False

    def start_chapter_tracking():
        global _current_chapter_start_time, _current_chapter_paused
        if _current_chapter_start_time is not None:
            finish_chapter_tracking()
        _current_chapter_start_time = time.time()
        _current_chapter_paused = False
        return None

    def mark_pause_opened():
        global _current_chapter_paused
        _current_chapter_paused = True
        return None

    def finish_chapter_tracking():
        global _current_chapter_start_time, _current_chapter_paused
        if _current_chapter_start_time is None:
            return None
        
        elapsed = time.time() - _current_chapter_start_time
        _current_chapter_start_time = None

        if elapsed > 5.0 and elapsed < 600.0:
            grant_achievement("dont_rush")

        if not _current_chapter_paused and elapsed >= 30.0:
            grant_achievement("without_blinking")

        if is_audio_muted():
            grant_achievement("absolute_silence")
        return None

    def track_gallery_cg(cg_name):
        _safe_init_achievements_persistent()
        if cg_name and cg_name not in persistent.seen_gallery_cg_set:
            persistent.seen_gallery_cg_set.add(cg_name)
            renpy.save_persistent()
            add_achievement_progress("nostalgia", 1)
        return None

    def track_bio_char(char_id):
        _safe_init_achievements_persistent()
        if char_id and char_id not in persistent.seen_glossary_chars_set:
            persistent.seen_glossary_chars_set.add(char_id)
            renpy.save_persistent()
            add_achievement_progress("deep_analysis", 1)
        return None

    ALL_GAME_ITEMS = [
        "maintenance_keycard",
        "uncharged_battery",
        "charged_battery",
        "bartender_uniform",
        "blank_chip",
        "reagent_a",
        "reagent_b",
        "coolant",
        "bio_spray",
        "admin_chip",
        "reagent_d",
        "mop",
        "empty_spray"
    ]

    def track_item_inspected(item_id):
        _safe_init_achievements_persistent()
        if item_id:
            persistent.inspected_items_set.add(str(item_id))
            renpy.save_persistent()
            count = len([x for x in ALL_GAME_ITEMS if x in persistent.inspected_items_set])
            set_achievement_progress("criminalist", count, notify=False)
            if count >= len(ALL_GAME_ITEMS):
                grant_achievement("criminalist")
        return None

    def check_notification_center_achievement():
        _safe_init_achievements_persistent()
        if getattr(persistent, "notifications", None) and len(persistent.notifications) >= 1:
            grant_achievement("mail_maniac")
        return None

    def toggle_sensitive_mode_with_check():
        if not persistent.sensitive_mode:
            if renpy.showing("cg-36-1") or renpy.showing("cg-36-1a") or renpy.showing("featured_cg-36-1b"):
                grant_achievement("pathological_interest")
        persistent.sensitive_mode = not persistent.sensitive_mode
        renpy.save_persistent()
        _safe_restart_interaction()
        return None

    def toggle_ai_sensitive_with_check():
        persistent.ai_sensitive_mode = not persistent.ai_sensitive_mode
        if not persistent.ai_sensitive_mode:
            persistent.ai_mode_full_run_valid = False
        renpy.save_persistent()
        _safe_restart_interaction()
        return None

    # Проверка полуночи (вызывается безопасно)
    def check_midnight_shift():
        if datetime.datetime.now().hour in (1, 2, 3, 4):
            grant_achievement("midnight_shift")
        return None

    # Трекинг времени в игре (16 часов) - с защитой от частых вызовов
    _last_playtime_timestamp = time.time()

    def _update_playtime_callback():
        global _last_playtime_timestamp
        now = time.time()
        delta = now - _last_playtime_timestamp
        if delta < 1.0:
            return
        _last_playtime_timestamp = now

        if 0 < delta < 120:
            _safe_init_achievements_persistent()
            persistent.total_playtime_seconds += delta
            hours = int(persistent.total_playtime_seconds // 3600)
            current_hours = persistent.achievements_progress.get("play_16_hours", 0)
            if hours != current_hours:
                set_achievement_progress("play_16_hours", hours, notify=True)

    if hasattr(config, "periodic_callbacks"):
        config.periodic_callbacks.append(_update_playtime_callback)
    else:
        config.interact_callbacks.append(_update_playtime_callback)
