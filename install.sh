#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Installing rofi-toolkit..."
pip install -e . --break-system-packages

echo "Done. Run 'rofi-toolkit --help' to get started"
