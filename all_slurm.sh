#!/bin/bash
#SBATCH -p medium
#SBATCH -t 24:00:00
#SBATCH -o run-%J
#SBATCH -p medium40

cd $SLURM_SUBMIT_DIR

echo "from root"
echo $(pwd)

module load python/3.9.0
module load singularity

$SLURM_SUBMIT_DIR/all.sh
