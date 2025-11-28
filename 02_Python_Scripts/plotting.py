# Script that provides functions to plot data.

# Import necessary libraries
import os
import matplotlib.pyplot as plt
import numpy as np


# Determine script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Function to plot histogram of a given distribution for a specific PDG ID
def plot_distribution(df, pdg_id, column_name, bins=50):
    '''
    Input:
        "df" is the DataFrame containing the data
        "pdg_id" is the PDG ID of the particle to filter
        "column_name" is the name of the column to plot (e.g., 'y' for rapidity)
        "bins" is the number of bins for the histogram (default is 50)
    Output:
        Displays a histogram of the specified distribution for the given PDG ID
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
    plt.show()

# Example usage
if __name__ == "__main__":
    # Example usage (this part can be removed or modified as needed)
    import pandas as pd

    # Create a sample DataFrame for demonstration consisting of PDG IDs and rapidity values for 10.000 particles
    data = {
        9: np.random.choice([2212, 111], size=10000),  # PDG IDs
        'y': np.random.normal(loc=0, scale=2, size=10000)  # Rapidity values
    }
    
    df = pd.DataFrame(data)

    # Plot distribution for protons (PDG ID 2212)
    plot_distribution(df, pdg_id=2212, column_name='y', bins=50)
    print(script_dir)

# End of script