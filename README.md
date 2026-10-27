<div align="center">

<h1>The Brightest Neon - Semitone Resonance</h1>

<p align="center">
  <img src="source_assets/promo/logos/window_icon600-600.png" alt="Project Logo" width="150">
</p>

<img src="source_assets/promo/promoassets/certified-ai-slop.png" alt="Certified AI Slop" width="480">

<p><strong>A Sci-Fi Mystery Kinetic Novel powered by Ren'Py</strong></p>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue.svg)](https://github.com/DomDotDot/DoctorNeonPrototype/releases)
[![RenPy](https://img.shields.io/badge/Ren'Py-8.5.x-faa61a?style=flat-square&logo=renpy)](https://www.renpy.org/)
[![GitHub Release](https://img.shields.io/github/v/release/DomDotDot/DoctorNeonPrototype?style=flat-square&color=41b883)](https://github.com/DomDotDot/DoctorNeonPrototype/releases/latest)

<!-- BADGES -->
<!-- STATS_BADGES:START -->
![Words](https://img.shields.io/badge/Words-120.1k-blue?style=flat-square&logo=gitbook&logoColor=white)
![Lines](https://img.shields.io/badge/Lines-5%20787-4c1?style=flat-square)
![Chapters](https://img.shields.io/badge/Chapters-11%20-8a2be2?style=flat-square)
![Dialogue](https://img.shields.io/badge/Dialogue-34%25-informational?style=flat-square)
<!-- STATS_BADGES:END -->
<br>

![BannerVolume1](source_assets/promo/promoassets/BNSR-Poster-vol1.jpg)

![BannerVolume2](source_assets/promo/promoassets/BNSR-Poster-vol2.png)

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/DomDotDot/DoctorNeonPrototype/blob/main/README.md)
[![ru](https://img.shields.io/badge/lang-ru-blue.svg)](https://github.com/DomDotDot/DoctorNeonPrototype/blob/main/README.ru.md)

</div>

---

## About the Project

**The Brightest Neon - Semitone Resonance** is a story-rich, atmosphere-heavy sci-fi kinetic visual novel. The game features deep narrative branching, a distinct futuristic neon noir aesthetic, rich audio design, and custom GLSL shader visual effects.

---

## Repository Structure

```text
.
├── game/                   # CORE GAME ASSETS & CODE
│   ├── audio/                # In-game music and sound effects (SFX)
│   ├── devtools/             # Developer debug utilities and cheats
│   ├── fonts/                # Custom typography and font subsets
│   ├── game-scripts/         # Story dialogue scripts (.rpy) organized by chapters & flashbacks
│   ├── gui/                  # Ren'Py GUI themes, frames, and widgets
│   ├── images/               # In-game sprites, backgrounds (BG), and event CGs
│   ├── libs/                 # Third-party Python libraries & helper modules
│   ├── modules/              # Modular subsystems (audio, gallery, glossary, save/load, shaders)
│   ├── tl/                   # Official translations (Russian, English)
│   ├── launch.rpy            # Initialization workflow & boot sequence
│   ├── script.rpy            # Script entry point
│   ├── options.rpy           # Build configuration, window title, and archive rules
│   └── screens.rpy           # UI screen definitions
│
├── mods/                   # NATIVE COMMUNITY MODS DIRECTORY
│   ├── mod_example_cyberpunk/# Reference modular mod demonstrating Mod API
│   ├── mod_toki_pona/        # Community translation pack example
│   └── <your_mod>/           # Place community mods and language packs here
│
├── source_assets/          # RAW SOURCE ASSETS (TRACKED VIA GIT LFS)
│   ├── audio/                # Uncompressed/raw soundtracks and stems
│   ├── images/               # Master character art, layered cutouts, PSD/PDN sketches
│   └── promo/                # High-res posters, banners, and store media
│                             # (Excluded from production game builds automatically)
│
├── tools/                  # DEVELOPER TOOLS & AUTOMATION
│   ├── script_stats_linter.py # Dialogue & word counter / README updater
│   └── install_git_hook.py    # Pre-commit hook installer
│
├── .gitattributes          # Git LFS filter rules for binary source assets
├── .gitignore              # Ignored build caches, saves, and binaries
└── README.md               # English project documentation
```

---

## Getting Started (For Developers)

### Prerequisites

1. **[Ren'Py SDK](https://www.renpy.org/latest/)**: Version **8.2+** (8.5.x recommended).
2. **[Git](https://git-scm.com/)** and **[Git LFS](https://git-lfs.com/)**: Required for pulling large source artwork and audio.
3. **[Python 3.10+](https://www.python.org/)**: For running developer tools and linters.

### Setup Steps

1. **Clone the repository and pull LFS objects:**
   ```bash
   git clone https://github.com/DomDotDot/DoctorNeonPrototype.git
   cd DoctorNeonPrototype
   git lfs install
   git lfs pull
   ```
2. **Install pre-commit hook (recommended):**
   ```bash
   python tools/install_git_hook.py
   ```
   *This hook automatically recalculates script word counts, badge metrics, and dialogue tables in `README.md` and `README.ru.md` before each commit.*
3. **Configure Git Rebase (prevents merge clutter across multiple machines):**
   ```bash
   git config pull.rebase true
   git config rebase.autoStash true
   ```
4. **Launch with Ren'Py:**
   * Open the **Ren'Py Launcher**.
   * In **Preferences** -> **Projects Directory**, select the directory containing this repo.
   * Refresh the list, select **DoctorNeonPrototype**, and click **Launch Project**.

---

## Native Modding System & Community Content

The game features a **full built-in native mod loader and manager**. You do **not** need to decompile files, extract `.rpa` archives, or touch core source files to create or install mods.

### For Players: Installing & Managing Mods

1. In the game's **Main Menu** or **Settings**, open **"Community Content & Mods"** (`Коммьюнити Контент и Моды`).
2. Toggle the master switch to **🟢 ENABLED** (accepting the community content notice).
3. Click **"Open Mods Folder"** to open your local `mods/` directory, and paste any downloaded mod folder there.
4. From the in-game Mod Manager, you can:
   * **Toggle mods on/off** individually without restarting the game.
   * **Adjust load priorities** for mods that override similar assets.
   * **Filter and search** mods by category (*Translation*, *Asset Replacement*, *Script*, *Modular*).
   * **Configure custom mod settings** via in-game sliders, toggles, and selectors.

---

### For Mod Creators: Creating a Mod

Every mod is an isolated folder located in the root `mods/` directory:
```text
mods/
└── my_cool_mod/
    ├── mod.json            # Required: Mod manifest metadata
    ├── icon.png            # Optional: 128x128 preview icon
    ├── settings.json       # Optional: Custom in-game settings schema
    └── my_script.rpy       # Custom Ren'Py code, screens, or hooks
```

#### 1. The Mod Manifest (`mod.json`)
Create a `mod.json` inside your mod directory:

```json
{
  "id": "my_cool_mod",
  "name": "My Neon Overhaul",
  "version": "1.0.0",
  "author": "YourName",
  "type": "modular",
  "description": "Adds custom shaders, dialogue scenes, and a HUD overlay.",
  "target_version": "0.8.x",
  "priority": 10,
  "icon": "icon.png",
  "has_settings": true,
  "settings_file": "settings.json"
}
```

#### Supported Mod Types (`type`)
* **`modular`**: Full-fledged code mods injecting custom Python logic, shaders, screens, and audio.
* **`translation`**: Community language translations. Automatically mounted into Ren'Py's translation search paths.
* **`asset_replacement`**: Overrides existing sprites, backgrounds, GUI textures, or music seamlessly without modifying core files.
* **`script`**: Adds new story branches, side-stories, or bonus chapters.

#### 2. Mod API: Hooks & Screen Overlays
The engine provides clean APIs for hooking into core gameplay without causing code conflicts:

```python
init python:
    # 1. Register an event hook
    def on_game_pulse(*args, **kwargs):
        print("Mod hook received game pulse event!")
    register_mod_hook("game_pulse", on_game_pulse)

    # 2. Register an overlay screen (category: "main_menu", "ingame", or "all")
    register_mod_overlay("my_custom_hud_screen", mod_id="my_cool_mod", category="ingame", order=10)

    # 3. Read interactive mod settings configured by the player
    custom_volume = get_mod_setting("my_cool_mod", "neon_intensity", default=100)
```

#### 3. Interactive Settings (`settings.json`)
If `"has_settings": true`, the Mod Manager dynamically builds an in-game options menu for your mod:
```json
{
  "neon_intensity": {
    "type": "slider",
    "title": "Neon Glow Intensity",
    "default": 80,
    "min": 0,
    "max": 100,
    "step": 5
  },
  "enable_cyber_sfx": {
    "type": "toggle",
    "title": "Enable Cybernetic Audio Filter",
    "default": true
  }
}
```

> **Reference Example:** Check out [`mods/mod_example_cyberpunk/`](mods/mod_example_cyberpunk/) for a complete working implementation of scripts, hooks, overlays, and custom settings.

---

## Contributing & Pull Requests

Contributions and fan improvements are always welcome!

1. **Fork** the repository and clone your fork.
2. Create a feature branch: `git checkout -b feature/awesome-feature`.
3. Keep changes focused and test thoroughly in Ren'Py.
4. Run the stats linter if story scripts were edited:
   ```bash
   python tools/script_stats_linter.py
   ```
5. Commit and open a **Pull Request** against the **`dev`** branch.

---

## Building Distributions

To package a standalone release for players (Windows, Linux, macOS):
1. Open the project in the **Ren'Py Launcher**.
2. Click **"Build Distributions"**.
3. Select your desired formats (e.g. PC: Windows + Linux, Mac).
4. Build rules in `game/options.rpy` ensure `source_assets/`, Git metadata, and developer scratch files are automatically stripped from release archives.

---


<!-- SCRIPT_STATS:START -->
## Story & Script Statistics

### General Metrics

| Metric | Value | Ratio |
| :--- | :---: | :--- |
| **Total Words** | **120 081** | `100%` |
| **Total Script Lines** | **5 787** | `100%` |
| Narration / Description | 79 736 words / 3 043 lines | `66.4%` ███████░░░ |
| Spoken Dialogue (Characters) | 40 345 words / 2 744 lines | `33.6%` ███░░░░░░░ |
| Unique Speakers | 103 | — |
| Script Files (.rpy) | 158 | — |

### Chapter Breakdown

| Chapter | Files | Lines | Words | Dialogue Share |
| :--- | :---: | :---: | :---: | :--- |
| **Chapter 1: The Blue Sheep** | 12 | 402 | 8 223 | `33.1%` ███░░░░░ |
| **Chapter 2: In Search of A Friend** | 8 | 98 | 2 942 | `15.2%` █░░░░░░░ |
| **Chapter 3: Escapism** | 18 | 331 | 6 836 | `32.1%` ███░░░░░ |
| **Chapter 4.0: Ark Aground** | 6 | 246 | 5 942 | `47.8%` ████░░░░ |
| **Chapter 4.5: From Exile to Constellation** | 22 | 1 120 | 26 972 | `37.6%` ███░░░░░ |
| **Chapter 5: An Offer You Can’t Refuse** | 37 | 959 | 15 622 | `37.7%` ███░░░░░ |
| **Chapter 6: First row. Fifth seat.** | 7 | 355 | 7 214 | `30.3%` ██░░░░░░ |
| **Chapter 7: Fog of War** | 6 | 308 | 6 344 | `31.8%` ███░░░░░ |
| **Chapter 8: School Days...?** | 22 | 1 484 | 27 701 | `31.5%` ███░░░░░ |
| **Chapter 9: Resonating Dissonance** | 7 | 183 | 4 155 | `26.1%` ██░░░░░░ |
| **Flashbacks & Memory Fragments** | 13 | 301 | 8 130 | `25.7%` ██░░░░░░ |
| **TOTAL** | **158** | **5 787** | **120 081** | `33.6%` |

### Character Dialogue Distribution

| Character | Lines | Words | Word Share (of dialogue) |
| :--- | :---: | :---: | :--- |
| **Neon** | 1 168 | 13 785 | `34.2%` ███░░░░░ |
| **Seraphina** | 164 | 3 516 | `8.7%` █░░░░░░░ |
| **Argon** | 164 | 3 063 | `7.6%` █░░░░░░░ |
| **Oganesson (Guardian)** | 140 | 2 499 | `6.2%` ░░░░░░░░ |
| **Lily** | 141 | 2 119 | `5.3%` ░░░░░░░░ |
| **Celeste** | 111 | 1 650 | `4.1%` ░░░░░░░░ |
| **Alex** | 99 | 1 614 | `4.0%` ░░░░░░░░ |
| **Meryl Kendrick** | 52 | 1 284 | `3.2%` ░░░░░░░░ |
| **Sibyl** | 36 | 880 | `2.2%` ░░░░░░░░ |
| **Marcus** | 48 | 792 | `2.0%` ░░░░░░░░ |
| **Nari** | 56 | 715 | `1.8%` ░░░░░░░░ |
| **Sophie** | 41 | 524 | `1.3%` ░░░░░░░░ |
| **Akane (Mother)** | 30 | 509 | `1.3%` ░░░░░░░░ |
| **Xenon** | 21 | 506 | `1.3%` ░░░░░░░░ |
| **Teacher Akari** | 18 | 308 | `0.8%` ░░░░░░░░ |
| **Anna** | 14 | 123 | `0.3%` ░░░░░░░░ |
| **Helium** | 1 | 1 | `0.0%` ░░░░░░░░ |

<details>
<summary><b>Additional and episodic characters (86)</b></summary>

| Character | Lines | Words | Word Share |
| :--- | :---: | :---: | :--- |
| **???** | 42 | 561 | `1.4%` ░░░░░░░░ |
| **Priest** | 22 | 492 | `1.2%` ░░░░░░░░ |
| **Young Oganesson** | 22 | 445 | `1.1%` ░░░░░░░░ |
| **Guts** | 14 | 296 | `0.7%` ░░░░░░░░ |
| **Hans** | 13 | 270 | `0.7%` ░░░░░░░░ |
| **Young Alex** | 18 | 246 | `0.6%` ░░░░░░░░ |
| **Student 1 (Amy)** | 8 | 234 | `0.6%` ░░░░░░░░ |
| **Entity / Illusion** | 10 | 224 | `0.6%` ░░░░░░░░ |
| **Student 2 (Carol)** | 16 | 218 | `0.5%` ░░░░░░░░ |
| **Mr. Baumann (CEO)** | 10 | 175 | `0.4%` ░░░░░░░░ |
| **Carol** | 13 | 168 | `0.4%` ░░░░░░░░ |
| **Oda** | 9 | 165 | `0.4%` ░░░░░░░░ |
| **Boss** | 7 | 162 | `0.4%` ░░░░░░░░ |
| **Amy** | 11 | 154 | `0.4%` ░░░░░░░░ |
| **Garden Staff** | 12 | 138 | `0.3%` ░░░░░░░░ |
| **Alex's Mom** | 9 | 129 | `0.3%` ░░░░░░░░ |
| **Диктор Новостей** | 3 | 128 | `0.3%` ░░░░░░░░ |
| **P.E. Teacher** | 14 | 123 | `0.3%` ░░░░░░░░ |
| **ABSU / FCS** | 7 | 98 | `0.2%` ░░░░░░░░ |
| **Часовой** | 14 | 96 | `0.2%` ░░░░░░░░ |
| **Bartender** | 4 | 91 | `0.2%` ░░░░░░░░ |
| **Old Man** | 9 | 82 | `0.2%` ░░░░░░░░ |
| **Dr. Grubenmann (CRO)** | 3 | 82 | `0.2%` ░░░░░░░░ |
| **Headteacher** | 3 | 78 | `0.2%` ░░░░░░░░ |
| **Bandit 1** | 4 | 75 | `0.2%` ░░░░░░░░ |
| **Automaton** | 9 | 72 | `0.2%` ░░░░░░░░ |
| **Bandit 2** | 3 | 72 | `0.2%` ░░░░░░░░ |
| **Young Hoshiko** | 7 | 69 | `0.2%` ░░░░░░░░ |
| **Unknown Female** | 2 | 67 | `0.2%` ░░░░░░░░ |
| **Kai Ito** | 4 | 65 | `0.2%` ░░░░░░░░ |
| **Bartender Staff** | 4 | 63 | `0.2%` ░░░░░░░░ |
| **Concierge** | 4 | 62 | `0.2%` ░░░░░░░░ |
| **Mika Kitamura** | 4 | 58 | `0.1%` ░░░░░░░░ |
| **Waitress** | 5 | 52 | `0.1%` ░░░░░░░░ |
| **Woman** | 5 | 49 | `0.1%` ░░░░░░░░ |
| **Worker 1** | 2 | 47 | `0.1%` ░░░░░░░░ |
| **Academy Director** | 2 | 43 | `0.1%` ░░░░░░░░ |
| **Rico** | 6 | 38 | `0.1%` ░░░░░░░░ |
| **Ishikawa-sensei** | 2 | 36 | `0.1%` ░░░░░░░░ |
| **Girl (Neon)** | 5 | 31 | `0.1%` ░░░░░░░░ |
| **Мать** | 1 | 31 | `0.1%` ░░░░░░░░ |
| **Fan 1** | 4 | 30 | `0.1%` ░░░░░░░░ |
| **Fan 2** | 3 | 29 | `0.1%` ░░░░░░░░ |
| **Fan 3** | 3 | 29 | `0.1%` ░░░░░░░░ |
| **Student A** | 2 | 28 | `0.1%` ░░░░░░░░ |
| **News Anchor** | 1 | 27 | `0.1%` ░░░░░░░░ |
| **Security Captain** | 3 | 25 | `0.1%` ░░░░░░░░ |
| **Student C** | 1 | 25 | `0.1%` ░░░░░░░░ |
| **Control Officer** | 4 | 24 | `0.1%` ░░░░░░░░ |
| **Concierge (Female)** | 3 | 24 | `0.1%` ░░░░░░░░ |
| **Consultant** | 2 | 24 | `0.1%` ░░░░░░░░ |
| **Рико** | 1 | 24 | `0.1%` ░░░░░░░░ |
| **Worker 2** | 2 | 23 | `0.1%` ░░░░░░░░ |
| **Отец** | 1 | 22 | `0.1%` ░░░░░░░░ |
| **CEO's Voice** | 1 | 21 | `0.1%` ░░░░░░░░ |
| **Medrobot** | 3 | 20 | `0.0%` ░░░░░░░░ |
| **Guard** | 4 | 19 | `0.0%` ░░░░░░░░ |
| **Commander** | 2 | 19 | `0.0%` ░░░░░░░░ |
| **Security Officer** | 2 | 17 | `0.0%` ░░░░░░░░ |
| **Mercenary Commander** | 3 | 16 | `0.0%` ░░░░░░░░ |
| **Fan 4** | 2 | 16 | `0.0%` ░░░░░░░░ |
| **Shareholder 2's Voice** | 1 | 16 | `0.0%` ░░░░░░░░ |
| **Student B** | 1 | 15 | `0.0%` ░░░░░░░░ |
| **Vendor** | 1 | 15 | `0.0%` ░░░░░░░░ |
| **Student 1** | 1 | 13 | `0.0%` ░░░░░░░░ |
| **Student 1 (Girl)** | 1 | 13 | `0.0%` ░░░░░░░░ |
| **Voice** | 3 | 11 | `0.0%` ░░░░░░░░ |
| **Bully 2** | 1 | 11 | `0.0%` ░░░░░░░░ |
| **Passenger** | 1 | 11 | `0.0%` ░░░░░░░░ |
| **Father** | 1 | 9 | `0.0%` ░░░░░░░░ |
| **Shareholder 1's Voice** | 1 | 9 | `0.0%` ░░░░░░░░ |
| **Celeste (Phantom)** | 1 | 8 | `0.0%` ░░░░░░░░ |
| **Fan 5** | 1 | 8 | `0.0%` ░░░░░░░░ |
| **Security Commander** | 1 | 8 | `0.0%` ░░░░░░░░ |
| **Shareholder 1** | 1 | 8 | `0.0%` ░░░░░░░░ |
| **Парень** | 1 | 8 | `0.0%` ░░░░░░░░ |
| **Bully 1** | 1 | 7 | `0.0%` ░░░░░░░░ |
| **Boy** | 2 | 6 | `0.0%` ░░░░░░░░ |
| **Courier** | 1 | 6 | `0.0%` ░░░░░░░░ |
| **Guard's Voice** | 1 | 6 | `0.0%` ░░░░░░░░ |
| **Bodyguard** | 2 | 5 | `0.0%` ░░░░░░░░ |
| **Passerby** | 1 | 5 | `0.0%` ░░░░░░░░ |
| **Clara** | 3 | 4 | `0.0%` ░░░░░░░░ |
| **Students** | 1 | 4 | `0.0%` ░░░░░░░░ |
| **Desk Neighbor** | 1 | 3 | `0.0%` ░░░░░░░░ |
| **Absolute Silence** | 1 | 1 | `0.0%` ░░░░░░░░ |

</details>

<!-- SCRIPT_STATS:END -->

## License & Rights

This project uses a hybrid license to encourage learning and modding while protecting proprietary content.

*   **Source Code** (Logic, Mechanics, GUI) is licensed under **MIT**.
    *   *You are free to use the code in your own projects, even commercial ones.*
*   **Story & Assets** (Script, Graphics, Music, Characters) are licensed under **CC BY-NC-SA 4.0**.
    *   *You are free to create mods, translations, and fan art.*
    *   ***Commercial use is prohibited.** You cannot sell the game or its assets.*

See [LICENSE](LICENSE) for the full text.
