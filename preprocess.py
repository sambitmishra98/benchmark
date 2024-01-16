import pandas as pd
from base.mesh_maker import MeshMaker
from base.config_maker import ConfigMaker
from base.partition_maker import PartitionMaker
from base.script_maker import ScriptMaker

if __name__ == '__main__':

    c = pd.read_csv('configurations.csv', comment='#', 
                    dtype={'nodelist':str, 
                           'nsteps':int, 'backend':str, 'caware':int, 'order':int, 'precision':str,
                           'nnodes':int, 'nparts-per-node':int, 
                           'etype':str, 'nelements':int, 
                           'partition':str, 'gpu':str
                           },
                    skipinitialspace=True,
                    )

    prefix = ''

    print(c)

    config_maker = ConfigMaker()
    config_maker.make_configs(c['nsteps'], c['caware'], c['order'], c['precision'],
                              c['nparts-per-node']*c['nnodes'],  
                              c['etype'], c['nelements'],)

    mesh_maker = MeshMaker()  # default prefix will be overwritten
    mesh_maker.make_meshes(c['nelements'], c['etype'])

    partition_maker = PartitionMaker()
    partition_maker.make_partitions(c['nelements'], 
                                    c['nparts-per-node']*c['nnodes'],
                                    c['etype'],)

    script_maker = ScriptMaker(prefix)
    script_maker.make_scripts(c['partition'], c['nodelist'], c['gpu'],
                              c['nsteps'], c['backend'], c['caware'], c['order'], c['precision'],
                              c['nnodes'], c['nparts-per-node'], 
                              c['etype'], c['nelements'], 
                              )
