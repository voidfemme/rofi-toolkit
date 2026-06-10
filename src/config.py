# config.py
import os

BLUETOOTH_SCAN_TIME = 5
BLUETOOTH_SHOW_SAVED = True
BLUETOOTH_SHOW_SCANNED = True

CALCULATOR_HISTORY = os.path.expanduser("~/Scripts/.rofi_calculator_history")

NK_CACHE_FILE = os.path.expanduser("~/.cache/nvim-keymaps.json")
NK_ROFI_CACHE_FILE = os.path.expanduser("~/.cache/nvim-keymaps.json")
NK_SOCKET_PATH = os.path.abspath("/tmp/nvim-server")

NK_HELP = """rofi-keymaps.sh - Neovim Keymap Browser

Usage: 
    rofi-keymaps.sh [OPTIONS]

Options:
    -h, --help          Show this help message
    -r, --refresh       Force refresh the keymap cache
    -c, --categories    Show only category list
    -f, --filter CAT    Filter by category
    --json              Export as JSON instead of rofi format
    --list              List all keymaps without rofi

Examples:
    rofi-keymaps.sh                    # Show all keymaps in rofi
    rofi-keymaps.sh -f Telescope       # Show only Telescope keymaps
    rofi-keymaps.sh --list             # List all keymaps in terminal
    rofi-keymaps.sh --refresh          # Force refresh cache

Note: For best experience, start Neovim with:
    nvim --listen $SOCKET_PATH

This allows the script to send keymaps directly to your Neovim instance."""
