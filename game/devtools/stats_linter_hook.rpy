# ==============================================================================
# Ren'Py Devtools: Story & Dialogue Statistics Hook
# ==============================================================================
# Позволяет обновлять статистику и бейджи в README прямо из движка Ren'Py (Shift+D или в dev-режиме)

init 99 python:
    import sys
    import os

    def update_story_statistics(notify=True):
        """
        Запускает анализ диалогов и обновляет README.md и README.ru.md
        """
        base_dir = config.basedir
        tools_dir = os.path.join(base_dir, "tools")
        linter_script = os.path.join(tools_dir, "script_stats_linter.py")

        if not os.path.exists(linter_script):
            print("[Devtools Stats] Error: script_stats_linter.py not found at: " + linter_script)
            if notify:
                renpy.notify("Ошибка: script_stats_linter.py не найден")
            return False

        try:
            # Импортируем и запускаем парсер напрямую в среде Python Ren'Py
            if tools_dir not in sys.path:
                sys.path.insert(0, tools_dir)

            import script_stats_linter
            scripts_path = os.path.join(config.gamedir, "game-scripts")
            data = script_stats_linter.analyze_project_scripts(scripts_path)

            readme_ru = os.path.join(base_dir, "README.ru.md")
            readme_en = os.path.join(base_dir, "README.md")

            script_stats_linter.update_readme_file(readme_ru, data, lang="ru", check_only=False)
            script_stats_linter.update_readme_file(readme_en, data, lang="en", check_only=False)

            total_words = data["totals"]["total_words"]
            total_lines = data["totals"]["total_lines"]
            print(f"[Devtools Stats] READMEs updated successfully! Words: {total_words}, Lines: {total_lines}")

            if notify:
                renpy.notify(f"Статистика сценария обновлена! Слов: {total_words:,}, Реплик: {total_lines:,}")
            return True
        except Exception as e:
            print(f"[Devtools Stats] Failed to update statistics: {e}")
            if notify:
                renpy.notify(f"Ошибка обновления статистики: {e}")
            return False

# Опционально: кнопка для быстрого вызова в меню разработчика или консоли
# Вызов в консоли разработчика (Shift+O): update_story_statistics()
