#!/bin/bash -eu

# Check if arguments were provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <module-name> <course-code>"
    echo "Example: $0 01-introduction TEKS4440"
    echo "This will rename template.tex in the module's report directory."
    exit 1
fi

MODULE_NAME="$1"
COURSE_CODE="$2"
OLD_NAME="template"

# Extract number from module name (e.g., "01-intro" -> "01")
# If no number is found at the start, use "x"
NUMBER=$(echo "$MODULE_NAME" | grep -o '^[0-9]\+' || echo "x")

# Construct the new filename
NEW_NAME="${COURSE_CODE}-assignment-${NUMBER}-sourander"

# Change to the module's report directory
cd "${MODULE_NAME}/report"

# Check if the original file exists
if [ ! -f "${OLD_NAME}.tex" ]; then
    echo "Error: ${OLD_NAME}.tex does not exist!"
    exit 1
fi

# Rename the tex file
echo "Renaming ${OLD_NAME}.tex to ${NEW_NAME}.tex"
mv "${OLD_NAME}.tex" "${NEW_NAME}.tex"

echo "Renaming process completed successfully."
