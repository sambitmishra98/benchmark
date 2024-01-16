import os
import subprocess

class PartitionMaker:
    def __init__(self):
        pass
    def make_partitions(self, nelements, npartitions, netype):

        os.system(f"mkdir -p partitions/")
        
        for elems, npart, etype in zip(nelements, npartitions, netype):
            mesh_file = f'meshes/{etype}{elems}.msh'
            partition_file = f'partitions/tasks{npart}_{etype}{elems}.pyfrm'

            if not os.path.isfile(mesh_file):
                print(f"The required TGV mesh with {etype} element type and size {elems} does not exist. Please create it first.")
                break

            if not os.path.isfile(partition_file):
                subprocess.run(f'pyfr import {mesh_file} {partition_file}', shell=True, check=True)
                print(f"Mesh imported:     {partition_file}")
                subprocess.run(f'pyfr partition {npart} {partition_file} partitions/', shell=True, check=True)
                print(f"Partition created: {partition_file}")
            else:
                print(f"Partition  exists: {partition_file}")
