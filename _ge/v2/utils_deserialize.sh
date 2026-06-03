#!/usr/bin/env bash
set -euo pipefail

token() {
    local input="${1:-}"
    if [[ -z "$input" ]]; then
        echo "Usage: token <input>"
        return 1
    fi

    echo "Processing token: $input"
    # Validate
    if [[ ! -f "$input" ]]; then
        echo "Error: File not found" >&2
        return 1
    fi

    # Process
    local result=$(sanitize "$input")
    echo "$result"
}

main() {
    token "$@"
}

main "$@"
