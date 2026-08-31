init python early:
    import time

    # Класс одного уведомления
    class GameNotification(object):
        def __init__(self, notif_id, title, message, link_itch=None, link_github=None, version_tag=None):
            self.id = notif_id
            self.title = title
            self.message = message
            self.timestamp = time.time()
            self.is_read = False
            
            # Опциональные данные для обновлений
            self.link_itch = link_itch
            self.link_github = link_github
            self.version_tag = version_tag

        def __eq__(self, other):
            if not isinstance(other, GameNotification):
                return False
            return self.id == other.id

        def __ne__(self, other):
            return not self.__eq__(other)

        # Этот метод помогает Ren'Py понять, как сохранять объект
        def __getstate__(self):
            return self.__dict__

        def __setstate__(self, dict):
            self.__dict__ = dict

# Обычный init для функций и переменных
init -999 python:
    # Функция безопасной очистки при сбое
    def _safe_check_persistent():
        try:
            # Пытаемся прочитать список. Если там мусор - сбросится в except
            if persistent.notifications:
                for n in persistent.notifications:
                    x = n.id 
        except:
            print("Обнаружены поврежденные уведомления. Сброс списка.")
            persistent.notifications = []

    # Запускаем проверку
    _safe_check_persistent()

    # Инициализация списка
    if persistent.notifications is None:
        persistent.notifications = []

    # --- ФУНКЦИИ УПРАВЛЕНИЯ ---

    def add_notification(notif_id, title, message, link_itch=None, link_github=None, version_tag=None, force_popup=False):
        """
        Добавляет уведомление, если уведомления с таким ID еще нет.
        """
        if persistent.notifications is None:
            persistent.notifications = []
        
        # Проверяем, есть ли уже уведомление с таким ID (чтобы не дублировать при каждом запуске)
        for n in persistent.notifications:
            if n.id == notif_id:
                return # Уже есть, выходим

        # Создаем новое
        new_note = GameNotification(notif_id, title, message, link_itch, link_github, version_tag)
        
        # Добавляем в начало списка (новые сверху)
        persistent.notifications.insert(0, new_note)
        
        # Если нужно всплывающее окно прямо сейчас (для важных обновлений)
        if force_popup:
            renpy.show_screen("update_popup_screen", note=new_note)
            
        renpy.restart_interaction()

    def mark_all_read():
        for n in persistent.notifications:
            n.is_read = True
        try:
            grant_achievement("mail_maniac")
        except:
            pass
        renpy.restart_interaction()
        
    def delete_notification(notif_obj):
        if notif_obj in persistent.notifications:
            persistent.notifications.remove(notif_obj)
            renpy.restart_interaction()
            
    def get_unread_count():
        if persistent.notifications is None:
            return 0
        return len([n for n in persistent.notifications if not n.is_read])