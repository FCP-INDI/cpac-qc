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
args = parser.parse_args()

qc_dir = os.path.join(args.qc_dir)
csv_file = os.path.join(qc_dir, "df.csv")

cpac_output_dir = args.cpac_output_dir

plots_dir = os.path.join(qc_dir, "plots")
os.makedirs(qc_dir, exist_ok=True)
os.makedirs(plots_dir, exist_ok=True)

if os.path.exists(csv_file):
    # Load the CSV file if it exists
    df = pd.read_csv(csv_file)
else:
    # Load in parallel and stream to disk as a Parquet dataset
    df = bids2table(cpac_output_dir, persistent=True, workers=10).flat
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
nii_gz_files["file_name"] = nii_gz_files.file_path.apply(lambda x: os.path.basename(x).split(".")[0])

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

# Prepare the arguments for each row
args = [
    (
        row['sub'], 
        row['ses'], 
        row['datatype'], 
        row['file_path'], 
        {
            "task": row.get('task', ''), 
            "run": row.get('run', ''),
            "space": row.get('space', ''),
            "reg": row.get('reg', ''), 
            "file_name": row["file_name"],
            "plots_dir": plots_dir
        }
    ) 
    for _, row in nii_gz_files.iterrows()
]

def process_row(args):
    run(*args[:4], **args[4])

# Use multiprocessing to process each row with 100 processes
with Pool(processes=100) as pool:
    for _ in tqdm(pool.imap_unordered(process_row, args), total=len(args), desc="Processing"):
        pass