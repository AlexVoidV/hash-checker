# Hash Checker
Ру-версия текста доступна здесь – [README.ru.md](README.ru.md).

A simple CLI program that calculates and optionally compares hash sums.

## Features
- Calculates the file's hash
- 4 hashes available: SHA256, MD5, SHA1, SHA512
- Compares it to the entered hash (optional, use `/c`)

## Requirements
- Python 3

## Usage
- Running the script: `python hash_checker.py`
- List of commands:
    - `/h` – help
    - `/t` – change the hash type
    - `/c` – enable/disable comparison
    - `/q` – quit

## Build to `.exe`
- Installing dependencies (use venv): 
    1. Using pip: `pip install pyinstaller` 
    2. Or using uv: `uv sync --no-dev`
- Building the application: `pyinstaller --onefile hash_checker.py`
- The application will be in: dist/hash_checker.exe

## Localization
Only EN and RU localization, no other languages ​​will be available.

## License
**MIT**
