################################################################################
## Управление аудио в меню паузы (Pause Audio Separation System)
## Doctor Neon Prototype
################################################################################

init -2:
    # Определение трека для меню паузы
    define pause_menu_music = "audio/music/BGM/Desolate.opus"

init python:
    # Каналы игрового аудио, которые приглушаются до 0 в паузе
    PAUSE_GAME_AUDIO_CHANNELS = ("music", "ambient", "ambient1")

    # Длительность затухания игрового звука при входе в паузу (сек)
    PAUSE_FADEOUT_DURATION = 1.0

    # Длительность плавного возвращения игрового звука при выходе из паузы (сек)
    PAUSE_FADEIN_DURATION = 1.2

    # Состояние активности звука паузы
    _pause_audio_active = False

    def enter_pause_audio():
        global _pause_audio_active
        _pause_audio_active = True

        # 1. Плавный фейд игрового аудио в 0
        for ch in PAUSE_GAME_AUDIO_CHANNELS:
            try:
                renpy.music.set_volume(0.0, delay=PAUSE_FADEOUT_DURATION, channel=ch)
            except Exception:
                pass

        # 2. Воспроизведение трека на канале pause_music
        try:
            renpy.music.play(
                pause_menu_music,
                channel="pause_music",
                loop=True,
                if_changed=True,
                fadein=0.6
            )
        except Exception:
            pass

    def exit_pause_audio():
        global _pause_audio_active
        if not _pause_audio_active:
            return
        _pause_audio_active = False

        # 1. Резкий обрыв трека
        try:
            renpy.music.stop(channel="pause_music", fadeout=0.0)
        except Exception:
            pass
        try:
            renpy.music.stop(channel="pause_musid", fadeout=0.0)
        except Exception:
            pass

        # 2. Плавный фейд на музыку и эмбиент игры
        for ch in PAUSE_GAME_AUDIO_CHANNELS:
            try:
                renpy.music.set_volume(1.0, delay=PAUSE_FADEIN_DURATION, channel=ch)
            except Exception:
                pass

    def _pause_audio_interact_watcher():
        """
        Слушатель взаимодействия: отслеживает выход из контекста меню паузы
        (включая выход из Save / Load / Settings) обратно в игру или переход в главное меню.
        """
        global _pause_audio_active
        if not _pause_audio_active:
            return

        # Если вышли в главное меню
        if getattr(renpy.store, "main_menu", False):
            _pause_audio_active = False
            try:
                renpy.music.stop(channel="pause_music", fadeout=0.0)
                renpy.music.stop(channel="pause_musid", fadeout=0.0)
            except Exception:
                pass
            for ch in PAUSE_GAME_AUDIO_CHANNELS:
                try:
                    renpy.music.set_volume(1.0, delay=0.0, channel=ch)
                except Exception:
                    pass
            return

        # Если контекст меню завершился (игрок вернулся к чтению/геймплею)
        if not renpy.context()._menu:
            exit_pause_audio()

    if _pause_audio_interact_watcher not in config.start_interact_callbacks:
        config.start_interact_callbacks.append(_pause_audio_interact_watcher)

    def _pause_audio_after_load():
        """
        Срабатывает после загрузки любого сохранения: останавливает музыку паузы
        и сбрасывает громкость игровых каналов на 100%.
        """
        global _pause_audio_active
        _pause_audio_active = False
        try:
            renpy.music.stop(channel="pause_music", fadeout=0.0)
            renpy.music.stop(channel="pause_musid", fadeout=0.0)
        except Exception:
            pass
        for ch in PAUSE_GAME_AUDIO_CHANNELS:
            try:
                renpy.music.set_volume(1.0, delay=0.0, channel=ch)
            except Exception:
                pass

    if _pause_audio_after_load not in config.after_load_callbacks:
        config.after_load_callbacks.append(_pause_audio_after_load)
