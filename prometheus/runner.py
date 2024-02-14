#!/usr/bin/env python3

import os
import shutil
import socket
import subprocess
import sys
import time

import psutil

from mpi4py import MPI

COMM = MPI.COMM_WORLD

if len(sys.argv) != 3 or not (sys.argv[1].isdigit() and sys.argv[2].isdigit()):
    print("USAGE: python3 runner.py MIN_PORT MAX_PORT_EXCLUSIVE # (for mock apis, i.e.)")
    print("i.e. for 100 machines: python3 runner.py 14100 14201")
    sys.exit(1)
PORT_RANGE = (int(sys.argv[1]), int(sys.argv[2]))

BENCHMARK_TIME_SECS = 60*10
PATH_TO_UVICORN = "./venv/bin/uvicorn"
PATH_TO_PROMETHEUS_SINGULARITY = "./container/prometheus.sif"
TIME_TO_START = 2*(PORT_RANGE[1] - PORT_RANGE[0])
SCRAPE_INTERVAL = "10s"
EVALUATION_INTERVAL = "10s"
TMP_DIR = "./tmp_prom"
TMP_CONF = f"{TMP_DIR}/prometheus.yml"

# Helper

def spawn(port):
    process = subprocess.Popen([
        PATH_TO_UVICORN,
        "api:app",
        "--host",
        "0.0.0.0",
        "--port",
        str(port)
    ])
    return process.pid

def kill(pid):
    root = psutil.Process(pid)
    for child in root.children(recursive=True):
        child.kill()
    root.kill()

def terminate(pid):
    root = psutil.Process(pid)
    for child in root.children(recursive=True):
        child.terminate()
    root.terminate()

# MPI Helper
def mpi_allgather_hostnames():
    rank = COMM.Get_rank()
    hostname = socket.gethostname()
    data = (rank, hostname)
    all_data = COMM.allgather(data)
    all_data.sort(key=lambda x: x[0])
    return [hostname for (_, hostname) in all_data]

def is_root():
    return COMM.Get_rank() == 0

################################################################

def calculate_port_ranges(hostnames):
    # given PORT_RANGE=(1000,2001)
    # hostname1 = (1000, 1250)
    # hostname2 = (1250, 1500)
    # hostname3 = (1500, 1750)
    # hostname4 = (1750, 2001) (take the rest)
    n = len(hostnames)
    delta = PORT_RANGE[1] - PORT_RANGE[0]
    res = []
    for i in range(len(hostnames)):
        res.append(
            (PORT_RANGE[0] + (delta//n)*i, PORT_RANGE[0]+(delta//n)*(i+1))
        )

    # take the rest
    res[-1] = (res[-1][0], PORT_RANGE[1])
    return res

def create_prometheus_config(hostnames, port_ranges):
    zipped = [*zip(hostnames, port_ranges)]
    targets = []
    for hostname, port_range in zipped:
        targets.extend([f"{hostname}:{port}" for port in range(*port_range)])
    cfg = f"""
global:
  scrape_interval:     {SCRAPE_INTERVAL}
  evaluation_interval: {EVALUATION_INTERVAL}

rule_files:
  # - "first.rules"
  # - "second.rules"

scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets: {targets}
"""
    return cfg

def prepare_tmp_folder(cfg):
    # Delete if exist and recreate
    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR)
    os.mkdir(TMP_DIR)

    # Write the config file in there
    with open(TMP_CONF, "w") as fp:
        fp.write(cfg)

def start_mock_exporter(port_range) -> list[int]:
    print(f"Spawning port range {port_range} on rank {COMM.Get_rank()}...")
    pids = [spawn(port) for port in range(*port_range)]
    time.sleep(TIME_TO_START)
    return pids

def do_benchmark():
    with open(f"{TMP_DIR}/vmstat.txt", "w") as fp:
        vmstat = subprocess.Popen(["vmstat", "1"], stdout=fp)

    process = subprocess.Popen([
        "singularity",
        "run",
        "--bind",
        f"{TMP_DIR}:/tsdb/prometheus-2.45.1.linux-amd64/data/",
        "--bind",
        f"{TMP_CONF}:/tsdb/prometheus-2.45.1.linux-amd64/prometheus.yml",
        PATH_TO_PROMETHEUS_SINGULARITY
    ])
    # Lets take 10 secs as warmup / init
    time.sleep(10)
    # actual running time
    time.sleep(BENCHMARK_TIME_SECS)
    kill(process.pid)
    kill(vmstat.pid)

def terminate_node_exporter(pids):
    # We can't kill bc we need to save results
    for pid in pids:
        terminate(pid)

def main():
    hostnames = mpi_allgather_hostnames()
    port_ranges = calculate_port_ranges(hostnames)
    if is_root():
        cfg = create_prometheus_config(hostnames, port_ranges)
        prepare_tmp_folder(cfg)
    COMM.Barrier()
    pids = start_mock_exporter(port_ranges[COMM.Get_rank()])
    COMM.Barrier()
    if is_root():
        do_benchmark()
    COMM.Barrier()
    terminate_node_exporter(pids)


if __name__ == "__main__":
    main()
