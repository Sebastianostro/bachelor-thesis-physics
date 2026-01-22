# -----------------------------
# IMPORTS
# -----------------------------
## Standard libraries
import numpy as np
## Third-party libraries

## Custom libraries
import quality_of_life as qol
import io_smash
import smash_output_functions as sof
import plotting as plot

# -----------------------------
# CONSTANTS AND SETTINGS
# -----------------------------
# Define file information (paths, names)
BASE_PATH_TO_DATA = '/home/sebastian/dev/python/bachelor-thesis-physics/05_Files_from_Virgo/'
DATA_DIR_NAME = 'Dilepton_Output_Std_Nevents_10000_OutInt_NaN/' # Example data subdirectory
FILE_NAME = 'Dileptons.oscar'  # Example SMASH output file name

# -----------------------------
# MAIN SCRIPT
# -----------------------------
# Construct full path to the SMASH file
path_to_smash_data = qol.get_path_to_output_file(FILE_NAME, DATA_DIR_NAME, BASE_PATH_TO_DATA)
full_dilepton_data = io_smash.read_smash_dilepton_output(path_to_smash_data)
short_dilepton_data = io_smash.aggregate_dilepton_pairs(full_dilepton_data)

# Enrich the DataFrame with PDG names, rapidity, and invariant mass
#smash_data_enriched = sof.calculate_rapidity(smash_data)
dilepton_data_enriched = sof.calculate_invariant_mass(short_dilepton_data, col_energy="p0", col_px="px", col_py="py", col_pz="pz")
dilepton_data_enriched = sof.enrich_dilepton_with_parent(dilepton_data_enriched)
dilepton_data_enriched = sof.adjust_shining_weights(dilepton_data_enriched)

#print(dilepton_data_enriched)
#print((dilepton_data_enriched["p_pdg_id"]==-1111))

#print((dilepton_data_enriched["p_pdg_id"]==-1111).sum())
bin_struct = np.linspace(0,0.7,36)
plot.plot_hist_dilepton_invariant_mass(dilepton_data_enriched, bin_edges= bin_struct,
                                       save_figure=True, file_name="Hist_np_1.5GeV_10000events.png")

# End of script
