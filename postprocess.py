import os
import re
import pandas as pd

PATTERN = re.compile(
    r'partition(pvc|gpu)_gpu(pvc|h100|a100|a40)_nodelist(\w+)_steps(\d+)_backend(cuda|opencl|openmp|hip|metal)_caware(0|1)_order(\d+)_precision(single|double)_nodes(\d+)_tasks(\d+)_(hex|tet|pri|pyr)(\d+)'
)

def parse_directory(directory, prefix):
    match = PATTERN.search(directory)
    if match:
        return match.groups()
    return None

def gather_data(root_dir, prefix=''):

    data = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == 'perf.csv':
                full_path = os.path.join(dirpath, filename)

                try:
                    df = pd.read_csv(full_path)
                except Exception as e:
                    print(f"Error reading {full_path}: {e}")
                    continue

                last_row = df.iloc[-1]
                steps = last_row['n']
                mean = last_row['mean']
                rel_err = last_row['rel-err']

                dir_params = parse_directory(dirpath, prefix)

                if mean and rel_err and dir_params:
                    data.append((dirpath, filename) + dir_params + (steps, mean, rel_err))

    return data
def main():
    root_dir = "./solns/"
    prefix = ''
    data = gather_data(root_dir, prefix)

    columns = ['directory', 'filename', 'partition', 'accelerator', 'nodelist', 'Steps', 'backend', 'CAware', 'order', 'precision', 'Nodes', 'Tasks', 'etype', 'Elements', 'actual-steps', 'mean-perf', 'rem-perf']

    df = pd.DataFrame(data, columns=columns)

    df = df.apply(pd.to_numeric, errors='ignore') 
    df['mean-perf-per-GPU'] = df['mean-perf'] / df['Tasks']

    # First order    by number of nodes, (ascending)
    #          then  if cuda-aware or not (descending)
    #           then by number of tasks, (ascending)
    df.sort_values(by=['Nodes', 'CAware', 'Tasks'], ascending=[True, False, True], inplace=True)

    # Get perf-per-GPU relative to the first entry
    first_entry = df.iloc[0]['mean-perf-per-GPU']
    df['norm-mean-perf-per-GPU'] = df['mean-perf-per-GPU'] / first_entry
    df['norm-rem-perf'] = df['rem-perf'] *df['mean-perf-per-GPU']/ first_entry

    # only print the columns for the following
    # precision, nodes, tasks, etype, elements, mean-perf-per-GPU, rem-perf

#    df = df[df['partition'] == 'pvc']

    # Print everything
    print(df[['backend', 'CAware', 'Tasks', 
              #'Elements', 
              'mean-perf-per-GPU', 'rem-perf',]].to_string(index=False),
          sep='\n', 
          end='\n\n')

    df.to_csv('output.csv', index=False)

if __name__ == "__main__":
    main()