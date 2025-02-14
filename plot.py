import pandas as pd
from multiprocessing import Pool
import os
from tqdm import tqdm
from colorama import Fore, Style, init
import subprocess
import nibabel as nib

base_dir = "/ocean/projects/med220004p/bshresth/vannucci/all_runs/scripts/outputs/ANTS_FSL_noBBR_strict/output/pipeline_cpac_fmriprep-options/"
quick_viz_path = "/ocean/projects/med220004p/bshresth/quick-viz/code"

def run(sub, ses, datatype, file_path, **kwargs):

    plots_dir = kwargs.get("plots_dir")

    # get the file name from **kwargs
    file_name = kwargs.get("file_name", "")

    # check if the image is a 3d or 4d or else using nibabel pixdim
    dim = len(nib.load(file_path).shape)

    if dim > 3:
        print(Fore.RED + f"NOT 3D: {file_name} \n its {dim}D " + Style.RESET_ALL)
        return

    # check if the above files exist
    if not os.path.exists(file_path):
        print(Fore.RED + f"NO FILE: {file_name}" + Style.RESET_ALL)
        return

    plot_path = f"{plots_dir}/{file_name}.png"

    # Check if the plot already exists
    if os.path.exists(plot_path):
        print(Fore.YELLOW + f"Plot already exists: {file_name}" + Style.RESET_ALL)
        return

    command = [
        "python", 
        f"{quick_viz_path}/plot_nii_overlay.py", 
        f"{file_path}",
        plot_path, 
        "--cmap", "autumn", 
        "--title", "",
        "--alpha", "0.5", 
        "--threshold", "50",
        "-b", "None"
    ]
    try:
        subprocess.run(command)
    except Exception as e:
        print(Fore.RED + f"Error on {file_name}" + Style.RESET_ALL)
        print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
        return
    print(Fore.GREEN + f"Success: {file_name}" + Style.RESET_ALL)
    return

if __name__ == "__main__":
    # Read in strict/strict.csv
    df = pd.read_csv("/ocean/projects/med220004p/bshresth/vannucci/all_runs/scripts/post_proc/strict/strict.csv")
    
    # Prepare the arguments for each row
    args = [(row['sub'], row['ses'], row['scan'], row['reg'], row['file_path']) for _, row in df.iterrows()]

    # Use multiprocessing to process each row with 50 processes
    with Pool(processes=50) as pool:
        for _ in tqdm(pool.imap_unordered(run, args), total=len(args), desc="Processing"):
            pass