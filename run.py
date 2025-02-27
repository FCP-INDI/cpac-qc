from qc.main import main
import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the QC application.')
    parser.add_argument('--n_procs', type=int, default=10, help='Number of processes to use')
    args = parser.parse_args()

    # Hard-coded values for the arguments
    cpac_output_dir = "/cpac_output_dir"
    qc_dir = "/qc_dir"
    overlay_csv = "/config/overlay.csv"  # Set to None if not using an overlay CSV
    if not os.path.exists(overlay_csv):
        overlay_csv = False
    n_procs = args.n_procs

    main(cpac_output_dir, qc_dir, overlay_csv, n_procs)

    # Copy contents of qc/templates to the qc_dir
    try: 
        os.system(f"cp -r /app/qc/templates/. {qc_dir}")
    except Exception as e:
        print(f"Error copying templates: {e}")
        pass