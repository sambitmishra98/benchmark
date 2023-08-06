import os
import re
import pandas as pd

def parse_directory(directory):
    dir_pattern = re.compile(r'nodelist([a-zA-Z0-9_\[\]-]+)_steps(\d+)_caware(\d+)_nodes(\d+)_tasks(\d+)_elems(\d+)')
    match = dir_pattern.search(directory)
    if match:
        return match.groups()
    return None


def gather_data(root_dir):

    data = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == 'perf.csv':
                full_path = os.path.join(dirpath, filename)
                df = pd.read_csv(full_path)
                last_row = df.iloc[-1]
                steps = last_row['n']
                mean = last_row['mean']
                rel_err = last_row['rel-err']

                dir_params = parse_directory(dirpath)

                if mean and rel_err and dir_params:
                    data.append((dirpath, filename) + dir_params + (steps, mean, rel_err))

    return data
def main():
    root_dir = "./solns/"
    data = gather_data(root_dir)

    df = pd.DataFrame(data, columns=['Directory', 'File Name', 'Node List', 'Steps', 'CAware', 'Nodes', 'Tasks', 'Elements', 'actual-steps', 'mean-perf', 'rem-perf'])
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

    print(df)

    df.to_csv('output.csv', index=False)

if __name__ == "__main__":
    main()