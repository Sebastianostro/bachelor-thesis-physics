# Script that provides functions to calculate rapidity and invariant mass from a SMASH output file.

# Import necessary libraries
import numpy as np
from functools import partial
import pdg
import pandas as pd

# Define constants if needed (currently none)

# Define functions
## Function to resolve column specification to actual column label in DataFrame to handle different input types in functions,
### e.g., string labels of columns or integer positions
def _resolve_col(df, col, default):
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

## Function to calculate rapidity values for data in a DataFrame
def calculate_rapidity(df, col_energy=None, col_beam=None)-> pd.DataFrame:
    '''
    Input:
        "df" is the original Pandas DataFrame without rapidity information
        "col_energy" is the column that contains the energy (aka p0, default value is "5" in standard SMASH output)
        "col_beam" is the column that contains the momentum in beam direction (aka pz for z-beam, default value is "8" in standard SMASH output)
    Output: 
        Original DataFrame enriched by a column containing the rapidity values (named 'y')
    '''
    p0_label = _resolve_col(df, col_energy, 5)  # Energy column
    pz_label = _resolve_col(df, col_beam, 8)  # pz column
    
    p0 = df[p0_label]
    pz = df[pz_label]

    df['y'] = 0.5 * np.log((p0 + pz) / (p0 - pz))
    return df

## Function to calculate invariant mass for data in a DataFrame
def calculate_invariant_mass(df, col_energy=None, col_px=None, col_py=None, col_pz=None)-> pd.DataFrame:
    '''
    Input: 
        "df" is the original Pandas DataFrame without invariant mass information
        "col_energy" is the column containing the energy (aka p0, default value is "5" in standard SMASH output)
        "col_px" is the column containing the momentum in x direction (default value is "6" in standard SMASH output)
        "col_py" is the column containing the momentum in y direction (default value is "7" in standard SMASH output)
        "col_pz" is the column containing the momentum in z direction (default value is "8" in standard SMASH output)
    Output: 
        Original DataFrame enriched by a column containing the invariant mass values (named 'm_inv')
    '''
    p0_label = _resolve_col(df, col_energy, 5)  # Energy column
    px_label = _resolve_col(df, col_px, 6)      # px column
    py_label = _resolve_col(df, col_py, 7)      # py column
    pz_label = _resolve_col(df, col_pz, 8)      # pz column

    p0 = df[p0_label]
    px = df[px_label]
    py = df[py_label]
    pz = df[pz_label]
    df['m_inv'] = (p0**2 - (px**2 + py**2 + pz**2))
    return df

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

## Function to add PDG names to the DataFrame based on PDG IDs
def add_pdg_names(df, pdg_column=9, long_name = False)-> pd.DataFrame:
    '''
    Input:
        "df" is the DataFrame without PDG names
        "pdg_column" is the column number that contains the PDG IDs (default value is "9" in SMASH output)
    Output:
        DataFrame enriched by a column containing the PDG names (named 'pdg_name')
    '''
    # Add PDG names to the DataFrame
    ## Create wrapper function
    get_pdg_name_wrap = partial(get_pdg_name, long_name=long_name)
    ## Apply wrapper function to the specified PDG ID column
    df['pdg_name'] = df[pdg_column].apply(get_pdg_name_wrap)
    return df

## Function to print basic statistics of the DataFrame
def print_basic_statistics(df):
    '''
    Input:
        "df" is the DataFrame containing SMASH data with columns for pdg names (named "pdg_name"), rapidity (named "y"), and invariant mass (named "m_inv")
    Output:
        Prints basic statistics such as total number of particles, number per type, mean rapidity, and mean invariant mass.
    '''
    unique_pdg_ids = df[9].unique()
    print(f"Unique PDG IDs in the data: {unique_pdg_ids}")

    # Number of total particles
    num_particles = len(df)
    # Number per unique particle type
    num_particles_per_type = df[9].value_counts()

    print(f"Total number of particles: {num_particles}")
    print(f"Number of particles per type: {num_particles_per_type}")
    mean_rapidity = df['y'].groupby(df['pdg_name']).mean()
    mean_invariant_mass = df['m_inv'].groupby(df['pdg_name']).mean()
    print(f"Mean Rapidity: {mean_rapidity}")
    print(f"Mean Invariant Mass: {mean_invariant_mass}")

# Test script functionality if run as main module
if __name__ == "__main__":
    # Example usage and test of functions
    id = input("Enter PDG ID: ")
    print(f"PDG name for entered PDG ID {id}: ", get_pdg_name(int(id), long_name=True))
# End of script
