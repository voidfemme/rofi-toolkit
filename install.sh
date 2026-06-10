#!/bin/bash
set -e

SCRIPT_DIR="$(dirname "$(realpath "$0")")"
cd "$SCRIPT_DIR"

echo "Installing rofi-toolkit..."
pip install -e . --break-system-packages

echo "Done. Run 'rofi-toolkit --help' to get started"
