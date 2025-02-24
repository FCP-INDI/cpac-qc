#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <CPAC_OUTPUT_DIR> <QC_DIR> <OVERLAY_CSV> <N_PROCS>"
    exit 1
fi

# Assign arguments to variables
CPAC_OUTPUT_DIR=$1
QC_DIR=$2
OVERLAY_CSV=$3
N_PROCS=$4

# Load the virtual environment
source /ocean/projects/med220004p/bshresth/projects/cpac_dashboard/venv/bin/activate

# Create the QC directory inside the specified QC_DIR
QC_DIR_PATH="$QC_DIR/QC"
mkdir -p "$QC_DIR_PATH"

# Run the main.py script with the specified directories
python main.py --cpac_output_dir "$CPAC_OUTPUT_DIR" --qc_dir "$QC_DIR_PATH" --overlay_csv "$OVERLAY_CSV" --n_procs 10

# Copy the index.html, script.js, and styles.css files to the QC directory
cp /ocean/projects/med220004p/bshresth/projects/cpac-qc/index.html "$QC_DIR_PATH"
cp /ocean/projects/med220004p/bshresth/projects/cpac-qc/script.js "$QC_DIR_PATH"
cp /ocean/projects/med220004p/bshresth/projects/cpac-qc/styles.css "$QC_DIR_PATH"

# Deactivate the virtual environment
deactivate