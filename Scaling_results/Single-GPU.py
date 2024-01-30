import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys

# Get input file from command line
if len(sys.argv) != 2:
    print("Usage: python3 Single-GPU.py <input_file>")
    sys.exit(1)
    
input_file = sys.argv[1]

# If the input_file contains the strong 'ACES'
if 'ACES' in input_file:
    cluster='ACES'
elif 'Spitfire' in input_file:
    cluster='Spitfire'
else:
    raise ValueError(f"Cluster not supported")

if 'V100' in input_file:
    GPU='V100'
    GPUs_per_node=4
elif 'PVC' in input_file:
    GPU='PVC'
    GPUs_per_node=4
else:
    raise ValueError(f"GPU not supported")

# Read the input file

# Set the aesthetics for the plot
sns.set_style('whitegrid')
sns.set_context("paper", font_scale=1.5)
sns.set_palette("colorblind")

# Read the performance data from the CSV file
df = pd.read_csv(input_file,
    usecols=['backend', 'elements', 'DoFs', 'mean-perf', ])

fig, ax = plt.subplots(figsize=(12, 5))

# Create a bar plot for the performance data, with eror bars, grouped by backend (cuda and opencl)

# df1 = df[df['backend'] == 'cuda']
# df2 = df[df['backend'] == 'opencl']
# 
# ax.bar(df1['elements']-0.5, df1['mean-perf']/1e9, width=1, label='CUDA')
# ax.bar(df2['elements']+0.5, df2['mean-perf']/1e9, width=1, label='OpenCL')

# Do the above in a pythonic way
for backend, df_backend in df.groupby('backend'):
    ax.bar(df_backend['elements'], df_backend['mean-perf']/1e9, width=1, label=backend)

# First, find the number of unique elements
#elements = df['elements'].unique()

# Then, for each element, plot the performance data

# for element in elements:
#     # Get the subset of the data for the current element
#     sub_df = df[df['elements'] == element]

#ax.errorbar(df['Tasks'], df['norm-mean-perf-per-GPU'], 
#            yerr=df['norm-rem-perf'], fmt='o-', capsize=5)
#

#ax.hlines(1, 0, df['Tasks'].max(), colors='k', linestyles='dashed', label='Ideal scaling')

#ax.plot(df['elements'], first_entry/df['mean-perf'], 'o-', label='Single GPU')

ax.set_title(r'$\mathbf{Single-GPU\ scaling}$'+'\n'+
                f'Cluster: {cluster}, {GPUs_per_node} {GPU} GPUs per node\n'+
                'Solver: PyFR 1.15.0 Jan 28th develop version')

ax.set_xlabel('Cuberoot of total number of hexahedral elements')
# A second x-axis for DoFs, just below elements

ax.set_xticks(df['elements'])


ax.set_ylabel('Performance (GDoF/s)')
              
#ax.set_ylabel('Performance metric\n'
#                'Computations performed per unit runtime per GPU \n '
#                '(GigaDegrees of Freedom per second per GPU â¡ GDoF/s/GPU)')
ax.set_ylim(bottom=0, top=1.7)


ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
          fancybox=True, shadow=True, ncol=3)

# Create a NOTE box below the plot

# Create a box with the text
#textstr = '\n'.join((
#    r'$\mathbf{NOTE}$',
#    r'Benchmarking performed in https://doi.org/10.1145/3569951.3597565',
#    r'includes non-computation runtime too, like overheads of writing solution files to disk.',))

# Add the box to the plot, just below the xlabel
# ax.text(0.0, -0.25, textstr, transform=ax.transAxes, fontsize=14,
#         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Save
plt.savefig(f'{cluster}-{GPU}_SingleGPUScaling.png', dpi=300, bbox_inches='tight')
