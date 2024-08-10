#!/bin/bash

# Usage message
usage() {
    echo "Usage: $0 -path /path/to/directory"
    exit 1
}

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -path) TARGET_DIR="$2"; shift ;;
        *) usage ;;
    esac
    shift
done

# Ensure the TARGET_DIR variable is set
if [ -z "$TARGET_DIR" ]; then
    echo "Error: -path is required."
    usage
fi

# Ensure the provided path exists and is a directory
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: $TARGET_DIR is not a valid directory."
    exit 1
fi

# Recursively delete empty directories in a depth-first manner
find "$TARGET_DIR" -depth -type d -empty -delete

echo "All empty directories deleted successfully."
