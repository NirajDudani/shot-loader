# Shot Loader for Nuke

A Python GUI tool for [Foundry Nuke](https://www.foundry.com/products/nuke) that turns a studio-style folder hierarchy into a clickable Project → Sequence → Shot → Element → Version dropdown, so compositors can open any scene or save an auto-incremented version without typing a path or renaming a file by hand.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Nuke](https://img.shields.io/badge/Nuke-11%2B-yellow)
![PySide2](https://img.shields.io/badge/PySide2-bundled%20with%20Nuke-41cd52)
![License](https://img.shields.io/badge/License-MIT-green)

---

## What It Does

Point Shot Loader at your project root, click **Load**, and the five dropdowns cascade through Project → Sequence → Shot → Element → Version as you select each one. **Open Scene** opens the selected `.nk` file; **Save Scene** reads the highest existing version in the target folder and saves a new file one version up (`v0001` → `v0002`), with zero-padded naming baked in — so versioning stays consistent across every artist on the show.

---

## Folder Structure Required

Shot Loader expects this exact hierarchy and naming convention:

```
Root_Directory/
├── Project_A/
│   ├── Sequence_001/
│   │   ├── Shot_001/
│   │   │   ├── Element_001/
│   │   │   │   ├── Project_A_Sequence_001_Shot_001_Element_001_v0001.nk
│   │   │   │   └── Project_A_Sequence_001_Shot_001_Element_001_v0002.nk
│   │   │   └── Element_002/
│   │   └── Shot_002/
│   └── Sequence_002/
└── Project_B/
```

Filenames must follow the pattern `<Project>_<Sequence>_<Shot>_<Element>_v<####>.nk` (four-digit zero-padded version). Folders and files that don't match are simply ignored by the loader.

---

## Installation

### Step 1 — Download

Clone the repo or download the ZIP:

```bash
git clone https://github.com/YOUR_USERNAME/shot-loader.git
```

Or click **Code → Download ZIP** on the GitHub page and extract it.

### Step 2 — Copy the Script

Copy `shot_loader.py` into your `.nuke` directory:

| OS | Default Path |
|----|-------------|
| Windows | `C:\Users\<you>\.nuke\` |
| macOS | `/Users/<you>/.nuke/` |
| Linux | `/home/<you>/.nuke/` |

> **Tip:** If you don't see a `.nuke` folder, open Nuke once and it will create one automatically. On Windows and macOS, hidden folders may not show by default — enable "Show hidden files" in your file browser.

### Step 3 — Register the Script

Open (or create) `menu.py` inside your `.nuke` directory and add this line:

```python
import shot_loader
```

### Step 4 — Restart Nuke

Close and reopen Nuke. You'll find the new entry at **Nuke → Tools → Shot Loader**.

---

## How to Use It

### 1. Open Shot Loader

Go to **Nuke → Tools → Shot Loader**. The dialog appears with an empty root-directory field at the top and five dropdowns below.

### 2. Select Your Root Directory

Click **Browse** and navigate to your project root (the folder that contains all your projects). The path will appear in the field next to the button.

### 3. Load the Structure

Click **Load**. The *Project* dropdown populates with every project folder found. Selecting a project auto-populates *Sequence*, which auto-populates *Shot*, and so on down to *Version*.

| Dropdown | What it reads |
|----------|---------------|
| Project | Subfolders directly under the root |
| Sequence | Subfolders of the selected project |
| Shot | Subfolders of the selected sequence |
| Element | Subfolders of the selected shot |
| Version | Trailing `v####` tokens from `.nk` filenames in the element folder, sorted latest-first |

### 4. Open a Scene

Once all five dropdowns are set, click **Open Scene**. Shot Loader builds the expected filename, verifies it exists on disk, and opens it in Nuke. If the file isn't there you'll get a "File Not Found" dialog showing the path it tried.

### 5. Save a New Version

With a scene open and the dropdowns set to the element you want to save into, click **Save Scene**. Shot Loader scans the element folder for the highest existing `v####` number, increments it by one, and saves the current script as:

```
<Project>_<Sequence>_<Shot>_<Element>_v<####>.nk
```

For example, if `v0006` already exists, the new save becomes `v0007` — zero-padded, inside the correct element folder. The dialog closes automatically on a successful save.

---

## Requirements

- **Nuke 11+** (any version with PySide2 bundled — this includes most modern releases)
- No external Python packages required; everything used (`os`, `PySide2`, `nuke`) ships with Nuke's embedded Python.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Menu entry doesn't appear | Make sure the file is named `shot_loader.py` and lives directly inside `.nuke/`. Check Nuke's Script Editor for import errors. |
| "No valid root folder selected" | Click **Browse** and pick a folder before clicking **Load**. The field accepts typed paths too, but they must point at an existing directory. |
| A dropdown is empty after selecting its parent | The parent folder contains no subfolders, or the folder names don't match the expected structure. Shot Loader only lists real subdirectories — loose files are ignored. |
| Version dropdown is empty even though `.nk` files exist | Filenames must end in `_v<digits>.nk` (e.g. `..._v0001.nk`). Files with non-standard suffixes (`_wip`, `_final`, no version token) are skipped. |
| "File Not Found" when opening a scene | The filename on disk doesn't exactly match `<Project>_<Sequence>_<Shot>_<Element>_v<####>.nk`. Check for typos, mismatched case on Linux, or extra tokens in the filename. |
| "Target save directory does not exist" | Save Scene writes into `<root>/<project>/<sequence>/<shot>/<element>/` — all five levels must already exist. Create the missing folder manually, then retry. |

---

## Contributing

Contributions are welcome — feel free to open issues or submit pull requests. If you're adding a feature, please test it against a root directory with at least two projects, mixed version counts per element (including one element with no versions yet), and a file whose name doesn't match the convention — to confirm the skip-paths stay graceful.

---

## License

MIT — use it however you like.
