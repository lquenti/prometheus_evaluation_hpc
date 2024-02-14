# Scalability Evaluation of Prometheus for HPC Monitoring

## [LINK TO THE REPORT](./report/main.pdf)

Don't forget to clone with `--recurse-submodules`!


This repo has all of the benchmarks as well as most of the data. Here is a description of all folders:


- `./datagen`: A way to preccompute realistic monitoring data based on tsbs. Unused in this report but very nice
- `./jitter`: The jitter benchmark and its analysis scripts
- `./node_exporter`: The end to end node exporter benchmarks / stress tests
- `./patched_node_exporter`: A git submodule showing to the patched benchmarker for benchmarking the metric gathering part
- `./report`: The latex report
- `./results_emmy`: All raw results for all benchmarks except the jitter one ran on the HPC cluster, with all its analysis jupyter scripts
- `all*.sh`: Scripts for running the benchmarks and deploying them onto the SLURM HPC scheduler
