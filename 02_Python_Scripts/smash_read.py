# Script that reads data from a SMASH output file and provides functions to calculate rapidity and invariant mass.

# Import necessary libraries
import pandas as pd
import numpy as np

# Define constants if needed (currently none)

# Define functions
## Function to read SMASH file
### This function reads a SMASH output file and returns its contents as a pandas DataFrame.
### It assumes the file is whitespace-delimited and may contain comment lines starting with '#'.
### The file structure is expected to be tabular with the following columns: t x y z mass p0 px py pz pdg ID charge
### Units per column: fm fm fm fm GeV GeV GeV GeV GeV none none e
### pdg ID corresponds to Particle Data Group identification numbers, see https://pdg.lbl.gov/2020/reviews/rpp2020-rev-monte-carlo-numbering.pdf for reference.
### Input: file_path (str) - path to the SMASH output file
### Output: pandas DataFrame containing the SMASH data
def read_smash_file(file_path):
    try:
        # Read the SMASH file using pandas
        data = pd.read_csv(file_path, delim_whitespace=True, comment='#', header=None)
        return data
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

## Function to calculate rapidity values for data in a DataFrame
### Input: 
# "df" is the original Pandas DataFrame without rapidity information
# "col_no_energy" is the column number that contains the energy (aka p0, default value is "5" in SMASH output)
# "col_no_beam" is the column number that contains the momentum in beam direction (aka pz for z-beam, default value is "8" in SMASH output)
### Output: Original DataFrame enriched by a column containing the rapidity values (named 'y')
def calculate_rapidity(df, col_no_energy=5, col_no_beam=8):
    p0 = df[col_no_energy]  # Energy column
    pz = df[col_no_beam]  # pz column
    df['y'] = 0.5 * np.log((p0 + pz) / (p0 - pz))
    return df

## Function to calculate invariant mass for data in a DataFrame
### Input: 
# "df" is the original Pandas DataFrame without invariant mass information
# "col_no_energy" is the column number that contains the energy (aka p0, default value is "5" in SMASH output)
# "col_no_px" is the column number that contains the momentum in x direction (default value is "6" in SMASH output)
# "col_no_py" is the column number that contains the momentum in y direction (default value is "7" in SMASH output)
# "col_no_pz" is the column number that contains the momentum in z direction (default value is "8" in SMASH output)
### Output: Original DataFrame enriched by a column containing the invariant mass values (named 'm_inv')
def calculate_invariant_mass(df, col_no_energy=5, col_no_px=6, col_no_py=7, col_no_pz=8):
    p0 = df[col_no_energy]
    px = df[col_no_px]
    py = df[col_no_py]
    pz = df[col_no_pz]
    df['m_inv'] = (p0**2 - (px**2 + py**2 + pz**2))
    return df

# End of script