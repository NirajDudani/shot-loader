# Shot-Loader  

A Nuke Python GUI tool designed to load and version-control scripts based on a structured production folder hierarchy.  

This tool helps artists quickly navigate projects, sequences, shots, elements, and versions — while enforcing a clean naming convention and automatic versioning workflow.

---

## Folder Structure Requirement  

This tool is designed to work with the following folder structure:

Root_Directory/  
│  
├── Project_A/  
│   ├── Sequence_001/  
│   │   ├── Shot_001/  
│   │   │   ├── Element_001/  
│   │   │   │   ├── Project_A_Sequence_001_Shot_001_Element_001_v0001.nk  
│   │   │   │   ├── Project_A_Sequence_001_Shot_001_Element_001_v0002.nk  
│   │   │   ├── Element_002/  
│   │   ├── Shot_002/  
│   ├── Sequence_002/  
│  
├── Project_B/  

⚠ The script expects this naming and directory structure to function correctly.

---

## Features  

### Project Navigation  
- Browse and select a root directory  
- Dynamically loads:
  - Projects  
  - Sequences  
  - Shots  
  - Elements  
  - Versions  

All dropdown menus update automatically based on selection.

---

### Load Scene  
- Opens the selected `.nk` file directly inside Nuke  
- Validates file existence before loading  
- Displays success or error messages  

---

### Automatic Versioned Save  

- Detects existing versions in the selected element folder  
- Automatically increments version number  
- Saves as:

Project_Sequence_Shot_Element_v####.nk  

No manual renaming required.

---

### Clean GUI Interface  

- Built using PySide2  
- Simple dropdown-based navigation  
- Designed for production-friendly workflow  

---

## Usage  

1. Launch the Shot Loader  
2. Click **Browse** and select your root directory  
3. Click **Load** to populate project structure  
4. Select:
   - Project  
   - Sequence  
   - Shot  
   - Element  
   - Version  
5. Click:
   - **Open Scene** to open a script  
   - **Save Scene** to auto-increment and save a new version  

---

## Installation  

1. Place the script inside your `.nuke` directory  
2. Add it to your `menu.py` if needed  
3. Restart Nuke  

The dialog runs using:

```python
nuke.executeInMainThread(show_dialog)
```

---

## Prerequisites  

- Nuke  
- Python (Nuke embedded)  
- PySide2  

---

## Contribution  

Contributions are welcome! Feel free to submit pull requests or raise issues for any suggestions or bugs.