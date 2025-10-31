import smash_read

# Define file information (paths, names)
path_to_file = '/home/ostrowski/smash/build/data/'  # Replace with your SMASH file path
path_to_data = '1/' # Example data subdirectory
file_name = 'particle_lists.oscar'  # Example SMASH output file name
smash_file = path_to_file + path_to_data + file_name  # full path to the SMASH file

# Main script execution
# Read the SMASH file and store the data in a DataFrame
smash_data = smash_read.read_smash_file(smash_file)
# Check if data was read successfully
if smash_data is not None:
    # Display the first few rows of the DataFrame
    print(smash_data.head())
    smash_data_enriched = smash_read.calculate_rapidity(smash_data)
    smash_data_enriched = smash_read.calculate_invariant_mass(smash_data)
    print(smash_data_enriched.head())
    print(smash_data_enriched[smash_data_enriched['m_inv']<0].head())  # Display first few rows with valid invariant mass
else:
    print("Failed to read SMASH data.")
