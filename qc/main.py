import pandas as pd
import os
from multiprocessing import Pool
from tqdm import tqdm

from bids2table import bids2table
import nibabel as nib
from colorama import Fore, Style, init

from qc.utils import *
from qc.plot import run

def main(cpac_output_dir, qc_dir, overlay_csv=None, n_procs=10):
    qc_dir = os.path.join(qc_dir)
    csv_file = os.path.join(qc_dir, "df.csv")

    plots_dir = os.path.join(qc_dir, "plots")
    os.makedirs(qc_dir, exist_ok=True)
    os.makedirs(plots_dir, exist_ok=True)

    overlay_dir = os.path.join(qc_dir, "overlays")
    os.makedirs(overlay_dir, exist_ok=True)

    if os.path.exists(csv_file):
        # Load the CSV file if it exists
        df = pd.read_csv(csv_file)
    else:
        # Load in parallel and stream to disk as a Parquet dataset
        df = bids2table(cpac_output_dir, workers=n_procs).flat
        # Save df as CSV
        #df.to_csv(csv_file, index=False)

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
    nii_gz_files.loc[:, "file_name"] = nii_gz_files.file_path.apply(lambda x: os.path.basename(x).replace(".nii.gz", ""))

    nii_gz_files.loc[:, "resource_name"] = nii_gz_files.apply(gen_resource_name, axis=1)

    nii_gz_files = nii_gz_files[nii_gz_files.file_path.apply(is_3d_or_4d)]

    # save nii_gz_files to csv
    nii_gz_files_csv_path = os.path.join(qc_dir, "nii_gz_files.csv")
    nii_gz_files.to_csv(nii_gz_files_csv_path, index=False)

    # for rows in overlay_csv find the resource_name and get the rows
    if overlay_csv:
        overlay_df = pd.read_csv(overlay_csv)
        overlay_df = overlay_df.fillna(False)
        results = overlay_df.apply(process_row, axis=1).tolist()

        # Flatten the list of lists
        results = [item for sublist in results for item in sublist]

        # Create a DataFrame from the results
        result_df = pd.DataFrame(results)
        result_df['relative_path'] = result_df.apply(lambda row: os.path.relpath(row['plot_path'], qc_dir), axis=1)

        # save the result_df to csv
        result_df_csv_path = os.path.join(qc_dir, "results.csv")
        result_df.to_csv(result_df_csv_path, index=False)

    args = [
        (
            row['sub'], 
            row['ses'],  
            row['file_path_1'],
            row['file_path_2'], 
            row['file_name'],
            row['plots_dir'],
            row['plot_path']
        ) 
        for _, row in result_df.iterrows()
    ]

    # Use multiprocessing to process each row with the specified number of processes
    with Pool(processes=n_procs) as pool:
        for _ in tqdm(pool.imap_unordered(run_wrapper, args), total=len(args), desc="Processing ..."):
            pass

if __name__ == "__main__":
    import argparse

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process CPAC output and generate QC.")
    parser.add_argument("--cpac_output_dir", required=True, help="Path to the CPAC output directory")
    parser.add_argument("--qc_dir", required=True, help="Path to the QC output directory")
    parser.add_argument("--overlay_csv", required=False, help="Overlay CSV file")
    parser.add_argument("--n_procs", type=int, default=10, help="Number of processes to use for multiprocessing")

    args = parser.parse_args()
    main(args.cpac_output_dir, args.qc_dir, args.overlay_csv, args.n_procs)