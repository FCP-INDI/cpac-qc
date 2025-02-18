
source ./venv/bin/activate

CPAC_OUTPUT_DIR=/ocean/projects/med220004p/bshresth/vannucci/all_runs/scripts/outputs/AFNI_FSL_strict_noBBR_run2/output/pipeline_cpac_fmriprep-options
QC_DIR=/ocean/projects/med220004p/bshresth/projects/cpac-qc
OVERLAY_CSV=/ocean/projects/med220004p/bshresth/projects/cpac-qc/overlay.csv

# Create the QC directory inside the specified QC_DIR
QC_DIR_PATH="$QC_DIR/QC"
mkdir -p "$QC_DIR_PATH"

# Run the main.py script with the specified directories
python main.py --cpac_output_dir "$CPAC_OUTPUT_DIR" --qc_dir "$QC_DIR_PATH" --overlay_csv "$OVERLAY_CSV" --n_procs 20

# Copy the index.html, script.js, and styles.css files to the QC directory
cp /ocean/projects/med220004p/bshresth/projects/cpac-qc/index.html "$QC_DIR_PATH"


# Deactivate the virtual environment
deactivate