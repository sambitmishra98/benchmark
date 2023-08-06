import pandas as pd
from base.mesh_maker import MeshMaker
from base.config_maker import ConfigMaker
from base.partition_maker import PartitionMaker
from base.script_maker import ScriptMaker

if __name__ == '__main__':

    c = pd.read_csv('configurations.csv', comment='#')

    Expected_columns = pd.Index(['nodelist', 'nsteps', 'caware','nnodes', 'nparts-per-node', 'nelements', ])

    if not c.columns.equals(Expected_columns):
        print(c.columns)
        print(Expected_columns)
        raise ValueError('Columns of configurations.csv do not match expected columns')

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
