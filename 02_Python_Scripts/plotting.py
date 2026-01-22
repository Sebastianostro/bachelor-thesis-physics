# Script that provides functions to plot data.

# Import necessary libraries
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import quality_of_life as qol

# Define directory to save figures
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '06_Figures'))

# Functions
## Define a function to fill small gaps in histogram data. Maximum number of empty bins to bridge linearly
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
            filled[gap_idx] = np.interp(centers[gap_idx], [centers[left], centers[right]], [counts[left], counts[right]],)
    return filled

def _plot_dilepton_hist_line(ax, df, col_bin_axis, col_weight, bin_edges,
                             label, color=None, linewidth=1.5, alpha=0.9,
                             gap_filling=False, max_gap_bins=2):
    col_plot_value = qol.resolve_col(df, col_bin_axis, 5)
    col_plot_weight = qol.resolve_col(df, col_weight, "block_weight")
    counts, edges = np.histogram(df[col_plot_value], bins=bin_edges, weights=df[col_plot_weight],)
    centers = 0.5 * (edges[1:] + edges[:-1])
    if gap_filling:
        counts = fill_small_gaps(counts, centers, max_gap_bins=max_gap_bins)
    ax.plot(
        centers,
        counts,
        color=color,
        linewidth=linewidth,
        alpha=alpha,
        label=label,
    )

## Function to plot histogram of invariant mass for dileptons including different decay channels
def plot_hist_dilepton_invariant_mass(dilepton_data_input: pd.DataFrame, bin_edges: np.ndarray,
                                      gap_filling = False, in_max_gap_bins = 2,
                                      save_figure=False, file_name=None):
    # Preprocessing data to separate different pseudo-parent PDG IDs and map to names for legend
    # First, filter only dilepton entries
    dilepton_only = dilepton_data_input[dilepton_data_input["p_pdg_id"]==-1111]
    # Get unique parent PDG IDs
    p_parent_pdg_ids = dilepton_only["p_parent_pdg_id"].unique()
    # Remove 0 (if present) which indicates no parent 
    # (should not be the case but would also be useful to cover the potential case of mutliple "parents" (in-going particles) per dilepton block)
    p_parent_pdg_ids = [id for id in p_parent_pdg_ids if id != 0]  # remove 0 if present
    # Map PDG IDs to names
    pdg_name_map = {id: qol.get_pdg_name(id) for id in p_parent_pdg_ids}

    # Get total number of events for title
    n_events = int(dilepton_data_input['event'].max()) + 1

    col_bin_axis = "m_inv"
    col_weight = "block_weight"
    # Start plotting
    fig, ax = plt.subplots(figsize=(8,5))
    # Get data for all dileptons
    all_dileptons = dilepton_only
    _plot_dilepton_hist_line(ax, all_dileptons, col_bin_axis=col_bin_axis, col_weight=col_weight, bin_edges = bin_edges, 
                             label="all dileptons", color="black", linewidth=2.0, alpha=0.9,
                             gap_filling=gap_filling, max_gap_bins=in_max_gap_bins,
                             )
    # Plot subsets for individual decay channels producing dileptons
    for id in p_parent_pdg_ids:
        sub = dilepton_data_input[dilepton_data_input["p_parent_pdg_id"] == id]
        _plot_dilepton_hist_line(ax, sub, bin_edges=bin_edges, col_bin_axis=col_bin_axis, col_weight=col_weight,
                                 label=pdg_name_map.get(id, str(id)), linewidth=1.5, alpha=0.9,
                                 gap_filling=gap_filling, max_gap_bins=in_max_gap_bins,
                                 )
    # Set overall properties
    ax.set_yscale("log")
    ax.set_ylim(bottom=0)
    ax.set_xscale("linear")
    x_limits = (0,bin_edges[-1])
    ax.set_xlim(x_limits)
    ax.set_xlabel("Invariant Mass $m_{inv}$ (GeV/$c^2$)")
    y_label = r'$\frac{dN}{d m_{inv}}$'
    ax.set_ylabel(y_label)
    ax.set_title(f"np @ 1.5 GeV ({n_events:,} events)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    # Save or show the figure
    if save_figure:
        if file_name is None:
            file_name = f"Hist_InvMass_{n_events}.png"
        save_path = qol.get_save_path(FIGURE_DIR, file_name)
        fig.savefig(save_path, bbox_inches='tight')
        plt.close(fig)
        print(f"Figure saved as {file_name} to {save_path}")
    else:
        plt.show()

# Function to plot histogram of a given distribution for a specific PDG ID
def plot_histogram(df, pdg_id, column_name, save_figure=False, file_name=None, density=False, bins=50):
    '''
    Input:
        "df" is the DataFrame containing the data
        "pdg_id" is the PDG ID of the particle to filter
        "column_name" is the name of the column to plot (e.g., 'y' for rapidity)
        "save_figure" is a boolean indicating whether to save the figure (default is False)
        "file_name" is the name of the file to save the figure as (if save_figure is True)
        "bins" is the number of bins for the histogram (default is 50)
    Output:
        Displays a histogram of the specified distribution for the given PDG ID and saves it if requested.
    '''
    # Filter the DataFrame for the specified PDG ID
    filtered_data = df[df[9] == pdg_id]  # Assuming PDG ID is in column 9
    data_to_plot = filtered_data[column_name]

    # Plot the histogram
    plt.figure(figsize=(10, 6))
    plt.hist(data_to_plot, density=density, bins=bins, alpha=0.7, color='blue', edgecolor='black')
    plt.title(f'Histogram of {column_name} for PDG ID {pdg_id}')
    plt.xlabel(column_name)
    y_axis_label = r'$\frac{dN}{d%s}$' % column_name
    plt.ylabel(y_axis_label)
    plt.grid(True)
    # Save the figure
    if save_figure:
        if file_name is None:
            file_name = f'histogram_{column_name}_pdg{pdg_id}.png'
        save_path = qol.get_save_path(FIGURE_DIR, file_name)
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()
        print(f"Figure saved as {file_name} to {save_path}")
    else:
        plt.show()

# Function to plot KDE of a given distribution for a specific PDG ID
def plot_distribution(df, pdg_id, column_name, save_figure=False, file_name=None, bins=50):
    '''
    Input:
        "df" is the DataFrame containing the data
        "pdg_id" is the PDG ID of the particle to filter
        "column_name" is the name of the column to plot (e.g., 'y' for rapidity)
        "save_figure" is a boolean indicating whether to save the figure (default is False)
        "file_name" is the name of the file to save the figure as (if save_figure is True)
        "bins" is the number of bins for the histogram (default is 50)
    Output:
        Displays a histogram of the specified distribution for the given PDG ID and saves it if requested.
    '''
    # Import necessary library
    from scipy.stats import gaussian_kde

    # Filter the DataFrame for the specified PDG ID
    filtered_data = df[df[9] == pdg_id]  # Assuming PDG ID is in column 9
    data_to_plot = filtered_data[column_name]

    fig, ax1 = plt.subplots(figsize=(10, 6))
    # Plot settings for histogram (left y-axis)
    color_hist = 'steelblue'
    counts, bins, patches = ax1.hist(data_to_plot, bins=bins, alpha=0.6, color=color_hist, label='Histogram')
    ax1.set_xlabel(column_name)
    ax1.set_ylabel('Counts', color=color_hist)
    ax1.tick_params(axis='y', labelcolor=color_hist)

    # Create a second y-axis for the KDE (right y-axis)
    ax2 = ax1.twinx()
    # Kernel Density Estimation using Gaussian kernels
    kde = gaussian_kde(data_to_plot)
    x_vals = np.linspace(data_to_plot.min(), data_to_plot.max(), 500)
    kde_vals = kde(x_vals)

    color_kde = 'darkorange'
    ax2.plot(x_vals, kde_vals, color=color_kde, label='KDE')
    ax2.set_ylabel('Normalised density (KDE)', color=color_kde)
    ax2.tick_params(axis='y', labelcolor=color_kde)

    # Ensure y=0 lines on both axes are at identical height:
    # set both bottoms to 0 and choose tops from the plotted data with a small margin
    top_counts = ax1.get_ylim()[1]
    top_kde = ax2.get_ylim()[1]

    margin = 1.05  # adjust if you want more/less headroom
    ax1.set_ylim(0, top_counts * margin)
    ax2.set_ylim(0, top_kde * margin)

    # Fine grid for plotting the KDE
    plt.title(f'Distribution of {column_name} for PDG ID {pdg_id} and KDE')
    plt.tight_layout()
    plt.show()

# End of functions

# Example usage
if __name__ == "__main__":
    # Example usage (this part can be removed or modified as needed)
    import pandas as pd

    # Create a sample DataFrame for demonstration consisting of PDG IDs and rapidity values for 10.000 particles
    data = {
        9: np.random.choice([2212, 111], size=10000),  # PDG IDs
        'y': np.random.normal(loc=0, scale=1, size=10000)  # Rapidity values
    }
    
    df = pd.DataFrame(data)

    # Plot histogram for protons (PDG ID 2212)
    plot_histogram(df, pdg_id=2212, column_name='y', save_figure=False, file_name='Test_figure.png', bins=50)
    #plot_distribution(df, pdg_id=2212, column_name='y', save_figure=False, file_name='Test_figure.png', bins=50)

# End of script
