import pandas as pd
from multiprocessing import Pool
import os
from tqdm import tqdm
from colorama import Fore, Style, init
import subprocess
import nibabel as nib

base_dir = "/ocean/projects/med220004p/bshresth/vannucci/all_runs/scripts/outputs/AFNI_FSL_strict_noBBR_run2/output/pipeline_cpac_fmriprep-options/sub-PA001/ses-V1W1/func/"
anat = "/ocean/projects/med220004p/bshresth/vannucci/all_runs/scripts/outputs/ANTS_FSL_noBBR_strict/output/pipeline_cpac_fmriprep-options/sub-PA001/ses-V1W1/anat/"
quick_viz_path = "/ocean/projects/med220004p/bshresth/quick-viz/code"

file_path_1 = os.path.join(base_dir, "sub-PA001_ses-V1W1_task-facesmatching_run-1_space-MNI152NLin2009cAsym_desc-head_bold.nii.gz[1]")
#file_path_1 = os.path.join(base_dir, "sub-PA001_ses-V1W1_desc-head_T1w.nii.gz")
file_path_2 = False

# extract slice_no and file_name provided at the end of the file name inside []
if "[" in file_path_1 and "]" in file_path_1:
    slice_no = int(file_path_1.split("[")[1].split("]")[0])
    file_path = file_path_1.split("[")[0]

    print(slice_no, file_path)
else:
    file_path = file_path_1

plot_path = "./plot_bold.png"
command = [
    "python", 
    f"{quick_viz_path}/plot_nii_overlay.py", 
    file_path,
    plot_path, 
    "--cmap", 'bwr', 
    "--title", "",
    "--alpha", "0.5", 
    "--threshold", "auto",
    "-v", str(slice_no)
]

# Add the background parameter if provided
if file_path_2:
    command.extend(["-b", file_path_2])
else:
    command.extend(["-b", "None"])

try:
    subprocess.run(command)
except Exception as e:
    print(Fore.RED + f"Error on {file_name}" + Style.RESET_ALL)
    print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)





NiftiOne