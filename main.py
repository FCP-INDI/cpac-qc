import pandas as pd
import os
import argparse
from multiprocessing import Pool
from tqdm import tqdm

from bids2table import bids2table
from plot import run
import nibabel as nib
from colorama import Fore, Style, init

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Process CPAC output and generate QC.")
parser.add_argument("--cpac_output_dir", required=True, help="Path to the CPAC output directory")
parser.add_argument("--qc_dir", required=True, help="Path to the QC output directory")
parser.add_argument("--overlay_csv", required=False, help="Overlay CSV file")
parser.add_argument("--n_procs", type=int, default=10, help="Number of processes to use for multiprocessing")

args = parser.parse_args()
cpac_output_dir = args.cpac_output_dir
qc_dir = os.path.join(args.qc_dir)
overlay_csv = args.overlay_csv
n_procs = args.n_procs

csv_file = os.path.join(qc_dir, "df.csv")

plots_dir = os.path.join(qc_dir, "plots")
os.makedirs(qc_dir, exist_ok=True)
os.makedirs(plots_dir, exist_ok=True)

if os.path.exists(csv_file):
    # Load the CSV file if it exists
    df = pd.read_csv(csv_file)
else:
    # Load in parallel and stream to disk as a Parquet dataset
    df = bids2table(cpac_output_dir, persistent=True, workers=n_procs).flat
    # Save df as CSV
    df.to_csv(csv_file, index=False)

for col in df.columns:
    if isinstance(df[col].iloc[0], dict):
        df[col] = df[col].apply(lambda x: str(x) if x else "")
        if df[col].nunique() == 1 and df[col].iloc[0] == "":
            df = df.drop(columns=[col])
            
# give me all columns that have more than one unique value and drop other columns
non_single_value_columns = df.columns[df.nunique() > 1].tolist()
df = df[non_single_value_columns]

# fill all columns with NaN with empty string
df = df.fillna("")

# drop json column too
df = df.drop(columns=["json"])

# give me all whose ext is nii.gz
nii_gz_files = df[df.file_path.str.endswith(".nii.gz")]

# add one column that breaks the file_path to the last name of the file and drops extension
nii_gz_files["file_name"] = nii_gz_files.file_path.apply(lambda x: os.path.basename(x).replace(".nii.gz", ""))

def gen_resource_name(row):
    sub = row["sub"]
    ses = row["ses"]
    task = row["task"] if row["task"] != "" else False
    run = int(row["run"]) if row["run"] != "" else False
    
    scan = f"task-{task}_run-{run}_" if task and run else ""
    resource_name = row["file_name"].replace(f"sub-{sub}_ses-{ses}_{scan}", "")
    return resource_name

nii_gz_files["resource_name"] = nii_gz_files.apply(gen_resource_name, axis=1)

# add a utility function to return rows provided a resource_name
def get_rows_by_resource_name(resource_name):
    # get all rows that have the resource_name
    rows = nii_gz_files[nii_gz_files.resource_name == resource_name]
    if len(rows) == 0:
        print(Fore.RED + f"NOT FOUND: {resource_name} " + Style.RESET_ALL)
        return None
    return rows

    

# check file_path and drop the ones that are higher dimensions for now
def is_3d(file_path):
    dim = len(nib.load(file_path).shape)
    if dim > 3:
        file_name = os.path.basename(file_path).split(".")[0]
        print(Fore.RED + f"NOT 3D: {file_name} \n its {dim}D " + Style.RESET_ALL)
        print(Fore.RED + f"Skipping for now ...." + Style.RESET_ALL)
        return False
    return True
nii_gz_files = nii_gz_files[nii_gz_files.file_path.apply(is_3d)]

# save nii_gz_files to csv
nii_gz_files_csv_path = os.path.join(qc_dir, "nii_gz_files.csv")
nii_gz_files.to_csv(nii_gz_files_csv_path, index=False)

# for rows in overlay_csv find the resource_name and get the rows
if overlay_csv:
    overlay_df = pd.read_csv(overlay_csv)
    overlay_df = overlay_df.fillna(False)

    def process_row(row):
        image_1 = row.get("image_1", False)
        image_2 = row.get("image_2", False)

        print(image_1, image_2)

        # get the resource name from the file name
        if image_1:
            resource_name_1 = get_rows_by_resource_name(image_1)
            if image_2:
                resource_name_2 = get_rows_by_resource_name(image_2)
            else:
                resource_name_2 = None
        else:
            print(Fore.RED + f"NOT FOUND: {image_1} " + Style.RESET_ALL)
            return
    
    overlay_df.apply(process_row, axis=1)

# # Prepare the arguments for each row
# args = [
#     (
#         row['sub'], 
#         row['ses'], 
#         row['datatype'], 
#         row['file_path'], 
#         {
#             "task": row.get('task', ''), 
#             "run": row.get('run', ''),
#             "space": row.get('space', ''),
#             "reg": row.get('reg', ''), 
#             "file_name": row["file_name"],
#             "plots_dir": plots_dir
#         }
#     ) 
#     for _, row in nii_gz_files.iterrows()
# ]

# def process_row(args):
#     run(*args[:4], **args[4])

# # Use multiprocessing to process each row with 100 processes
# with Pool(processes=n_procs) as pool:
#     for _ in tqdm(pool.imap_unordered(process_row, args), total=len(args), desc="Processing"):
#         pass