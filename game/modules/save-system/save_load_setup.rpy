################################################################################
## Модуль системы сохранений и загрузки (Save & Load System Setup)
## Doctor Neon Prototype - Cyber-Glassmorphic Save Architecture
################################################################################

default save_current_chapter_number = "Пролог"
default save_current_chapter_title = ""
default save_selected_category = "manual"
default save_current_page = 1
default save_chapter_filter = "all"
default save_selected_slot = "1-1"
default save_current_mode = "save"
default save_modal_state = None

init -1 python:
    import datetime

    # Регистрация колбэка для сохранения расширенных метаданных в JSON сейва
    def dn_save_json_callback(d):
        d["version"] = str(config.version)
        d["chapter_number"] = str(getattr(store, "save_current_chapter_number", "Пролог"))
        d["chapter_title"] = str(getattr(store, "save_current_chapter_title", ""))
        
        # Захват последней произнесённой реплики для превью диалога
        try:
            if hasattr(store, "_history_list") and store._history_list:
                last_h = store._history_list[-1]
                d["last_who"] = str(last_h.who or "")
                d["last_what"] = str(last_h.what or "")
            else:
                d["last_who"] = ""
                d["last_what"] = ""
        except:
            d["last_who"] = ""
            d["last_what"] = ""

    if dn_save_json_callback not in config.save_json_callbacks:
        config.save_json_callbacks.append(dn_save_json_callback)

    def update_chapter_save_info(chap_text, tit_text):
        """Обновляет метаданные текущей главы при показе экрана главы."""
        store.save_current_chapter_number = str(chap_text)
        store.save_current_chapter_title = str(tit_text) if tit_text else ""
        store.save_name = str(chap_text) + ((" - " + str(tit_text)) if tit_text else "")

    def format_slot_label(slot_str):
        """Возвращает форматированное имя слота."""
        if not slot_str:
            return ""
        s = str(slot_str)
        if s.startswith("auto-"):
            return _("АВТО ") + s.replace("auto-", "#")
        elif s.startswith("quick-"):
            return _("QUICK ") + s.replace("quick-", "#")
        else:
            return _("СЛОТ ") + s

    def get_save_slot_info(slot):
        """
        Возвращает нормализованный словарь метаданных для слота сохранения.
        Полностью совместим как с новыми сейвами, так и со старыми/архивными.
        Все поля гарантированно являются строками или булевыми значениями.
        """
        if not slot:
            return {
                "slot": "",
                "exists": False,
                "is_empty": True,
                "slot_label": "",
                "version": "",
                "current_version": str(config.version),
                "is_version_match": True,
                "chapter_number": "",
                "chapter_title": "",
                "full_chapter": _("Слот не выбран"),
                "time_str": _("Нет данных"),
                "short_time": "",
                "runtime_str": "--:--",
                "last_who": "",
                "last_what": "",
                "mtime": 0
            }
        
        slot_str = str(slot)
        if not renpy.can_load(slot_str):
            return {
                "slot": slot_str,
                "exists": False,
                "is_empty": True,
                "slot_label": str(format_slot_label(slot_str)),
                "version": "",
                "current_version": str(config.version),
                "is_version_match": True,
                "chapter_number": "",
                "chapter_title": "",
                "full_chapter": _("Свободный слот"),
                "time_str": _("Нет данных"),
                "short_time": "",
                "runtime_str": "--:--",
                "last_who": "",
                "last_what": "",
                "mtime": 0
            }

        try:
            meta = renpy.slot_json(slot_str) or {}
        except:
            meta = {}
        mtime = renpy.slot_mtime(slot_str)

        # Определение версии сейва (из custom 'version' или Ren'Py '_version')
        save_ver = str(meta.get("version") or meta.get("_version") or "")
        curr_ver = str(config.version)
        is_version_match = (save_ver == curr_ver) if save_ver else True

        # Определение названия сохранения / главы
        chap_num = meta.get("chapter_number")
        chap_tit = meta.get("chapter_title")
        
        save_name_val = meta.get("_save_name")
        if not save_name_val:
            try:
                scan_res = renpy.scan_saved_game(slot_str)
                if scan_res and isinstance(scan_res, (list, tuple)) and len(scan_res) > 0:
                    if isinstance(scan_res[0], str):
                        save_name_val = scan_res[0]
            except:
                save_name_val = ""

        if not chap_num:
            if save_name_val and isinstance(save_name_val, str) and save_name_val.strip():
                chap_num = save_name_val.strip()
                chap_tit = ""
            else:
                chap_num = _("Сюжетное сохранение")
                chap_tit = _("Архивная запись")

        chap_num_str = str(chap_num)
        chap_tit_str = str(chap_tit) if chap_tit else ""
        if chap_tit_str.strip():
            full_chapter = chap_num_str + " — " + chap_tit_str
        else:
            full_chapter = chap_num_str

        # Время в игре
        runtime = meta.get("_game_runtime", 0)
        try:
            runtime = float(runtime)
        except:
            runtime = 0.0
        hours = int(runtime // 3600)
        mins = int((runtime % 3600) // 60)
        if hours > 0:
            runtime_str = str(hours) + _(" ч ") + str(mins) + _(" мин")
        else:
            runtime_str = str(mins) + _(" мин")

        # Время сохранения
        if mtime:
            dt = datetime.datetime.fromtimestamp(mtime)
            time_str = dt.strftime("%d.%m.%Y, %H:%M")
            short_time = dt.strftime("%d.%m.%y %H:%M")
        else:
            time_str = _("Время неизвестно")
            short_time = ""

        last_who = str(meta.get("last_who", ""))
        last_what = str(meta.get("last_what", ""))

        return {
            "slot": slot_str,
            "exists": True,
            "is_empty": False,
            "slot_label": str(format_slot_label(slot_str)),
            "version": save_ver,
            "current_version": curr_ver,
            "is_version_match": is_version_match,
            "chapter_number": chap_num_str,
            "chapter_title": chap_tit_str,
            "full_chapter": str(full_chapter),
            "time_str": str(time_str),
            "short_time": str(short_time),
            "runtime_str": str(runtime_str),
            "last_who": last_who,
            "last_what": last_what,
            "mtime": mtime or 0
        }

    def get_manual_page_slots(page, count=6):
        """Возвращает список идентификаторов слотов для указанной страницы."""
        try:
            p = int(page)
        except:
            p = 1
        return ["{}-{}".format(p, i) for i in range(1, count + 1)]

    def get_special_slots(prefix, max_slots=10):
        """Возвращает список специальных слотов (auto или quick), отсортированных по дате."""
        slots = ["{}-{}".format(prefix, i) for i in range(1, max_slots + 1)]
        def sort_key(s):
            m = renpy.slot_mtime(s)
            return (1 if m else 0, m or 0)
        return sorted(slots, key=sort_key, reverse=True)

    def get_recent_slots(limit=18):
        """Возвращает все существующие слоты игры, отсортированные от новых к старым."""
        try:
            all_slots = renpy.list_saved_games(fast=True)
        except:
            all_slots = []
        
        valid = []
        for s in all_slots:
            if s.startswith("_reload") or s.startswith("_trace"):
                continue
            m = renpy.slot_mtime(s)
            if m:
                valid.append((s, m))
        
        valid.sort(key=lambda x: x[1], reverse=True)
        return [x[0] for x in valid[:limit]]

    def get_known_save_chapters():
        """Собирает список всех уникальных номеров глав из существующих сохранений для фильтра."""
        try:
            all_slots = renpy.list_saved_games(fast=True)
        except:
            all_slots = []
        
        chapters = set()
        for s in all_slots:
            if s.startswith("_reload") or s.startswith("_trace"):
                continue
            meta = renpy.slot_json(s)
            if meta and isinstance(meta, dict):
                chap = meta.get("chapter_number")
                if chap and isinstance(chap, str) and chap.strip():
                    chapters.add(chap.strip())
        
        return sorted(list(chapters))

    # Прямые функции движка сохранения, загрузки и удаления
    def execute_slot_save(slot_str):
        if not slot_str or main_menu:
            return
        slot = str(slot_str)
        if slot.startswith("auto-"):
            renpy.notify(_("Нельзя вручную перезаписывать слот автосохранения."))
            return

        # Синхронизация системного номера страницы для движка Ren'Py
        try:
            persistent._file_page = str(getattr(store, "save_current_page", 1))
        except:
            pass

        s_name = str(getattr(store, "save_name", ""))
        try:
            with renpy.savelocation.SyncfsLock():
                renpy.save(slot, extra_info=s_name)

            if renpy.can_load(slot):
                renpy.notify(_("Игра сохранена в ") + format_slot_label(slot))
            else:
                renpy.notify(_("Внимание: запись слота не завершена."))
        except Exception as e:
            renpy.notify(_("Ошибка при сохранении: ") + str(e))

        renpy.restart_interaction()

    def execute_slot_load(slot_str):
        if not slot_str:
            return
        slot = str(slot_str)
        if not renpy.can_load(slot):
            return
        if config.autosave_on_quit and not slot.startswith("auto-"):
            renpy.loadsave.force_autosave()
        renpy.load(slot)

    def execute_slot_delete(slot_str):
        if not slot_str:
            return
        slot = str(slot_str)
        if not renpy.can_load(slot):
            return
        try:
            with renpy.savelocation.SyncfsLock():
                renpy.unlink_save(slot)
            renpy.notify(_("Сохранение удалено: ") + format_slot_label(slot))
        except Exception as e:
            renpy.notify(_("Ошибка удаления: ") + str(e))
        renpy.restart_interaction()

    # Запросы на сохранение, загрузку и удаление с вызовом реактивного модального окна
    def request_slot_save(slot_str):
        if not slot_str or main_menu:
            return
        slot = str(slot_str)
        if slot.startswith("auto-"):
            renpy.notify(_("Нельзя вручную перезаписывать слот автосохранения."))
            return

        if renpy.can_load(slot):
            info = get_save_slot_info(slot)
            time_str = info.get("time_str", "")
            store.save_modal_state = {
                "type": "overwrite",
                "slot": slot,
                "title": _("ПЕРЕЗАПИСЬ СЛОТА"),
                "message": _("В слоте {slot_name} уже есть сохранение (от {time}).\nПерезаписать его?").format(slot_name=format_slot_label(slot), time=time_str),
                "is_danger": False
            }
        else:
            execute_slot_save(slot)
        renpy.restart_interaction()

    def request_slot_load(slot_str):
        if not slot_str or not renpy.can_load(str(slot_str)):
            return
        slot = str(slot_str)
        info = get_save_slot_info(slot)
        save_ver = info.get("version", "")
        curr_ver = info.get("current_version", "")

        # Если версия не совпадает — реактивное окно предупреждения
        if save_ver and save_ver != curr_ver:
            store.save_modal_state = {
                "type": "version_warning",
                "slot": slot,
                "title": _("НЕСОВПАДЕНИЕ ВЕРСИЙ"),
                "save_ver": str(save_ver),
                "curr_ver": str(curr_ver),
                "message": _("Внимание! Это сохранение создано в другой версии новеллы. Загрузка данных из другой версии может привести к непредвиденным ошибкам, сбоям в сценарии или пропуску сюжетных переменных.\n\nВы действительно хотите продолжить загрузку?"),
                "is_danger": True
            }
        elif not main_menu:
            store.save_modal_state = {
                "type": "load",
                "slot": slot,
                "title": _("ЗАГРУЗКА ИГРЫ"),
                "message": _("Загрузить сохранение {slot_name}?\nНесохранённый прогресс текущей сессии будет утерян.").format(slot_name=format_slot_label(slot)),
                "is_danger": False
            }
        else:
            execute_slot_load(slot)
        renpy.restart_interaction()

    def request_slot_delete(slot_str):
        if not slot_str or not renpy.can_load(str(slot_str)):
            return
        slot = str(slot_str)
        info = get_save_slot_info(slot)
        time_str = info.get("time_str", "")
        store.save_modal_state = {
            "type": "delete",
            "slot": slot,
            "title": _("УДАЛЕНИЕ СОХРАНЕНИЯ"),
            "message": _("Безвозвратно удалить сохранение {slot_name} (от {time})?").format(slot_name=format_slot_label(slot), time=time_str),
            "is_danger": True
        }
        renpy.restart_interaction()

    # Классы действий для поддержки get_sensitive в интерфейсе
    class SmartFileLoad(Action):
        def __init__(self, slot):
            self.slot = slot
        def __call__(self):
            request_slot_load(self.slot)
        def get_sensitive(self):
            return bool(self.slot and renpy.can_load(str(self.slot)))

    class SmartFileSave(Action):
        def __init__(self, slot):
            self.slot = slot
        def __call__(self):
            request_slot_save(self.slot)
        def get_sensitive(self):
            if not self.slot or main_menu:
                return False
            if str(self.slot).startswith("auto-"):
                return False
            return True

    class SmartFileDelete(Action):
        def __init__(self, slot):
            self.slot = slot
        def __call__(self):
            request_slot_delete(self.slot)
        def get_sensitive(self):
            return bool(self.slot and renpy.can_load(str(self.slot)))
