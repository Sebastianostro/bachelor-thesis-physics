# -----------------------------
# IMPORTS
# -----------------------------
## Standard libraries
import sys
import plotting as plot
## Third-party libraries
import pdg
## Custom libraries
import io_smash
import smash_output_functions as sof

# -----------------------------
# CONSTANTS AND SETTINGS
# -----------------------------
# Define file information (paths, names)
data_dir_name = 'Dilepton_Nevents_5_OutInt_NaN/' # Example data subdirectory
file_name = 'Dileptons.oscar'  # Example SMASH output file name

# -----------------------------
# Connect to PDG database
# -----------------------------
api = pdg.connect()

# Construct full path to the SMASH file
path_to_smash_data = io_smash.get_path_to_output_file(file_name, data_dir_name)
full_dilepton_data = io_smash.read_smash_dilepton_output(path_to_smash_data)
short_dilepton_data = io_smash.aggregate_dilepton_pairs(full_dilepton_data)

# Print the first few rows of the DataFrame
print(short_dilepton_data)
# Enrich the DataFrame with PDG names, rapidity, and invariant mass
#smash_data_enriched = sof.add_pdg_names(smash_data)
#smash_data_enriched = sof.calculate_rapidity(smash_data)
#smash_data_enriched = sof.calculate_invariant_mass(smash_data)

# Calculate and print some basic statistics
#sof.print_basic_statistics(smash_data_enriched)

# Plot histograms of rapidity and invariant mass
#plot.plot_distribution(smash_data_enriched, pdg_id=2212, column_name='y', bins=50)  # Proton rapidity
# End of script

