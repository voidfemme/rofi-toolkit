#!/bin/bash

PYTHON_SCRIPT="/home/rsp/scripts/rofi_calculator.py"

# Enable debug output
set -x

copy_to_clipboard() {
    echo -n "$1" | xclip -selection clipboard
    notify-send "Calculator" "Copied to clipboard: $1"
}

while true; do
    # Get history and current expression
    history=$(python3 "$PYTHON_SCRIPT" --history)
    expression=$(echo -e "$history\n:Calculate" | rofi -dmenu -p "Calculator:" -format 's')

    # Check if user wants to calculate or selected history item
    if [[ "$expression" == ":Calculate" ]]; then
        # User wants to calculate, open another rofi for input
        expression=$(rofi -dmenu -p "Calculate:")
    elif [[ "$expression" == *"="* ]]; then
        # User selected a history item, extract the expression
        expression=$(echo "$expression" | cut -d'=' -f1 | xargs)
    elif [[ -z "$expression" ]]; then
        # User pressed Esc, exit
        exit 0
    fi

    # Debug: Print the expression
    echo "Debug: Expression to evaluate: $expression"

    # Evaluate the expression and store the result
    result=$(python3 "$PYTHON_SCRIPT" "$expression")

    # Debug: Print the raw result
    echo "Debug: Raw result from Python script: $result"

    # Check if result is empty
    if [ -z "$result" ]; then
        notify-send "Calculator Error" "No output from Python script"
        continue
    fi

    # Display results in Rofi and get user selection
    selection=$(echo -e "$result" | rofi -dmenu -p "Result (Enter to copy):" -format 's')

    # Debug: Print the selection
    echo "Debug: User selection: $selection"

    # Check if selection is empty (user pressed Esc)
    if [ -z "$selection" ]; then
        continue
    fi

    # Copy the selected value to clipboard
    copy_to_clipboard "$selection"

    # Ask if the user wants to continue
    continue_calc=$(echo -e "Yes\nNo" | rofi -dmenu -p "Continue calculating?")
    if [[ "$continue_calc" != "Yes" ]]; then
        break
    fi
done
