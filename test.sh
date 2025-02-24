
source ./venv/bin/activate

CPAC_OUTPUT_DIR=/ocean/projects/med220004p/bshresth/vannucci/all_runs/scripts/outputs/AFNI_FSL_strict_noBBR_run2/output/pipeline_cpac_fmriprep-options
QC_DIR=/ocean/projects/med220004p/bshresth/projects/cpac-qc
OVERLAY_CSV=/ocean/projects/med220004p/bshresth/projects/cpac-qc/overlay.csv

bash gen_qc.sh $CPAC_OUTPUT_DIR $QC_DIR $OVERLAY_CSV 10