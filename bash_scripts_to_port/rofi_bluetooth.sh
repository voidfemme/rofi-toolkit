#!/bin/bash

# ```python
# (method) def add_argument(
#     *name_or_flags: str,
#     action: str | type[Action] = ...,
#     nargs: int | str | None = None,
#     const: Any = ...,
#     default: Any = ...,
#     type: _ActionType = ...,
#     choices: Iterable[Any] | None = ...,
#     required: bool = ...,
#     help: str | None = ...,
#     metavar: str | tuple[str, ...] | None = ...,
#     dest: str | None = ...,
#     version: str = ...,
#     **kwargs: Any
# ) -> Action
# ```
# parser = argparse.ArgumentParser(description="")
# parser.add_argument('integers', metavar='int', nargs='+', type=int, help='an integer to be summed')
# parser.add_argument('--log', help='the file where the sum should be written')
#
# args = parser.parse_args()
# with (open(args.log, 'w') if args.log is not None
#   else contextlib.nullcontext(sys.stdout)) as log:
#       log.write('%s' % sum(args.integers))
#
# The module contains the following public classes:
# 
#     - ArgumentParser -- The main entry point for command-line parsing. As the
#         example above shows, the add_argument() method is used to populate
#         the parser with actions for optional and positional arguments. Then
#         the parse_args() method is invoked to convert the args at the
#         command-line into an object with attributes.
# 
#     - ArgumentError -- The exception raised by ArgumentParser objects when
#         there are errors with the parser's actions. Errors raised while
#         parsing the command-line are caught by ArgumentParser and emitted
#         as command-line messages.
# 
#     - FileType -- A factory for defining types of files to be created. As the
#         example above shows, instances of FileType are typically passed as
#         the type= argument of add_argument() calls. Deprecated since
#         Python 3.14.
# 
#     - Action -- The base class for parser actions. Typically actions are
#         selected by passing strings like 'store_true' or 'append_const' to
#         the action= argument of add_argument(). However, for greater
#         customization of ArgumentParser actions, subclasses of Action may
#         be defined and passed as the action= argument.
# 
#     - HelpFormatter, RawDescriptionHelpFormatter, RawTextHelpFormatter,
#         ArgumentDefaultsHelpFormatter -- Formatter classes which
#         may be passed as the formatter_class= argument to the
#         ArgumentParser constructor. HelpFormatter is the default,
#         RawDescriptionHelpFormatter and RawTextHelpFormatter tell the parser
#         not to change the formatting for help text, and
#         ArgumentDefaultsHelpFormatter adds information about argument defaults
#         to the help.
#
#

SCAN_TIME=5

SHOW_SAVED=true
SHOW_SCANNED=true

# Parse args
for arg in "$@"; do
    case "$arg" in
        --saved)
            SHOW_SCANNED=false
            ;;
        --scan)
            SHOW_SAVED=false
            ;;
    esac
done

# Scan and capture new devices
scan_devices() {
    timeout "$SCAN_TIME" bluetoothctl scan on 2>/dev/null | \
        grep "\[NEW\] Device" | \
        sed 's/\[NEW\] Device //'
}

# Get known devices
get_saved_devices() {
    bluetoothctl devices | cut -d ' ' -f 2-
}

# Add status labels
annotate_devices() {
    while IFS= read -r device; do # -z = "if the string is empty"
        [ -z "$device" ] && continue

        mac=$(echo "$device" | awk '{print $1}')

        info=$(bluetoothctl info "$mac" 2>/dev/null)

        if echo "$info" | grep -q "Connected: yes"; then
            echo "$device (connected)"
        elif echo "$info" | grep -q "Paired: yes"; then
            echo "$device (disconnected)"
        else
            echo "$device (new)"
        fi
    done
}

# Deduplicate by MAC
dedupe_devices() {
    awk '!seen[$1]++'
}

# Build device list
build_device_list() {
    scanned=""
    saved=""

    if $SHOW_SCANNED; then
        scanned=$(scan_devices | annotate_devices)
    fi

    if $SHOW_SAVED; then
        saved=$(get_saved_devices | annotate_devices)
    fi

    if $SHOW_SCANNED && $SHOW_SAVED; then
        printf "%s\n%s\n%s" \
            "$scanned" \
            "== Scan again ==" \
            "$saved" | dedupe_devices
    elif $SHOW_SCANNED; then
        printf "%s\n== Scan again ==" "$scanned"
    else
        printf "%s" "$saved"
    fi
}

connect_device() {
    mac="$1"

    if ! bluetoothctl info "$mac" | grep -q "Paired: yes"; then
        if ! bluetoothctl pair "$mac"; then
            notify-send "Bluetooth Error" "Pairing failed"
            exit 1
        fi
    fi

    if ! bluetoothctl connect "$mac"; then
        notify-send "Bluetooth Error" "Connection failed"
        exit 1
    fi
}

disconnect_device() {
    mac="$1"
    if ! bluetoothctl disconnect "$mac"; then
        notify-send "Bluetooth Error" "Disconnect failed"
        exit 1
    fi
}

# Main loop (supports "Scan again")
while true; do
    devices=$(build_device_list)

    choice=$(echo -e "$devices" | rofi -dmenu -i -p "Bluetooth Devices")

    [ -z "$choice" ] && exit 0

    if [ "$choice" = " == Scan again ==" ]; then
        continue
    fi

    mac=$(echo "$choice" | awk '{print $1}')

    if echo "$choice" | grep -q "(connected)$"; then
        disconnect_device "$mac"
    else
        connect_device "$mac"
    fi

    sleep 1

    human_readable_name=$(echo $choice | awk '{$1=""; sub(/^ /, ""); print}' | sed 's/ (connected)//;s/ (disconnected)//')
    echo "Next echo statement says: [[echo \"choice = \$choice\"]]"
    echo "choice = $choice"
    echo "Next echo statement says: [[echo \"human_readable_name = \$human_readable_name\"]]"
    echo "human_readable_name = $human_readable_name"


    if bluetoothctl info "$mac" | grep -q "Connected: yes"; then
        notify-send "$human_readable_name" "Bluetooth Connected"
    else
        notify-send "$human_readable_name" "Bluetooth Disconnected"
    fi

    exit 0
done
