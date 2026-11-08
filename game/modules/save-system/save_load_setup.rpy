################################################################################
## Модуль системы сохранений и загрузки (Save & Load System Setup)
## Doctor Neon Prototype — Native Ren'Py Save/Load Helpers
################################################################################

default save_name = _("Пролог")

init -1 python:

    def update_chapter_save_info(chap_text, tit_text):
        """
        Обновляет стандартную переменную store.save_name при показе экрана главы.
        Ren'Py автоматически записывает store.save_name в метаданные сейва
        при вызове нативного FileSave(slot) и читает через FileSaveName(slot).
        """
        chap_str = str(chap_text).strip() if chap_text else ""
        tit_str = str(tit_text).strip() if tit_text else ""
        if chap_str and tit_str:
            store.save_name = chap_str + " — " + tit_str
        elif chap_str:
            store.save_name = chap_str
        elif tit_str:
            store.save_name = tit_str
        else:
            store.save_name = _("Сюжетное сохранение")

    def get_save_slot_title(slot):
        """
        Возвращает читаемый заголовок карточки слота на основе нативного FileCurrentPage().
        """
        page = FileCurrentPage()
        if page == "auto":
            return _("АВТО #{}").format(slot)
        elif page == "quick":
            return _("БЫСТРОЕ #{}").format(slot)
        return _("СЛОТ {}-{}").format(page, slot)

    def format_save_slot_chapter(raw_name, max_len=38):
        """
        Форматирует название главы из FileSaveName(slot) в одну аккуратную строку.
        """
        text_val = str(raw_name).strip() if raw_name else ""
        if not text_val:
            return _("Сюжетное сохранение")
        if len(text_val) > max_len:
            return text_val[:max_len - 1].rstrip() + "…"
        return text_val
