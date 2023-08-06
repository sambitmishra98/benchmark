import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

fff = 1

# Set the aesthetics for the plot
sns.set_style('whitegrid')
sns.set_context("paper", font_scale=1.4)


sns.set_style('whitegrid')
sns.set_context("paper", font_scale=1.5)
sns.set_palette("colorblind")

# Read the performance data from the CSV file
df = pd.read_csv(f'output.csv', 
    usecols=['Directory', 
             'Node List', 'Steps', 'CAware', 'Nodes', 'Tasks', 'Elements', 
             'actual-steps', 'mean-perf', 'rem-perf', 
             'mean-perf-per-GPU', 'norm-mean-perf-per-GPU','norm-rem-perf'])

fig, ax = plt.subplots(figsize=(12, 5))

# Create a bar plot for the performance data, with eror bars
ax.errorbar(df['Tasks'], df['norm-mean-perf-per-GPU'], 
            yerr=df['norm-rem-perf'], fmt='o-', capsize=5)

ax.hlines(1, 0, df['Tasks'].max(), colors='k', linestyles='dashed', label='Ideal scaling')

first_entry = df.iloc[0]['mean-perf-per-GPU']/1e9

ax.set_title(r'$\mathbf{Weak-scaling\ efficiency\ comparison\ on\ FASTER}$'+'\n'+
                'Cluster: FASTER, GPU: 40GB NVIDIA A100\n'+
                'Solver: PyFR 1.15.0\n'+
                'Case setup: Taylor Green Vortex case with mesh size ~256³ DoF/GPU\n'+
                f'Normalisation performed w.r.t. simulation on first GPU: {first_entry:.2f} GDoF/s/GPU')

ax.set_xlabel('Total number of GPUs used')
ax.set_xlim(0, 16)
ax.set_xticks(df['Tasks'])
ax.set_ylabel('Normalised performance')
              
#ax.set_ylabel('Performance metric\n'
#                'Computations performed per unit runtime per GPU \n '
#                '(GigaDegrees of Freedom per second per GPU ≡ GDoF/s/GPU)')
ax.set_ylim(bottom=0)

ax.legend(loc='lower left')

# Create a NOTE box below the plot

# Create a box with the text
textstr = '\n'.join((
    r'$\mathbf{NOTE}$',
    r'Benchmarking performed in https://doi.org/10.1145/3569951.3597565',
    r'includes non-computation runtime too, like overheads of writing solution files to disk.',))

# Add the box to the plot, just below the xlabel
ax.text(0.0, -0.25, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))




# Save
plt.savefig(f'perf-per-GPU.png', dpi=300, bbox_inches='tight')
