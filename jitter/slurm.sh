#!/bin/bash
#SBATCH -t 12:00:00
#SBATCH -p standard96

module load python/3.9.16

SCRIPT_DIR=/scratch-emmy/usr/nimlarsq/jitter-analysis

cd ${SCRIPT_DIR}
source venv/bin/activate
python3 ${SCRIPT_DIR}/analyze.py
