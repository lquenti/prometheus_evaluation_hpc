import json
import os

DIRECTORY = "full_pipeline_results"

print("parsing the results...")
def get_filepaths_dict(directory):
    filepaths_dict = {}
    for foldername in os.listdir(directory):
        if foldername.isdigit():
            folder_path = os.path.join(directory, foldername)
            foldername = int(foldername)
            if os.path.isdir(folder_path):
                filepaths_dict[foldername] = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename != "vmstat.txt"]
    return filepaths_dict

def read_files_with_a_single_digit(list_of_files):
    ret = []
    for path in list_of_files:
        with open(path, "r") as fp:
            ret.append(int(fp.read()))
    return ret

filepaths_dict = get_filepaths_dict(DIRECTORY)
number_dict = {}
for k,v in filepaths_dict.items():
    number_dict[k] = read_files_with_a_single_digit(v)

with open("./results.json", "w") as fp:
    json.dump(number_dict, fp, indent=2)

#############################

print("parsing vmstat...")

def parse_vmstat(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

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

def get_vmstat_dict(directory):
    filepaths_dict = {}
    for foldername in os.listdir(directory):
        if foldername.isdigit():
            folder_path = os.path.join(directory, foldername)
            foldername = int(foldername)
            if os.path.isdir(folder_path):
                filepaths_dict[foldername] = os.path.join(folder_path, "vmstat.txt")
    return filepaths_dict

vmstatpath_dict = get_vmstat_dict(DIRECTORY)
vmstat_dict = {}
for k,v in vmstatpath_dict.items():
    vmstat_dict[k] = parse_vmstat(v)

with open("./vmstat.json", "w") as fp:
    json.dump(vmstat_dict, fp, indent=2)
