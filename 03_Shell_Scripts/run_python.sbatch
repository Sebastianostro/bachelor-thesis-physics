#!/bin/bash
#SBATCH --job-name=smash_analyze
#SBATCH --partition=main
#SBATCH --time=0-01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G

#SBATCH --output=./slurm_files/slurm_%x_%j.out
#SBATCH --error=./slurm_files/slurm_%x_%j.err

set -euo pipefail
export LC_ALL=C

# Pfade anpassen
WORKDIR="${SLURM_SUBMIT_DIR:-$PWD}"
CONTAINER="$WORKDIR/../python_container/python312.sif"

cd "$WORKDIR"

apptainer exec --bind "$WORKDIR:/work" "$CONTAINER" bash -lc '
  set -euo pipefail
  cd /work
  source .venv/bin/activate
  python3 ./02_Python_Scripts/output_analysis.py
'
