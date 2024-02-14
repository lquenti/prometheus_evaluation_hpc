#!/usr/bin/env python3

import shutil
import os
import subprocess
import sys
import time

from dataclasses import dataclass

import psutil


NE_NUMBER_OF_PROCESSES = [1,2,4,8,16,32]

NE_PATH = "./node_exporter.sh"
OUTPUT_PATH = "./results"

@dataclass
class BenchmarkType():
    name: str
    path_to_script: str

BENCHMARKTYPE_SEQUENTIAL = BenchmarkType(
    name="sequential",
    path_to_script="./sequential_benchmark.sh"
)
BENCHMARKTYPE_PARALLEL_GO = BenchmarkType(
    name="parallel_go",
    path_to_script="./parallel_benchmark_go.sh"
)
BENCHMARKTYPE_PARALLEL_WRK = BenchmarkType(
    name="parallel_wrk",
    path_to_script="./parallel_benchmark_wrk.sh"
)

def prepare():
    # reset output folder
    # (only if you are the only process, i.e. you do all benchmarks)
    if len(sys.argv) == 1:
        try:
            shutil.rmtree(OUTPUT_PATH)
        except FileNotFoundError:
            pass

    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

def kill(pid):
    root = psutil.Process(pid)
    for child in root.children(recursive=True):
        child.kill()
    root.kill()

def run_benchmark_generic(benchmark_type: BenchmarkType, number_of_processes):
    # Create Output Folder
    folder = f"{OUTPUT_PATH}/{benchmark_type.name}"
    file = f"{folder}/output_{number_of_processes}.txt"
    os.makedirs(folder, exist_ok=True)

    # load up vmstat
    with open(f"{folder}/vmstat_{number_of_processes}.txt", "w") as fp:
        vmstat = subprocess.Popen(["vmstat", "1"], stdout=fp)

    with open(file, 'w') as fp:
    	result = subprocess.run(
    	    [benchmark_type.path_to_script],
    	    text=True,
    	    stdout=fp,
    	    stderr=subprocess.STDOUT # merge
    	)

    kill(vmstat.pid)


def run_benchmark_sequential(number_of_processes):
    run_benchmark_generic(BENCHMARKTYPE_SEQUENTIAL, number_of_processes)
def run_benchmark_parallel_go(number_of_processes):
    run_benchmark_generic(BENCHMARKTYPE_PARALLEL_GO, number_of_processes)
def run_benchmark_parallel_wrk(number_of_processes):
    run_benchmark_generic(BENCHMARKTYPE_PARALLEL_WRK, number_of_processes)

def main():
    prepare()

    for n in NE_NUMBER_OF_PROCESSES:
        print(f"STARTING {n=}")

        os.environ['NUMBER_OF_PROCESSES'] = str(n)
        process = subprocess.Popen([NE_PATH])
        time.sleep(2)
    
        # If no arguments are given, run all
        if len(sys.argv) == 1:
            print("BEGIN SEQUENTIAL")
            run_benchmark_sequential(n)
            print("BEGIN BEGIN PARALLEL GO")
            run_benchmark_parallel_go(n)
            print("BEGIN BEGIN PARALLEL WRK")
            run_benchmark_parallel_wrk(n)
        elif sys.argv[1] == "only-seq":
            print("BEGIN SEQUENTIAL")
            run_benchmark_sequential(n)
        elif sys.argv[1] == "only-go":
            print("BEGIN BEGIN PARALLEL GO")
            run_benchmark_parallel_go(n)
        elif sys.argv[1] == "only-wrk":
            print("BEGIN BEGIN PARALLEL WRK")
            run_benchmark_parallel_wrk(n)
        else:
            print(f"Illegal arguments! {sys.argv}")
            return

        # We have to kill the subprocesses
        # https://stackoverflow.com/a/27034438/9958281
        kill(process.pid)
        time.sleep(2)
        print(f"ENDING {n=}")

    

if __name__ == "__main__":
    main()
