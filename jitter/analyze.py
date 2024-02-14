import os
import shutil

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

DIR = os.path.dirname(os.path.abspath(__file__))

def plot_density_log_scale(data: list[int]):
    # Set the style of seaborn
    sns.set(style="whitegrid")

    # Create a density plot
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data, log_scale=True)

    plt.xlabel('Value (log scale)')
    plt.title('Density Plot on Log Scale')
    plt.show()

def count_s(filename):
    ns = 0
    with open(filename, "r") as fp:
        for line in fp:
            ns += int(line)
    return ns/1000000000

def load_file_to_int(filename):
    with open(filename, "r") as fp:
        return [int(x) for x in fp.readlines()]

def count_numbers(filename):
    with open(filename, "r") as fp:
        return len(fp.readlines())

# bin counts

# Decision:
# - Square-root choice: trivial
# - sturges Formula: easy and often used, but normally for normal distributed data...
# - rice rule: could overestimate the number of needed bins but many bins are good for tails
def calculate_bins_square_root(data):
    """Calculate the number of bins using the Square-root choice."""
    N = len(data)
    return int(np.sqrt(N))
def calculate_bins_sturges(data):
    """Calculate the number of bins using Sturges' formula."""
    N = len(data)
    return int(np.log2(N)) + 1
def calculate_bins_rice_rule(data):
    """Calculate the number of bins using Rice Rule."""
    N = len(data)
    return int(2 * (N ** (1/3)))

def plot_histogram_with_numpy(data, outpath, show_cnt = False, title = None, bins=10):
    # Compute the histogram
    counts, bin_edges = np.histogram(data, bins=bins)
    print(f"counts: {counts}")
    print(f"bin edges: {bin_edges}")

    # Calculate bin widths
    bin_widths = np.diff(bin_edges)

    # Plot the histogram
    bars = plt.bar(bin_edges[:-1], counts, width=bin_widths, edgecolor='black')
    plt.xlabel('Deltas')
    plt.ylabel('Frequency')
    if title is not None:
        plt.title(title)
    plt.yscale('log')

    if show_cnt:
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{count}', ha='center', va='bottom')
    
    plt.savefig(outpath)
    plt.clf()
    return counts, bin_edges

def find_txt_files(directory):
    txt_files = []
    # Walk through the directory recursively
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                txt_files.append(os.path.join(root, file))
    return txt_files


print("searching for files")
jitter_paths = find_txt_files("./jitter")
baseline_paths = find_txt_files("./jitter_baseline")

print("creating results structure")
if os.path.exists("./results"):
    shutil.rmtree("./results")
os.makedirs("./results")
os.makedirs("./results/jitter")
os.makedirs("./results/jitter_baseline")

for benchmarktype in ["jitter", "jitter_baseline"]:
    print(f"begin {benchmarktype} data")
    paths = find_txt_files(f"./{benchmarktype}")
    for path in paths:
        filename = os.path.splitext(os.path.basename(path))[0]
        print("------------------------")
        print(f"{benchmarktype}: {filename}")
        data = load_file_to_int(path)
        with open(f"./results/{benchmarktype}/{filename}.stats.txt", "w") as fp:
            s = f"seconds: {count_s(path)}"
            n = f"numbers: {count_numbers(path)}"
            p50 = f"p50: {np.percentile(data, 50)}"
            p90 = f"p90: {np.percentile(data, 90)}"
            p99 = f"p99: {np.percentile(data, 99)}"
            p99_9 = f"p99_9: {np.percentile(data, 99.9)}"
            print(s)
            fp.write(f"{s}\n")
            print(n)
            fp.write(f"{n}\n")
            print(p50)
            fp.write(f"{p50}\n")
            print(p90)
            fp.write(f"{p90}\n")
            print(p99)
            fp.write(f"{p99}\n")
            print(p99_9)
            fp.write(f"{p99_9}\n")
    
        print("plotting 10")
        plot_histogram_with_numpy(
            data, 
            f"./results/{benchmarktype}/{filename}_10.png",
            bins=10,
            show_cnt=True
        )
        print("plotting 25")
        plot_histogram_with_numpy(
            data, 
            f"./results/{benchmarktype}/{filename}_25.png",
            bins=25,
            show_cnt=True
        )
        print("plotting 50")
        plot_histogram_with_numpy(
            data, 
            f"./results/{benchmarktype}/{filename}_50.png",
            bins=50
        )
        print("plotting 100")
        plot_histogram_with_numpy(
            data, 
            f"./results/{benchmarktype}/{filename}_100.png",
            bins=100
        )
        print("plotting sqrt")
        plot_histogram_with_numpy(
            data, 
            f"./results/{benchmarktype}/{filename}_sqrt.png",
            bins=calculate_bins_square_root(data)
        )
        print("plotting sturges")
        plot_histogram_with_numpy(
            data, 
            f"./results/{benchmarktype}/{filename}_sturges.png",
            bins=calculate_bins_sturges(data)
        )
        print("plotting rice")
        plot_histogram_with_numpy(
            data, 
            f"./results/{benchmarktype}/{filename}_rice.png",
            bins=calculate_bins_rice_rule(data)
        )
    
        data_without_extremes = np.array(data)[np.array(data) <= np.percentile(data, 99.95)]
        print("cutoff plotting 10")
        plot_histogram_with_numpy(
            data_without_extremes, 
            f"./results/{benchmarktype}/{filename}_10_cutoff.png",
            bins=10,
            show_cnt=True
        )
        print("cutoff plotting 25")
        plot_histogram_with_numpy(
            data_without_extremes, 
            f"./results/{benchmarktype}/{filename}_25_cutoff.png",
            bins=25,
            show_cnt=True
        )
        print("cutoff plotting 50")
        plot_histogram_with_numpy(
            data_without_extremes, 
            f"./results/{benchmarktype}/{filename}_50_cutoff.png",
            bins=50
        )
        print("cutoff plotting 100")
        plot_histogram_with_numpy(
            data_without_extremes, 
            f"./results/{benchmarktype}/{filename}_100_cutoff.png",
            bins=100
        )
        print("cutoff plotting sqrt")
        plot_histogram_with_numpy(
            data_without_extremes, 
            f"./results/{benchmarktype}/{filename}_sqrt_cutoff.png",
            bins=calculate_bins_square_root(data_without_extremes)
        )
        print("cutoff plotting sturges")
        plot_histogram_with_numpy(
            data_without_extremes, 
            f"./results/{benchmarktype}/{filename}_sturges_cutoff.png",
            bins=calculate_bins_sturges(data_without_extremes)
        )
        print("cutoff plotting rice")
        plot_histogram_with_numpy(
            data_without_extremes, 
            f"./results/{benchmarktype}/{filename}_rice_cutoff.png",
            bins=calculate_bins_rice_rule(data_without_extremes)
        )
    print("----------------------------")
