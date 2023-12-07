#!/usr/bin/env python3

import os
import shutil
import subprocess
import time

import psutil

PATH_TO_UVICORN = "./venv/bin/uvicorn"
PATH_TO_PROMETHEUS_SINGULARITY = "./container/prometheus.sif"
PORT_RANGE = (14000, 14101)
TIME_TO_START = 2*(PORT_RANGE[1] - PORT_RANGE[0])
SCRAPE_INTERVAL = "10s"
EVALUATION_INTERVAL = "10s"
BENCHMARK_TIME_SECS = 60*5
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

################################################################

def create_prometheus_config():
    targets = [f"localhost:{port}" for port in range(*PORT_RANGE)]
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

def start_mock_exporter() -> list[int]:
    pids = [spawn(port) for port in range(*PORT_RANGE)]
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
    cfg = create_prometheus_config()
    prepare_tmp_folder(cfg)
    pids = start_mock_exporter()
    do_benchmark()
    terminate_node_exporter(pids)


if __name__ == "__main__":
    main()
