#!/bin/bash

rm -rf ./full_pipeline_results
rm -rf ./tmp_node_mock
rm -rf ./tmp_prom
mkdir ./full_pipeline_results

api_mock_nodes=(10 50 100 500 1000 2500 5000 7500 10000)

for i in "${api_mock_nodes[@]}"; do
  ./venv/bin/python3 runner.py  1400 $((1400 + i + 1))
  mv ./tmp_node_mock ./full_pipeline_results/$i
  mv ./tmp_prom/vmstat.txt ./full_pipeline_results/$i/vmstat.txt
done


