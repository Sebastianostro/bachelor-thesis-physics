# -----------------------------
# IMPORTS
# -----------------------------
## Standard libraries
import sys
import plotting as plot
import numpy as np
from matplotlib import pyplot as plt
## Third-party libraries
import pdg
## Custom libraries
import io_smash
import smash_output_functions as sof

# -----------------------------
# CONSTANTS AND SETTINGS
# -----------------------------
# Define file information (paths, names)
data_dir_name = 'Dilepton_Output_Std_Nevents_10000_OutInt_NaN/' # Example data subdirectory
file_name = 'Dileptons.oscar'  # Example SMASH output file name

# -----------------------------
# Connect to PDG database
# -----------------------------
api = pdg.connect()

# Construct full path to the SMASH file
path_to_smash_data = io_smash.get_path_to_output_file(file_name, data_dir_name)
full_dilepton_data = io_smash.read_smash_dilepton_output(path_to_smash_data)
short_dilepton_data = io_smash.aggregate_dilepton_pairs(full_dilepton_data)

# Enrich the DataFrame with PDG names, rapidity, and invariant mass
#smash_data_enriched = sof.add_pdg_names(smash_data)
#smash_data_enriched = sof.calculate_rapidity(smash_data)
dilepton_data_enriched = sof.calculate_invariant_mass(short_dilepton_data, col_energy="p0", col_px="px", col_py="py", col_pz="pz")
dilepton_data_enriched = sof.enrich_dilepton_with_parent(dilepton_data_enriched)
dilepton_data_enriched = sof.adjust_shining_weights(dilepton_data_enriched)

plot.plot_hist_dilepton_invariant_mass(dilepton_data_enriched, save_figure=True, file_name="Hist_np_1.5GeV_10000events.png", in_max_gap_bins=4, in_bins=40)

# End of script
