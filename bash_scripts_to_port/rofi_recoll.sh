#!/bin/bash
# rofi_recoll.sh — file content search via recollq using rofi-blocks
#
# Usage:
#   rofi -modi blocks -show blocks -blocks-wrap ~/Scripts/rofi_recoll.sh \
#        -show-icons -icon-theme "Papirus"
#
# Controls:
#   Enter      — open selected file
#   Alt+1      — show full abstract for selected entry in message bar

emit() { printf '%s\n' "$1"; }

build_lines() {
    local query="$1"
    recollq -n 20 -F "url title mtype abstract" "$query" 2>/dev/null \
    | grep -v '^:' \
    | while read -r f_url f_title f_mtype f_abstract _rest; do
        local url title mtype abstract path filename icon short_abstract display
        url=$(printf '%s'      "$f_url"      | base64 -d 2>/dev/null | tr -d '\0')
        title=$(printf '%s'    "$f_title"    | base64 -d 2>/dev/null | tr -d '\0')
        mtype=$(printf '%s'    "$f_mtype"    | base64 -d 2>/dev/null | tr -d '\0')
        abstract=$(printf '%s' "$f_abstract" | base64 -d 2>/dev/null | tr -d '\0' | tr '\n' ' ')
        path="${url#file://}"
        filename=$(basename "$path")
        icon="${mtype/\//-}"

        case "$mtype" in
            text/plain|text/markdown|text/org|application/pdf|\
            application/msword|application/vnd.oasis*|application/epub*)
                short_abstract=$(printf '%s' "$abstract" | cut -c1-60)
                display="$filename   ${short_abstract}…   $path"
                ;;
            *)
                display="$filename   $path"
                abstract=""
                ;;
        esac

        jq -n \
            --arg text "$display" \
            --arg icon "$icon" \
            --arg data "${path}|||${abstract}" \
            '{text: $text, icon: $icon, data: $data}'
    done | jq -s '.'
}

# Initial output — "input action": "send" makes rofi fire INPUT_CHANGE events
# instead of filtering locally, so our script controls the list on every keystroke
emit '{"input action":"send","prompt":"🔍 Search","lines":[],"message":"Type to search files..."}'

while IFS= read -r event; do
    name=$(printf '%s'  "$event" | jq -r '.name  // empty')
    value=$(printf '%s' "$event" | jq -r '.value // empty')
    data=$(printf '%s'  "$event" | jq -r '.data  // empty')

    case "$name" in
        "input change")
            if [[ -z "$value" ]]; then
                emit '{"lines":[],"message":"Type to search files..."}'
            else
                lines=$(build_lines "$value")
                emit "$(printf '%s' "$lines" | jq -c '{"lines":.,"message":""}')"
            fi
            ;;
        "active entry")
            # Fires just before Alt+1 custom key — show full abstract in message bar
            abstract="${data#*|||}"
            if [[ -n "$abstract" ]]; then
                emit "$(printf '%s' "$abstract" | jq -Rc '{"message":.}')"
            fi
            ;;
        "select entry")
            path="${data%%|||*}"
            [[ -f "$path" ]] && coproc (xdg-open "$path" >/dev/null 2>&1)
            emit '{"lines":[]}'
            ;;
    esac
done
