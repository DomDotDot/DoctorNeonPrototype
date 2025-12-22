# The Brightest Neon - Semitone Resonance

![Banner](image-assets/promo/promoassets/BNSR-Poster.jpg)

<!-- BADGES -->
![Status](https://img.shields.io/badge/Status-In%20Development-yellow?style=flat-square)
[![Crowdin](https://badges.crowdin.net/thebrightestneon-sr/localized.svg)](https://crowdin.com/project/thebrightestneon-sr)
![RenPy](https://img.shields.io/badge/Ren'Py-8.x-faa61a?style=flat-square&logo=renpy)
[![License](https://img.shields.io/github/license/DomDotDot/DoctorNeonPrototype?style=flat-square)](LICENSE)
> A Sci-Fi Mystery Kinetic Novel.

## 📂 Project Structure

This repository contains the **source code** of the project (Developer View).
Folder layout:

```text
.
├── game/                   # 🎮 MAIN GAME FOLDER
│   ├── audio/              # Music and SFX
│   ├── fonts/              # Game fonts
│   ├── gui/                # Ren'Py GUI elements
│   ├── images/             # Sprites, BGs, and CGs (included in the build)
│   ├── libs/               # 3rd Party libraries
│   ├── modules/            # Game modules
│   ├── tl/                 # Translation folder
│   ├── launch.rpy          # Pre-menu workflow
│   ├── script.rpy          # Main script
│   ├── options.rpy         # Build config and settings
│
├── image-assets/           # 🎨 PROMO & SOURCE FILES
│   ├── pdn-sketches/       # Paint.NET Source files
│   ├── promo/              # Steam/Itch.io assets
│   └── ...                 # (These files are NOT included in the final build)
│
├── .gitignore              # Git ignore list (cache, saves)
└── README.md               # Project documentation
```

---

## 🚀 How to Run (For Developers)

1.  Install the **[Ren'Py SDK](https://www.renpy.org/latest/)** (Version 8.x+ recommended).
2.  Clone this repository or download the ZIP.
3.  Open the Ren'Py Launcher.
4.  Go to **"Preferences"** -> **"Projects Directory"** and select the folder where this repo is located.
5.  Click **"Refresh"**. The project should appear in the list.
6.  Click **"Launch Project"** to start the game.

---

## 🛠 Development Process (Git Flow)

We use a simple branching structure:

*   🔴 **`main`** — Stable version. Only tested code goes here. This branch must always run without errors.
*   🟡 **`dev`** — Main development branch. All active work and new ideas happen here.
*   🔵 **`feature/name`** — Temporary branches for major mechanics (e.g., `feature/inventory` or `feature/minigame`). Once finished, they are merged into `dev` and deleted.
*   🔵 **`l10n_dev`** — Service branch for Crowdin (automatic translation updates).

### How to contribute:
1.  Switch to the `dev` branch.
2.  Make your changes to the code/script.
3.  Verify that it runs correctly in Ren'Py.
4.  Commit your changes (`git commit`).
5.  When the update is ready for release, merge `dev` into `main`.

---

## 🤝 Contributing & Modding

This is an **Open Source** project. I encourage mods, fan translations, and community code improvements.
You **do not need** to unpack `.rpa` archives or decompile the game. The entire source code is available right here.

### How to submit changes (Pull Requests)

Follow the standard GitHub flow:
1.  **Fork** this repository.
2.  Make changes in your fork.
3.  Create a **Pull Request (PR)** to the `dev` branch (or `main` for critical hotfixes).
4.  Once reviewed, I will merge your changes into the game.

---

## 🌍 Localization (Crowdin)

We use **Crowdin** to manage translations.
The game uses the **Gettext (.po/.pot)** format for synchronization.

[![Help Translate](https://img.shields.io/badge/Translate_on-Crowdin-brightgreen?style=for-the-badge&logo=crowdin)](https://crowdin.com/project/thebrightestneon-sr)

### ✋ For Translators
> **Please do not manually edit `.rpy` files in the `game/tl/` folder!**
Your changes will be overwritten during the next sync.

1.  Go to the project page on [Crowdin](https://crowdin.com/project/thebrightestneon-sr).
2.  Select your language.
3.  Translate directly in the browser. Your changes will automatically make it into the game.
4.  If you don't know Russian (Source Language), you can use the **English** translation as a reference inside the Crowdin editor.

### 🛠 For Developers (Sync Workflow)

To sync `.rpy` files (Ren'Py code) and `.po` files (Crowdin format), we use the **[Ren'Py Translator ToolKit (renpy-ttk)](https://beuc.net/renpy-ttk/)**.

Translation system workflow:
1.  `game/tl/pot/game.pot` — Template (generated from the Russian source).
2.  `game/tl/english_us/game.po` — Translation file (synced with Crowdin).

### Tool Setup
1.  Download `renpy-ttk` (v1.10 or newer) from the [official site](https://beuc.net/renpy-ttk/).
2.  Unpack it into your Ren'Py Projects Directory (next to your game folder).
3.  The **renpy-ttk** project will appear in your Ren'Py Launcher.

### Scenario 1: You changed the original Russian text
If you edited dialogue in `script.rpy`, you need to update the Crowdin template:
1.  Open **renpy-ttk** in the launcher.
2.  Select **`tl2pot`** (Generate POT template).
3.  Select the project folder.
4.  This updates `game/tl/pot/game.pot`.
5.  Commit and push (`git push`). Crowdin will detect the new strings.

### Scenario 2: You want to apply new translations
Crowdin (or the `l10n_dev` branch) updated the `.po` file, but the game still shows old text? You need to inject it:
1.  Ensure you have the latest `game/tl/english_us/game.po` (run `git pull`).
2.  Run **renpy-ttk**.
3.  Select **`mo2tl`** (Inject PO/MO into Ren'Py).
4.  A file explorer will open. Select the language folder (e.g., `tl/english_us`).
5.  The script will overwrite the `.rpy` files in the translation folder. The game now displays the new text.

> **Important:** Never edit translation text manually in `tl/english_us/*.rpy`. Your changes will be wiped out during the next `mo2tl` injection. Edit either on Crowdin or in the `.po` file.

---

### 🛠 For Coders & Modders

If you want to add a feature or fix a bug:
*   Try not to modify existing files (`script.rpy`) unless it's a bug fix.
*   It's better to create a new file (e.g., `game/scripts/my_feature.rpy`) — Ren'Py will detect it automatically. This reduces merge conflicts.
*   Use `init python` blocks or separate `labels` so your logic doesn't break the main plot flow.

---

## 📦 Building

To create a distribution for players (Windows/Linux/Mac):
1. Open the Ren'Py Launcher.
2. Select the project.
3. Click **"Build Distributions"**.
4. Files from `image-assets` and Git system files are **automatically excluded** from the build (configured in `options.rpy`).

## 📜 License & Rights

This project uses a hybrid license to encourage learning and modding while protecting proprietary content.

*   💻 **Source Code** (Logic, Mechanics, GUI) is licensed under **MIT**.
    *   *You are free to use the code in your own projects, even commercial ones.*
*   🎨 **Story & Assets** (Script, Graphics, Music, Characters) are licensed under **CC BY-NC-SA 4.0**.
    *   *You are free to create mods, translations, and fan art.*
    *   *⛔ **Commercial use is prohibited.** You cannot sell the game or its assets.*

See [LICENSE](LICENSE) for the full text.
