# Project: DoctorNeonPrototype Technical Audit & Action Plan Tracker

## Architecture
- **Engine**: Ren'Py 8.x (Ren'Py 8.3.7 / 8.5.3, Python 3 environment)
- **Subsystems**:
  - Narrative Scripts: `game/game-scripts/` (Volume 1: Prologue to Ch4.5, Volume 2: Ch5 to Ch9; 158 `.rpy` scripts, 5,993 lines, 125,317 words)
  - Engine Modules: `game/modules/` (achievements, glossary, inventory, sound, update, dlc-download, main-menu, gallery)
  - Core Launch & Options: `game/launch.rpy`, `game/script.rpy`, `game/options.rpy`, `game/screens.rpy`, `game/gui.rpy`
  - Devtools & Automation: `game/devtools/`, `tools/` (`script_stats_linter.py`, `rpy-to-text-converter.py`, `update_stats.bat`)
  - Asset Repository: `game/` (images, audio, fonts, gui; 1,933 files, 654.49 MB) vs `source_assets/`, `unused/`, `backups/`
  - Distribution Manifests: `game/dlc_manifest.json`, `files.txt`, `project.json`

---

## 1. Milestone Status Overview

| Milestone ID | Description | Target Scope | Implementation Status | Notes |
|:---|:---|:---|:---:|:---|
| **M1** | Codebase & Devtools Technical Audit | Audit scripts, AST syntax, rollback safety, security leaks, devtools | **DONE** | Completed in `PROJECT_AUDIT_REPORT.md` (Sections 1–3) |
| **M2** | Asset Inventory & Performance Audit | Audit media formats, bloat, dead assets, duplicates, paths | **DONE** | Completed in `PROJECT_AUDIT_REPORT.md` (Section 4) |
| **M3** | Comprehensive Report Generation | Compile full report with metrics, tables, and Action Plan | **DONE** | Root `PROJECT_AUDIT_REPORT.md` created |
| **M4** | Multi-Perspective Gate & Forensic Audit | 2 Reviewers, 2 Challengers, 1 Forensic Auditor validation | **DONE** | Verdicts CLEAN / APPROVED |
| **PHASE-1** | Immediate Hotfixes & Security | 10 hotfix tasks: cheats, DLC launch, crash, paths, Zip Slip, SSL | **IN PROGRESS / PARTIAL** | 7 Completed, 2 Partial, 1 Pending (70% Done / 90% Mitigated) |
| **PHASE-2** | Asset Optimization (-364 MB) | 6 asset tasks: Ch5 CG AVIF, font subset, items WebP, MP3->Opus, dead assets, junk | **PENDING** | 0 Completed, 6 Pending (0% Done). Blocked by Art Hazard Protocol |
| **PHASE-3** | Architecture Refactoring | 8 core tasks: default state, GPU text shaders, Dimmer, audio TODOs, menus, ambient | **IN PROGRESS / PARTIAL** | 5 Completed, 1 Partial, 2 Pending; 6 auxiliary fixes Done (75% Done) |
| **PHASE-4** | CI/CD Automation & Toolchains | 6 tasks: dynamic badges, linter, --check flag, PR block, converter CLI, toolchains | **IN PROGRESS / PARTIAL** | 5 Completed, 1 Pending (83% Done) |

---

## 2. Feature & Survey Inventory

| # | Feature / Area | Description | Milestone | Audit Survey Status | Code Implementation Status | Primary Commit / File Reference |
|---|----------------|-------------|:---:|:---:|:---:|:---|
| 1 | Crash Log Correlation | Correlate `errors.txt`, `traceback.txt`, `log.txt` with code | M1 | DONE | **DONE** | `6ae9647` (dissolve fix), `248d7e9` |
| 2 | Launch & Startup Logic | Resolve `launch.rpy:79` DLC label typo and startup sequencing | M1 | DONE | **DONE** | `fbf9697` (`game/launch.rpy:78-80`) |
| 3 | State & Rollback Safety | Audit inventory/glossary `init python` vs `default` declarations | M1 | DONE | **DONE** | `d436884`, `daf8c3d` (`inventory-class.rpy:1-3`, `bio_system-class.rpy:2`) |
| 4 | Production Build Leaks | Fix `renpy_warp` daemons leaking into release builds and scanning ports | M1 | DONE | **DONE** | `a27671e`, `cc7a90b` (`options.rpy:217-218`, daemon wiped) |
| 5 | Security Audit | Remediate Zip Slip in DLC unpacker, `verify=False` SSL, and cheat bypass `or True` | M1 | DONE | **DONE** | `1ecee4c` (cheats), `1471498` (Zip Slip), `eb9440b` (SSL verify) |
| 6 | Performance & Redraws | Optimize `LavaLampName` GPU shaders and `Dimmer` 100 FPS matrix allocations | M1 | DONE | **IN PROGRESS / PARTIAL** | `cc31d07` (GPU Shaders DONE), `d3e5c71` (Dimmer 30 FPS PARTIAL) |
| 7 | Codebase Hygiene | Identify orphaned `.rpyc` files, `.bak`, `.pdn` files, and compiler junk | M1 | DONE | **IN PROGRESS / PARTIAL** | `2c93862` (orphaned .rpyc DONE), `949f76b` (.gitignore PARTIAL) |
| 8 | Missing Script References | Map 164 missing audio references and missing Chapter 5 CG/BG scenes | M1 | DONE | **IN PROGRESS / PARTIAL** | `1a9cdfb`, `11205b7` (Audio TODOs DONE); Ch5 scenes PENDING |
| 9 | Asset Inventory & Metrics | Tabulate repository disk metrics across all folders and media types | M2 | DONE | **DONE** | Documented in `PROJECT_AUDIT_REPORT.md` Section 4 |
| 10 | Uncompressed CG Bloat | Document 120 Chapter 5 PNGs (300.62 MB) and AVIF/WebP conversion savings | M2 | DONE | **PENDING** | 120 PNGs intact on disk; Art Preservation Hazard identified |
| 11 | Font CJK Bloat | Analyze `WDXLLubrifontTC-Regular.ttf` 9.86 MB bloat and subsetting to <300 KB | M2 | DONE | **PENDING** | 0% completed; full 20k CJK glyphs retained |
| 12 | Dead Assets Pruning | Catalog 69 confirmed dead assets in `game/` (67.42 MB) for safe quarantine | M2 | DONE | **PENDING** | Files remain in `game/`; blocked by 22 Ch5 CG backup requirement |
| 13 | Duplicate Assets Audit | Audit 41 intra-`game/` duplicates and source duplicates (99 source vs 120 game) | M2 | DONE | **PENDING** | 22 unique Ch5 files missing from `source_assets/` |
| 14 | Asset Path & Case Errors | Fix `absolutesIlence.png`, `ch05_cg01_v01.avif`, `particle.png`, `mop.png` | M2 | DONE | **IN PROGRESS / PARTIAL** | `bb82849` (mop DONE), `f6e6784` (particle DONE), `858757e` (fallback PARTIAL) |
| 15 | Manifest Synchronization | Reconcile `dlc_manifest.json` (version, 3 omitted BGM) and `files.txt` discrepancies | M2 | DONE | **PENDING** | Version remains `0.7.3-stable`; 3 active BGM missing; `files.txt` stale |
| 16 | Devtools & Linter Health | Audit `tools/script_stats_linter.py` (5,993 lines, 125,317 words) & CI/CD | M1 | DONE | **DONE** | `72eb410f`, `03b9a609`, `8489fc7`, `a494c95b`, `48b7c5a7` |
| 17 | Synthesis & Report Draft | Generate `PROJECT_AUDIT_REPORT.md` adhering to GFM and R1/R2/R3 requirements | M3 | DONE | **DONE** | Sections 1–5 fully synthesized and updated |
| 18 | Multi-Perspective Review | Dual-reviewer verification on technical accuracy and file/line citations | M4 | DONE | **DONE** | APPROVED by reviewer_gate2 |
| 19 | Challenger Stress Testing | Adversarial verification of report metrics, disk numbers, and calculations | M4 | DONE | **DONE** | APPROVED by challenger_gate2 |
| 20 | Forensic Integrity Audit | Forensic audit ensuring authentic analysis without dummy/facade data | M4 | DONE | **DONE** | CLEAN by auditor_gate2 |

---

## 3. Detailed Implementation Tasks Matrix (Roadmap & Action Plan)

### Phase 1: Immediate Hotfixes & Security
| # | Task | Target File & Line | Git Commit | Status | Scope & Remaining Work |
|---|------|-------------------|:---:|:---:|---|
| **1.1** | Отключение чит-меню в продакшене | `game/modules/main-menu/sub-menus/menu_data.rpy:298` | `1ecee4c` | **DONE** | `or True` removed; strictly guarded by `if config.developer:`. |
| **1.2** | Исправление вызова DLC в launch.rpy | `game/launch.rpy:78-80` | `fbf9697` | **DONE** | `if renpy.has_label("dlc_check_sequence"): call dlc_check_sequence`. |
| **1.3** | Устранение опечатки dissolv в Главе 5 | `game/game-scripts/chapters/chapter5/7-daughter-truth.rpy:24` | `6ae9647` | **DONE** | `with dissolve` committed. Clean in working tree. |
| **1.4** | Регистр файла `absolutesIlence.png` | `game/modules/achievements/achievements-class.rpy:95-101` | `858757e` | **PARTIAL** | *Done*: Programmatic fallback handles both cases. *Remaining*: Git index still has uppercase `I` (`game/images/achievements/absolutesIlence.png`). |
| **1.5** | Исправление битых путей меню и эффектов | `effects.rpy:60,63`, `options.rpy:83`, `menu_play.rpy:165` | `f6e6784`, `f598035`, `188f363` | **PARTIAL** | *Done*: `particle.png` fixed, menu music cleared, flags added. *Remaining*: `menu_play.rpy:165` points to non-existent `vol1/.../ch05_cg01_v01.avif`. |
| **1.6** | Уязвимость Zip Slip (CWE-22) | `game/modules/dlc-download/dlc-config-new.rpy:149-155` | `1471498` | **DONE** | Canonical `os.path.commonpath` verification added. |
| **1.7** | Изоляция `renpy_warp` и удаление дубликата | `game/options.rpy:217-218`, `renpy_warp_1.34.0...rpe.py` | `a27671e`, `cc7a90b` | **DONE** | Excluded from builds via `build.classify`; duplicate file wiped. |
| **1.8** | SSL валидация в автоапдейтере | `game/modules/update/update_checker.rpy:73` | `eb9440b` | **DONE** | `verify=False` purged; standard TLS verification enforced. |
| **1.9** | Синхронизация манифеста DLC | `game/dlc_manifest.json:204` | — | **PENDING** | *Remaining*: Version remains `0.7.3-stable`; 3 active BGM missing; 26 dead audio tracks present. |
| **1.10**| Добавление ассета `mop.png` в инвентарь | `game/images/items/mop.png`, `4.0-quest-hub-level3.rpy:11` | `bb82849`, `e29b228` | **DONE** | Valid 34.3 KB PNG created, committed to game and source_assets, wired in script. |

### Phase 2: Asset Optimization & Space Reclamation (-364.38 MB)
| # | Task | Target Resources | Current Metric | Status | Scope & Remaining Work |
|---|------|-----------------|:---:|:---:|---|
| **2.1** | Пакетное сжатие CG Главы 5 | `game/images/cg/vol2/chapter5/` | 120 PNGs, 300.62 MB | **PENDING** | 0% completed. **CRITICAL ART HAZARD**: 22 unique CGs missing from `source_assets/`! Must backup before converting. Atomic script coupling update. |
| **2.2** | Сабсеттинг CJK шрифта WDXLLubrifontTC | `game/fonts/WDXLLubrifontTC-Regular.ttf` | 10,336,832 B (9.86 MB) | **PENDING** | 0% completed. Subset to Latin + Cyrillic via `pyftsubset` (-9.61 MB). |
| **2.3** | Ресайз иконок инвентаря (2048px -> 512px) | `game/images/items/` (10 PNGs) | 10.67 MB uncompressed | **PENDING** | 0% completed. Resize to 512x512 WebP (-10.14 MB) + atomic script path updates in `Item(...)`. |
| **2.4** | Конвертация 4 MP3 в Opus 128k | `game/audio/music/BGM/` (4 MP3s) | 10.27 MB | **PENDING** | 0% completed. Convert Caduceus, CallYou, DroppedHydrangea, LoneMission to Opus (-6.77 MB). |
| **2.5** | Архивация 69 dead assets (26 audio, 43 images) | `game/audio/` (45.79 MB), `game/images/` (21.62 MB) | 67.42 MB dead assets | **PENDING** | 0% completed. Move to `unused/` quarantine AFTER backing up 22 Ch5 CGs. |
| **2.6** | Очистка мусора (zip, bak, saves, pdn) | `english_us.zip`, `*.bak`, `game/saves/`, `*.pdn` | ~8.43 MB junk | **PENDING** | 0% completed. Delete zip (3.19 MB), 239 bak files (1.75 MB), 25 saves (3.49 MB), disk pdn files. |

### Phase 3: Architecture Refactoring & State Safety
| # | Task | Target File & Line | Git Commit | Status | Scope & Remaining Work |
|---|------|-------------------|:---:|:---:|---|
| **3.1** | Перевод инвентаря и глоссария на `default` | `inventory-class.rpy:1-3`, `bio_system-class.rpy:2` | `d436884`, `daf8c3d` | **DONE** | Variables declared with `default`; `Item` inherits `renpy.store.object`. `_rollback=False` scoped to quest puzzle. |
| **3.2** | GPU-шейдеры имен (текстовые шейдеры) | `game/modules/characters/name_effects.rpy:16-52, 98-112` | `cc31d07` | **DONE** | Ren'Py 8 GPU Text Shaders replace 25 FPS CPU rasterization loop. |
| **3.3** | ATL / Оптимизация Dimmer | `game/modules/auto-highlight.rpy:53-74` | `d3e5c71` | **PARTIAL** | *Done*: Polling frequency reduced from 100 FPS (0.01) to 30 FPS (0.033) with matrixcolor interpolation. *Remaining*: Pure ATL syntax if required. |
| **3.4** | Оптимизация галереи CG (статические thumbs / H7) | `game/modules/gallery/gallery-setup.rpy:76` | — | **PENDING** | *Remaining*: Currently calls dynamic `Transform(self.thumb)` on 1080p full textures. Generate 384x216 WebP thumbnails. |
| **3.5** | Заглушки отсутствующих сцен Главы 5 (C4) | `10-father-sacrifice.rpy:134`, `11-wasteland.rpy:18` | — | **PENDING** | *Remaining*: `cg_argon_sacrifice_window` and `bg earth_wasteland_night` lack visual placeholder bindings. |
| **3.6** | Заглушение 274 отсутствующих аудиовызовов | 78 narrative script files across Chapters 4.5–9 | `1a9cdfb`, `11205b7` | **DONE** | All 274 missing audio calls commented out with `# TODO: missing audio: play ...`. |
| **3.7** | Удаление дубликата экрана main_menu | `game/screens.rpy:369`, `main-menu_custom-new.rpy` | `ffe3ea5` | **DONE** | Duplicate `screen main_menu()` removed from `screens.rpy`. Single source of truth preserved. |
| **3.8** | Слайдер ambient в настройках звука | `menu_settings.rpy:217-229`, `tl/english_us/` | `97c9fc4` | **DONE** | Volume bar and reset button wired to `Preference("ambient volume")`. Localization synced. |
| **3.9** | Сопутствующие рефакторинги (M2–M6, H8) | `punctuation.rpy`, `update_checker.rpy`, `achievements-class.rpy`, `dlc_builder.rpy` | `5421f2d`, `286622b`, `fb1e7b7`, `861b548`, `ac8c6ef`, `2c93862` | **DONE** | M2 skip guard, M3 notification race, M4 persistent save, M5 dead code, M6 threaded DLC builder, H8 orphaned .rpyc all resolved. |

### Phase 4: CI/CD Automation & Toolchains
| # | Task | Target File & Line | Git Commit | Status | Scope & Remaining Work |
|---|------|-------------------|:---:|:---:|---|
| **4.1** | Динамические бейджи в документации | `README.md:10-15`, `README.ru.md:10-15` | `72eb410f` | **DONE** | Shields.io dynamic badges synced across EN and RU documentation. |
| **4.2** | Динамический подсчет глав в линтере | `tools/script_stats_linter.py:459-472` | `03b9a609` | **DONE** | Hardcoded chapter count removed; dynamically calculated from dictionary. |
| **4.3** | Флаг `--check` в линтере и код возврата | `tools/script_stats_linter.py:685-758` | `8489fc7`, `03b9a609` | **DONE** | Returns exit code 0 when synced, exit code 1 when diff found. |
| **4.4** | Шаг блокировки PR в GitHub Actions | `.github/workflows/stats_lint.yml:38-53` | `a494c95b` | **DONE** | Fails PR with error annotation if README stats are out of sync. |
| **4.5** | Рефакторинг `rpy-to-text-converter.py` | `tools/rpy-to-text-converter.py:233-268, 357-386` | `48b7c5a7` | **DONE** | `extract_label_lines()` isolates scope; full `argparse` CLI added (`--chapter`, `--output`). |
| **4.6** | Фиксация версий зависимостей / toolchains | `project.json`, `options.rpy:26`, `dlc_manifest.json:204` | — | **PENDING** | *Remaining*: Version consolidation (`0.8.2-early` vs `0.7.3-stable`), `files.txt` generator, CI `renpy lint` workflow. |

### Low-Priority Defects (L1–L10)
| ID | Defect Description | Target File & Line | Git Commit | Status | Scope & Remaining Work |
|:---|:---|:---|:---:|:---:|:---|
| **L1** | Updater-config duplicate `"mb_total"` | `game/modules/updater/updater-config.rpy:16` | `1ed8971` | **DONE** | Duplicate dictionary key removed. |
| **L2** | Chapter 5 duplicate `return` | `game/game-scripts/chapters/chapter5/chapter-5.rpy:37` | `248d7e9` | **DONE** | Redundant return statement removed. |
| **L3** | Language setup dictionary PEP8 indent | `game/modules/language/language_setup.rpy:26-29` | `28870f9` | **DONE** | Closing brace indented by 4 spaces. |
| **L4** | Chapter 3 1-start `default` indent | `game/game-scripts/chapters/chapter3/1-start.rpy:1-21` | `792463e` | **DONE** | Aligned to column 0 at file header. |
| **L5** | Compiler `.rpyc.bak` and `.bak` junk | `.gitignore:35-40`, local filesystem | `949f76b` | **PARTIAL** | *Done*: `.gitignore` updated. *Remaining*: 76 `.bak` and 22 `.disabled` files remain on disk. |
| **L6** | Converter hardcode & recursive call | `tools/rpy-to-text-converter.py:270-366` | `48b7c5a` | **DONE** | Cleaned up with isolated label bounds. |
| **L7** | Batch script pause in automated CI | `tools/update_stats.bat:63, 76` | `e1203ea` | **DONE** | Guarded by CI check and `--no-pause` flag. |
| **L8** | DLC files_manifest explicit UTF-8 | `game/modules/dlc-download/files_manifest.rpy:48, 65` | `4b66b3f` | **DONE** | Explicit `encoding="utf-8"` added to all `open()` calls. |
| **L9** | Progressive download voice directory | `progressive_download.txt:9` | `defc864` | **DONE** | Path corrected to `+ voice game/audio/voice/**`. |
| **L10**| CTC `.pdn` junk files in `game/` | `game/options.rpy:230`, `source_assets/images/ctc/` | `c648466`, `3fcd00d` | **PARTIAL** | *Done*: Backed up to source_assets and excluded from builds. *Remaining*: Files remain on disk in `game/images/ctc/`. |

---

## 4. Actionable Summary of Remaining Implementation Work

### 1. Phase 2 Asset Optimization & Space Reclamation (-364.38 MB / -58.7%)
1. **Chapter 5 CG Conversion (2.1)**:
   - 120 PNG files in `game/images/cg/vol2/chapter5/` (300.62 MB) must be converted to AVIF or WebP (quality=85).
   - Expected space saving: **~262.77 MB**.
   - Requires atomic update of image references in narrative scripts and `menu_play.rpy:165`.
2. **CJK Font Subsetting (2.2)**:
   - `game/fonts/WDXLLubrifontTC-Regular.ttf` (9.86 MB / 10,336,832 bytes) retains 20,000+ Chinese characters.
   - Run `pyftsubset` with Latin and Cyrillic glyph sets.
   - Expected space saving: **~9.61 MB** (down to ~250 KB).
3. **Inventory Items Downscaling (2.3)**:
   - 10 PNG icons in `game/images/items/` (10.67 MB, up to 2048px) must be resized to 512x512 WebP.
   - Expected space saving: **~10.14 MB**.
   - Requires updating `Item(...)` constructors in `level-3/4.0-quest-hub-level3.rpy` and `level-2/3.0-quest-hub-level2.rpy`.
4. **BGM Audio MP3 -> Opus (2.4)**:
   - 4 MP3 files in `game/audio/music/BGM/` (`Caduceus`, `CallYou`, `DroppedHydrangea`, `LoneMission`) totaling 10.27 MB.
   - Convert to Opus 128 kbps. Expected saving: **~6.77 MB**.
5. **Dead Assets Quarantine (2.5)**:
   - 26 dead audio tracks (45.79 MB) and 37 dead image files (21.62 MB) in `game/`.
   - Move to quarantine directory `unused/` after Art Preservation backup. Expected saving: **67.42 MB**.
6. **Repository Junk Removal (2.6)**:
   - Remove `game/tl/english_us.zip` (3.19 MB).
   - Clean 239 `.bak`/`.disabled` files (1.75 MB) and 25 development saves in `game/saves/` (3.49 MB).
   - Remove tracked `.pdn` files from `game/images/ctc/`. Expected saving: **~8.43 MB**.

### 2. CRITICAL: Art Preservation Protocol (Art Destruction Hazard)
- **Observation**: `source_assets/images/chapter-5/16-9/` contains only **99 files**, whereas `game/images/cg/vol2/chapter5/` has **120 files**.
- **22 unique PNG files (50.93 MB)** exist ONLY in `game/`:
  `ch05_bg25_v01.png`, `ch05_cg55_v01..v02`, `ch05_cg56_v01..v05`, `ch05_cg57_v01..v03`, `ch05_cg58_v01`, `ch05_cg59_v01`, `ch05_cg60_v01`, `ch05_cg61_v01`, `ch05_cg62_v01`, `ch05_cg63_v01..v02`, `ch05_cg64_v01`, `ch05_cg65_v01..v02`, `ch05_cg66_v01`.
- **9 of these 22** are classified as dead assets (`ch05_bg25_v01`, `ch05_cg56_v04`, `ch05_cg58_v01..cg63_v02`).
- **RULE**: Any script or developer performing optimization or pruning **MUST first copy all 22 unique files to `source_assets/images/chapter-5/16-9/`** before executing any `rm` or format conversion. Deleting them from `game/` without backup will permanently destroy master-quality artwork.

### 3. CG Gallery Static Thumbnails (Task 3.4 / Defect H7)
- `game/modules/gallery/gallery-setup.rpy:76` dynamically invokes `Transform(self.thumb, fit="cover", size=(gal_thumb_x, gal_thumb_y))` on full 1080p graphics in the live render loop.
- Generate pre-rendered 384x216 WebP thumbnails in `game/images/gallery/thumbs/`.
- Refactor `get_thumbnail_displayable()` to return pre-rendered thumbnail paths directly.

### 4. Chapter 5 Missing Visual Placeholders (Task 3.5 / Defect C4)
- Narrative calls to `cg_argon_sacrifice_window`, `bg space_orbit_distant_explosion`, and `bg earth_wasteland_night` in `10-father-sacrifice.rpy`, `11-wasteland.rpy`, and `12-oganesson.rpy` currently produce black screens or missing image fallbacks.
- Define temporary placeholder image declarations pointing to existing space/wasteland art until final assets are delivered.

### 5. Distribution Manifests & Toolchain Consolidation (Tasks 1.9 & 4.6)
- **`game/dlc_manifest.json`**:
  - Update `"version"` from `"0.7.3-stable"` to `"0.8.2-early"`.
  - Add 3 active BGM tracks (`Caduceus.mp3`, `CallYou.mp3`, `LoneMission.mp3`).
  - Remove 26 dead audio references.
- **`files.txt`**:
  - Outdated since April 2026; missing 1,580+ files and containing 241 non-existent references.
  - Create an automated manifest generation tool (`tools/generate_files_manifest.py`).
- **Version SSOT & CI Workflow**:
  - Establish `project.json` as the single source of truth for version numbering across `options.rpy`, `dlc_manifest.json`, and Inno Setup installer.
  - Implement `.github/workflows/renpy_lint.yml` to automatically run `renpy lint` in headless mode on Pull Requests.

### 6. Residual Path Bugs & Git Repository Hygiene (Tasks 1.4, 1.5, L5, L10)
- **Chapter 5 Menu Banner (1.5)**: Correct `menu_play.rpy:165` from non-existent `"images/cg/vol1/chapter5/ch05_cg01_v01.avif"` to `"images/cg/vol2/chapter5/ch05_cg01_v01.png"` (or `.webp` after Phase 2).
- **Achievement Icon Git Index (1.4)**: Execute `git mv -f game/images/achievements/absolutesIlence.png game/images/achievements/absolutesilence.png` and commit to ensure canonical lowercase naming on case-sensitive filesystems.
- **Local Disk Junk Cleanup (L5, L10)**: Safely remove remaining 76 `.bak` files, 22 `.disabled` files, and 2 `.pdn` files from `game/images/ctc/`.

---

## 5. Verification Tools & Commands

```powershell
# 1. Script Stats & Documentation Sync Check (Pass: exit code 0)
python tools/script_stats_linter.py --check

# 2. Ren'Py AST & Script Syntax Compilation Lint (Pass: 0 errors across 11,232 dialogue blocks)
& "f:\RenPyDevelopment\renpy-8.3.7-sdk\lib\py3-windows-x86_64\python.exe" "f:\RenPyDevelopment\renpy-8.3.7-sdk\renpy.py" "f:\RenPyDevelopment\Projects\DoctorNeonPrototype" lint
```
