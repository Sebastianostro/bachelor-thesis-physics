#!/usr/bin/env bash
#SBATCH --job-name=BUILD-SMASH
#SBATCH --nodes=1
#SBATCH --cores=6
#SBATCH --output=slurm_build_smash_%j.out
#SBATCH --error=slurm_build_smash_%j.err
#SBATCH --partition=debug
#SBATCH --time=0-0:30:00
#SBATCH --mail-user=sebastian.ostrowski@hotmail.com --mail-type=FAIL,END
#SBATCH --mem=10G
user="$(whoami)"
smash_devel_path="/lustre/hyihp/${user}/smash-devel"
tmp_build_folder="/tmp/${user}/smash-build" 

if [[ -d "${tmp_build_folder}" ]]; then
  rm -r "${tmp_build_folder}"
fi

mkdir -p "${tmp_build_folder}" && cd "${tmp_build_folder}" || exit 1

export pythia_version="8316"
singularity exec "${hybrid_con}" cmake -DPythia_CONFIG_EXECUTABLE="${LH}/install_dependencies_smash/pythia${pythia_version}/bin/pythia8-config" "${smash_devel_path}" && \
singularity exec "${hybrid_con}" make -j6 || exit 1

cd -
build_folder="/lustre/hyihp/${user}/smash-devel/build"
if [[ -d "${build_folder}" ]]; then
  rm -r "${build_folder}"
fi
mv "${tmp_build_folder}" "${build_folder}"
