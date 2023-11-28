#!/usr/bin/env python3

import shutil
import os
import subprocess
import time

from dataclasses import dataclass

import psutil


NE_NUMBER_OF_PROCESSES = [1,2,4,8,16,32,64,128]

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
    try:
        shutil.rmtree(OUTPUT_PATH)
    except FileNotFoundError:
        pass

    os.makedirs(OUTPUT_PATH)

def run_benchmark_generic(benchmark_type: BenchmarkType, number_of_processes):
    # Create Output Folder
    folder = f"{OUTPUT_PATH}/{benchmark_type.name}"
    file = f"{folder}/output_{number_of_processes}.txt"
    os.makedirs(folder, exist_ok=True)
    result = subprocess.run(
        [benchmark_type.path_to_script],
        capture_output=True,
        text=True
    )
    with open(file, 'w') as fp:
        fp.write("stdout:\n")
        fp.write(result.stdout)
        fp.write("stderr:\n")
        fp.write(result.stderr)

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
    
        # TODO can they be together for caching reasons?
        print("BEGIN SEQUENTIAL")
        run_benchmark_sequential(n)
        print("BEGIN BEGIN PARALLEL GO")
        run_benchmark_parallel_go(n)
        print("BEGIN BEGIN PARALLEL WRK")
        run_benchmark_parallel_wrk(n)

        # We have to kill the subprocesses
        # https://stackoverflow.com/a/27034438/9958281
        rootp = psutil.Process(process.pid)
        for childp in rootp.children(recursive=True):
            childp.kill()
        rootp.kill()
        time.sleep(2)
        print(f"ENDING {n=}")

    

if __name__ == "__main__":
    main()
