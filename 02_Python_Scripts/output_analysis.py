# -----------------------------
# IMPORTS
# -----------------------------
## Standard libraries
import numpy as np
## Third-party libraries
import pdg
## Custom libraries
import io_smash
import smash_output_functions as sof
import plotting as plot

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

#print(dilepton_data_enriched)
#print((dilepton_data_enriched["p_pdg_id"]==-1111))

#print((dilepton_data_enriched["p_pdg_id"]==-1111).sum())
bin_struct = np.linspace(0,0.7,36)
plot.plot_hist_dilepton_invariant_mass(dilepton_data_enriched, bin_edges= bin_struct,save_figure=True, file_name="Hist_np_1.5GeV_10000events.png")

# End of script
