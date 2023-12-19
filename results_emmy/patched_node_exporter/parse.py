import sys
import re
import json

def extract_numbers(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()

    pattern = re.compile(r'total time:\s+(\d+)')
    numbers = []

    for line in content:
        match = pattern.search(line)
        if match:
            numbers.append(int(match.group(1)))

    return numbers

if __name__ == "__main__":
    numbers = extract_numbers(sys.argv[1])
    with open('./total_times.json', 'w') as f:
        json.dump(numbers, f)

