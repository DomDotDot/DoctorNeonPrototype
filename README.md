# The Brightest Neon - Semitone Resonance

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/DomDotDot/DoctorNeonPrototype/blob/main/README.md)
[![ru](https://img.shields.io/badge/lang-ru-blue.svg)](https://github.com/DomDotDot/DoctorNeonPrototype/blob/main/README.ru.md)

![BannerVolume1](source_assets/promo/promoassets/BNSR-Poster-vol1.jpg)
![BannerVolume2](source_assets/promo/promoassets/BNSR-Poster-vol2.png)

<!-- BADGES -->
![Status](https://img.shields.io/badge/Status-In%20Development-yellow?style=flat-square)
![RenPy](https://img.shields.io/badge/Ren'Py-8.x-faa61a?style=flat-square&logo=renpy)
[![License](https://img.shields.io/github/license/DomDotDot/DoctorNeonPrototype?style=flat-square)](LICENSE)
> A Sci-Fi Mystery Kinetic Novel.

## Project Structure

This repository contains the **source code** of the project (Developer View).
Folder layout:

```text
.
├── game/                   #   MAIN GAME FOLDER
│   ├── audio/              # Music and SFX
│   ├── devtools/           # Tools for game development
│   ├── fonts/              # Game fonts
│   ├── game-scripts/       # Game scripts (rpy)
│   ├── gui/                # Ren'Py GUI elements
│   ├── images/             # Sprites, BGs, and CGs (included in the build)
│   ├── libs/               # 3rd Party libraries
│   ├── modules/            # Game modules
│   ├── tl/                 # Translation folder
│   ├── launch.rpy          # Pre-menu workflow
│   ├── script.rpy          # Main script
│   ├── options.rpy         # Build config and settings
│
├── source_assets/          #   PROMO & SOURCE FILES
│   ├── images/             # Source images for game assets
│   ├── legacy/             # Legacy assets (no longer used)
│   ├── pdn-sketches/       # Paint.NET Source files
│   ├── promo/              # Steam/Itch.io assets
│   └── ...                 # (These files are NOT included in the final build)
│
├── .gitignore              # Git ignore list (cache, saves)
└── README.md               # Project documentation
```

---

## How to Run (For Developers)

1.  Install the **[Ren'Py SDK](https://www.renpy.org/latest/)** (Version 8.x+ recommended).
2.  Clone this repository or download the ZIP.
3.  Open the Ren'Py Launcher.
4.  Go to **"Preferences"** -> **"Projects Directory"** and select the folder where this repo is located.
5.  Click **"Refresh"**. The project should appear in the list.
6.  Click **"Launch Project"** to start the game.

---

## Development Process (Git Flow)

We use a simple branching structure:

*   🔴 **`main`** — Stable version. Only tested code goes here. This branch must always run without errors.
*   🟡 **`dev`** — Main development branch. All active work and new ideas happen here.
*   🔵 **`feature/name`** — Temporary branches for major mechanics (e.g., `feature/inventory` or `feature/minigame`). Once finished, they are merged into `dev` and deleted.

### How to contribute:
1.  Switch to the `dev` branch.
2.  Make your changes to the code/script.
3.  Verify that it runs correctly in Ren'Py.
4.  Commit your changes (`git commit`).
5.  When the update is ready for release, merge `dev` into `main`.

---

## Contributing & Modding

This is an **Open Source** project. I encourage mods, fan translations, and community code improvements.
You **do not need** to unpack `.rpa` archives or decompile the game. The entire source code is available right here.

### How to submit changes (Pull Requests)

Follow the standard GitHub flow:
1.  **Fork** this repository.
2.  Make changes in your fork.
3.  Create a **Pull Request (PR)** to the `dev` branch (or `main` for critical hotfixes).
4.  Once reviewed, I will merge your changes into the game.

---

### For Coders & Modders

If you want to add a feature or fix a bug:
*   Try not to modify existing files (`script.rpy`) unless it's a bug fix.
*   It's better to create a new file (e.g., `game/modules/module/my_feature.rpy`) — Ren'Py will detect it automatically. This reduces merge conflicts.
*   Use `init python` blocks or separate `labels` so your logic doesn't break the main plot flow.

---

## Building

To create a distribution for players (Windows/Linux/Mac):
1. Open the Ren'Py Launcher.
2. Select the project.
3. Click **"Build Distributions"**.
4. Files from `source_assets` and Git system files are **automatically excluded** from the build (configured in `options.rpy`).

## License & Rights

This project uses a hybrid license to encourage learning and modding while protecting proprietary content.

*   💻 **Source Code** (Logic, Mechanics, GUI) is licensed under **MIT**.
    *   *You are free to use the code in your own projects, even commercial ones.*
*   🎨 **Story & Assets** (Script, Graphics, Music, Characters) are licensed under **CC BY-NC-SA 4.0**.
    *   *You are free to create mods, translations, and fan art.*
    *   *⛔ **Commercial use is prohibited.** You cannot sell the game or its assets.*

See [LICENSE](LICENSE) for the full text.
