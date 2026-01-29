#!/bin/bash
# Generelles Setting
# Für Tests auf Partition "debug" gehen und Zeit auf ~10 Minuten oder weniger setzen
# Idealerweise nach Test-Runs über "seff <Job_ID>" oder für Arrays "sacct -j <job_ID> --format=JobID,Elapsed,AllocCPUS,CPUTime,TotalCPU,MaxRSS,ReqMem"  
# CPU-Effizienz = CPUTime / (Elapsed * AllocCPUS)
# Faustregel: Wenn TotalCPU ~ Elapsed -> single-core, TotalCPU ~ N x Elapsed -> N Kerne aktiv
# Auf virgo ist immer 2 CPUs der Standard, auch wenn weniger angefragt ist, SMASH kann kein Multithreading (Stand: 29.01.2026)

#SBATCH --job-name=scaled_test
#SBATCH --partition=main
#SBATCH --time=0-01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=256M

# Array: 0..4 (5 Runs). Parallelität kann man begrenzen z.B. max. 2 gleichzeitig über 0-4%2:
#SBATCH --array=0-99%20

# Separate Logfiles pro Array-Task:
#SBATCH --output=./slurm_files/slurm_%x_%A_%a.out
#SBATCH --error=./slurm_files/slurm_%x_%A_%a.err

# E-Mail-Benachrichtigung einstellen, falls gewünscht
#SBATCH --mail-user=sebastian.ostrowski@hotmail.com --mail-type=ALL 

# Festlegen, dass Jobabbruch bei irgendwelchen Problemen sofort erfolgt.
set -euo pipefail

# Export working directory
export SLURM_WORKING_DIR=${LH:-}
if [ -z "$SLURM_WORKING_DIR" ]; then
    SLURM_WORKING_DIR=${SLURM_SUBMIT_DIR:-$PWD}
fi

# Set config file, decaymode file and container paths for SMASH
CONFIG_FILE=$SLURM_WORKING_DIR/smash_configs/config_dilepton_standard_oscar.yaml
DECAY_FILE=$SLURM_WORKING_DIR/smash_configs/decaymodes_dilepton_new.txt
CONTAINER=/lustre/hyihp/AG-Elfner/Containers/Production/smash-3.3-max.sif

# Set basis run ID and output root
RUN_ID_BASE=Dilepton_Out_Std_Nevents_10000x100_OutInt_NaN
OUTPUT_ROOT=$SLURM_WORKING_DIR/smash_outputs

usage() {
    echo "Usage: $0 [-c config.yaml] [-d decay.txt] [-C container.sif] [-o output_root] [-r run_id_base] [-- smash_args]"
}

while getopts ":c:d:C:o:r:h" opt; do
    case "$opt" in
        c) CONFIG_FILE="$OPTARG" ;;
        d) DECAY_FILE="$OPTARG" ;;
        C) CONTAINER="$OPTARG" ;;
        o) OUTPUT_ROOT="$OPTARG" ;;
        r) RUN_ID_BASE="$OPTARG" ;;   # wichtig: das ist jetzt die BASE, nicht die finale ID
        h) usage; exit 0 ;;
        \?) echo "Unknown option: -$OPTARG"; usage; exit 2 ;;
        :)  echo "Option -$OPTARG requires an argument."; usage; exit 2 ;;
    esac
done
shift $((OPTIND - 1))
SMASH_EXTRA_ARGS=("$@")   # als Array, damit Quotes korrekt bleiben

# Eindeutige Run-ID pro Array-Task
# - SLURM_ARRAY_TASK_ID ist 0..N
# - %A ist die Array-Job-ID, sorgt zusätzlich für Eindeutigkeit über mehrere Submits hinweg
TASK_ID="${SLURM_ARRAY_TASK_ID:-0}"
ARRAY_JOB_ID="${SLURM_ARRAY_JOB_ID:-${SLURM_JOB_ID:-nojob}}"

RUN_ID="${RUN_ID_BASE}/run_${ARRAY_JOB_ID}_${TASK_ID}"

# Output directory
output_dir_smash="$OUTPUT_ROOT"
run_out_dir="$output_dir_smash/$RUN_ID"

mkdir -p "$run_out_dir"
mkdir -p "./slurm_files" 2>/dev/null || true

echo "Working dir:        $SLURM_WORKING_DIR"
echo "Config file:        $CONFIG_FILE"
echo "Decay file:         $DECAY_FILE"
echo "Container:          $CONTAINER"
echo "Output root:        $output_dir_smash"
echo "Run output dir:     $run_out_dir"
echo "Array task:         $TASK_ID (array job: $ARRAY_JOB_ID)"
echo "Extra SMASH args:   ${SMASH_EXTRA_ARGS[*]:-<none>}"

# Run SMASH
singularity exec "$CONTAINER" smash -i "$CONFIG_FILE" -d "$DECAY_FILE" -o "$run_out_dir/" -n "${SMASH_EXTRA_ARGS[@]}"

echo "SMASH run completed. Outputs are in $run_out_dir/"