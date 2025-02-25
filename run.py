from qc.main import main

if __name__ == '__main__':
    # Hard-coded values for the arguments
    cpac_output_dir = "/cpac_output_dir"
    qc_dir = "/qc_dir"
    overlay_csv = "/config/overlay.csv"  # Set to None if not using an overlay CSV
    if not overlay_csv:
        overlay_csv = "/app/qc/config/overlay.csv"
    n_procs = 10

    main(cpac_output_dir, qc_dir, overlay_csv, n_procs)