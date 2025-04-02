#!/bin/bash

# Check if directory argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Directory containing files to rename
DIR="$1"

# Get files sorted by size (smallest to largest)
files=($(find "$DIR" -maxdepth 1 -type f -exec stat -f "%z %N" {} \; | sort -n | awk '{print $2}'))

counter=1
for file in "${files[@]}"; do
    mv "$file" "$DIR/${counter}.mid"
    ((counter++))
done