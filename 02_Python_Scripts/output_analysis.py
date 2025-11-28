import sys
from pathlib import Path

import smash_read as sr
import smash_output_functions as sof
import pdg

api = pdg.connect()

# Define file information (paths, names)
path_to_file = '/home/ostrowski/smash/build/data/'  # Replace with your SMASH file path
path_to_data = '1/' # Example data subdirectory
file_name = 'particle_lists.oscar'  # Example SMASH output file name
smash_file = Path(path_to_file) / path_to_data / file_name  # full path to the SMASH file
print(f"Lese SMASH Datei: {smash_file}")

# Check file exists before attempting to read
if not smash_file.exists():
    print(f"Datei nicht gefunden: {smash_file}")
    sys.exit(1)

# Main script execution
# Read the SMASH file and store the data in a DataFrame
try:
    smash_data = sr.read_smash_file(smash_file)
except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(1)

# Check if data was read successfully
if smash_data is None:
    print("Error: SMASH data appears to be empty!")
    sys.exit(1)

# Enrich the DataFrame with PDG names, rapidity, and invariant mass
smash_data_enriched = sof.add_pdg_names(smash_data)
smash_data_enriched = sof.calculate_rapidity(smash_data)
smash_data_enriched = sof.calculate_invariant_mass(smash_data)

# Calculate and print some basic statistics
sof.print_basic_statistics(smash_data_enriched)

# Plot histograms of rapidity and invariant mass
sof.plot_distribution(smash_data_enriched, 2112, 'y')
# End of script

