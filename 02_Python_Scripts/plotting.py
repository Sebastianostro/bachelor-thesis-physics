# Script that provides functions to plot data.

# Import necessary libraries
import os
import matplotlib.pyplot as plt
import numpy as np

# Define directory to save figures
script_dir = os.path.dirname(os.path.abspath(__file__))
figure_dir = os.path.abspath(os.path.join(script_dir, '..', '03_Figures'))

# Functions
## Function to ensure directory exists
def _ensure_dir(path):
    os.makedirs(path, exist_ok=True)

## Function to get the save path for figures
def get_save_path(filename: str) -> str:
    """
    Return absolute path for saving an image inside the figures_dir.
    Ensures the directory exists.
    """
    _ensure_dir(figure_dir)
    return os.path.join(figure_dir, filename)

# Function to plot histogram of a given distribution for a specific PDG ID
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
    # Filter the DataFrame for the specified PDG ID
    filtered_data = df[df[9] == pdg_id]  # Assuming PDG ID is in column 9
    data_to_plot = filtered_data[column_name]

    # Plot the histogram
    plt.figure(figsize=(10, 6))
    plt.hist(data_to_plot, bins=bins, alpha=0.7, color='blue', edgecolor='black')
    plt.title(f'Histogram of {column_name} for PDG ID {pdg_id}')
    plt.xlabel(column_name)
    plt.ylabel('Counts')
    plt.grid(True)
    # Save the figure
    if save_figure:
        if file_name is None:
            file_name = f'histogram_{column_name}_pdg{pdg_id}.png'
        save_path = get_save_path(file_name)
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()
        print(f"Figure saved as {file_name} to {save_path}")
    else:
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

    # Plot distribution for protons (PDG ID 2212)
    plot_distribution(df, pdg_id=2212, column_name='y', save_figure=True, file_name='Test_figure.png', bins=50)

# End of script