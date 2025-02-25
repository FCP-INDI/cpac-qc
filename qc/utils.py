import pandas as pd
import os
import argparse
from multiprocessing import Pool
from tqdm import tqdm

from bids2table import bids2table
import nibabel as nib
from colorama import Fore, Style, init

from qc.plot import run

def gen_resource_name(row):
    sub = row["sub"]
    ses = row["ses"]
    task = row["task"] if row["task"] != "" else False
    run = int(row["run"]) if row["run"] != "" else False
    
    scan = f"task-{task}_run-{run}_" if task and run else ""
    resource_name = row["file_name"].replace(f"sub-{sub}_ses-{ses}_{scan}", "")
    return resource_name


# add a utility function to return rows provided a resource_name
def get_rows_by_resource_name(resource_name):
    # get all rows that have the resource_name
    rows = nii_gz_files[nii_gz_files.resource_name == resource_name]
    if len(rows) == 0:
        print(Fore.RED + f"NOT FOUND: {resource_name} " + Style.RESET_ALL)
        return None
    return rows

# check file_path and drop the ones that are higher dimensions for now
def is_3d_or_4d(file_path):
    dim = len(nib.load(file_path).shape)
    if dim > 4:
        file_name = os.path.basename(file_path).split(".")[0]
        print(Fore.RED + f"NOT 3D: {file_name} \n its {dim}D " + Style.RESET_ALL)
        print(Fore.RED + f"Skipping for now ...." + Style.RESET_ALL)
        return False
    return True

def process_row(row):
    image_1 = row.get("image_1", False)
    image_2 = row.get("image_2", False)

    resource_name_1 = get_rows_by_resource_name(image_1) if image_1 else None
    resource_name_2 = get_rows_by_resource_name(image_2) if image_2 else None

    if resource_name_1 is None:
        print(Fore.RED + f"NOT FOUND: {image_1} " + Style.RESET_ALL)
        return []

    result_rows = []
    seen = set()  # To track duplicates

    for _, res1_row in resource_name_1.iterrows():
        scan = f"task-{res1_row['task']}_run-{int(res1_row['run'])}_" if res1_row['task'] and res1_row['run'] else ""

        if resource_name_2 is not None:
            for _, res2_row in resource_name_2.iterrows():
                file_name = f"ses-{res1_row['ses']}_{scan + res1_row['resource_name']} overlaid on {res2_row['resource_name']}"
                if file_name not in seen:
                    seen.add(file_name)
                    sub_dir = os.path.join(overlay_dir, res1_row['sub'], res1_row['ses'])
                    os.makedirs(sub_dir, exist_ok=True)
                    plot_path = os.path.join(sub_dir, f"{scan + res1_row['resource_name']} overlaid on {res2_row['resource_name']}.png")
                    result_rows.append({
                        "sub": res1_row["sub"],
                        "ses": res1_row["ses"],
                        "file_path_1": res1_row["file_path"],
                        "file_path_2": res2_row["file_path"],
                        "file_name": file_name,
                        "plots_dir": overlay_dir,
                        "plot_path": plot_path
                    })
        else:
            file_name = f"ses-{res1_row['ses']}_{scan + res1_row['resource_name']}"
            if file_name not in seen:
                seen.add(file_name)
                sub_dir = os.path.join(plots_dir, res1_row['sub'], res1_row['ses'])
                os.makedirs(sub_dir, exist_ok=True)
                plot_path = os.path.join(sub_dir, f"{scan + res1_row['resource_name']}.png")
                result_rows.append({
                    "sub": res1_row["sub"],
                    "ses": res1_row["ses"],
                    "file_path_1": res1_row["file_path"],
                    "file_path_2": None,
                    "file_name": file_name,
                    "plots_dir": plots_dir,
                    "plot_path": plot_path
                })

    return result_rows

def run_wrapper(args):
    return run(*args)