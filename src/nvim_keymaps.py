# src/nvim_keymaps.py
from config import NK_CACHE_FILE, NK_ROFI_CACHE_FILE, NK_SOCKET_PATH
from rofi import Rofi
from src.utils.notify_send import notify
import os
import re
import subprocess
import sys
import time


def escape_markup(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def unescape_markup(text: str) -> str:
    return text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")


# Function to export keymaps from Neovim
def export_keymaps() -> str:
    # Try to use existing Neovim instance
    result = subprocess.run(
        [
            "nvim",
            "--server",
            NK_SOCKET_PATH,
            "--remote-send",
            "<Esc>:ExportKeymaps rofi<CR>",
        ],
        capture_output=True,
    )
    if result.returncode == 0:
        # Wait a moment for export to complete
        time.sleep(0.5)
    else:
        # Start headless Neovim to export keymaps
        result = subprocess.run(
            [
                "nvim",
                "--headless",
                "-c",
                f"lua require('custom.keymaps').save_keymaps_to_file('{NK_ROFI_CACHE_FILE}', 'rofi')",
                "-c",
                "qa",
            ],
            capture_output=True,
        )
    return result.stdout.decode("utf-8")


# Function to check if cache is fresh (less than 1 hour old)
def is_cache_fresh() -> bool:
    if not os.path.exists(NK_ROFI_CACHE_FILE):
        return False
    cache_age = int(time.time()) - int(os.path.getmtime(NK_ROFI_CACHE_FILE))
    return cache_age < 3600


# Function to get keymaps for rofi
def get_keymaps() -> list[str]:
    if not is_cache_fresh():
        export_keymaps()

    if os.path.exists(NK_ROFI_CACHE_FILE):
        # Remove duplicates and escape markup
        with open(NK_ROFI_CACHE_FILE, "r") as f:
            lines = sorted(f.readlines())

        if not lines:
            sys.exit(0)

        result = []
        for line in lines:
            # Split the line by pipes and escape each part
            key_part, desc_part, category_part = line.split("|")

            # Escape markup in each part
            key_escaped = escape_markup(key_part)
            desc_escaped = escape_markup(desc_part)
            category_escaped = escape_markup(category_part)
            result.append(f"{key_escaped}|{desc_escaped}|{category_escaped}")
        return result
    raise FileNotFoundError


# Function to parse selected keymap and execute action
def execute_keymap(selection: str) -> None:
    # Parse the selection format: "🅝 <leader>sf | [S]earch [F]iles | Telescope"
    # Note: We need to unescape the markup
    parts = selection.split("|")
    key = unescape_markup(parts[0].strip())
    description = unescape_markup(parts[1].strip())
    category = unescape_markup(parts[2].strip())

    # Show what we're executing
    notify("Neovim keymap", f"Executing: {key}\n{description}", expire_time=2000)

    # try to send to existing Neovim instance
    result = subprocess.run(
        ["nvim", "--server", NK_SOCKET_PATH, "--remote-send", f"<Esc>{key}"],
        capture_output=True,
    )

    if result.returncode == 0:
        notify(f"Sent to existing Neovim instance {key}")
    else:
        # If no server, copy to clipboard and notify
        subprocess.run(["wl-copy"], input=key, capture_output=False)
        notify(
            "Neovim Keymap",
            f"No Neovim server found.\nKeymap copied to clipboard: {key}",
            expire_time=3000,
        )


def show_help():
    return """
rofi-keymaps.sh - Neovim Keymap Browser

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

This allows the script to send keymaps directly to your Neovim instance.
    """


def nvim_keymaps_menu(
    rofi: Rofi,
    refresh: bool = False,
    categories: bool = False,
    filter_category: str | None = None,
    json_output: bool = False,
    list_only: bool = False,
):
    if refresh:
        os.remove(NK_CACHE_FILE) if os.path.exists(NK_CACHE_FILE) else None
        os.remove(NK_ROFI_CACHE_FILE) if os.path.exists(NK_ROFI_CACHE_FILE) else None

    if json_output:
        if not is_cache_fresh() or not os.path.exists(NK_CACHE_FILE):
            subprocess.run(
                [
                    "nvim",
                    "--headless",
                    "-c",
                    f"lua require('custom.keymaps').save_keymaps_to_file('{NK_CACHE_FILE}', 'json')",
                    "-c",
                    "qa",
                ]
            )
        if os.path.exists(NK_CACHE_FILE):
            with open(NK_CACHE_FILE, "r") as f:
                print(f.readlines())
        else:
            notify("Error: Could not export JSON keymaps")
            sys.exit(1)
        sys.exit(0)

    try:
        keymaps = get_keymaps()

        if categories:
            available_categories = sorted(
                set(line.split("|")[2].strip() for line in keymaps)
            )

            if list_only:
                for category in available_categories:
                    print(category)
            else:
                index, key = rofi.select(
                    "Select Category", available_categories, width=30
                )
                if key == 0:
                    selected_category = available_categories[index]
                    if selected_category:
                        nvim_keymaps_menu(rofi, filter_category=selected_category)
                else:
                    sys.exit(0)
            sys.exit(0)

        # apply category filter if specified
        if filter_category:
            keymaps = [
                line
                for line in keymaps
                if f"| {filter_category.lower()}" in line.lower()
            ]
            if not keymaps:
                notify(f"No keymaps found for category: {filter_category}")
                sys.exit(1)

        # Handle list-only mode
        if list_only:
            for keymap in keymaps:
                print(unescape_markup(keymap))
            sys.exit(0)

        # Show in rofi and handle selection
        index, key = rofi.select(
            "Neovim Keymaps",
            keymaps,
            width=80,
            lines=15,
            rofi_args=["-markup-rows"],
            key1=("Alt+c", None),
            key2=("Alt+r", None),
            key3=("Alt+h", None),
        )
        selected = keymaps[index]

        # Handle rofi exit codes and custom keys
        match key:
            case 0:
                # Normal selection
                if selected:
                    execute_keymap(selected)
            case 1:
                # Alt+c - show categories
                nvim_keymaps_menu(rofi, categories=True)
            case 2:
                # Alt+r - Refresh cache
                nvim_keymaps_menu(rofi, refresh=True)
            case 3:
                # Alt+h - Show help
                notify("Neovim Keymap Browser", show_help())
            case -1:
                # Escape pressed
                sys.exit(0)
            case _:
                sys.exit(key)
    except FileNotFoundError as e:
        notify(f"Error: Could not load keymaps\n{e}")
        sys.exit(1)
