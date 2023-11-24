#!/usr/bin/env python3

import shutil
import os
import subprocess
import time

import psutil


# BEGIN CONFIG
NE_NUMBER_OF_PROCESSES = [1,2,4,8,16,32,64,128]

NE_PATH = "./node_exporter.sh"
SEQ_PATH = "./sequential_benchmark.sh"
OUTPUT_PATH = "./results"
# END CONFIG

def prepare():
    # reset output folder
    try:
        shutil.rmtree(OUTPUT_PATH)
    except FileNotFoundError:
        pass

    os.makedirs(OUTPUT_PATH)

# TODO MAKE A MORE GENERIC VERSION OF ME
def run_benchmark_sequential(number_of_processes):
    # Create output folder
    folder = f"{OUTPUT_PATH}/sequential"
    file = f"{folder}/output_{number_of_processes}.txt"
    os.makedirs(folder, exist_ok=True)
    result = subprocess.run(
        [SEQ_PATH],
        capture_output=True,
        text=True,
        shell=True
    )
    with open(file, 'w') as fp:
        fp.write("stdout:\n")
        fp.write(result.stdout)
        fp.write("stderr:\n")
        fp.write(result.stderr)

def main():
    prepare()

    for n in NE_NUMBER_OF_PROCESSES:
        print(f"STARTING {n=}")

        os.environ['NUMBER_OF_PROCESSES'] = str(n)
        process = subprocess.Popen([NE_PATH])
        time.sleep(2)

    
        run_benchmark_sequential(n)

        # We have to kill the subprocesses
        # https://stackoverflow.com/a/27034438/9958281
        rootp = psutil.Process(process.pid)
        for childp in rootp.children(recursive=True):
            childp.kill()
        rootp.kill()
        time.sleep(2)

    

if __name__ == "__main__":
    main()
