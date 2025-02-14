#!/bin/bash

# Load the virtual environment
source /ocean/projects/med220004p/bshresth/projects/cpac_dashboard/venv/bin/activate

# Define the CPAC output directory and QC directory
CPAC_OUTPUT_DIR="/ocean/projects/med220004p/bshresth/vannucci/all_runs/scripts/outputs/AFNI_FSL_strict_noBBR_run2/output"
QC_DIR="."

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