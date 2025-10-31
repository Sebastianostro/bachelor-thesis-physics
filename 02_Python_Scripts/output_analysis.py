import smash_read
import pdg

api = pdg.connect()

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
    #print(smash_data.head())
    smash_data_enriched = smash_read.calculate_rapidity(smash_data)
    smash_data_enriched = smash_read.calculate_invariant_mass(smash_data)
    #print(smash_data_enriched.head())
else:
    print("Failed to read SMASH data.")

unique_pdg_ids = smash_data[9].unique()
print(f"Unique PDG IDs in the data: {unique_pdg_ids}")

for pdg_id in unique_pdg_ids:
    particle = api.get_particle_by_mcid(int(pdg_id))
    if particle is not None:
        print(f"PDG ID: {pdg_id}, Name: {particle}")
    else:
        print(f"PDG ID: {pdg_id}, Name: Unknown particle")
