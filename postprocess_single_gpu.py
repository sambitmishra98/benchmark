import os
import re
import pandas as pd

MEAN_OVER_TIMESTEPS = 10000

PATTERN = re.compile(
    r'(\w+)partition(pvc|gpu)_gpu(pvc|h100|a100)_nodelist(\w+)_steps(\d+)_backend(cuda|opencl|openmp|hip|metal)_caware(0|1)_order(\d+)_precision(single|double)_nodes(\d+)_tasks(\d+)_(hex|tet|pri|pyr)(\d+)'
)

DOF_DAT_FILE_NAME = 'degrees_of_freedom.dat'

def calculate_performance(a, b, c):
    try:
        return round(float(a) / (float(c) - float(b)) * MEAN_OVER_TIMESTEPS, 6)
    except (ZeroDivisionError, ValueError):
        return None

def parse_location(location):
    match = PATTERN.search(location)
    if match:
        return match.groups()
    else:
        raise ValueError('Unknown format in location: ' + location)

def gather_data(root_dir, prefix=''):
    data = []
    for dirpath, _, filenames in os.walk(root_dir):
        if DOF_DAT_FILE_NAME in filenames:
            parsed_location = parse_location(dirpath.replace(root_dir, ''))
            if int(parsed_location[4]) == MEAN_OVER_TIMESTEPS:
                full_path = os.path.join(dirpath, DOF_DAT_FILE_NAME)
                with open(full_path, 'r') as data_file:
                    lines = data_file.readlines()
                    if len(lines) == 3 and ('soln-1.pyfrs' in filenames):
                        performance = calculate_performance(*[line.strip() for line in lines])
                        data.append((dirpath, DOF_DAT_FILE_NAME) + parsed_location + (lines[0].strip(), performance))
                    else:
                        data.append((dirpath, DOF_DAT_FILE_NAME) + parsed_location + (None, None))
    return data

def main():
    root_dir = 'solns/'
    data = gather_data(root_dir, prefix='')
    columns = ['directory', 'filename', 
               'prefix', 'partition', 'accelerator', 'nodelist', 
               'steps', 'backend', 'caware', 'order', 'precision', 
               'nodes', 'tasks', 'etype', 'elements', 'DoFs', 
               'mean-perf']
    df = pd.DataFrame(data, columns=columns)

    df = df.apply(pd.to_numeric, errors='ignore')
    df.sort_values(by=['prefix', 'tasks'], 
                   ascending=[True, True],
                   inplace=True,
                   )

    # Divide mean performance by number of tasks
    df['mean-perf'] = df['mean-perf'].astype(float)
    df['tasks'] = df['tasks'].astype(float)
    
    df['mean-perf-per-GPU'] = df['mean-perf'] / df['tasks']

    print(df[['prefix', 'elements', 'tasks', 'DoFs', 
              'mean-perf', 'mean-perf-per-GPU']])
    df.to_csv('result_single-GPU.csv', index=False)
    print("Data processed and saved to 'result.csv'.")

if __name__ == "__main__":
    main()
