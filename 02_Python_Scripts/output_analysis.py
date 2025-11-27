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

#print(smash_data.head())
smash_data_enriched = sof.calculate_rapidity(smash_data)
smash_data_enriched = sof.calculate_invariant_mass(smash_data)
#print(smash_data_enriched.head())
unique_pdg_ids = smash_data[9].unique()
print(f"Unique PDG IDs in the data: {unique_pdg_ids}")

for pdg_id in unique_pdg_ids:
    particle = api.get_particle_by_mcid(int(pdg_id))
    if particle is not None:
        print(f"PDG ID: {pdg_id}, Name: {particle}")
    else:
        print(f"PDG ID: {pdg_id}, Name: Unknown particle")
# End of script

