#!/usr/bin/env bash
#SBATCH --job-name=cleanup
#SBATCH --nodes=1
#SBATCH --output=./slurm_files/slurm_job_%j.out
#SBATCH --error=./slurm_files/slurm_job_%j.err
#SBATCH --partition=debug
#SBATCH --time=0-00:30:00

# Export working directory 
export SLURM_WORKING_DIR=$LH

# -----------------------------
# Global control
# -----------------------------
# dry run flag: true -> only show, false -> execute command
DRY_RUN=true

# Switches to decide if script cleans slurm files (.out and .err) and/or outputs
DELETE_SLURM_FILES=true
DELETE_OUTPUT_DIR=true

# -----------------------------
# File deletion of SLURM files
# -----------------------------
if [[ "$DELETE_SLURM_FILES" == true ]]; then
    slurm_files_dir=$SLURM_WORKING_DIR/slurm_files
    if [[ -d "$slurm_files_dir" ]]; then
        if [[ "$DRY_RUN" == true ]]; then
            echo "[DRY-RUN] The following files would be deleted:"
            find "$slurm_files_dir" -maxdepth 1 -type f -name "slurm_job_*" -print
        else
            find "$slurm_files_dir" -maxdepth 1 -type f -name "slurm_job_*" -delete
        fi
    else
        echo "Ordner existiert nicht: $slurm_files_dir"
    fi
fi

# -----------------------------
# Control list of folders
# -----------------------------
# Set subfolder list to be deleted in output_dir_smash
FOLDERS_TO_DELETE=(
  "Dilepton_Output_Bin_Nevents_5_OutInt_NaN"
  "Dilepton_Output_Std_Nevents_5_OutInt_NaN"
  # "noch_ein_ordner"
)

if [[ "$DELETE_OUTPUT_DIR" == true ]]; then
    output_dir_smash=$SLURM_WORKING_DIR/smash_outputs
    for folder in "${FOLDERS_TO_DELETE[@]}"; do
        # Create target directory to be deleted
        TARGET="$output_dir_smash/$folder"
        # Check if target directory exists. If yes, delete folder. If no, print message to .out file.
        if [[ -d "$TARGET" ]]; then
            if [[ "$DRY_RUN" == true ]]; then
                echo "[DRY-RUN] Would delete: $TARGET"
            else
                echo "Deleting: $TARGET"
                rm -rf -- "$TARGET"
            fi
        else
            echo "Folder does not exist: $TARGET"
        fi
    done
fi
