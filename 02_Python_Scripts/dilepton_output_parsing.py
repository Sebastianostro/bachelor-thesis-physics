# -----------------------------
# IMPORTS
# -----------------------------
## Standard libraries
from __future__ import annotations
import sys
from dataclasses import dataclass
from io import StringIO
import re
from typing import Optional, List, Dict, Any
import numpy as np
import pandas as pd

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
## Define a dataclass to represent a run of SMASH output data
@dataclass
class DileptonRun:
    df: pd.DataFrame

    @staticmethod
    def from_blocked_file(path: str, comment_prefix: str = "#") -> "DileptonRun":
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
        return DileptonRun(df=df)

    def add_derived_columns(self) -> None:
        # Beispiel: neue Spalte aus vorhandenen
        # self.df["ratio"] = self.df["A"] / self.df["B"]
        pass

_INTERACTION_RE = re.compile(
    r"#\s*interaction.*?\bweight\s+(?P<weight>[-+0-9.eE]+).*?\bpartial\s+(?P<partial>[-+0-9.eE]+).*?\btype\s+(?P<type>[-+0-9]+)"
)

_EVENT_RE = re.compile(r"#\s*event\s+(?P<event>\d+)\s+ensemble\s+(?P<ensemble>\d+)")


@dataclass
class BlockContext:
    weight: Optional[float] = None
    partial: Optional[float] = None
    itype: Optional[int] = None
    event: Optional[int] = None
    ensemble: Optional[int] = None


def read_smash_table_with_blocks(path: str) -> pd.DataFrame:
    """
    Liest SMASH/OSCAR-ähnliche Tabellen mit Kommentarzeilen und blockweisen Metadaten.
    Hängt Block-Metadaten (weight/partial/type + optional event/ensemble) an jede Datenzeile.
    """
    colnames: Optional[List[str]] = None
    rows: List[List[Any]] = []

    ctx = BlockContext()

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Header: Spaltennamen
            if line.startswith("#!"):
                # Beispiel: "#!OSCAR... Dileptons t x y z mass ..."
                parts = line.split()
                # Spaltennamen beginnen hier typischerweise nach dem "Dileptons"-Token
                # Falls das bei dir anders ist, kann man es anpassen.
                try:
                    idx = parts.index("Dileptons")
                    colnames = parts[idx + 1 :]
                except ValueError:
                    # Fallback: alles nach dem ersten Token
                    colnames = parts[1:]
                continue

            # Kommentarzeilen: Block-/Event-Kontext extrahieren
            if line.startswith("#"):
                m_int = _INTERACTION_RE.search(line)
                if m_int:
                    ctx.weight = float(m_int.group("weight"))
                    ctx.partial = float(m_int.group("partial"))
                    ctx.itype = int(m_int.group("type"))
                    continue

                m_evt = _EVENT_RE.search(line)
                if m_evt:
                    ctx.event = int(m_evt.group("event"))
                    ctx.ensemble = int(m_evt.group("ensemble"))
                    continue

                # Sonstige Kommentarzeilen ignorieren
                continue

            # Datenzeile: schnell parsen
            # np.fromstring ist deutlich schneller als split+map(float)
            data = np.fromstring(line, sep=" ")
            if data.size == 0:
                continue

            if colnames is None:
                raise ValueError("Keine Spaltennamen gefunden (fehlende '#!' Headerzeile?).")

            if data.size != len(colnames):
                raise ValueError(
                    f"Spaltenanzahl passt nicht: got {data.size}, expected {len(colnames)}\n"
                    f"Line: {line}"
                )

            # Daten + Block-Metadaten
            rows.append(
                data.tolist()
                + [ctx.weight, ctx.partial, ctx.itype, ctx.event, ctx.ensemble]
            )

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
    path_to_file = "example_smash_output.txt"
    run = DileptonRun.from_blocked_file(path_to_file)
    run.add_derived_columns()
    df = run.df
    print(df.head())
# End of script