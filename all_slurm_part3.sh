#!/bin/bash
#SBATCH --exclusive
#SBATCH -o run-%J
#SBATCH -p medium40


cd $SLURM_SUBMIT_DIR

echo "from root"
echo $(pwd)

module load python/3.9.16
module load singularity/3.10.3

$SLURM_SUBMIT_DIR/all_part3.sh
