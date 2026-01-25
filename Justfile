# Justfile for managing course modules (tex templates)
COURSE_CODE := "TIES5350"
OUTPUT_DIR := "build"
AUX_DIR := "aux"

default:
    @just --list

# Start a new module from the template
# Usage: just new <module-name>
# Example: just new 01-introduction
new module_name:
    @test ! -d "{{module_name}}" || (echo "Error: Directory '{{module_name}}' already exists." && exit 1)
    @echo "Creating new module: {{module_name}}"
    cp -r 00-report-template "{{module_name}}"
    just rename {{module_name}}
    @echo "Module {{module_name}} initialized."

# Rename the template files in a module to follow course naming convention
rename module_name:
    ./scripts/rename.sh "{{module_name}}" "{{COURSE_CODE}}"

# Build the PDF for a module
# Usage: just build <module-name>
# Example: just build 01-introduction
build module_name:
    #!/usr/bin/env bash
    set -euo pipefail
    NUMBER=$(echo "{{module_name}}" | grep -o '^[0-9]\+' || echo "x")
    MAIN_TEX="{{COURSE_CODE}}-assignment-${NUMBER}-sourander.tex"
    cd "{{module_name}}/report"
    latexmk -xelatex -shell-escape -bibtex -synctex=1 \
        -interaction=nonstopmode -file-line-error \
        -output-directory="{{OUTPUT_DIR}}" \
        -auxdir="{{AUX_DIR}}" \
        -f "$MAIN_TEX"

# Create a submission ZIP for a module using scripts/submitzip.sh
# Usage: just zip <module-name>
# Example: just zip 01-introduction
zip module_name:
    ./scripts/submitzip.sh "{{module_name}}"


# Clean auxiliary files for a module
# Usage: just clean <module-name>
# Example: just clean 01-introduction
clean module_name:
    #!/usr/bin/env bash
    set -euo pipefail
    cd "{{module_name}}/report"
    latexmk -bibtex -output-directory="{{OUTPUT_DIR}}" -auxdir="{{AUX_DIR}}" -c

# Clean everything including PDFs for a module
# Usage: just distclean <module-name>
# Example: just distclean 01-introduction
distclean module_name:
    #!/usr/bin/env bash
    set -euo pipefail
    cd "{{module_name}}/report"
    latexmk -bibtex -output-directory="{{OUTPUT_DIR}}" -auxdir="{{AUX_DIR}}" -C

# Open the generated PDF for a module
# Usage: just open <module-name>
# Example: just open 01-introduction
open module_name:
    #!/usr/bin/env bash
    set -euo pipefail
    NUMBER=$(echo "{{module_name}}" | grep -o '^[0-9]\+' || echo "x")
    PDF_PATH="{{module_name}}/report/{{OUTPUT_DIR}}/{{COURSE_CODE}}-assignment-${NUMBER}-sourander.pdf"
    if [ -f "$PDF_PATH" ]; then
        xdg-open "$PDF_PATH" || open "$PDF_PATH"
    else
        echo "Error: PDF not found at $PDF_PATH"
        exit 1
    fi