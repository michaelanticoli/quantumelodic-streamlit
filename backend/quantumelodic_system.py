from pathlib import Path
import shutil

# Define the base path for the new integrated project structure
base_dir = Path("/mnt/data/quantumelodic_system")
subdirs = ["core", "utils", "gui", "data", "output"]

# Create folder structure
for subdir in subdirs:
    (base_dir / subdir).mkdir(parents=True, exist_ok=True)

# Define where each file goes based on filename pattern
file_map = {
    "core": [
        "quantumelodic_master_script.py",
        "quantum_full_system_code.py",
        "core_module.py",
        "features_module.py",
        "enhanced_system_module.py"
    ],
    "utils": [
        "csv_quantum.py",
        "Quantumelodic Templates.py"
    ],
    "gui": [
        "quantumelodic-adaptive-personalized.py",
        "quantumelodic-advanced-features.py",
        "quantumelodic-advanced-collaborative.py"
    ],
    "output": [
        "quantumelodic-enhanced-data-models.py",
        "quantumelodies-complete.py"
    ]
}

# Move files to their respective folders
for folder, files in file_map.items():
    for fname in files:
        src = Path(f"/mnt/data/{fname}")
        dest = base_dir / folder / fname
        if src.exists():
            shutil.copy(src, dest)

# Create a README.md file summarizing the project
readme_content = """
# Quantumelodic MetaSystem Codebase

## Overview
This package contains the modular system for generating music from astrological charts using planetary mappings, aspects, and rhythmic translation logic.

## Structure

- `core/`: Central logic scripts for mapping astrology to sound
- `utils/`: Data loading, CSV processing, templates
- `gui/`: Adaptive, interactive, and collaborative extensions
- `output/`: Full rendering and data output pipelines
- `data/`: (Reserved) For charts, CSVs, and datasets
- `output/`: (Reserved) For generated MIDI/WAV files

## Usage
To run a full session:
```bash
python core/quantumelodic_master_script.py
