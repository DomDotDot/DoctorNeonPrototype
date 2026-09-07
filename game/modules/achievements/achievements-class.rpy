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
    # БЕЗОПАСНАЯ И БЫСТРАЯ ИНИЦИАЛИЗАЦИЯ PERSISTENT (КЭШИРОВАННАЯ)
    # =========================================================================
    _persistent_initialized = False

    def _safe_init_achievements_persistent():
        global _persistent_initialized
        if _persistent_initialized:
            return
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
        if getattr(persistent, "seen_books_set", None) is None:
            persistent.seen_books_set = set()
        if getattr(persistent, "seen_failures_set", None) is None:
            persistent.seen_failures_set = set()
        if getattr(persistent, "invalid_item_use_count", None) is None:
            persistent.invalid_item_use_count = 0
        if getattr(persistent, "hide_achievement_notifications", None) is None:
            persistent.hide_achievement_notifications = True
        if getattr(persistent, "ai_mode_full_run_valid", None) is None:
            persistent.ai_mode_full_run_valid = False
        _persistent_initialized = True

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
            if self.id in persistent.achievements:
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
            if self.icon:
                if renpy.loadable(self.icon) or renpy.has_image(self.icon):
                    return self.icon
                # Fallback для Linux/Android при различиях в регистре символов имени файла
                if "absolutesilence.png" in self.icon.lower():
                    for alt in ("images/achievements/absolutesIlence.png", "images/achievements/absolutesilence.png"):
                        if renpy.loadable(alt) or renpy.has_image(alt):
                            return alt
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

            # Быстрый выход, если достижение уже получено
            if self.id in persistent.achievements:
                return None

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

            # Быстрый выход, если уже получено или amount <= 0
            if self.id in persistent.achievements or amount <= 0:
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

            # Быстрый выход, если уже получено
            if self.id in persistent.achievements:
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
        _safe_init_achievements_persistent()
        # Мгновенный выход за O(1), если уже открыто
        if str(ach_id) in persistent.achievements:
            return None
        ach = get_achievement(ach_id)
        if ach:
            ach.unlock(notify=notify)
        else:
            persistent.achievements[str(ach_id)] = {
                "unlocked": True,
                "timestamp": time.time()
            }
            renpy.save_persistent()
            if notify and not getattr(persistent, "hide_achievement_notifications", True):
                prefix = renpy.translate_string(_("Достижение получено: {}"))
                renpy.notify(prefix.format(ach_id))
            _safe_restart_interaction()
        return None

    def unlock_achievement(ach_id, notify=True):
        return grant_achievement(ach_id, notify=notify)

    def add_achievement_progress(ach_id, amount=1, notify=True):
        _safe_init_achievements_persistent()
        if str(ach_id) in persistent.achievements or amount <= 0:
            return None
        ach = get_achievement(ach_id)
        if ach:
            ach.add_progress(amount=amount, notify=notify)
        else:
            current = persistent.achievements_progress.get(str(ach_id), 0)
            persistent.achievements_progress[str(ach_id)] = current + amount
            renpy.save_persistent()
            _safe_restart_interaction()
        return None

    def set_achievement_progress(ach_id, value, notify=True):
        _safe_init_achievements_persistent()
        if str(ach_id) in persistent.achievements:
            return None
        ach = get_achievement(ach_id)
        if ach:
            ach.set_progress(value=value, notify=notify)
        else:
            val = max(0, int(value))
            current = persistent.achievements_progress.get(str(ach_id), 0)
            if current != val:
                persistent.achievements_progress[str(ach_id)] = val
                renpy.save_persistent()
                _safe_restart_interaction()
        return None

    def has_achievement(ach_id):
        _safe_init_achievements_persistent()
        return str(ach_id) in persistent.achievements

    def get_achievement_progress(ach_id):
        ach = get_achievement(ach_id)
        if ach:
            return (ach.get_progress(), ach.max_progress)
        _safe_init_achievements_persistent()
        return (persistent.achievements_progress.get(str(ach_id), 0), 1)

    def get_achievements_stats():
        _safe_init_achievements_persistent()
        total = len(achievements_list)
        if total == 0:
            return (0, 0, 0)
        unlocked = sum(1 for a in achievements_list if a.id in persistent.achievements)
        percent = int((float(unlocked) / float(total)) * 100)
        return (unlocked, total, percent)

    def show_achievement_notification(ach):
        _safe_init_achievements_persistent()
        if getattr(persistent, "hide_achievement_notifications", True):
            return
        try:
            sound_path = "audio/sfx/keycard-accepted.opus"
            if renpy.loadable(sound_path):
                renpy.sound.play(sound_path, channel="sfx")
        except:
            pass
        renpy.show_screen("achievement_popup_toast", ach=ach)

    def check_platinum_achievement():
        _safe_init_achievements_persistent()
        if "completionist_100" in persistent.achievements:
            return None
        plat_ach = get_achievement("completionist_100")
        if plat_ach:
            if all(a.id in persistent.achievements for a in achievements_list if a.id != "completionist_100"):
                plat_ach.unlock(notify=True)

    def unlock_all_achievements(notify=False):
        for ach in achievements_list:
            ach.unlock(notify=notify)
        renpy.save_persistent()
        renpy.notify(_("Все достижения разблокированы!"))
        _safe_restart_interaction()
        return None

    def reset_all_achievements():
        global _persistent_initialized
        persistent.achievements = {}
        persistent.achievements_progress = {}
        persistent.total_playtime_seconds = 0
        persistent.seen_gallery_cg_set = set()
        persistent.seen_glossary_chars_set = set()
        persistent.inspected_items_set = set()
        persistent.seen_books_set = set()
        persistent.seen_failures_set = set()
        persistent.invalid_item_use_count = 0
        _persistent_initialized = False
        renpy.save_persistent()
        _safe_init_achievements_persistent()
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
        
        _safe_init_achievements_persistent()
        elapsed = time.time() - _current_chapter_start_time
        _current_chapter_start_time = None

        if "dont_rush" not in persistent.achievements and 5.0 < elapsed < 600.0:
            grant_achievement("dont_rush")

        if "without_blinking" not in persistent.achievements and not _current_chapter_paused and elapsed >= 30.0:
            grant_achievement("without_blinking")

        if "absolute_silence" not in persistent.achievements and is_audio_muted():
            grant_achievement("absolute_silence")
        return None

    def track_gallery_cg(cg_name):
        _safe_init_achievements_persistent()
        if "nostalgia" in persistent.achievements or not cg_name:
            return None
        if cg_name not in persistent.seen_gallery_cg_set:
            persistent.seen_gallery_cg_set.add(cg_name)
            add_achievement_progress("nostalgia", 1)
        return None

    def track_bio_char(char_id):
        _safe_init_achievements_persistent()
        if "deep_analysis" in persistent.achievements or not char_id:
            return None
        if char_id not in persistent.seen_glossary_chars_set:
            persistent.seen_glossary_chars_set.add(char_id)
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
        if "criminalist" in persistent.achievements or not item_id:
            return None
        if str(item_id) not in persistent.inspected_items_set:
            persistent.inspected_items_set.add(str(item_id))
            renpy.save_persistent()
            count = len([x for x in ALL_GAME_ITEMS if x in persistent.inspected_items_set])
            set_achievement_progress("criminalist", count, notify=False)
            if count >= len(ALL_GAME_ITEMS):
                grant_achievement("criminalist")
        return None

    def check_notification_center_achievement():
        _safe_init_achievements_persistent()
        if "mail_maniac" in persistent.achievements:
            return None
        if getattr(persistent, "notifications", None) and len(persistent.notifications) >= 1:
            grant_achievement("mail_maniac")
        return None

    def toggle_sensitive_mode_with_check():
        _safe_init_achievements_persistent()
        if "pathological_interest" not in persistent.achievements and not persistent.sensitive_mode:
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
        _safe_init_achievements_persistent()
        if "midnight_shift" in persistent.achievements:
            return None
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
            if "play_16_hours" not in persistent.achievements:
                hours = int(persistent.total_playtime_seconds // 3600)
                current_hours = persistent.achievements_progress.get("play_16_hours", 0)
                if hours != current_hours:
                    set_achievement_progress("play_16_hours", hours, notify=True)

    if getattr(renpy.config, "periodic_callbacks", None) is not None:
        renpy.config.periodic_callbacks.append(_update_playtime_callback)
    elif getattr(renpy.config, "interact_callbacks", None) is not None:
        renpy.config.interact_callbacks.append(_update_playtime_callback)

    # -------------------------------------------------------------------------
    # НОВЫЕ ХУКИ И ТРЕКЕРЫ (С ОПТИМИЗИРОВАННЫМ РАННИМ ВЫХОДОМ)
    # -------------------------------------------------------------------------

    # 1. Трекинг книг в библиотеке ("Книжный Червь")
    def track_library_book(book_id):
        _safe_init_achievements_persistent()
        if "bookworm" in persistent.achievements or not book_id:
            return None
        if str(book_id) not in persistent.seen_books_set:
            persistent.seen_books_set.add(str(book_id))
            renpy.save_persistent()
            count = len(persistent.seen_books_set)
            set_achievement_progress("bookworm", count, notify=True)
        return None

    # 2. Трекинг неудач / поражений ("Хроники неудач")
    def track_failure(fail_id):
        _safe_init_achievements_persistent()
        if "failure_chronicles" in persistent.achievements or not fail_id:
            return None
        if str(fail_id) not in persistent.seen_failures_set:
            persistent.seen_failures_set.add(str(fail_id))
            renpy.save_persistent()
            count = len(persistent.seen_failures_set)
            set_achievement_progress("failure_chronicles", count, notify=True)
        return None

    # 3. Использование неподходящих предметов ("Запасной план")
    def track_invalid_item_use():
        _safe_init_achievements_persistent()
        if "backup_plan" in persistent.achievements:
            return None
        persistent.invalid_item_use_count += 1
        renpy.save_persistent()
        if persistent.invalid_item_use_count >= 5:
            grant_achievement("backup_plan")
        return None

    # 4. Тайминг выборов ("Интуиция детектива" и "Мучительные сомнения")
    _choice_display_time = 0.0

    def on_choice_menu_show():
        global _choice_display_time
        _safe_init_achievements_persistent()
        if "detective_intuition" in persistent.achievements:
            return None
        _choice_display_time = time.time()
        return None

    def on_choice_menu_choice():
        global _choice_display_time
        _safe_init_achievements_persistent()
        if "detective_intuition" in persistent.achievements:
            return None
        if _choice_display_time > 0:
            elapsed = time.time() - _choice_display_time
            if 0.05 <= elapsed <= 1.5:
                grant_achievement("detective_intuition")
            _choice_display_time = 0.0
        return None

    # 5. Сохранения игры ("Синдром Сохранения" - 50 сохранений)
    def on_game_saved_callback():
        _safe_init_achievements_persistent()
        if "save_scummer" in persistent.achievements:
            return None
        add_achievement_progress("save_scummer", 1, notify=True)

    _orig_renpy_save = getattr(renpy, "save", None)
    if _orig_renpy_save is not None:
        def _ach_wrapped_save(*args, **kwargs):
            res = _orig_renpy_save(*args, **kwargs)
            try:
                on_game_saved_callback()
            except:
                pass
            return res
        renpy.save = _ach_wrapped_save

    # 6. Режим кинотеатра (100 строк авточтения подряд без пропуска/ручных кликов)
    _consecutive_afm_lines = 0

    def check_afm_mode_callback(event, interact=True, **kwargs):
        global _consecutive_afm_lines
        _safe_init_achievements_persistent()
        if "cinema_mode" in persistent.achievements:
            return

        if event in ("show", "begin"):
            is_skipping = False
            is_afm = False
            try:
                # Проверяем пропуск диалогов (CTRL / кнопка Пропуск)
                if getattr(renpy, "is_skipping", None) and renpy.is_skipping():
                    is_skipping = True
                elif getattr(renpy.config, "skipping", None):
                    is_skipping = True

                # Проверяем исключительно Авточтение (Auto Forward)
                if not is_skipping:
                    if getattr(renpy, "is_auto_forwarding", None) and renpy.is_auto_forwarding():
                        is_afm = True
            except:
                pass

            if is_afm and not is_skipping:
                _consecutive_afm_lines += 1
                if _consecutive_afm_lines >= 100:
                    grant_achievement("cinema_mode")
            else:
                _consecutive_afm_lines = 0

    if getattr(renpy.config, "all_character_callbacks", None) is not None:
        renpy.config.all_character_callbacks.append(check_afm_mode_callback)

    # 7. Полиглот (смена языка в игре)
    def check_polyglot_on_lang_change():
        _safe_init_achievements_persistent()
        if "polyglot" in persistent.achievements:
            return None
        try:
            if not getattr(store, "main_menu", False):
                grant_achievement("polyglot")
        except:
            pass
        return None
