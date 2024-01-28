import pandas as pd
import numpy as np

SCALING_TYPE = 'weak'
BASE_ELEMENTS = 80
BASE_PARTS_PER_NODE = 12

# GLOBAL VARIABLES
NODELIST = 'fc036'
NSTEPS = 100
BACKEND = ['opencl', 'cuda']
CAWARE = [0,1]
ORDER = 3
PRECISION = 'double'
#NNODES = 1
#NPARTS_PER_NODE = 1
ETYPE = 'hex'
#NELEMENTS = 64
PARTITION = 'gpu'
GPU = 'h100'

# Create a csv file called config_weak.csv

# ---------------------------------------------------

c = pd.DataFrame(columns=['nodelist', 'nsteps', 'backend', 'caware', 'order', 'precision',
                            'nnodes', 'nparts-per-node', 
                            'etype', 'nelements', 
                            'partition', 'gpu',
                            ])

# ---------------------------------------------------
# We shall use the following parameters for the weak scaling study:
# nodelist = 'fc031'
# nsteps = 100
# backend = 'opencl'
# caware = 0
# order = 3
# precision = 'double'
# nnodes =  # CALCULATED LATER
# nparts-per-node = # CALCULATED LATER
# etype = 'hex'
# nelements = # CALCULATED LATER
# partition = 'gpu'
# gpu = 'a100'

# below is equal to [1,2,3,4,5,6,7,8]
npnode_list = np.array([20,18,16,14,12,10,8,6,4,2,1])
nnode_list = np.ones(len(npnode_list), dtype=int)

if SCALING_TYPE == 'weak':
    nelements_list = np.array(np.round(BASE_ELEMENTS * np.array(np.cbrt(np.array(npnode_list, dtype=float)))), dtype=int)
elif SCALING_TYPE == 'strong':
    nelements_list = BASE_ELEMENTS * np.ones(len(npnode_list), dtype=int)
else:
    raise ValueError('SCALING_TYPE must be either "weak" or "strong".')


# Empty dataframe
c = pd.DataFrame(columns=['nodelist', 'nsteps', 'backend', 'caware', 'order', 'precision',
                            'nnodes', 'nparts-per-node', 
                            'etype', 'nelements', 
                            'partition', 'gpu',
                            ])

for backend in BACKEND:
    for caware in CAWARE:

        if backend == 'opencl' and caware == 1:
            continue

        c = c._append(pd.DataFrame({'nodelist'           : [NODELIST]  * len(nnode_list),
                                    'nsteps'             : [NSTEPS]    * len(nnode_list),
                                        'backend'        : [backend]   * len(nnode_list),
                                        'caware'         : [caware]    * len(nnode_list),
                                        'order'          : [ORDER]     * len(nnode_list),
                                        'precision'      : [PRECISION] * len(nnode_list),
                                        'nnodes'         : nnode_list,
                                        'nparts-per-node': npnode_list,
                                        'etype'          : [ETYPE]     * len(nnode_list),
                                        'nelements'      : nelements_list,
                                        'partition'      : [PARTITION] * len(nnode_list),
                                        'gpu'            : [GPU]       * len(nnode_list)
                                        }))
        
# Write the config_weak.csv file
c.to_csv(f'configuration_{SCALING_TYPE}_{ETYPE}{BASE_ELEMENTS}.csv', 
         index=False)
