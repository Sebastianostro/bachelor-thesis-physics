# Script that parses the smash data.

# Import necessary libraries
from __future__ import annotations
import pandas as pd
import sys
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