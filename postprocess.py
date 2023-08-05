import os
import re
import glob
import pandas as pd

def parse_wall_time(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            if "wall-time" in line:
                return float(line.split('=')[1].strip())
    return None

def parse_directory(directory):
    dir_pattern = re.compile(r'solns/([a-zA-Z0-9_\[\]-]+)_steps(\d+)_samples(\d+)_caware(\d+)_nodes(\d+)_tasks(\d+)_elems(\d+)')
    match = dir_pattern.search(directory)
    if match:
        return match.groups()
    return None

def parse_filename(filename):
    file_pattern = re.compile(r'bm_t([\d\.]+).dat')
    match = file_pattern.search(filename)
    if match:
        return match.groups()
    return None

def gather_data(root_dir):
    data = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.dat'):
                full_path = os.path.join(dirpath, filename)
                wall_time = parse_wall_time(full_path)
                dir_params = parse_directory(dirpath)
                file_params = parse_filename(filename)

                if wall_time and dir_params and file_params:
                    data.append((dirpath, filename) + dir_params + file_params + (wall_time,))

    return data

def main():
    root_dir = "./solns/"
    data = gather_data(root_dir)

    df = pd.DataFrame(data, columns=['Directory', 'File Name', 
                                     'Exp', 'Steps', 'Samples', 'Caware', 'Nodes', 
                                     'Tasks', 'Elements', 'time', 'Wall Time'])
    df = df.apply(pd.to_numeric, errors='ignore') 
    compute_performance(df)

if __name__ == "__main__":
    main()
