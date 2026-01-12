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

# -----------------------------
# Connect to PDG database
# -----------------------------
api = pdg.connect()



# Define file information (paths, names)
data_dir_name = 'Dilepton_Nevents_5_OutInt_NaN/' # Example data subdirectory
file_name = 'Dileptons.oscar'  # Example SMASH output file name
# Construct full path to the SMASH file
path_to_smash_data = io_smash.get_path_to_output_file(file_name, data_dir_name)

smash_data = io_smash.read_smash_table_with_blocks(path_to_smash_data)

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

