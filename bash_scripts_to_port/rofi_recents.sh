#!/bin/bash

# Ensure noclobber is set for script safety
set -o noclobber

# Check if required tools are installed
if ! command -v rofi &> /dev/null || ! command -v find &> /dev/null; then
    echo "Error: rofi and find are required."
    exit 1
fi

# User-configurable variables
BASE_DIR="$HOME"            # Base directory for searching files
RECENT_COUNT=10             # Number of recent files to display
FILE_TYPE_FILTER="*"        # File type filter, e.g., "*.txt" for text files

# Find, list, and open recent files with rofi
selected_file=$(find "$BASE_DIR" -type f -name "$FILE_TYPE_FILTER" -printf '%T@ %p\n' | sort -nr | head -n "$RECENT_COUNT" | cut -d' ' -f2- | rofi -dmenu -p "Open Recent File:")

# Open the selected file
if [ -n "$selected_file" ]; then
  xdg-open "$selected_file"
fi

