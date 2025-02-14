#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <CPAC_OUTPUT_DIR> <QC_DIR>"
    exit 1
fi

# Assign arguments to variables
CPAC_OUTPUT_DIR=$1
QC_DIR=$2

# Load the virtual environment
source /ocean/projects/med220004p/bshresth/projects/cpac_dashboard/venv/bin/activate

# Create the QC directory inside the specified QC_DIR
QC_DIR_PATH="$QC_DIR/QC"
mkdir -p "$QC_DIR_PATH"

# Run the main.py script with the specified directories
python /ocean/projects/med220004p/bshresth/projects/cpac_dashboard/main.py --cpac_output_dir "$CPAC_OUTPUT_DIR" --qc_dir "$QC_DIR_PATH"

# Copy the index.html, script.js, and styles.css files to the QC directory
cp /ocean/projects/med220004p/bshresth/projects/cpac_dashboard/index.html "$QC_DIR_PATH"
cp /ocean/projects/med220004p/bshresth/projects/cpac_dashboard/script.js "$QC_DIR_PATH"
cp /ocean/projects/med220004p/bshresth/projects/cpac_dashboard/styles.css "$QC_DIR_PATH"

# Deactivate the virtual environment
deactivate