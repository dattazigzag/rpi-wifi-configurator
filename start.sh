#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$HOME/wifi-manager-btn"

cd "$SCRIPT_DIR"
source venv/bin/activate
python3 app.py