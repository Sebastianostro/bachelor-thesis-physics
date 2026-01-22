# -----------------------------
# IMPORTS
# -----------------------------
## Standard libraries
import sys
from pathlib import Path
import pandas as pd
## Third-party libraries
import pdg
## Custom libraries
import smash_output_functions as sof
import plotting as plot

# -----------------------------
# CLASSES AND FUNCTIONS
# -----------------------------

## Function to get output file path
def get_path_to_output_file(file_name, folder_name, root_path)-> Path:
    # Define file information (paths, names)
    path_to_data = root_path  # Your data path (top level)
    path_to_data_folder = folder_name # Data subdirectory (subfolder under root path)
    path_to_file = Path(path_to_data) / path_to_data_folder / file_name  # full path to the file

    # Check file exists before attempting to read
    if not path_to_file.exists():
        print(f"Datei nicht gefunden: {path_to_file}")
        sys.exit(1)
    return path_to_file

## Function to apply data types to DataFrame columns
def apply_data_types(df: pd.DataFrame, data_typ_def: dict[str, str]) -> pd.DataFrame:
    """Apply data types to columns that exist in df."""
    dtype_map = {k: v for k, v in data_typ_def.items() if k in df.columns}
    return df.astype(dtype_map)
