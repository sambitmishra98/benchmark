import pandas as pd
from base.mesh_maker import MeshMaker
from base.config_maker import ConfigMaker
from base.partition_maker import PartitionMaker
from base.script_maker import ScriptMaker

# Taking even 1000 steps may suffice.

c = pd.DataFrame( 
               [
#                ['fc024', 500,         1,                     1,    1,             32, ],
#                ['fc024', 500,         1,                     1,    2,             40, ],
#                ['fc024', 500,         1,                     1,    4,             51, ],
#                ['fc024', 500,         1,                     1,    6,             58, ],
#                ['fc024', 500,         1,                     1,    8,             64, ],
#                ['fc024', 500,         1,                     1,   10,             69, ],
#                ['fc024', 500,         1,                     1,   12,             73, ],
#                ['fc024', 500,         1,                     1,   14,             77, ],
#                ['fc024', 500,         1,                     1,   16,             81, ],
#                ['fc024', 500,         1,                     1,    1,             64, ],
#                ['fc024', 500,         1,                     1,    2,             81, ],
#                ['fc024', 500,         1,                     1,    4,            102, ],
#                ['fc024', 500,         1,                     1,    6,            116, ],
#                ['fc024', 500,         1,                     1,    8,            128, ],
#                ['fc024', 500,         1,                     1,   10,            138, ],
#                ['fc024', 500,         1,                     1,   12,            147, ],
#                ['fc024', 500,         1,                     1,   14,            154, ],
#                ['fc024', 500,         1,                     1,   16,            161, ],
#                ['fc004', 2000,        1,                     1,    1,             96, ],
#                ['fc024', 500,         1,                     1,    2,            121, ],
#                ['fc024', 500,         1,                     1,    4,            152, ],
#                ['fc024', 500,         1,                     1,    6,            174, ],
#                ['fc024', 500,         1,                     1,    8,            192, ],
#                ['fc024', 500,         1,                     1,   10,            207, ],
#                ['fc024', 500,         1,                     1,   12,            220, ],
#                ['fc024', 500,         1,                     1,   14,            231, ],
                ['fc026', 100,           1,                     1,   1,             96, ],
#                ['fc004', 10,           1,                     1,   16,            242, ],
#        ['fc[004,024]', 20000,   1,                     2,    8,            242, ],
                ], 

    columns=['nodelist', 'nsteps', 'caware','nnodes', 'nparts-per-node', 'nelements', ])

if __name__ == '__main__':

    prefix = ''

    print(c)

    # --- Make configurations ---

    config_maker = ConfigMaker()
    config_maker.make_configs(c['nsteps'], c['caware'],
                              c['nparts-per-node']*c['nnodes'], c['nelements'])

    # --- Make mesh and partitions ---

    mesh_maker = MeshMaker('elems')  # default prefix will be overwritten
    mesh_maker.make_meshes(c['nelements'])

    partition_maker = PartitionMaker()
    partition_maker.make_partitions(c['nelements'], 
                                    c['nparts-per-node']*c['nnodes'])

    # --- Make scripts ---
    
    script_maker = ScriptMaker(prefix)
    script_maker.make_scripts(
                              c['nodelist'],  
                              c['nsteps'], 
                              c['caware'],
                              c['nnodes'], 
                              c['nparts-per-node'], 
                              c['nelements'], 
                              )
