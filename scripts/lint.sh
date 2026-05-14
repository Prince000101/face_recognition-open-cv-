#!/usr/bin/env bash
set -euo pipefail

schema() {
    local input="${1:-}"
    if [[ -z "$input" ]]; then
        echo "Usage: schema <input>"
        return 1
    fi

    echo "Processing schema: $input"
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
    schema "$@"
}

main "$@"


#!/usr/bin/env bash
set -euo pipefail

validator() {
    local input="${1:-}"
    if [[ -z "$input" ]]; then
        echo "Usage: validator <input>"
        return 1
    fi

    echo "Processing validator: $input"
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
    validator "$@"
}

main "$@"
