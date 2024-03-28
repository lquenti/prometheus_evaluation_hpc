import os
import shutil

import matplotlib.pyplot as plt
import numpy as np

DIR = os.path.dirname(os.path.abspath(__file__))

def load_file_to_int(filename):
    with open(filename, "r") as fp:
        return [int(x) for x in fp.readlines()]

def find_txt_files(directory):
    txt_files = []
    # Walk through the directory recursively
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                txt_files.append(os.path.join(root, file))
    return txt_files

def create_save_cdf(data, filename):
    # Calculate the cumulative counts as a sum in numpy
    cumulative = np.cumsum(np.sort(data))

    # Normalize the cumulative sum
    cumulative = cumulative / np.max(cumulative)

    # Create plot using matplotlib
    plt.figure()
    plt.plot(np.sort(data), cumulative)
    plt.xlabel('Value')
    plt.ylabel('Cumulative Distribution')
    
    plt.savefig(filename)

def create_save_cdf_log(data, filename):
    # Calculate the cumulative counts as a sum in numpy
    cumulative = np.cumsum(np.sort(data))

    # Normalize the cumulative sum
    cumulative = cumulative / np.max(cumulative)

    # Create plot using matplotlib
    plt.figure()
    plt.plot(np.sort(data), cumulative)
    plt.xlabel('Value')
    plt.ylabel('Cumulative Distribution')

    plt.yscale('log')
    
def create_save_cdf_loglog(data, filename):
    # Calculate the cumulative counts as a sum in numpy
    cumulative = np.cumsum(np.sort(data))

    # Normalize the cumulative sum
    cumulative = cumulative / np.max(cumulative)

    # Create plot using matplotlib
    plt.figure()
    plt.plot(np.sort(data), cumulative)
    plt.xlabel('Value')
    plt.ylabel('Cumulative Distribution')

    plt.xscale('log')
    plt.yscale('log')
    
    plt.savefig(filename)

print("searching for files")
jitter_paths = find_txt_files("./jitter")
baseline_paths = find_txt_files("./jitter_baseline")

print("creating results structure")
if os.path.exists("./results_cdf"):
    shutil.rmtree("./results_cdf")
os.makedirs("./results_cdf")
os.makedirs("./results_cdf/jitter")
os.makedirs("./results_cdf/jitter_baseline")

for benchmarktype in ["jitter", "jitter_baseline"]:
    print(f"begin {benchmarktype} data")
    paths = find_txt_files(f"./{benchmarktype}")
    for path in paths:
        filename = os.path.splitext(os.path.basename(path))[0]
        print("------------------------")
        print(f"{benchmarktype}: {filename}")
        data = load_file_to_int(path)

        create_save_cdf(data, f"./results_cdf/{benchmarktype}/{filename}.png")
        create_save_cdf_log(data, f"./results_cdf/{benchmarktype}/{filename}_log.png")
        create_save_cdf_loglog(data, f"./results_cdf/{benchmarktype}/{filename}_log.png")
        
        print("plotting cdf")
    print("----------------------------")
