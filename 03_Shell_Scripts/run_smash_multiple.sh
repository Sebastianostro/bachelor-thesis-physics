#!/bin/bash
#SBATCH --job-name=test_multiple
#SBATCH --output=./slurm_files/slurm_job_%j.out
#SBATCH --error=./slurm_files/slurm_job_%j.err
#SBATCH --partition=main
#SBATCH --time=0-04:00:00
#SBATCH --mail-user=sebastian.ostrowski@hotmail.com --mail-type=ALL

# Define number of total runs and naming
TOTAL_RUNS=10
RUN_PREFIX=Dilepton_Out_Std_Nevents_10000_OutInt_NaN

# Optional overrides
CONFIG_FILE=
DECAY_FILE=
CONTAINER=
OUTPUT_ROOT=

usage() {
    echo "Usage: $0 [-n total_runs] [-p run_prefix] [-c config.yaml] [-d decay.txt] [-C container.sif] [-o output_root]"
}

while getopts ":n:p:c:d:C:o:h" opt; do
    case "$opt" in
        n) TOTAL_RUNS=$OPTARG ;;
        p) RUN_PREFIX=$OPTARG ;;
        c) CONFIG_FILE=$OPTARG ;;
        d) DECAY_FILE=$OPTARG ;;
        C) CONTAINER=$OPTARG ;;
        o) OUTPUT_ROOT=$OPTARG ;;
        h)
            usage
            exit 0
            ;;
        \?)
            echo "Unknown option: -$OPTARG"
            usage
            exit 2
            ;;
        :)
            echo "Option -$OPTARG requires an argument."
            usage
            exit 2
            ;;
    esac
done

for i in $(seq 1 "$TOTAL_RUNS"); do
    RUN_ID="${RUN_PREFIX}/${i}"
    sbatch ./run_smash_basic.sh \
        ${CONFIG_FILE:+-c "$CONFIG_FILE"} \
        ${DECAY_FILE:+-d "$DECAY_FILE"} \
        ${CONTAINER:+-C "$CONTAINER"} \
        ${OUTPUT_ROOT:+-o "$OUTPUT_ROOT"} \
        -r "$RUN_ID"
done
