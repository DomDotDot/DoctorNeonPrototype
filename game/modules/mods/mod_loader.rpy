# ==============================================================================
# Doctor Neon - Community Content & Mod Loader Core
# ==============================================================================

# Персистентные переменные (по умолчанию выключены)
default persistent.community_content_enabled = False
default persistent.enabled_mods = []
default persistent.mod_priorities = {}
default persistent.mod_settings = {}

init -995 python:
    import os
    import json
    import shutil

    MODS_FOLDER_NAME = "mods"
    
    def get_mods_dir():
        """Возвращает абсолютный путь к папке mods/ в корне проекта."""
        return os.path.normpath(os.path.join(config.basedir, MODS_FOLDER_NAME))

    def ensure_mods_dir():
        """Гарантирует существование папки mods/."""
        mdir = get_mods_dir()
        if not os.path.exists(mdir):
            try:
                os.makedirs(mdir)
            except Exception as e:
                print(f"[ModLoader] Ошибка создания папки mods: {e}")
        return mdir

    # Список обнаруженных модов в памяти
    _discovered_mods = []
    _discovered_translations = []

    # Состояние поиска и фильтрации
    mod_search_query = ""
    mod_category_filter = "all" # "all", "translation", "asset_replacement", "script", "modular", "active"
    mod_sort_mode = "priority" # "priority", "name", "author"

    # ==========================================================================
    # Mod Hook & Overlay API
    # ==========================================================================
    _mod_hooks = {}
    _registered_mod_overlays = []

    def register_mod_hook(event_name, callback_fn):
        """
        Регистрирует функцию обратного вызова на событие mod hook.
        Пример: register_mod_hook("cyber_pulse", my_callback)
        """
        global _mod_hooks
        if event_name not in _mod_hooks:
            _mod_hooks[event_name] = []
        if callback_fn not in _mod_hooks[event_name]:
            _mod_hooks[event_name].append(callback_fn)

    def trigger_mod_hooks(event_name, *args, **kwargs):
        """
        Безопасно вызывает все зарегистрированные обработчики события.
        """
        if not getattr(persistent, "community_content_enabled", False):
            return
        callbacks = _mod_hooks.get(event_name, [])
        for cb in callbacks:
            try:
                cb(*args, **kwargs)
            except Exception as e:
                print(f"[ModLoader] Ошибка выполнения хука {event_name}: {e}")

    def register_mod_overlay(screen_name, mod_id=None, category="main_menu", order=0):
        """
        Регистрирует экран оверлея из мода.
        category: "main_menu", "ingame", "all"
        """
        global _registered_mod_overlays
        for entry in _registered_mod_overlays:
            if entry["screen"] == screen_name and entry["category"] == category:
                return
        _registered_mod_overlays.append({
            "screen": screen_name,
            "mod_id": mod_id,
            "category": category,
            "order": order
        })
        _registered_mod_overlays.sort(key=lambda x: x["order"])

    def get_active_mod_overlays(category="main_menu"):
        """
        Возвращает список имен экранов для активных модов в указанной категории.
        """
        if not getattr(persistent, "community_content_enabled", False):
            return []
        
        enabled = getattr(persistent, "enabled_mods", [])
        active_screens = []
        for entry in _registered_mod_overlays:
            if entry["category"] in (category, "all"):
                mid = entry.get("mod_id")
                if mid is None or mid in enabled:
                    active_screens.append(entry["screen"])
        return active_screens

    def get_discovered_mods():
        global _discovered_mods
        return _discovered_mods

    def get_active_community_translations():
        """Возвращает список активных коммьюнити-переводов для экрана выбора языка."""
        if not getattr(persistent, "community_content_enabled", False):
            return []
        
        active_tls = []
        enabled_list = getattr(persistent, "enabled_mods", [])
        for mod in _discovered_mods:
            if mod.get("type") == "translation" and mod.get("id") in enabled_list:
                tl_data = mod.get("translation_data", {})
                code = tl_data.get("lang_code") or mod.get("language_code")
                if code:
                    active_tls.append({
                        "name": tl_data.get("name", mod.get("name")),
                        "native_name": tl_data.get("native_name", tl_data.get("name", mod.get("name"))),
                        "sub_name": tl_data.get("sub_name", f"Мод: {mod.get('name')}"),
                        "code": code,
                        "flag": tl_data.get("flag") or mod.get("icon_rel_path") or "gui/flags/unknown.png",
                        "font": tl_data.get("font", "DejaVuSans.ttf"),
                        "progress": tl_data.get("progress", 100),
                        "official": False,
                        "mod_id": mod.get("id"),
                        "author": mod.get("author", "")
                    })
        return active_tls

    def scan_mods():
        """
        Безопасно сканирует папку mods/ и собирает манифесты mod.json и settings.json.
        """
        global _discovered_mods, _discovered_translations
        sanitize_mod_settings()
        _discovered_mods = []
        _discovered_translations = []

        mods_dir = ensure_mods_dir()
        if not os.path.isdir(mods_dir):
            return _discovered_mods

        # Убеждаемся, что mods/ есть в config.searchpath для загрузки иконок превью
        if mods_dir not in config.searchpath:
            config.searchpath.append(mods_dir)

        try:
            entries = sorted(os.listdir(mods_dir))
        except Exception as e:
            print(f"[ModLoader] Ошибка чтения каталога mods: {e}")
            return _discovered_mods

        for folder_name in entries:
            # Игнорируем скрытые папки и служебные файлы
            if folder_name.startswith(".") or folder_name.startswith("_"):
                continue

            folder_path = os.path.join(mods_dir, folder_name)
            if not os.path.isdir(folder_path):
                continue

            # Защита от Path Traversal
            try:
                common = os.path.commonpath([mods_dir, folder_path])
                if os.path.abspath(common) != os.path.abspath(mods_dir):
                    continue
            except:
                continue

            manifest_path = os.path.join(folder_path, "mod.json")
            if not os.path.exists(manifest_path):
                continue

            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"[ModLoader] Не удалось прочитать манифест {manifest_path}: {e}")
                continue

            mod_id = data.get("id", folder_name)
            mod_type = data.get("type", "general") # "translation", "asset_replacement", "script", "general"
            
            # Поиск иконки 1:1
            icon_file = data.get("icon", "icon.png")
            icon_abs = os.path.join(folder_path, icon_file)
            icon_rel = f"{folder_name}/{icon_file}" if os.path.exists(icon_abs) else None

            # Проверка настроек мода (settings.json)
            has_settings_flag = data.get("has_settings", None)
            settings_file = data.get("settings_file", "settings.json")
            settings_abs = os.path.join(folder_path, settings_file)
            settings_schema = None
            has_settings = False

            if has_settings_flag is not False and os.path.exists(settings_abs):
                try:
                    with open(settings_abs, "r", encoding="utf-8") as sf:
                        settings_schema = json.load(sf)
                    has_settings = True
                except Exception as e:
                    print(f"[ModLoader] Ошибка загрузки {settings_abs}: {e}")
                    has_settings = False
            elif has_settings_flag is True:
                has_settings = True

            default_pri = int(data.get("priority", 10))

            mod_info = {
                "id": mod_id,
                "folder_name": folder_name,
                "folder_path": folder_path,
                "name": data.get("name", folder_name),
                "version": data.get("version", "1.0.0"),
                "author": data.get("author", _("Неизвестный автор")),
                "type": mod_type,
                "description": data.get("description", ""),
                "target_version": data.get("target_version", "*"),
                "icon_file": icon_file,
                "icon_abs_path": icon_abs if icon_rel else None,
                "icon_rel_path": icon_rel,
                "translation_data": data.get("translation_data", {}),
                "language_code": data.get("language_code") or data.get("translation_data", {}).get("lang_code"),
                "default_priority": default_pri,
                "has_settings": has_settings,
                "settings_schema": settings_schema
            }

            _discovered_mods.append(mod_info)

            if mod_type == "translation":
                _discovered_translations.append(mod_info)

        _sort_discovered_mods()
        return _discovered_mods

    def _sort_discovered_mods():
        global _discovered_mods
        _discovered_mods.sort(key=lambda m: get_mod_priority(m["id"]), reverse=True)

    # ==========================================================================
    # Управление приоритетами
    # ==========================================================================

    def get_mod_priority(mod_id):
        """Возвращает эффективный приоритет мода (пользовательский или дефолтный)."""
        if not hasattr(persistent, "mod_priorities") or persistent.mod_priorities is None:
            persistent.mod_priorities = {}
        if mod_id in persistent.mod_priorities:
            return persistent.mod_priorities[mod_id]
        for m in _discovered_mods:
            if m["id"] == mod_id:
                return m.get("default_priority", 10)
        return 10

    def set_mod_priority(mod_id, priority_value):
        """Устанавливает приоритет мода, обновляет сортировку и config.searchpath."""
        if not hasattr(persistent, "mod_priorities") or persistent.mod_priorities is None:
            persistent.mod_priorities = {}
        persistent.mod_priorities[mod_id] = int(priority_value)
        _sort_discovered_mods()
        apply_mod_searchpaths()
        renpy.save_persistent()
        renpy.restart_interaction()

    def adjust_mod_priority(mod_id, delta):
        """Изменяет приоритет мода на delta (+1 или -1)."""
        cur = get_mod_priority(mod_id)
        new_val = max(0, min(999, cur + delta))
        set_mod_priority(mod_id, new_val)

    def reset_mod_priorities():
        """Сбрасывает все пользовательские приоритеты к авторским дефолтам."""
        persistent.mod_priorities = {}
        _sort_discovered_mods()
        apply_mod_searchpaths()
        renpy.save_persistent()
        renpy.restart_interaction()

    import ast

    def _unwrap_setting_value(val):
        """Гарантирует, что значение является скаляром, а не словарем или его строковым представлением."""
        if val is None:
            return val
        if isinstance(val, dict):
            return val.get("value", val.get("label", str(val)))
        if isinstance(val, str):
            s = val.strip()
            if s.startswith("{") and ("value" in s or "label" in s):
                try:
                    parsed = ast.literal_eval(s)
                    if isinstance(parsed, dict):
                        return parsed.get("value", parsed.get("label", s))
                except:
                    pass
        return val

    def sanitize_mod_settings():
        """Очищает сохраненные настройки от устаревших структур-словарей."""
        if not hasattr(persistent, "mod_settings") or not isinstance(persistent.mod_settings, dict):
            return
        changed = False
        for mod_id, settings in persistent.mod_settings.items():
            if isinstance(settings, dict):
                for k, v in list(settings.items()):
                    unwrapped = _unwrap_setting_value(v)
                    if unwrapped != v:
                        settings[k] = unwrapped
                        changed = True
        if changed:
            try:
                renpy.save_persistent()
            except:
                pass

    def get_mod_setting(mod_id, key, default=None):
        """
        Возвращает значение настройки мода.
        Сначала проверяет persistent.mod_settings, затем default из settings.json.
        """
        if not hasattr(persistent, "mod_settings") or persistent.mod_settings is None:
            persistent.mod_settings = {}
        
        mod_vals = persistent.mod_settings.get(mod_id, {})
        if key in mod_vals:
            return _unwrap_setting_value(mod_vals[key])

        # Ищем дефолт в схеме
        for m in _discovered_mods:
            if m["id"] == mod_id and m.get("settings_schema"):
                for opt in m["settings_schema"].get("options", []):
                    if opt.get("id") == key:
                        val = opt.get("default", default)
                        return _unwrap_setting_value(val)
        return _unwrap_setting_value(default)

    def set_mod_setting(mod_id, key, value):
        """Сохраняет значение настройки мода."""
        if not hasattr(persistent, "mod_settings") or persistent.mod_settings is None:
            persistent.mod_settings = {}
        if mod_id not in persistent.mod_settings:
            persistent.mod_settings[mod_id] = {}
        persistent.mod_settings[mod_id][key] = _unwrap_setting_value(value)
        renpy.save_persistent()
        renpy.restart_interaction()

    def toggle_mod_setting(mod_id, key):
        """Переключает булеву настройку мода."""
        cur = bool(get_mod_setting(mod_id, key, False))
        set_mod_setting(mod_id, key, not cur)

    def adjust_slider_setting(mod_id, key, delta, min_val, max_val):
        """Корректирует числовое значение слайдера."""
        cur = get_mod_setting(mod_id, key, min_val)
        try:
            cur = float(cur) if isinstance(cur, float) else int(cur)
        except:
            cur = min_val
        new_val = max(min_val, min(max_val, cur + delta))
        set_mod_setting(mod_id, key, new_val)

    def cycle_choice_setting(mod_id, key, choices):
        """Циклически переключает значение среди списка вариантов."""
        if not choices:
            return
        cur = get_mod_setting(mod_id, key, None)
        if isinstance(cur, dict):
            cur = cur.get("value", cur.get("label", str(cur)))
        values = [c.get("value", c) if isinstance(c, dict) else c for c in choices]
        if cur in values:
            idx = (values.index(cur) + 1) % len(values)
        else:
            idx = 0
        set_mod_setting(mod_id, key, values[idx])

    def reset_mod_settings(mod_id):
        """Сбрасывает все настройки указанного мода на авторские дефолты."""
        if hasattr(persistent, "mod_settings") and persistent.mod_settings and mod_id in persistent.mod_settings:
            del persistent.mod_settings[mod_id]
        renpy.save_persistent()
        renpy.restart_interaction()

    # ==========================================================================
    # Поиск и фильтрация модов
    # ==========================================================================

    def set_mod_search_query(query):
        global mod_search_query
        mod_search_query = query.strip()
        renpy.restart_interaction()

    def clear_mod_search_query():
        global mod_search_query
        mod_search_query = ""
        renpy.restart_interaction()

    def set_mod_category_filter(category):
        global mod_category_filter
        mod_category_filter = category
        renpy.restart_interaction()

    def cycle_mod_sort_mode():
        global mod_sort_mode
        modes = ["priority", "name", "author"]
        idx = (modes.index(mod_sort_mode) + 1) % len(modes)
        mod_sort_mode = modes[idx]
        renpy.restart_interaction()

    def get_filtered_mods():
        """Возвращает список модов с учетом текущего поискового запроса, фильтра и сортировки."""
        res = list(_discovered_mods)

        # 1. Фильтрация по поисковому запросу
        if mod_search_query:
            q = mod_search_query.lower()
            res = [
                m for m in res
                if q in m.get("name", "").lower()
                or q in m.get("author", "").lower()
                or q in m.get("description", "").lower()
                or q in m.get("id", "").lower()
            ]

        # 2. Фильтрация по категории
        if mod_category_filter == "active":
            enabled = getattr(persistent, "enabled_mods", [])
            res = [m for m in res if m["id"] in enabled]
        elif mod_category_filter != "all":
            res = [m for m in res if m.get("type") == mod_category_filter]

        # 3. Сортировка
        if mod_sort_mode == "priority":
            res.sort(key=lambda m: get_mod_priority(m["id"]), reverse=True)
        elif mod_sort_mode == "name":
            res.sort(key=lambda m: m.get("name", "").lower())
        elif mod_sort_mode == "author":
            res.sort(key=lambda m: m.get("author", "").lower())

        return res

    # ==========================================================================
    # Применение в Ren'Py
    # ==========================================================================

    def apply_mod_searchpaths():
        """
        Применяет пути активных модов в config.searchpath в порядке их приоритета.
        """
        if not getattr(persistent, "community_content_enabled", False):
            return

        enabled = getattr(persistent, "enabled_mods", [])
        # Сортируем: низший приоритет сначала, высший в конец,
        # чтобы при вставке insert(0, ...) высший приоритет оказался на вершине
        active_mods = [m for m in _discovered_mods if m["id"] in enabled]
        active_mods.sort(key=lambda m: get_mod_priority(m["id"]))

        for mod in active_mods:
            fpath = mod["folder_path"]
            if os.path.isdir(fpath):
                if fpath in config.searchpath:
                    config.searchpath.remove(fpath)
                config.searchpath.insert(0, fpath)
                    
        sync_active_mod_translations()
        sync_active_modular_mods()

    def sync_active_mod_translations():
        """
        Синхронизирует файлы перевода из tl/ активного мода в game/tl/
        для корректной загрузки движком Ren'Py.
        """
        if not getattr(persistent, "community_content_enabled", False):
            return

        enabled = getattr(persistent, "enabled_mods", [])
        for mod in _discovered_mods:
            if mod.get("type") == "translation" and mod["id"] in enabled:
                lang_code = mod.get("translation_data", {}).get("lang_code") or mod.get("language_code")
                if not lang_code:
                    continue
                mod_tl_dir = os.path.join(mod["folder_path"], "tl", lang_code)
                game_tl_dir = os.path.join(config.gamedir, "tl", lang_code)
                if os.path.isdir(mod_tl_dir):
                    try:
                        if not os.path.exists(game_tl_dir):
                            os.makedirs(game_tl_dir)
                        for fname in os.listdir(mod_tl_dir):
                            src = os.path.join(mod_tl_dir, fname)
                            dst = os.path.join(game_tl_dir, fname)
                            if os.path.isfile(src):
                                if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
                                    shutil.copy2(src, dst)
                    except Exception as e:
                        print(f"[ModLoader] Ошибка синхронизации перевода {lang_code}: {e}")

    # ==========================================================================
    # Хук модульных модов (Modular Mods Runtime Hooking)
    # ==========================================================================

    def get_modules_mods_dir():
        """Возвращает абсолютный путь к папке внутри игры: game/modules/mods/."""
        return os.path.normpath(os.path.join(config.gamedir, "modules", "mods"))

    def hook_modular_mod(mod_info):
        """
        Хукает модульный мод из mods/<folder_name> в game/modules/mods/<folder_name>.
        Копирует структуру мода (скрипты .rpy, экраны, подпапки), исключая служебные файлы.
        """
        mod_id = mod_info.get("id")
        folder_name = mod_info.get("folder_name")
        src_dir = mod_info.get("folder_path")
        if not src_dir or not os.path.isdir(src_dir):
            return

        dest_base = get_modules_mods_dir()
        dest_dir = os.path.normpath(os.path.join(dest_base, folder_name))

        # Защита от Path Traversal
        try:
            common = os.path.commonpath([dest_base, dest_dir])
            if os.path.abspath(common) != os.path.abspath(dest_base) or os.path.abspath(dest_dir) == os.path.abspath(dest_base):
                return
        except:
            return

        # Если у мода есть выделенная папка module/ или modules/, используем её как корень хука
        sub_module = os.path.join(src_dir, "module")
        if not os.path.isdir(sub_module):
            sub_module = os.path.join(src_dir, "modules")
        
        source_root = sub_module if os.path.isdir(sub_module) else src_dir

        # Служебные файлы и папки, которые не нужно копировать в game/modules/mods/
        ignored_names = {"mod.json", "settings.json", "README.txt", "README.md", "icon.png", "tl", ".git", ".gitignore"}

        try:
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            for root, dirs, files in os.walk(source_root):
                dirs[:] = [d for d in dirs if d not in ignored_names and not d.startswith(".")]

                rel_path = os.path.relpath(root, source_root)
                target_subdir = os.path.normpath(os.path.join(dest_dir, rel_path))
                if not os.path.exists(target_subdir):
                    os.makedirs(target_subdir)

                for f in files:
                    if f in ignored_names or f.startswith("."):
                        continue
                    src_file = os.path.join(root, f)
                    dst_file = os.path.join(target_subdir, f)
                    if not os.path.exists(dst_file) or os.path.getmtime(src_file) > os.path.getmtime(dst_file):
                        shutil.copy2(src_file, dst_file)

            print(f"[ModLoader] Модуль [{mod_id}] успешно хукнут в {dest_dir}")
        except Exception as e:
            print(f"[ModLoader] Ошибка хука модуля [{mod_id}]: {e}")

    def unhook_modular_mod(mod_id, folder_name):
        """
        Анхукает модульный мод: удаляет его директорию из game/modules/mods/<folder_name>
        вместе со всеми скомпилированными .rpyc файлами, сохраняя игру чистой.
        """
        dest_base = get_modules_mods_dir()
        dest_dir = os.path.normpath(os.path.join(dest_base, folder_name))

        try:
            common = os.path.commonpath([dest_base, dest_dir])
            if os.path.abspath(common) != os.path.abspath(dest_base) or os.path.abspath(dest_dir) == os.path.abspath(dest_base):
                return
        except:
            return

        if os.path.isdir(dest_dir):
            try:
                shutil.rmtree(dest_dir, ignore_errors=True)
                print(f"[ModLoader] Модуль [{mod_id}] успешно анхукнут (удален из {dest_dir})")
            except Exception as e:
                print(f"[ModLoader] Ошибка анхука модуля [{mod_id}]: {e}")

    def sync_active_modular_mods():
        """
        Синхронизирует хуки модульных модов:
        - Если мод активен и коммьюнити контент включен -> хукаем в game/modules/mods/
        - Если мод отключен или коммьюнити контент выключен -> анхукаем
        """
        is_community_on = getattr(persistent, "community_content_enabled", False)
        enabled = getattr(persistent, "enabled_mods", []) if is_community_on else []

        for mod in _discovered_mods:
            if mod.get("type") in ("modular", "script"):
                mod_id = mod["id"]
                folder = mod["folder_name"]
                if is_community_on and mod_id in enabled:
                    hook_modular_mod(mod)
                else:
                    unhook_modular_mod(mod_id, folder)

    def get_mod_icon_displayable(mod):
        """Возвращает дисплайэбл для 1:1 иконки мода."""
        rel_path = mod.get("icon_rel_path")
        if rel_path and renpy.loadable(rel_path):
            return rel_path
        abs_path = mod.get("icon_abs_path")
        if abs_path and os.path.exists(abs_path):
            try:
                with open(abs_path, "rb") as f:
                    data = f.read()
                return im.Data(data, filename=os.path.basename(abs_path))
            except Exception as e:
                pass
        return None

    def enable_community_content():
        """Включает режим коммьюнити контента."""
        persistent.community_content_enabled = True
        scan_mods()
        apply_mod_searchpaths()
        sync_active_modular_mods()
        renpy.save_persistent()
        renpy.restart_interaction()

    def disable_community_content():
        """Выключает режим коммьюнити контента."""
        persistent.community_content_enabled = False
        if _preferences.language not in (None, "english_us"):
            renpy.change_language(None)
        sync_active_modular_mods()
        renpy.save_persistent()
        renpy.restart_interaction()

    def toggle_mod(mod_id):
        """Переключает статус активности конкретного мода."""
        if not hasattr(persistent, "enabled_mods") or persistent.enabled_mods is None:
            persistent.enabled_mods = []

        if mod_id in persistent.enabled_mods:
            persistent.enabled_mods.remove(mod_id)
            for mod in _discovered_mods:
                if mod["id"] == mod_id and mod.get("type") == "translation":
                    lang_code = mod.get("translation_data", {}).get("lang_code") or mod.get("language_code")
                    if _preferences.language == lang_code:
                        renpy.change_language(None)
        else:
            persistent.enabled_mods.append(mod_id)
            sync_active_mod_translations()

        apply_mod_searchpaths()
        sync_active_modular_mods()
        renpy.save_persistent()
        renpy.restart_interaction()

    def is_mod_enabled(mod_id):
        return mod_id in getattr(persistent, "enabled_mods", [])

    def rescan_mods():
        """Пересканирует папку модов."""
        scan_mods()
        apply_mod_searchpaths()
        sync_active_modular_mods()
        renpy.restart_interaction()

    def open_mods_folder():
        """Открывает папку mods/ в системном проводнике."""
        mdir = ensure_mods_dir()
        try:
            if renpy.windows:
                os.startfile(mdir)
            elif renpy.mac:
                import subprocess
                subprocess.Popen(["open", mdir])
            else:
                import subprocess
                subprocess.Popen(["xdg-open", mdir])
        except Exception as e:
            print(f"[ModLoader] Ошибка открытия проводника: {e}")

# Инициализация при запуске игры
init 10 python:
    scan_mods()
    if getattr(persistent, "community_content_enabled", False):
        apply_mod_searchpaths()
        sync_active_modular_mods()
