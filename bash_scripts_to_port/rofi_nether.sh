#!/bin/bash

# Function to process coordinates
process_coordinates() {
    # Remove any spaces and replace "/" or "," with space
    local input=$(echo "$1" | tr -d ' ' | tr '/,' ' ')
    
    # Read the two numbers
    read x y <<< "$input"
    
    # Check if both numbers are valid
    if [[ $x =~ ^-?[0-9]+$ ]] && [[ $y =~ ^-?[0-9]+$ ]]; then
        # Calculate nether coordinates
        nether_x=$(( x / 8 ))
        nether_y=$(( y / 8 ))
        echo "$nether_x, $nether_y"
    else
        echo "Invalid input. Please enter two valid numbers."
    fi
}

# Check if xclip is installed
if ! command -v xclip &> /dev/null; then
    echo "xclip is not installed. Please install it to use clipboard functionality."
    exit 1
fi

# Main script
input=$(rofi -dmenu -p "Enter coordinates (x,y):")

if [ -n "$input" ]; then
    result=$(process_coordinates "$input")
    
    if [[ $result != Invalid* ]]; then
        # Copy result to clipboard
        echo -n "$result" | xclip -selection clipboard
        
        # Display result and notify user it's copied to clipboard
        echo -en "$result\n(Copied to clipboard)" | rofi -dmenu -p "Result"
    else
        # Display error message
        echo -en "$result" | rofi -dmenu -p "Error"
    fi
fi
