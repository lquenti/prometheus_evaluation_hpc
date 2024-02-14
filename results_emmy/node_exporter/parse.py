import re
import json
import os

def parse_sequential(data):
    section_pattern = re.compile(r'(\d+) threads and (\d+).*?'
                                 r'Latency\s+(\d+\.\d+)([a-z]+)\s+(\d+\.\d+)([a-z]+)\s+(\d+\.\d+)([a-z]+)\s+(\d+\.\d+)%.*?'
                                 r'Req/Sec\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)%.*?'
                                 r'(\d+) requests in.*?, (\d+\.\d+)([A-Z]+) read.*?'
                                 r'Requests/sec:\s+(\d+\.\d+).*?'
                                 r'Transfer/sec:\s+(\d+\.\d+)([A-Z]+)', re.DOTALL)
    matches = section_pattern.findall(data)
    results = []
    for match in matches:
        result = {
            "threads": int(match[0]),
            "connections": int(match[1]),
            "latency_avg": f"{match[2]}{match[3]}",
            "latency_stdev": f"{match[4]}{match[5]}",
            "latency_max": f"{match[6]}{match[7]}",
            "latency_stdev_pct": float(match[8]),
            "req_sec_avg": float(match[9]),
            "req_sec_stdev": float(match[10]),
            "req_sec_max": float(match[11]),
            "req_sec_stdev_pct": float(match[12]),
            "requests": int(match[13]),
            "read_mb": f"{match[14]}{match[15]}",
            "requests_per_sec": float(match[16]),
            "transfer_per_sec_mb": f"{match[17]}{match[18]}"
        }
        results.append(result)
    return results

import re

def parse_wrk(data):
    section_pattern = re.compile(
        r'Running benchmark with (?P<threads>\d+) threads and (?P<connections>\d+) connections for (?P<duration_seconds>\d+)s.*?'
        r'Latency\s+(?P<latency_avg>\d+\.\d+)(?P<latency_avg_unit>[a-z]+)\s+(?P<latency_stdev>\d+\.\d+)(?P<latency_stdev_unit>[a-z]+)\s+(?P<latency_max>\d+\.\d+)(?P<latency_max_unit>[a-z]+)\s+(?P<latency_stdev_pct>\d+\.\d+)%.*?'
        r'Req/Sec\s+(?P<req_sec_avg>\d+\.\d+)\s+(?P<req_sec_stdev>\d+\.\d+)\s+(?P<req_sec_max>\d+\.\d+)\s+(?P<req_sec_stdev_pct>\d+\.\d+)%.*?'
        r'(?P<requests>\d+) requests in.*?, (?P<read_size>\d+\.\d+)(?P<read_unit>[A-Z]+) read.*?(?:\n.*?timeout (?P<timeout>\d+))?.*?'
        r'Requests/sec:\s+(?P<requests_per_sec>\d+\.\d+).*?'
        r'Transfer/sec:\s+(?P<transfer_per_sec_size>\d+\.\d+)(?P<transfer_per_sec_unit>[A-Z]+)', re.DOTALL)
    
    matches = section_pattern.finditer(data)
    results = []
    for match in matches:
        result = {
            "threads": int(match.group('threads')),
            "connections": int(match.group('connections')),
            "duration_seconds": int(match.group('duration_seconds')),
            "latency_avg": f"{match.group('latency_avg')}{match.group('latency_avg_unit')}",
            "latency_stdev": f"{match.group('latency_stdev')}{match.group('latency_stdev_unit')}",
            "latency_max": f"{match.group('latency_max')}{match.group('latency_max_unit')}",
            "latency_stdev_pct": float(match.group('latency_stdev_pct')),
            "req_sec_avg": float(match.group('req_sec_avg')),
            "req_sec_stdev": float(match.group('req_sec_stdev')),
            "req_sec_max": float(match.group('req_sec_max')),
            "req_sec_stdev_pct": float(match.group('req_sec_stdev_pct')),
            "requests": int(match.group('requests')),
            "read_mb": f"{match.group('read_size')}{match.group('read_unit')}",
            "requests_per_sec": float(match.group('requests_per_sec')),
            "transfer_per_sec_mb": f"{match.group('transfer_per_sec_size')}{match.group('transfer_per_sec_unit')}",
            "timeouts": int(match.group('timeout')) if match.group('timeout') else 0  # Default to 0 if no timeout information
        }
        if result["timeouts"] != 0:
            print(result)
        results.append(result)
    return results


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

for benchmark_type in results_structure.keys():
    results_structure[benchmark_type] = extract_numbers(results_structure[benchmark_type])

for benchmark_type in results_structure.keys():
    parse = parse_sequential if "sequential" in benchmark_type else parse_wrk
    for n in results_structure[benchmark_type]['vmstat'].keys():
        results_structure[benchmark_type]['vmstat'][n] = parse_vmstat(results_structure[benchmark_type]['vmstat'][n])
    for n in results_structure[benchmark_type]['output'].keys():
        results_structure[benchmark_type]['output'][n] = parse(results_structure[benchmark_type]['output'][n])

print(type(results_structure["sequential"]["output"][8]))

with open('parsed.json', 'w') as fp:
    json.dump(results_structure, fp, indent=2)
