# Script that reads data from a SMASH output file and provides functions to calculate rapidity and invariant mass.

# Import necessary libraries
import pandas as pd

# Define constants if needed (currently none)

# Define functions
## Function to read SMASH file
def read_smash_file(file_path):
    '''
    This function reads a SMASH output file and returns its contents as a pandas DataFrame.
    It assumes the file is whitespace-delimited and may contain comment lines starting with '#'.
    The file structure is expected to be tabular with the following columns: t x y z mass p0 px py pz pdg ID charge
    Units per column: fm fm fm fm GeV GeV GeV GeV GeV none none e
    pdg ID corresponds to Particle Data Group identification numbers, see https://pdg.lbl.gov/2020/reviews/rpp2020-rev-monte-carlo-numbering.pdf for reference.
    
    Input: 
        file_path (str) - path to the SMASH output file
    Output: 
        pandas DataFrame containing the SMASH data
    '''
    try:
        # Read the SMASH file using pandas
        data = pd.read_csv(file_path, sep='\\s+', comment='#', header=None)
        return data
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# End of script