#!/bin/bash
#SBATCH --exclusive
#SBATCH -o run-%J
#SBATCH -p medium40
#SBATCH -t 24:00:00

cd $SLURM_SUBMIT_DIR

echo "from root"
echo $(pwd)

module load go/1.19.5
module load python/3.9.16
module load singularity/3.10.3

$SLURM_SUBMIT_DIR/all_part2_2.sh
