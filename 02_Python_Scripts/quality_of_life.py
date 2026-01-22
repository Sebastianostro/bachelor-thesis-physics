# -----------------------------
# IMPORTS
# -----------------------------
## Standard libraries
import sys
import os
from pathlib import Path
import pandas as pd
## Third-party libraries
import pdg
## Custom libraries

# -----------------------------
# CLASSES AND FUNCTIONS
# -----------------------------

## Function to get output file path
def get_path_to_output_file(file_name, root_path, folder_name="")-> Path:
    # Define file information (paths, names)
    full_path_to_file = Path(root_path) / folder_name / file_name  # full path to the file
    # Check file exists before attempting to read
    if not full_path_to_file.exists():
        raise FileNotFoundError(f"File not found: {full_path_to_file}")
    return full_path_to_file

## Function to get the save path for figures
def get_save_path(directory: str | Path, filename: str) -> Path:
    """
    Return absolute path for saving an image inside the figures_dir.
    Ensures the directory exists.
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    return directory / filename

## Function to get PDG name from PDG ID
def get_pdg_name(pdg_id, long_name = False)-> str:
    # Connect to PDG API
    api = pdg.connect()

    particle = api.get_particle_by_mcid(int(pdg_id))
    if particle is not None:
        if long_name:
            return str(particle)
        else:
        # Keep only the part after the colon (particle short name).
            return str(particle).split(":", 1)[-1].strip()
    else:
        return "Unknown particle"

## Function to apply data types to DataFrame columns
def apply_data_types(df: pd.DataFrame, data_typ_def: dict[str, str]) -> pd.DataFrame:
    """Apply data types to columns that exist in df."""
    dtype_map = {k: v for k, v in data_typ_def.items() if k in df.columns}
    return df.astype(dtype_map)

## Function to resolve column specification to actual column label in DataFrame to handle different input types in functions,
### e.g., string labels of columns or integer positions
def resolve_col(df, col, default):
    if col is None:
        col = default
    # String -> direct label
    if isinstance(col, str):
        return col
    # int: if label exists -> take it; else interpret as position argument
    if isinstance(col, int):
        if col in df.columns:
            return col
        return df.columns[col]
    raise TypeError(f"Unsupported column spec: {col!r}")
