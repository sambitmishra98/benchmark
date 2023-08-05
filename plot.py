import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np


fff = 1

# Set the aesthetics for the plot
sns.set_style('whitegrid')
sns.set_context("paper", font_scale=1.4)


array = np.array([[2534619525,	2649364621,	2629667798,	2480419833,	2304416728,	1944781174	,1183374862	,531710884.5,	897497112.3,],
[2623557887,	2716498812,	2703703529,	2556276758,	2556276758,	2556541174	,982887099.7,	1169064024,	940039931.9,],
[2597989021,	2687875652,	2684235783,	2670484778,	2545093408,	1179718368,	2653238691,	1308269951,	1182079029,]])/1e9


legend_cols = ['Exp', 'Steps', 'Samples', 'Caware', 'Nodes']

# Read the performance data from the CSV file
df = pd.read_csv(f'consolidated_performance_data_{fff}.csv',
                 usecols=['Directory', *legend_cols, 'Elements', 'Tasks',
                          'Performance_Per_GPU-GDOF', 'time'])
df = df[df['time'] != 0]

# Group the data and calculate the mean and standard deviation of performance
df_grouped = df.groupby([*legend_cols, 'Tasks'])[
    'Performance_Per_GPU-GDOF'].agg(['mean', 'std']).reset_index()

# Plotting the data
fig, ax = plt.subplots(figsize=(15, 9))
for key, grp in df_grouped.groupby([*legend_cols,]):

    # Create a formatted legend label using the column names and key values
    legend_label = f"{key[0]},"+\
                   f" timesteps: {key[1]},"+\
                   f" runtime samples: {key[2]},"+\
                   f" if cuda-aware: {bool(key[3])},"+\
                   f" number of nodes: {key[4]}"

    # Customize error bar style
    ax.errorbar(grp['Tasks'], grp['mean'], yerr=grp['std'], 
                fmt='o-', capsize=5, 
                label=' Current Liqid version',
                )

# Set the x-axis label, y-axis label, and title of the plot

ax.plot([1,2,4,6,8,10,12,14,16], array[fff-1,:], label='Previous Liqid version', color='black', linestyle='--', linewidth=2)

ax.set_xlabel('Total number of GPUs used')
ax.set_xlim(left=0)
ax.set_ylabel('Performance metric\n' 
              'Computations performed per unit runtime per GPU \n '
              '(GigaDegrees of Freedom per second per GPU ≡ GDoF/s/GPU)')
ax.set_ylim(bottom=0)
ax.set_title(r'$\mathbf{Weak-scaling\ performance\ comparison\ for\ different\ configurations}$'+'\n'+
             'Cluster: FASTER, GPU: 40GB NVIDIA A100\n'+
             'Solver: PyFR 1.15.0, Case setup: Taylor Green Vortex case with mesh size ~128³ DoF/GPU'+'\n'+
             legend_label+'\n')

ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),)

# Save the plot as an image file
plt.savefig(f'performance_plot_{fff}.png', dpi=300, bbox_inches='tight')
