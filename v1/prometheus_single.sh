#!/bin/bash
#SBATCH --exclusive
#SBATCH -o run-%J
#SBATCH -p medium40
#SBATCH -t 24:00:00

module load python/3.9.16
module load singularity/3.10.3

echo "part 1"
echo $(pwd)
cd $SLURM_SUBMIT_DIR/prometheus_single
./full_benchmark_single.sh
