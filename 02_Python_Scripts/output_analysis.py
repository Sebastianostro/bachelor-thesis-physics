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
DATA_DIR_NAME = 'Dilepton_Out_Std_Nevents_10000_OutInt_NaN/' # Example data subdirectory
FILE_NAME = 'Dileptons.oscar'  # Example SMASH output file name
SINGLE_RUN = False  # Whether to process a single run or aggregate multiple runs
# -----------------------------
# MAIN SCRIPT
# -----------------------------
if SINGLE_RUN:
    # Process single run
    path_to_smash_data = qol.get_path_to_output_file(file_name=FILE_NAME, folder_name=DATA_DIR_NAME, root_path=BASE_PATH_TO_DATA)
    smash_data = io_smash.read_smash_dilepton_output(path_to_smash_data)
    short_dilepton_data = io_smash.aggregate_dilepton_pairs(smash_data)   
    dilepton_data_enriched = sof.calculate_invariant_mass(short_dilepton_data, col_energy="p0", col_px="px", col_py="py", col_pz="pz")
    dilepton_data_enriched = sof.enrich_dilepton_with_parent(dilepton_data_enriched)
    dilepton_data_enriched = sof.adjust_shining_weights(dilepton_data_enriched)
else:
    dilepton_data_enriched = sof.aggregate_runs(root_dir=BASE_PATH_TO_DATA, data_dir=DATA_DIR_NAME, filename=FILE_NAME)

bin_struct = np.linspace(0,0.7,36)
plot.plot_hist_multiple(dilepton_data_enriched, col_bin_axis="m_inv", col_weight="block_weight_adj",
                        bin_edges= bin_struct, save_figure=True, file_name="Hist_np_1.5GeV_10kx10_events.png")

#print(dilepton_data_enriched)
#print((dilepton_data_enriched["p_pdg_id"]==-1111))

#print((dilepton_data_enriched["p_pdg_id"]==-1111).sum())

# End of script
