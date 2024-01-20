import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# Set the aesthetics for the plot
sns.set_style('whitegrid')
sns.set_context("paper", font_scale=1.5)
sns.set_palette("colorblind")

# Read the performance data from the CSV file
df = pd.read_csv('result_single-GPU.csv')


elements_per_box = {'tet': '12', 
                    #'pyr':  '6 Ã (p+1)(p+2)(p+3)/6', WRONG
                    'pri':  '2',
                    'hex':  '1',
                    }

# group df data by partition and accelerator
grouped_df = df.groupby(['backend', 'caware'])

# Plot each group as an independant plot. The plot name is the group name single-GPU-performance_partition{partition}_accelerator{accelerator}.png
for name, group in grouped_df:

    # Create the 2x2 subplot structure
    fig, axes = plt.subplots(2, 2, figsize=(15, 10), sharey=True, sharex='col')

    # Define the etype and precision mappings for subplots
    subplots = {
        ('single', 'tet'): axes[0, 0],
        ('single', 'hex'): axes[0, 1],
        ('double', 'tet'): axes[1, 0],
        ('double', 'hex'): axes[1, 1]
    }
    df = group

    # Plotting
    for (precision, etype), ax in subplots.items():
        filtered_df = df[(df['precision'] == precision) & (df['etype'] == etype)]
        if not filtered_df.empty:
            # Pivot the data for grouped bar plot
            pivot_df = filtered_df.pivot_table(index='elements', columns='order', values='mean-perf-per-GPU')
            pivot_df.plot(kind='bar', ax=ax, legend=False, )
            
            # Setting the individual subplot titles
            ax.set_title(f'Precision: {precision.capitalize()}, Element Type: {etype.upper()}')
#            ax.set_xlabel('Number of Elements')

            # set x-axis ticks labels to have a Â³ suffix
            # If tet, then also have a prefix of 8* for the labels

            #if etype == 'tet':
            #    ax.set_xticklabels([f'8*{int(x)}Â³' for x in pivot_df.index])
            #else:
            #    ax.set_xticklabels([f'{int(x)}Â³' for x in pivot_df.index])

            # Use elements_per_box to set the x-axis ticks labels to have a Â³ suffix and elements_per_box prefix
            ax.set_xticklabels([f'{elements_per_box[etype]}Ã{int(x)}Â³' for x in pivot_df.index], rotation=0)

#            ax.set_ylabel('Performance (DoF/s)')
            ax.set_ylim(bottom=0, top=8e9)

            # major and minor grid
            ax.grid(True, which='major', color='k', linestyle='-', alpha=0.2)
            ax.grid(True, which='minor', color='k', linestyle='-', alpha=0.1)
            ax.minorticks_on()
    # Y-axuis label for the leftmost subplots
    axes[0, 0].set_ylabel('Performance (DoF/s)')
    axes[1, 0].set_ylabel('Performance (DoF/s)')
    
    # X-axis label for the bottom subplots
    axes[1, 0].set_xlabel('Number of Elements (Nâ)')
    axes[1, 1].set_xlabel('Number of Elements (Nâ)')


    # Title, with heading as Single-GPU Performance and subheading as the partition and accelerator
    fig.suptitle(f'Single-GPU Performance\n'+
                 f'Mean performance computed over 10000 timesteps'+
                 f'\nPartition: {name[0]}, Accelerator: {name[1]}')

    # Setting a common legend for all subplots
    handles, labels = axes[0, 0].get_legend_handles_labels()
#    fig.legend(handles, labels, loc='upper right', ncol=len(labels), title='Polynomial order')

    # Createa note in the bottom of the figure for how to calculate the number of DoFs. Ensure that the note is not overlapping with the legend
    fig.text(0.05, 0.0, f'NOTE: The total degrees of freedom (DoF) is\n'+
             f'DoF = (NâÂ³ Ã (order+1))Â³ for HEX elements \n'+
             f'DoF = (NâÂ³ Ã (order+1)(order+2)(order+3)/6) for TET elements', 
             ha='left', fontsize=12)

    # Adjusting the layout
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    # Save the figure
    partition = name[0]
    accelerator = name[1]
    plt.savefig(f'single-GPU-performance_backend{partition}_caware{accelerator}.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
