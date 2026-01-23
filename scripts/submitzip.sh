#!/bin/bash -eu
# ---------------------------------------------------------
# submitzip.sh
# Usage: ./submitzip.sh 02-system-peri-n-sensor-int
#
# Creates a zip archive with the required submission files.
# - Includes all PDFs from report/build/ at root
# - Includes code/ while respecting .gitignore rules
# ---------------------------------------------------------

if [ $# -ne 1 ]; then
    echo "Usage: $0 <assignment-directory>"
    exit 1
fi

ASSIGN_DIR="$1"

if [ ! -d "$ASSIGN_DIR" ]; then
    echo "Error: Directory '$ASSIGN_DIR' not found."
    exit 1
fi

REPORT_DIR="$ASSIGN_DIR/report"
CODE_DIR="$ASSIGN_DIR/code"
PDF_DIR="$REPORT_DIR/build"

# Find a SINGLE .tex file in the report directory and derive basename from it
shopt -s nullglob
TEX_FILES=("$REPORT_DIR"/*.tex)
shopt -u nullglob

if [ ${#TEX_FILES[@]} -ne 1 ]; then
    echo "Error: Expected exactly one .tex file in '$REPORT_DIR', found ${#TEX_FILES[@]}" >&2
    if [ ${#TEX_FILES[@]} -gt 0 ]; then
        echo "Candidates:" >&2
        for f in "${TEX_FILES[@]}"; do echo "  - $(basename "$f")" >&2; done
    fi
    exit 1
fi

BASENAME=$(basename "${TEX_FILES[0]}" .tex)
ZIPNAME="${BASENAME}.zip"

echo "Creating archive: $ZIPNAME"

# Start fresh
rm -f "$ZIPNAME"

# 1. Add PDFs (all of them) to root of zip
zip -j "$ZIPNAME" "$PDF_DIR"/*.pdf

# 2. Add code directory, respecting .gitignore
if [ -d "$CODE_DIR" ]; then
    echo "Adding code/ (respecting .gitignore)..."
    (
        cd "$CODE_DIR" || exit 1
        # git ls-files --cached    => files staged/tracked
        # git ls-files --others --exclude-standard => untracked but not ignored
        FILES=$(git ls-files --cached --others --exclude-standard)
        if [ -n "$FILES" ]; then
            # Add them under code/ inside the zip
            zip -r "$OLDPWD/$ZIPNAME" $FILES -x "*.o" "*.elf"
        else
            echo "No files to include from code/ (maybe everything is ignored?)"
        fi
    )
else
    echo "Warning: Code directory '$CODE_DIR' not found. Skipping."
fi

echo "Done. Contents of $ZIPNAME:"
unzip -l "$ZIPNAME"

echo -e "\nYou can drop any extra files using command:"
echo "   zip -d $ZIPNAME path/to/file.txt"