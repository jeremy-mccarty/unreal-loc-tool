#!/bin/bash
source .venv/bin/activate
pyinstaller --noconfirm --onefile --windowed src/main.py
