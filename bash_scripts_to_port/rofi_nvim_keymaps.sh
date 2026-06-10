#!/bin/bash
# rofi-keymaps.sh - Display Neovim keymaps in rofi

# Configuration
CACHE_FILE="$HOME/.cache/nvim-keymaps.json"
ROFI_CACHE_FILE="$HOME/.cache/nvim-keymaps-rofi.txt"
SOCKET_PATH="/tmp/nvim-server"

# Function to escape markup for rofi
escape_markup() {
    echo "$1" | sed 's/</\&lt;/g; s/>/\&gt;/g; s/&/\&amp;/g'
}

# Function to export keymaps from Neovim
export_keymaps() {
    # Try to use existing Neovim instance
    if nvim --server "$SOCKET_PATH" --remote-send '<Esc>:ExportKeymaps rofi<CR>' 2>/dev/null; then
        # Wait a moment for export to complete
        sleep 0.5
    else
        # Start headless Neovim to export keymaps
        nvim --headless -c "lua require('custom.keymaps').save_keymaps_to_file('$ROFI_CACHE_FILE', 'rofi')" -c "qa" 2>/dev/null
    fi
}

# Function to check if cache is fresh (less than 1 hour old)
is_cache_fresh() {
    if [[ -f "$ROFI_CACHE_FILE" ]]; then
        local cache_age=$(($(date +%s) - $(stat -c %Y "$ROFI_CACHE_FILE" 2>/dev/null || echo 0)))
        [[ $cache_age -lt 3600 ]] # 1 hour in seconds
    else
        return 1
    fi
}

# Function to get keymaps for rofi
get_keymaps() {
    if ! is_cache_fresh; then
        export_keymaps
    fi
    
    if [[ -f "$ROFI_CACHE_FILE" ]]; then
        # Remove duplicates and escape markup
        cat "$ROFI_CACHE_FILE" | sort -u | while IFS= read -r line; do
            if [[ -n "$line" ]]; then
                # Split the line by pipes and escape each part
                key_part=$(echo "$line" | cut -d'|' -f1)
                desc_part=$(echo "$line" | cut -d'|' -f2)
                category_part=$(echo "$line" | cut -d'|' -f3)
                
                # Escape markup in each part
                key_escaped=$(escape_markup "$key_part")
                desc_escaped=$(escape_markup "$desc_part")
                category_escaped=$(escape_markup "$category_part")
                
                echo "$key_escaped|$desc_escaped|$category_escaped"
            fi
        done
    else
        echo "Error: Could not load keymaps"
        exit 1
    fi
}

# Function to parse selected keymap and execute action
execute_keymap() {
    local selection="$1"
    
    # Parse the selection format: "🅝 <leader>sf | [S]earch [F]iles | Telescope"
    # Note: We need to unescape the markup
    local key=$(echo "$selection" | cut -d'|' -f1 | sed 's/^[^[:space:]]*[[:space:]]*//' | sed 's/[[:space:]]*$//' | sed 's/\&lt;/</g; s/\&gt;/>/g; s/\&amp;/\&/g')
    local description=$(echo "$selection" | cut -d'|' -f2 | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//' | sed 's/\&lt;/</g; s/\&gt;/>/g; s/\&amp;/\&/g')
    local category=$(echo "$selection" | cut -d'|' -f3 | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//' | sed 's/\&lt;/</g; s/\&gt;/>/g; s/\&amp;/\&/g')
    
    # Show what we're executing
    notify-send "Neovim Keymap" "Executing: $key\n$description" -t 2000
    
    # Try to send to existing Neovim instance
    if nvim --server "$SOCKET_PATH" --remote-send "<Esc>$key" 2>/dev/null; then
        echo "Sent to existing Neovim instance: $key"
    else
        # If no server, copy to clipboard and notify
        echo -n "$key" | xclip -selection clipboard 2>/dev/null || echo -n "$key" | pbcopy 2>/dev/null
        notify-send "Neovim Keymap" "No Neovim server found.\nKeymap copied to clipboard: $key" -t 3000
    fi
}

# Function to show help
show_help() {
    cat << EOF
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
EOF
}

# Parse command line arguments
FILTER_CATEGORY=""
REFRESH_CACHE=false
SHOW_CATEGORIES=false
LIST_ONLY=false
JSON_OUTPUT=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -r|--refresh)
            REFRESH_CACHE=true
            shift
            ;;
        -c|--categories)
            SHOW_CATEGORIES=true
            shift
            ;;
        -f|--filter)
            FILTER_CATEGORY="$2"
            shift 2
            ;;
        --json)
            JSON_OUTPUT=true
            shift
            ;;
        --list)
            LIST_ONLY=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

# Force refresh if requested
if [[ "$REFRESH_CACHE" == "true" ]]; then
    rm -f "$ROFI_CACHE_FILE" "$CACHE_FILE"
fi

# Handle JSON output
if [[ "$JSON_OUTPUT" == "true" ]]; then
    if ! is_cache_fresh || [[ ! -f "$CACHE_FILE" ]]; then
        nvim --headless -c "lua require('custom.keymaps').save_keymaps_to_file('$CACHE_FILE', 'json')" -c "qa" 2>/dev/null
    fi
    if [[ -f "$CACHE_FILE" ]]; then
        cat "$CACHE_FILE"
    else
        echo "Error: Could not export JSON keymaps"
        exit 1
    fi
    exit 0
fi

# Get keymaps
KEYMAPS=$(get_keymaps)

# Handle categories view
if [[ "$SHOW_CATEGORIES" == "true" ]]; then
    CATEGORIES=$(echo "$KEYMAPS" | cut -d'|' -f3 | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//' | sort -u)
    if [[ "$LIST_ONLY" == "true" ]]; then
        echo "$CATEGORIES"
    else
        SELECTED_CATEGORY=$(echo "$CATEGORIES" | rofi -dmenu -i -p "Select Category" -theme-str 'window {width: 30%;}')
        if [[ -n "$SELECTED_CATEGORY" ]]; then
            # Re-run script with category filter
            exec "$0" --filter "$SELECTED_CATEGORY"
        fi
    fi
    exit 0
fi

# Apply category filter if specified
if [[ -n "$FILTER_CATEGORY" ]]; then
    KEYMAPS=$(echo "$KEYMAPS" | grep -i "| $FILTER_CATEGORY$")
    if [[ -z "$KEYMAPS" ]]; then
        echo "No keymaps found for category: $FILTER_CATEGORY"
        exit 1
    fi
fi

# Handle list-only mode
if [[ "$LIST_ONLY" == "true" ]]; then
    echo "$KEYMAPS" | sed 's/\&lt;/</g; s/\&gt;/>/g; s/\&amp;/\&/g'
    exit 0
fi

# Show in rofi and handle selection
SELECTED=$(echo "$KEYMAPS" | rofi -dmenu -i -p "Neovim Keymaps" \
    -theme-str 'window {width: 80%;}' \
    -theme-str 'listview {lines: 15;}' \
    -markup-rows \
    -kb-custom-1 "Alt+c" \
    -kb-custom-2 "Alt+r" \
    -kb-custom-3 "Alt+h")

# Handle rofi exit codes and custom keys
case $? in
    0)  # Normal selection
        if [[ -n "$SELECTED" ]]; then
            execute_keymap "$SELECTED"
        fi
        ;;
    10) # Alt+c - Show categories
        exec "$0" --categories
        ;;
    11) # Alt+r - Refresh cache
        exec "$0" --refresh
        ;;
    12) # Alt+h - Show help
        show_help | rofi -dmenu -p "Help" -theme-str 'window {width: 60%; height: 70%;}' -theme-str 'textbox {horizontal-align: 0;}'
        ;;
    1)  # Escape pressed
        exit 0
        ;;
    *)  # Other exit codes
        exit $?
        ;;
esac
