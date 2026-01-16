#!/bin/bash
#SBATCH --job-name=test
#SBATCH --nodes=1
#SBATCH --output=./slurm_files/slurm_job_%j.out
#SBATCH --error=./slurm_files/slurm_job_%j.err
#SBATCH --partition=main
#SBATCH --time=0-04:00:00
#SBATCH --mail-user=sebastian.ostrowski@hotmail.com --mail-type=ALL

# Export working directory 
export SLURM_WORKING_DIR=$LH

# Set config file, decaymode file and container paths for SMASH
CONFIG_FILE=$SLURM_WORKING_DIR/smash_configs/config_dilepton_standard_oscar.yaml
DECAY_FILE=$SLURM_WORKING_DIR/smash_configs/decaymodes_dilepton_new.txt
CONTAINER=/lustre/hyihp/AG-Elfner/Containers/Production/smash-3.3-max.sif

# Set some run_id variables
RUN_ID=Dilepton_Output_Std_Nevents_5_OutInt_NaN

# Create output directory for SMASH if it doesn't exist
output_dir_smash=$SLURM_WORKING_DIR/smash_outputs

if [ ! -d $output_dir_smash ]; then
    mkdir -p $output_dir_smash
fi

# Output file run ID
echo "Running SMASH with config file: $CONFIG_FILE, decay_file: $DECAY_FILE and container: $CONTAINER"

# set specific config with '-i', command line option with '-c', and so on
singularity exec $CONTAINER smash -i $CONFIG_FILE -d $DECAY_FILE -o $output_dir_smash/$RUN_ID/ -n

# wait for the smash processes to finish
wait
echo "SMASH run completed. Outputs are in $output_dir_smash/$RUN_ID/"