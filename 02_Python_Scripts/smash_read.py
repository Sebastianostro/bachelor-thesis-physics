# First script to read and display contents of a SMASH file
# Import necessary libraries
import pandas as pd
import numpy as np

# Define constants if needed (currently none)

# Define file information (paths, names)
path_to_file = '/home/ostrowski/smash/build/data/'  # Replace with your SMASH file path
path_to_data = '1/' # Example data subdirectory
file_name = 'particle_lists.oscar'  # Example SMASH output file name
smash_file = path_to_file + path_to_data + file_name  # full path to the SMASH file

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

#TODO: Add rapidity and invariant mass calculations
## Function to calculate rapidity on DataFrame and add as new column to end
### Input: DataFrame with columns including energy (p0) and momentum in z-direction (pz)
def calculate_rapidity(df):
    E = df[4]  # Energy column
    pz = df[7]  # pz column
    rapidity = 0.5 * np.log((E + pz) / (E - pz))
    return rapidity


## Function to calculate invariant mass


# Main script execution
# Read the SMASH file and store the data in a DataFrame
smash_data = read_smash_file(smash_file)
# Check if data was read successfully
if smash_data is not None:
    # Display the first few rows of the DataFrame
    print(smash_data.head())
else:
    print("Failed to read SMASH data.")

# Calculate rapidity for each particle and add it as a new column
# Rapidity y is calculated using the formula: y = 0.5 * ln((E + pz) / (E - pz))
# where E is the energy and pz is the momentum in the z-direction
if smash_data is not None:
    E = smash_data[4]  # Energy column
    pz = smash_data[7]  # pz column
    smash_data['rapidity'] = 0.5 * np.log((E + pz) / (E - pz))
    print(smash_data[['rapidity']].head())



