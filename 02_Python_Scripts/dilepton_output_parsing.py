# -----------------------------
# IMPORTS
# -----------------------------
## Standard libraries
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Optional, List, Dict, Any
import numpy as np
import pandas as pd

import io_smash

# -----------------------------
# CONSTANTS AND SETTINGS
# -----------------------------
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

# -----------------------------
# FUNCTIONS AND CLASSES
# -----------------------------
## Regular expressions for parsing block metadata
_INTERACTION_RE = re.compile(
    r"#\s*interaction.*?\bweight\s+(?P<weight>[-+0-9.eE]+).*?\bpartial\s+(?P<partial>[-+0-9.eE]+).*?\btype\s+(?P<type>[-+0-9]+)"
)

_EVENT_RE = re.compile(r"#\s*event\s+(?P<event>\d+)\s+ensemble\s+(?P<ensemble>\d+)")

## Dataclass to hold block context information
@dataclass
class BlockContext:
    weight: Optional[float] = None
    partial: Optional[float] = None
    itype: Optional[int] = None
    event: Optional[int] = None
    ensemble: Optional[int] = None

## Function to read SMASH/OSCAR-like tables with block metadata
def read_smash_table_with_blocks(path: Path) -> pd.DataFrame:
    """
    Liest SMASH/OSCAR-ähnliche Tabellen mit Kommentarzeilen und blockweisen Metadaten.
    Hängt Block-Metadaten (weight/partial/type + optional event/ensemble) an jede Datenzeile.
    """
    # column names and data rows
    colnames: List[str] = []
    rows: List[List[Any]] = []
    # initial block context
    ctx = BlockContext()
    # variables to track event state
    had_data_in_event = False
    seen_event = False

    # helper function to append empty event row if no dileptons were recorded in an event
    def _append_empty_event() -> None:
        if not colnames:
            raise ValueError("Keine Spaltennamen gefunden (fehlende '#!' Headerzeile?).")
        rows.append(
            [0.0] * len(colnames)
            + [0.0, 0.0, 0, ctx.event, 0] # default values for empty event
        )

    # read the file line by line
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            # clean line and skip empty lines
            line = line.strip()
            if not line:
                continue

            # Header: column names
            if line.startswith("#!"):
                # Example: "#!OSCAR... Dileptons t x y z mass ..."
                parts = line.split()
                # look for "Dileptons" token to find column names
                try:
                    idx = parts.index("Dileptons")
                    colnames = parts[idx + 1 :]
                except ValueError:
                    # Fallback: alles nach dem ersten Token
                    colnames = parts[1:]
                continue

            # Extract block metadata from comment lines
            if line.startswith("#"):
                # interaction line parsing. If line matches the pattern defined in _INTERACTION_RE,
                # it is treated as 'true' although not a real bool. if line does not match, m_int contains 'None'
                m_int = _INTERACTION_RE.search(line)
                if m_int:
                    ctx.weight = float(m_int.group("weight"))
                    ctx.partial = float(m_int.group("partial"))
                    ctx.itype = int(m_int.group("type"))
                    continue
                # events line parsing.
                m_evt = _EVENT_RE.search(line)
                if m_evt:
                    # If we have seen an event but had no data lines, append an empty event row
                    if seen_event and not had_data_in_event:
                        _append_empty_event()
                    # Update context with new event info
                    ctx.event = int(m_evt.group("event"))
                    ctx.ensemble = int(m_evt.group("ensemble"))
                    # Mark that we have seen an event
                    seen_event = True
                    had_data_in_event = False
                    continue

                # Ignore other comment lines
                continue

            # Datenzeile: schnell parsen
            # np.fromstring ist deutlich schneller als split+map(float)
            data = np.fromstring(line, sep=" ")
            if data.size == 0:
                continue

            if colnames is None:
                raise ValueError("No column names found (maybe missing '#!' in header line?).")

            if data.size != len(colnames):
                raise ValueError(
                    f"Number of columns do not fit: got {data.size}, expected {len(colnames)}\n"
                    f"Line: {line}"
                )

            # Append data row with current block context
            rows.append(
                data.tolist()
                + [ctx.weight, ctx.partial, ctx.itype, ctx.event, ctx.ensemble]
            )
            had_data_in_event = True
    # After finishing reading, check if the last event had no data (because at least one event line was seen)
    if seen_event and not had_data_in_event:
        _append_empty_event()

    df = pd.DataFrame(
        rows,
        columns=colnames + ["block_weight", "block_partial", "block_type", "event", "ensemble"],
    )
    return df

# -----------------------------
# MAIN SCRIPT EXECUTION
# -----------------------------
if __name__ == "__main__":
    # Beispielhafte Nutzung des Dilepton-Dataclass
    data_dir_name = 'Dilepton_Nevents_5_OutInt_NaN/' # Example data subdirectory
    file_name = 'Dileptons.oscar'  # Example SMASH output file name
    # Construct full path to the SMASH file
    path_to_smash_data = io_smash.get_path_to_output_file(file_name, data_dir_name)

    df = read_smash_table_with_blocks(path_to_smash_data)
    print(df.head())
# End of script