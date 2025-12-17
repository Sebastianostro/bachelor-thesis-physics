# Script that reads data from a SMASH output files.

# Import necessary libraries
import pandas as pd
import sys
from pathlib import Path

# Define constants if needed (currently none)

# Define functions
## Function to get output file path
def get_output_file(file_name, folder_name, base_path='/home/sebastian/dev/python/bachelor-thesis-physics/05_Files_from_Virgo/')-> Path:
    # Define file information (paths, names)
    path_to_file = base_path  # Replace with your SMASH file path
    path_to_data = folder_name # Example data subdirectory
    smash_file = Path(path_to_file) / path_to_data / file_name  # full path to the SMASH file
    print(f"Lese SMASH Datei: {smash_file}")

    # Check file exists before attempting to read
    if not smash_file.exists():
        print(f"Datei nicht gefunden: {smash_file}")
        sys.exit(1)
    return smash_file

## Function to read SMASH particle_list file in .oscar format
def read_smash_particle_file(file_path):
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
        return None

## Function to read SMASH dilepton file in .oscar format
def read_smash_dilepton_file(file_path):
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
        return data
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# End of script