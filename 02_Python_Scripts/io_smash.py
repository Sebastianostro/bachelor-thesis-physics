# Imports
import sys
from pathlib import Path
import pandas as pd

# Constants
BASE_PATH_TO_DATA = '/home/sebastian/dev/python/bachelor-thesis-physics/05_Files_from_Virgo/'

# Define functions
## Function to get output file path
def get_path_to_output_file(file_name, folder_name, base_path=BASE_PATH_TO_DATA)-> Path:
    # Define file information (paths, names)
    path_to_data = base_path  # Your SMASH data path (top level)
    path_to_data_folder = folder_name # Data subdirectory (subfolder for specific simulations)
    path_to_smash_file = Path(path_to_data) / path_to_data_folder / file_name  # full path to the SMASH file

    # Check file exists before attempting to read
    if not path_to_smash_file.exists():
        print(f"Datei nicht gefunden: {path_to_smash_file}")
        sys.exit(1)
    return path_to_smash_file

## Function to read SMASH dilepton file in .oscar format
def read_smash_dilepton_file(file_path)-> pd.DataFrame:
    '''
    This function reads a SMASH Dileptons.oscar output file and returns its contents as a pandas DataFrame.
    It assumes the file is whitespace-delimited and may contain comment lines starting with '#'.
    The file structure is expected to be tabular with the following columns and units:
    t  x  y  z  mass p0  px  py  pz  pdg  ID   charge ncoll form_time xsecfac proc_id_origin proc_type_origin time_last_coll pdg_mother1 pdg_mother2 baryon_number strangeness
    fm fm fm fm GeV  GeV GeV GeV GeV none none e      none  fm        none    none           none             fm             none        none        none          none
    pdg ID corresponds to Particle Data Group identification numbers, see https://pdg.lbl.gov/2020/reviews/rpp2020-rev-monte-carlo-numbering.pdf for reference.
    
    Input: 
        file_path (str) - path to the Dileptons.oscar output file
    Output: 
        pandas DataFrame containing the dilepton data
    '''
    try:
        # Read the SMASH file using pandas
        data = pd.read_csv(file_path, sep='\\s+', comment='#', header=None)
        if data.empty:
            print("WARNING: The Dileptons.oscar file is empty. An empty DataFrame will be returned!")
            return pd.DataFrame()  # Return an empty DataFrame
        else:
            return data
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

## Function to read SMASH particle_list file in .oscar format
def read_smash_particle_file(file_path)-> pd.DataFrame:
    '''
    This function reads a SMASH particle_lists.oscar output file and returns its contents as a pandas DataFrame.
    It assumes the file is whitespace-delimited and may contain comment lines starting with '#'.
    The file structure is expected to be tabular with the following columns: t x y z mass p0 px py pz pdg ID charge
    Units per column: fm fm fm fm GeV GeV GeV GeV GeV none none e
    pdg ID corresponds to Particle Data Group identification numbers, see https://pdg.lbl.gov/2020/reviews/rpp2020-rev-monte-carlo-numbering.pdf for reference.
    
    Input: 
        file_path (str) - path to the SMASH output file
    Output: 
        pandas DataFrame containing the SMASH data
    '''
    try:
        # Read the SMASH file using pandas
        data = pd.read_csv(file_path, sep='\\s+', comment='#', header=None)
        return data
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Test script functionality if run as main module
    # Example usage
    data_dir_name = 'Dilepton_Nevents_5_OutInt_NaN/' # Example data subdirectory
    file_name = 'Dileptons.oscar'  # Example SMASH output file name
    # Construct full path to the SMASH file
    path_to_smash_data = get_path_to_output_file(file_name, data_dir_name)
    smash_data = read_smash_dilepton_file(path_to_smash_data)
    print(smash_data.head())