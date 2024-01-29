import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys

# Get input file from command line
if len(sys.argv) != 2:
    print("Usage: python3 StrongScaling.py <input_file>")
    sys.exit(1)
    
input_file = sys.argv[1]


# Read the input file

# Set the aesthetics for the plot
sns.set_style('whitegrid')
sns.set_context("paper", font_scale=1.5)
sns.set_palette("colorblind")

# Read the performance data from the CSV file
df = pd.read_csv(input_file,
    usecols=['backend', 'caware', 'elements', 'tasks',  'DoFs', 'mean-perf', ])

fig, ax = plt.subplots(figsize=(12, 5))

# Find the number of unique elements
elements = df['elements'].unique()

# Strong scaling is done for a fixed number of elements
# So, for a set of simulations with the same element, backend and caware values,
# plot a line plot of performance vs number of tasks

line_styles = ['s--', '>-.', 'o-', ]
alphas = [0.4, 0.6, 1]

# line colors are grey for cuda 0 , green for cuda 1 and red for opencl 0
line_colors = ['grey', 'green', 'red']

for element in elements:

    if element == 32:
        line_style = line_styles[0]
        alpha = alphas[0]
    elif element == 64:
        line_style = line_styles[1]
        alpha = alphas[1]
    elif element == 128:
        line_style = line_styles[2]
        alpha = alphas[2]

    # Get the subset of the data for the current element
    sub_df = df[df['elements'] == element]
    # Then, for each element, plot the performance data
    for backend, df_backend in sub_df.groupby('backend'):
        for caware, df_caware in df_backend.groupby('caware'):

            if backend == 'cuda' and caware == 0:
                line_color = line_colors[0]
            elif backend == 'cuda' and caware == 1:
                line_color = line_colors[1]
            elif backend == 'opencl' and caware == 0:
                line_color = line_colors[2]

            ax.plot(df_caware['tasks'], df_caware['mean-perf']/1e9, line_style, 
                    color=line_color, alpha=alpha,
                    label=f'{element}^3 elements, {backend}, {caware}')

# for element in elements:
#     # Get the subset of the data for the current element
#     sub_df = df[df['elements'] == element]

#ax.errorbar(df['Tasks'], df['norm-mean-perf-per-GPU'], 
#            yerr=df['norm-rem-perf'], fmt='o-', capsize=5)
#

#ax.hlines(1, 0, df['Tasks'].max(), colors='k', linestyles='dashed', label='Ideal scaling')

first_entry = df.iloc[0]['mean-perf']/1e9

#ax.plot(df['elements'], first_entry/df['mean-perf'], 'o-', label='Single GPU')

ax.set_title(r'$\mathbf{Single-GPU\ scaling}$'+'\n'+
                'Cluster: Spitfire, 4 NVIDIA A100 GPUs per node\n'+
                'Solver: PyFR 1.15.0 Jan 28th develop version')

ax.set_xlabel('Tasks')
# A second x-axis for DoFs, just below elements

ax.set_ylabel('Performance (GDoF/s)')
              
#ax.set_ylabel('Performance metric\n'
#                'Computations performed per unit runtime per GPU \n '
#                '(GigaDegrees of Freedom per second per GPU â¡ GDoF/s/GPU)')
ax.set_ylim(bottom=0)

# outside
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
plt.savefig(f'Spitfire-V100_StrongScaling.png', dpi=300, bbox_inches='tight')
