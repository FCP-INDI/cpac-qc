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

# Create the QC directory inside the specified QC_DIR
QC_DIR_PATH="$QC_DIR/QC"
mkdir -p "$QC_DIR_PATH"

# Run the main.py script with the specified directories
python main.py --cpac_output_dir "$CPAC_OUTPUT_DIR" --qc_dir "$QC_DIR_PATH" --overlay_csv "$OVERLAY_CSV" --n_procs "$N_PROCS"

# Copy the index.html, script.js, and styles.css files to the QC directory
cp /qc/resources/index.html "$QC_DIR_PATH"
cp /qc/resources/script.js "$QC_DIR_PATH"
cp /qc/resources/styles.css "$QC_DIR_PATH"