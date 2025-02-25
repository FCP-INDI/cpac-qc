from qc.main import main
import os

if __name__ == '__main__':
    # Hard-coded values for the arguments
    cpac_output_dir = "/cpac_output_dir"
    qc_dir = "/qc_dir"
    overlay_csv = "/config/overlay.csv"  # Set to None if not using an overlay CSV
    if not os.path.exists(overlay_csv):
        overlay_csv = "/app/qc/config/overlay.csv"
    n_procs = 10

    main(cpac_output_dir, qc_dir, overlay_csv, n_procs)

    #copy contents of qc/templates to the qc_dir
    try: 
        os.system(f"cp -r /app/qc/templates/. {qc_dir}")
    except Exception as e:
        print(f"Error copying templates: {e}")
        pass