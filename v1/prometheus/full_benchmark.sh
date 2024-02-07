#!/bin/bash

rm -rf ./full_pipeline_results
rm -rf ./tmp_node_mock
rm -rf ./tmp_prom
mkdir ./full_pipeline_results

api_mock_nodes=(1500 1750 2000 2250 2500 3000)
#api_mock_nodes=(10)

for i in "${api_mock_nodes[@]}"; do
  mpirun -n 2 -npernode 1 ./venv/bin/python3 runner.py  1400 $((1400 + i + 1))
  echo "mpi done"
  mv ./tmp_node_mock ./full_pipeline_results/$i
  mv ./tmp_prom/vmstat.txt ./full_pipeline_results/$i/vmstat.txt
done


