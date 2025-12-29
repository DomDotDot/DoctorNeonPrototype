init offset = -1 # Загружаем это до остальных скриптов

# Определения для главного меню.  
       
# Переменная, которая будет храниться между прохождениями.
# 0 - стандартное меню
# 1 - первый этап
# 2 - второй этап
# и т.д

default persistent.main_menu_level = 0
default persistent.sensitive_mode = False
default persistent.ai_sensitive_mode = False

# --- МУЗЫКА ---
define main_menu_music_default = "audio/music/BGM/NightMare.opus"
define main_menu_music_unlocked_1 = "audio/music/BGM/FearForUnreal.opus"
define main_menu_music_unlocked_2 = "audio/music/BGM/WitheredFlower.opus"
define main_menu_music_unlocked_3 = "audio/music/BGM/Sorrowless.opus"
define main_menu_music_unlocked_4 = "audio/music/BGM/BuzzingGoodbye.opus"

# --- ФОНЫ (Умное переключение) ---
# ConditionSwitch сам проверяет условия и ставит нужную картинку.
image main_menu_bg_dynamic = ConditionSwitch(
"persistent.main_menu_level == 4", "gui/main_menu/background_unlocked_4.avif",
"persistent.main_menu_level == 3", "gui/main_menu/background_unlocked_3.avif",
"persistent.main_menu_level == 2", "gui/main_menu/background_unlocked_2.avif",
"persistent.main_menu_level == 1", "gui/main_menu/background_unlocked_1.avif",
"True", "gui/main_menu/background_default.avif"
)

image main_menu_logo = "gui/main_menu/logo2.avif"