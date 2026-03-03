[![Python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![Latest Release](https://img.shields.io/github/v/release/jeremy-mccarty/unreal-loc-tool?logo=github&label=Release&color=blue)](https://github.com/jeremy-mccarty/unreal-loc-tool/releases/latest)
[![CI/CD](https://github.com/jeremy-mccarty/unreal-loc-tool/actions/workflows/build.yml/badge.svg)](https://github.com/jeremy-mccarty/unreal-loc-tool/actions/workflows/build.yml)

## Downloads

[![Download Linux](https://img.shields.io/badge/Download-Linux-blue?logo=linux)](https://github.com/jeremy-mccarty/unreal-loc-tool/releases/latest)
[![Download Windows](https://img.shields.io/badge/Download-Windows-brightgreen?logo=windows)](https://github.com/jeremy-mccarty/unreal-loc-tool/releases/latest)
[![Download macOS](https://img.shields.io/badge/Download-macOS-lightgrey?logo=apple)](https://github.com/jeremy-mccarty/unreal-loc-tool/releases/latest)

Convert CSV localization files to Unreal-compatible `.po` files and back, with batch folder support and metadata preservation.

# Unreal Localization Tool

A Python application to convert CSV files to `.po` files for Unreal Engine localization, and convert `.po` files back to CSV. Built with `Tkinter`.

## Features

* Convert CSV → `.po` (Unreal format) and `.po` → CSV.
* Batch conversion of folders recursively.
* Preserves namespace, key, source string, translation, and source location.
* Detects language from file name automatically.
* Skips `.po` header automatically and validates duplicate keys.
* Dark/Light theme support via `sv_ttk`.
* Cross-platform: Windows, Linux, and macOS.
* Generates standalone executables via PyInstaller.

## Using the Executable

- Download the latest release for your OS from the [Releases page](https://github.com/jeremy-mccarty/unreal-loc-tool/releases).  
- Run the executable; no Python installation required.

## Usage

1. **Convert a single file:**  
   - Click **Select CSV File** or **Select PO File**.  
   - Choose the target output folder or file.  
   - Click **Convert**.  
2. **Batch conversion:**  
   - Select a folder containing CSV or PO files.  
   - Subfolders will be processed recursively.  
   - Output folder structure is preserved.  
3. Check the **Output Log** for messages or errors.

## Installation

1. Clone the repository:

```bash
git clone git@github.com:jeremy-mccarty/unreal-loc-tool.git
cd unreal-loc-tool
```

2. Create a Python virtual environment:

``` bash
python -m venv venv
```

3. Activate the virtual environment:

Linux/macOS:
``` bash
source venv/bin/activate
```

Windows (PowerShell):
``` bash
.\venv\Scripts\Activate.ps1
```

4. Install dependencies:
``` bash
pip install -r requirements.txt
```

## Running the App

With the virtual environment active, run:

``` bash
python app/main.py
```

## Building Executables

You can create a standalone executable using PyInstaller:

``` bash
pyinstaller --noconfirm --onefile --name UnrealLocTool app/main.py
```

The executable will be located in the "dist" folder.

## GitHub Actions Auto-Build

## GitHub Actions Auto-Build

- Whenever a tag like `v1.0.0` is pushed, GitHub Actions will:
  1. Build standalone executables for Windows, macOS, and Linux.  
  2. Upload them as artifacts.  
  3. Create a GitHub release with the executables attached.  

- The badge above reflects the **latest workflow status**.

## Release Guide

Push a version tag:

``` bash
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions will automatically:
* Build executables for all supported OSes.
* Upload artifacts to a GitHub release.
* Generate release notes automatically.

## License

MIT License — see the LICENSE file for details.
