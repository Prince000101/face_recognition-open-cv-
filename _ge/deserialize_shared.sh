#!/usr/bin/env bash
set -euo pipefail

query() {
    local input="${1:-}"
    if [[ -z "$input" ]]; then
        echo "Usage: query <input>"
        return 1
    fi

    echo "Processing query: $input"
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
    query "$@"
}

main "$@"
