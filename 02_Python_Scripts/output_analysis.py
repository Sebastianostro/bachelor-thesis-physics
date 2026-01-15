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


dilepton_only = dilepton_data_enriched[dilepton_data_enriched["p_pdg_id"]==-1111]

# Plot histogram of invariant mass for dileptons

# Optional: nur bestimmte IDs plotten
pdg_ids = sorted(dilepton_only["p_parent_pdg_id"].unique())
pdg_ids = [pdg_id for pdg_id in pdg_ids if pdg_id != 0]  # remove 0 if present
pdg_name_map = {pdg_id: sof.get_pdg_name(pdg_id) for pdg_id in pdg_ids}

bins = 60  # oder np.linspace(min,max,n)
plt.figure(figsize=(8,5))

max_gap_bins = 2  # maximum number of empty bins to bridge linearly

def fill_small_gaps(counts, centers, max_gap_bins):
    mask = counts > 0
    idx = np.where(mask)[0]
    if idx.size < 2:
        return counts
    filled = counts.copy()
    for left, right in zip(idx[:-1], idx[1:]):
        gap = right - left - 1
        if 0 < gap <= max_gap_bins:
            gap_idx = np.arange(left + 1, right)
            filled[gap_idx] = np.interp(
                centers[gap_idx],
                [centers[left], centers[right]],
                [counts[left], counts[right]],
            )
    return filled

all_dileptons = dilepton_only
all_counts, all_edges = np.histogram(
    all_dileptons["m_inv"],
    bins=bins,
    weights=all_dileptons["block_weight"],
)
all_centers = 0.5 * (all_edges[1:] + all_edges[:-1])
all_counts = fill_small_gaps(all_counts, all_centers, max_gap_bins)
plt.plot(
    all_centers,
    all_counts,
    color="black",
    linewidth=2.0,
    alpha=0.9,
    label="all dileptons",
)

for pdg_id in pdg_ids:
    sub = dilepton_data_enriched[dilepton_data_enriched["p_parent_pdg_id"] == pdg_id]
    counts, edges = np.histogram(
        sub["m_inv"],
        bins=bins,
        weights=sub["block_weight"],  # falls vorhanden/gewünscht
    )
    centers = 0.5 * (edges[1:] + edges[:-1])
    counts = fill_small_gaps(counts, centers, max_gap_bins)
    plt.plot(
        centers,
        counts,
        linewidth=1.5,
        alpha=0.9,
        label=pdg_name_map.get(pdg_id, str(pdg_id)),
    )
plt.yscale("log")
plt.ylim(bottom=0)
plt.xscale("linear")
plt.xlim(0, 0.7)
plt.xlabel("Invariant Mass $m_{inv}$")
plt.ylabel("Counts")
plt.title("Dilepton invariant mass per decay channel (10,000 events)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Print the first few rows of the DataFrame
#print(hist_data)

# Calculate and print some basic statistics
#sof.print_basic_statistics(smash_data_enriched)
# Plot histograms of rapidity and invariant mass
#plot.plot_distribution(dilepton_data_enriched, pdg_id=2212, column_name='m_inv', bins=50)  # Proton rapidity
# End of script
