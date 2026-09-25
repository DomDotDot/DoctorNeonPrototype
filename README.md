# The Brightest Neon - Semitone Resonance

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/DomDotDot/DoctorNeonPrototype/blob/main/README.md)
[![ru](https://img.shields.io/badge/lang-ru-blue.svg)](https://github.com/DomDotDot/DoctorNeonPrototype/blob/main/README.ru.md)

![BannerVolume1](source_assets/promo/promoassets/BNSR-Poster-vol1.jpg)
![BannerVolume2](source_assets/promo/promoassets/BNSR-Poster-vol2.png)

<!-- BADGES -->
<!-- STATS_BADGES:START -->
![Words](https://img.shields.io/badge/Words-119.9k-blue?style=flat-square&logo=gitbook&logoColor=white)
![Lines](https://img.shields.io/badge/Lines-5%20786-4c1?style=flat-square)
![Chapters](https://img.shields.io/badge/Chapters-11%20-8a2be2?style=flat-square)
![Dialogue](https://img.shields.io/badge/Dialogue-34%25-informational?style=flat-square)
<!-- STATS_BADGES:END -->
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

### Developer Tools & Script Linter

*   **Story & Dialogue Stats Linter**: Run `tools/update_stats.bat` (or `python tools/script_stats_linter.py`) to automatically analyze dialogue, word counts, and refresh the badges and statistics in the README.

---

## Building

To create a distribution for players (Windows/Linux/Mac):
1. Open the Ren'Py Launcher.
2. Select the project.
3. Click **"Build Distributions"**.
4. Files from `source_assets` and Git system files are **automatically excluded** from the build (configured in `options.rpy`).


---

<!-- SCRIPT_STATS:START -->
## Story & Script Statistics

### General Metrics

| Metric | Value | Ratio |
| :--- | :---: | :--- |
| **Total Words** | **119 913** | `100%` |
| **Total Script Lines** | **5 786** | `100%` |
| Narration / Description | 79 587 words / 3 037 lines | `66.4%` ███████░░░ |
| Spoken Dialogue (Characters) | 40 326 words / 2 749 lines | `33.6%` ███░░░░░░░ |
| Unique Speakers | 103 | — |
| Script Files (.rpy) | 158 | — |

### Chapter Breakdown

| Chapter | Files | Lines | Words | Dialogue Share |
| :--- | :---: | :---: | :---: | :--- |
| **Chapter 1: The Blue Sheep** | 12 | 404 | 8 316 | `33.9%` ███░░░░░ |
| **Chapter 2: In Search of A Friend** | 8 | 98 | 2 944 | `15.2%` █░░░░░░░ |
| **Chapter 3: Escapism** | 18 | 331 | 6 840 | `32.0%` ███░░░░░ |
| **Chapter 4.0: Ark Aground** | 6 | 246 | 5 952 | `47.7%` ████░░░░ |
| **Chapter 4.5: From Exile to Constellation** | 22 | 1 120 | 26 966 | `37.5%` ███░░░░░ |
| **Chapter 5: An Offer You Can’t Refuse** | 37 | 951 | 15 385 | `38.2%` ███░░░░░ |
| **Chapter 6: First row. Fifth seat.** | 7 | 355 | 7 214 | `30.3%` ██░░░░░░ |
| **Chapter 7: Fog of War** | 6 | 305 | 6 309 | `32.0%` ███░░░░░ |
| **Chapter 8: School Days...?** | 22 | 1 484 | 27 689 | `31.6%` ███░░░░░ |
| **Chapter 9: Resonating Dissonance** | 7 | 183 | 4 155 | `26.1%` ██░░░░░░ |
| **Flashbacks & Memory Fragments** | 13 | 309 | 8 143 | `24.9%` ██░░░░░░ |
| **TOTAL** | **158** | **5 786** | **119 913** | `33.6%` |

### Character Dialogue Distribution

| Character | Lines | Words | Word Share (of dialogue) |
| :--- | :---: | :---: | :--- |
| **Neon** | 1 169 | 13 766 | `34.1%` ███░░░░░ |
| **Seraphina** | 164 | 3 488 | `8.6%` █░░░░░░░ |
| **Argon** | 164 | 3 072 | `7.6%` █░░░░░░░ |
| **Oganesson (Guardian)** | 140 | 2 501 | `6.2%` ░░░░░░░░ |
| **Lily** | 141 | 2 119 | `5.3%` ░░░░░░░░ |
| **Celeste** | 111 | 1 650 | `4.1%` ░░░░░░░░ |
| **Alex** | 100 | 1 634 | `4.1%` ░░░░░░░░ |
| **Meryl Kendrick** | 52 | 1 284 | `3.2%` ░░░░░░░░ |
| **Sibyl** | 36 | 880 | `2.2%` ░░░░░░░░ |
| **Marcus** | 48 | 840 | `2.1%` ░░░░░░░░ |
| **Nari** | 56 | 715 | `1.8%` ░░░░░░░░ |
| **Sophie** | 41 | 527 | `1.3%` ░░░░░░░░ |
| **Xenon** | 21 | 506 | `1.3%` ░░░░░░░░ |
| **Akane (Mother)** | 31 | 494 | `1.2%` ░░░░░░░░ |
| **Teacher Akari** | 18 | 308 | `0.8%` ░░░░░░░░ |
| **Anna** | 14 | 136 | `0.3%` ░░░░░░░░ |
| **Helium** | 1 | 1 | `0.0%` ░░░░░░░░ |

<details>
<summary><b>Additional and episodic characters (86)</b></summary>

| Character | Lines | Words | Word Share |
| :--- | :---: | :---: | :--- |
| **???** | 42 | 502 | `1.2%` ░░░░░░░░ |
| **Priest** | 22 | 492 | `1.2%` ░░░░░░░░ |
| **Young Oganesson** | 24 | 446 | `1.1%` ░░░░░░░░ |
| **Hans** | 14 | 301 | `0.7%` ░░░░░░░░ |
| **Guts** | 14 | 296 | `0.7%` ░░░░░░░░ |
| **Young Alex** | 18 | 246 | `0.6%` ░░░░░░░░ |
| **Student 1 (Amy)** | 8 | 234 | `0.6%` ░░░░░░░░ |
| **Entity / Illusion** | 10 | 224 | `0.6%` ░░░░░░░░ |
| **Student 2 (Carol)** | 16 | 218 | `0.5%` ░░░░░░░░ |
| **Carol** | 13 | 168 | `0.4%` ░░░░░░░░ |
| **Oda** | 9 | 165 | `0.4%` ░░░░░░░░ |
| **Boss** | 7 | 162 | `0.4%` ░░░░░░░░ |
| **Mr. Baumann (CEO)** | 10 | 158 | `0.4%` ░░░░░░░░ |
| **Amy** | 11 | 154 | `0.4%` ░░░░░░░░ |
| **Garden Staff** | 12 | 138 | `0.3%` ░░░░░░░░ |
| **Alex's Mom** | 9 | 129 | `0.3%` ░░░░░░░░ |
| **Диктор Новостей** | 3 | 128 | `0.3%` ░░░░░░░░ |
| **P.E. Teacher** | 14 | 123 | `0.3%` ░░░░░░░░ |
| **Часовой** | 14 | 96 | `0.2%` ░░░░░░░░ |
| **ABSU / FCS** | 6 | 92 | `0.2%` ░░░░░░░░ |
| **Bartender** | 4 | 91 | `0.2%` ░░░░░░░░ |
| **Dr. Grubenmann (CRO)** | 3 | 82 | `0.2%` ░░░░░░░░ |
| **Old Man** | 9 | 82 | `0.2%` ░░░░░░░░ |
| **Bandit 1** | 4 | 75 | `0.2%` ░░░░░░░░ |
| **Headteacher** | 3 | 74 | `0.2%` ░░░░░░░░ |
| **Bandit 2** | 3 | 72 | `0.2%` ░░░░░░░░ |
| **Automaton** | 9 | 72 | `0.2%` ░░░░░░░░ |
| **Young Hoshiko** | 7 | 69 | `0.2%` ░░░░░░░░ |
| **Unknown Female** | 2 | 65 | `0.2%` ░░░░░░░░ |
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
| **Girl (Neon)** | 5 | 34 | `0.1%` ░░░░░░░░ |
| **Мать** | 1 | 31 | `0.1%` ░░░░░░░░ |
| **Fan 1** | 4 | 30 | `0.1%` ░░░░░░░░ |
| **Fan 2** | 3 | 29 | `0.1%` ░░░░░░░░ |
| **Fan 3** | 3 | 29 | `0.1%` ░░░░░░░░ |
| **Student A** | 2 | 28 | `0.1%` ░░░░░░░░ |
| **News Anchor** | 1 | 27 | `0.1%` ░░░░░░░░ |
| **Security Captain** | 3 | 25 | `0.1%` ░░░░░░░░ |
| **Student C** | 1 | 25 | `0.1%` ░░░░░░░░ |
| **Consultant** | 2 | 24 | `0.1%` ░░░░░░░░ |
| **Guard** | 4 | 24 | `0.1%` ░░░░░░░░ |
| **Control Officer** | 4 | 24 | `0.1%` ░░░░░░░░ |
| **Рико** | 1 | 24 | `0.1%` ░░░░░░░░ |
| **Concierge (Female)** | 3 | 24 | `0.1%` ░░░░░░░░ |
| **Worker 2** | 2 | 23 | `0.1%` ░░░░░░░░ |
| **Отец** | 1 | 22 | `0.1%` ░░░░░░░░ |
| **CEO's Voice** | 1 | 21 | `0.1%` ░░░░░░░░ |
| **Medrobot** | 3 | 20 | `0.0%` ░░░░░░░░ |
| **Commander** | 2 | 19 | `0.0%` ░░░░░░░░ |
| **Security Officer** | 2 | 17 | `0.0%` ░░░░░░░░ |
| **Shareholder 2's Voice** | 1 | 16 | `0.0%` ░░░░░░░░ |
| **Mercenary Commander** | 3 | 16 | `0.0%` ░░░░░░░░ |
| **Fan 4** | 2 | 16 | `0.0%` ░░░░░░░░ |
| **Vendor** | 1 | 15 | `0.0%` ░░░░░░░░ |
| **Student B** | 1 | 15 | `0.0%` ░░░░░░░░ |
| **Student 1** | 1 | 13 | `0.0%` ░░░░░░░░ |
| **Student 1 (Girl)** | 1 | 13 | `0.0%` ░░░░░░░░ |
| **Passenger** | 1 | 11 | `0.0%` ░░░░░░░░ |
| **Voice** | 3 | 11 | `0.0%` ░░░░░░░░ |
| **Father** | 1 | 9 | `0.0%` ░░░░░░░░ |
| **Shareholder 1's Voice** | 1 | 9 | `0.0%` ░░░░░░░░ |
| **Security Commander** | 1 | 8 | `0.0%` ░░░░░░░░ |
| **Shareholder 1** | 1 | 8 | `0.0%` ░░░░░░░░ |
| **Парень** | 1 | 8 | `0.0%` ░░░░░░░░ |
| **Fan 5** | 1 | 8 | `0.0%` ░░░░░░░░ |
| **Celeste (Phantom)** | 1 | 8 | `0.0%` ░░░░░░░░ |
| **Boy** | 2 | 7 | `0.0%` ░░░░░░░░ |
| **Bully 2** | 1 | 7 | `0.0%` ░░░░░░░░ |
| **Bully 1** | 1 | 6 | `0.0%` ░░░░░░░░ |
| **Guard's Voice** | 1 | 6 | `0.0%` ░░░░░░░░ |
| **Courier** | 1 | 6 | `0.0%` ░░░░░░░░ |
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

*   💻 **Source Code** (Logic, Mechanics, GUI) is licensed under **MIT**.
    *   *You are free to use the code in your own projects, even commercial ones.*
*   🎨 **Story & Assets** (Script, Graphics, Music, Characters) are licensed under **CC BY-NC-SA 4.0**.
    *   *You are free to create mods, translations, and fan art.*
    *   *⛔ **Commercial use is prohibited.** You cannot sell the game or its assets.*

See [LICENSE](LICENSE) for the full text.
