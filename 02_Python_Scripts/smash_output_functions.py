# Script that provides functions to calculate rapidity and invariant mass from a SMASH output file.

# Import necessary libraries
import numpy as np
import pdg
import matplotlib.pyplot as plt

# Define constants if needed (currently none)

# Define functions
## Function to calculate rapidity values for data in a DataFrame
def calculate_rapidity(df, col_no_energy=5, col_no_beam=8):
    '''
    Input: 
    "df" is the original Pandas DataFrame without rapidity information
    "col_no_energy" is the column number that contains the energy (aka p0, default value is "5" in SMASH output)
    "col_no_beam" is the column number that contains the momentum in beam direction (aka pz for z-beam, default value is "8" in SMASH output)
    Output: 
    Original DataFrame enriched by a column containing the rapidity values (named 'y')
    '''
    p0 = df[col_no_energy]  # Energy column
    pz = df[col_no_beam]  # pz column
    df['y'] = 0.5 * np.log((p0 + pz) / (p0 - pz))
    return df

## Function to calculate invariant mass for data in a DataFrame
def calculate_invariant_mass(df, col_no_energy=5, col_no_px=6, col_no_py=7, col_no_pz=8):
    '''
    Input: 
        "df" is the original Pandas DataFrame without invariant mass information
        "col_no_energy" is the column number that contains the energy (aka p0, default value is "5" in SMASH output)
        "col_no_px" is the column number that contains the momentum in x direction (default value is "6" in SMASH output)
        "col_no_py" is the column number that contains the momentum in y direction (default value is "7" in SMASH output)
        "col_no_pz" is the column number that contains the momentum in z direction (default value is "8" in SMASH output)
    Output: 
        Original DataFrame enriched by a column containing the invariant mass values (named 'm_inv')
    '''
    p0 = df[col_no_energy]
    px = df[col_no_px]
    py = df[col_no_py]
    pz = df[col_no_pz]
    df['m_inv'] = (p0**2 - (px**2 + py**2 + pz**2))
    return df

## Function to add PDG names to the DataFrame based on PDG IDs
def add_pdg_names(df, pdg_column=9):
    '''
    Input:
        "df" is the DataFrame without PDG names
        "pdg_column" is the column number that contains the PDG IDs (default value is "9" in SMASH output)
    Output:
        DataFrame enriched by a column containing the PDG names (named 'pdg_name')
    '''
    # Connect to PDG API
    api = pdg.connect()
    
    # Function to get PDG name from PDG ID
    def get_pdg_name(pdg_id):
        particle = api.get_particle_by_mcid(int(pdg_id))
        if particle is not None:
            return str(particle)
        else:
            return "Unknown particle"
    
    # Add PDG names to the DataFrame
    df['pdg_name'] = df[pdg_column].apply(get_pdg_name)
    return df

## Function to print basic statistics of the DataFrame
def print_basic_statistics(df):
    '''
    Input:
        "df" is the DataFrame containing SMASH data with columns for pdg names (named "pdg_name"), rapidity (named "y"), and invariant mass (named "m_inv")
    Output:
        Prints basic statistics such as total number of particles, number per type, mean rapidity, and mean invariant mass.
    '''
    unique_pdg_ids = df[9].unique()
    print(f"Unique PDG IDs in the data: {unique_pdg_ids}")

    # Number of total particles
    num_particles = len(df)
    # Number per unique particle type
    num_particles_per_type = df['pdg_name'].value_counts()

    print(f"Total number of particles: {num_particles}")
    print(f"Number of particles per type: {num_particles_per_type}")
    mean_rapidity = df['y'].groupby(df['pdg_name']).mean()
    mean_invariant_mass = df['m_inv'].groupby(df['pdg_name']).mean()
    print(f"Mean Rapidity: {mean_rapidity}")
    print(f"Mean Invariant Mass: {mean_invariant_mass}")

## Function to plot histograms of rapidity and invariant mass
def plot_histograms(df, normalized=False):
    '''
    Input:
        "df" is the DataFrame containing SMASH data with columns for rapidity (named "y") and invariant mass (named "m_inv")
        "normalized" is a boolean indicating whether to normalize the histograms (default is False)
    Output:
        Displays histograms of rapidity and invariant mass.
    '''
    # Plot histogram of rapidity
    if normalized:
        weights_rapidity = np.ones_like(df['y']) / len(df)
        weights_invariant_mass = np.ones_like(df['m_inv']) / len(df)
    else:
        weights_rapidity = None
        weights_invariant_mass = None
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.hist(df['y'], bins=50, weights=weights_rapidity, alpha=0.7, color='blue')
    plt.title('Rapidity Distribution')
    plt.xlabel('Rapidity (y)')
    plt.ylabel('Counts' if not normalized else 'Normalized Counts')
    plt.grid()
    # Plot histogram of invariant mass
    plt.subplot(1, 2, 2)
    plt.hist(df['m_inv'], bins=50, weights=weights_invariant_mass, alpha=0.7, color='green')
    plt.title('Invariant Mass Distribution')
    plt.xlabel('Invariant Mass (m_inv)')
    plt.ylabel('Counts' if not normalized else 'Normalized Counts')
    plt.grid()
    plt.tight_layout()
    plt.show()

# End of script