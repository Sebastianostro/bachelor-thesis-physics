# Script that reads data from a SMASH output files.

# Import necessary libraries
from __future__ import annotations
import pandas as pd
import sys
from pathlib import Path
from dataclasses import dataclass
from io import StringIO

# Define constants, dictionaries etc. if needed (maybe moved to another file later if there are more dictionaries)
OSCAR_DATA_TYPES = {
    "t": "float32",
    "x": "float32",
    "y": "float32",
    "z": "float32",
    "mass": "float32",
    "p0": "float32",
    "px": "float32",
    "py": "float32",
    "pz": "float32",
    "pdg": "int32",
    "ID": "int32",
    "charge": "int8",
    "ncoll": "int16",
    "form_time": "float32",
    "xsecfac": "float32",
    "proc_id_origin": "int16",
    "proc_type_origin": "int16",
    "time_last_coll": "float32",
    "pdg_mother1": "int32",
    "pdg_mother2": "int32",
    "baryon_number": "int8",
    "strangeness": "int8",
    "weight": "float64",
    "partial": "float64",
}

# Define functions
## Function to get output file path
def get_path_to_output_file(file_name, folder_name, base_path='/home/sebastian/dev/python/bachelor-thesis-physics/05_Files_from_Virgo/')-> Path:
    # Define file information (paths, names)
    path_to_data = base_path  # Replace with your SMASH file path
    path_to_data_folder = folder_name # Example data subdirectory
    path_to_smash_file = Path(path_to_data) / path_to_data_folder / file_name  # full path to the SMASH file
    #print(f"Lese SMASH Datei: {path_to_smash_file}")

    # Check file exists before attempting to read
    if not path_to_smash_file.exists():
        print(f"Datei nicht gefunden: {path_to_smash_file}")
        sys.exit(1)
    return path_to_smash_file

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

## Define a dataclass to represent a run of SMASH output data
@dataclass
class TableRun:
    df: pd.DataFrame

    @staticmethod
    def from_blocked_file(path: str, comment_prefix: str = "#") -> "TableRun":
        # Datei lesen und in Blöcke aus Datenzeilen aufteilen
        blocks: list[list[str]] = []
        current: list[str] = []

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if not s:
                    continue
                if s.startswith(comment_prefix):
                    # Kommentarzeile trennt Blöcke (oder enthält Header)
                    if current:
                        blocks.append(current)
                        current = []
                    continue
                current.append(line)

        if current:
            blocks.append(current)

        # Jeden Block als Tabelle lesen
        dfs = []
        for i, lines in enumerate(blocks):
            text = "".join(lines)
            df_i = pd.read_csv(StringIO(text), sep=r"\s+", engine="python")
            df_i["block_id"] = i
            dfs.append(df_i)

        df = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
        return TableRun(df=df)

    def add_derived_columns(self) -> None:
        # Beispiel: neue Spalte aus vorhandenen
        # self.df["ratio"] = self.df["A"] / self.df["B"]
        pass

    def filter_valid(self) -> "TableRun":
        # Beispiel: nur physikalisch sinnvolle Zeilen
        # return TableRun(self.df[self.df["T"] >= 0].copy())
        return self

# Nutzung:
# run = TableRun.from_blocked_file("output.txt")
# run.add_derived_columns()
# df = run.df


# End of script