import pandas as pd
from multiprocessing import Pool
import os
from tqdm import tqdm
from colorama import Fore, Style, init
import subprocess
import nibabel as nib

base_dir = "/ocean/projects/med220004p/bshresth/vannucci/all_runs/scripts/outputs/ANTS_FSL_noBBR_strict/output/pipeline_cpac_fmriprep-options/"
quick_viz_path = "/ocean/projects/med220004p/bshresth/quick-viz/code"

def run(sub, ses, file_path_1, file_path_2, file_name, plots_dir, plot_path):

    # check if the above files exist
    if not os.path.exists(file_path_1):
        print(Fore.RED + f"NO FILE: {file_name}" + Style.RESET_ALL)
        return



    # Check if the plot already exists
    if os.path.exists(plot_path):
        print(Fore.YELLOW + f"Plot already exists: {file_name}" + Style.RESET_ALL)
        return
    
    command = [
        "python", 
        f"{quick_viz_path}/plot_nii_overlay.py", 
        f"{file_path_1}",
        plot_path, 
        "--cmap", 'bwr', 
        "--title", "",
        "--alpha", "0.5", 
        "--threshold", "auto"
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
        return
    return
