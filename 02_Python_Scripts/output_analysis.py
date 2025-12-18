import sys

import smash_read as sr
import smash_output_functions as sof
import plotting as plot
import pdg

api = pdg.connect()

# Define file information (paths, names)
data_dir_name = 'Dilepton_Nevents_5_OutInt_NaN/' # Example data subdirectory
file_name = 'Dileptons.oscar'  # Example SMASH output file name
# Construct full path to the SMASH file
path_to_smash_data = sr.get_path_to_output_file(file_name, data_dir_name)

# Read the SMASH file and store the data in a DataFrame
try:
    smash_data = sr.read_smash_dilepton_file(path_to_smash_data)
except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(1)

# Check if data was read successfully
if smash_data is None:
    print("Error: SMASH data appears to be empty!")
    sys.exit(1)

# Print the first few rows of the DataFrame
print(smash_data.head())
# Enrich the DataFrame with PDG names, rapidity, and invariant mass
#smash_data_enriched = sof.add_pdg_names(smash_data)
#smash_data_enriched = sof.calculate_rapidity(smash_data)
#smash_data_enriched = sof.calculate_invariant_mass(smash_data)

# Calculate and print some basic statistics
#sof.print_basic_statistics(smash_data_enriched)

# Plot histograms of rapidity and invariant mass
#plot.plot_distribution(smash_data_enriched, pdg_id=2212, column_name='y', bins=50)  # Proton rapidity
# End of script

