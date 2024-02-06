import json
import re
import os

# - [x] Get sequential::output correctly parsed
# - [x] Get vmstat correctly parsed
# - [x] Get parallel_wrk::output correctly parsed
# - [x] Get parallel_go::output correctly parsed
# - [x] Create a sane JSON structure out of this

"""
Looking like

Running 1m test @ http://localhost:24343
  1 threads and 10 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   102.44us  114.80us  11.47ms   96.71%
    Req/Sec    79.15k     1.33k   87.98k    93.84%
  4734116 requests in 1.00m, 4.75GB read
Requests/sec:  78771.28
Transfer/sec:     80.98MB
"""
WRK_REGEX = re.compile(r"""\s*Running (?P<time>.*?) test \@ .*?
\s*(?P<threads>\d+) threads and (?P<connections>\d+) connections *?
.*?
\s*Latency\s*(?P<latency_avg>\S+)\s+(?P<latency_stdev>\S+)\s+(?P<latency_max>\S+)\s*.*?
\s*Req/Sec\s*(?P<reqsec_avg>\S+)\s+(?P<reqsec_stdev>\S+)\s+(?P<reqsec_max>\S+)\s*.*?
\s*(?P<total_reqs>\d+) requests in \S+, (?P<amount>\S+) read\s*
\s*Requests/sec: \s*(?P<reqs_sec>\S+)
\s*Transfer/sec:\s*(?P<transfer_sec>\S+)""", re.MULTILINE)

"""
Looking like

Running benchmark with 900 goroutines for 60 seconds
Running 60s test @ http://localhost:24343
  900 goroutine(s) running concurrently
1807813 requests in 59.792676902s, 1.79GB read
Requests/sec:           30234.69
Transfer/sec:           30.59MB
Avg Req Time:           29.767132ms
Fastest Request:        55.441µs
Slowest Request:        262.012151ms
Number of Errors:       0
"""
GO_WRK_REGEX = re.compile(r"""\s*Running benchmark with (?P<goroutines>\d+) goroutines for (?P<time>\d+) seconds\s*
\s*Running 60s test @ http://localhost:24343\s*
\s*\d+ goroutine\(s\) running concurrently\s*
\s*(?P<total_reqs>\d+) requests in (?P<total_time>\S+), (?P<total_data>\S+) read\s*
\s*Requests/sec:\s+(?P<reqs_sec>\S+)\s*
\s*Transfer/sec:\s+(?P<data_sec>\S+)\s*
\s*Avg Req Time:\s+(?P<avg_req_time>\S+)\s*
\s*Fastest Request:.*?
\s*Slowest Request:.*?
Number of Errors:\s+(?P<num_errors>\d+)""", re.MULTILINE)



def parse_vmstat(text: str):
    lines = text.split("\n")
    # The fist line contains all descriptions of the cols
    columns = lines[1].split()

    parsed_output = []

    for line in lines[2:]:
        if line.strip() == '' or 'procs' in line or 'cache' in line:
            # then header line, thus no values
            continue
        values = line.split()
        row = dict(zip(columns, values))
        parsed_output.append(row)

    return parsed_output

def parse_wrk(text: str):
    return [m.groupdict() for m in WRK_REGEX.finditer(text)]
def parse_go_wrk(text: str):
    return [m.groupdict() for m in GO_WRK_REGEX.finditer(text)]

def get_directory_structure(rootdir):
    dir_structure = {}

    for dirpath, dirnames, filenames in os.walk(rootdir):
        # We'll use os.path.relpath to get relative path to the root directory
        path = dirpath.split(os.sep)
        subdir = dict.fromkeys(filenames)
        
        # Reading file contents and assigning it to the file keys
        for file in filenames:
            with open(os.path.join(dirpath, file), 'r') as f:
                subdir[file] = f.read()

        # Nested assignment using reference to innermost dictionary
        current_layer = dir_structure
        for part in path:
            if part not in current_layer:
                current_layer[part] = {}
            current_layer = current_layer[part]
        current_layer.update(subdir)

    return dir_structure

def extract_numbers(file_dict):
    """
    Creates a nested dictionary for files with prefixes 'output' and 'vmstat'.
    The structure will be:
    {
        "output": {N: content of output_N.txt},
        "vmstat": {N: content of vmstat_N.txt}
    }
    """
    custom_dict = {"output": {}, "vmstat": {}}

    for file_name, content in file_dict.items():
        if file_name.startswith("output_") or file_name.startswith("vmstat_"):
            parts = file_name.split('_')
            prefix = parts[0]
            number = parts[1].split('.')[0]

            # Ensuring the number is an integer
            try:
                number = int(number)
            except ValueError:
                continue  # skip file if the number part isn't an integer

            custom_dict[prefix][number] = content

    return custom_dict


results_structure = get_directory_structure("./results")['.']['results']

# Parse what is vmstat and what is output
for benchmark_type in results_structure.keys():
    results_structure[benchmark_type] = extract_numbers(results_structure[benchmark_type])

# Parse the actual output and vmstat files
for benchmark_type in results_structure.keys():
    parse = parse_go_wrk if "go" in benchmark_type else parse_wrk

    for n in results_structure[benchmark_type]['vmstat'].keys():
        results_structure[benchmark_type]['vmstat'][n] = parse_vmstat(results_structure[benchmark_type]['vmstat'][n])
    for n in results_structure[benchmark_type]['output'].keys():
        results_structure[benchmark_type]['output'][n] = parse(results_structure[benchmark_type]['output'][n])

with open('parsed.json', 'w') as fp:
    json.dump(results_structure, fp, indent=2)
