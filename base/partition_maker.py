import os
import subprocess

class PartitionMaker:
    def __init__(self, mesh_dir='meshes', partition_dir='partitions'):
        self.mesh_dir = mesh_dir
        self.partition_dir = partition_dir

    def make_partitions(self, nelements, npartitions):

        os.system(f"mkdir -p {self.partition_dir}")
        
        for elems, npart in zip(nelements, npartitions):
            mesh_file = f'{self.mesh_dir}/elems{elems}.msh'
            partition_file = f'{self.partition_dir}/parts{npart}_elems{elems}.pyfrm'

            if not os.path.isfile(mesh_file):
                print(f"Mesh of size {elems} does not exist. Please create it first.")
                break

            if not os.path.isfile(partition_file):
                subprocess.run(f'pyfr import {mesh_file} {partition_file}', shell=True, check=True)
                print(f"Mesh imported:     {partition_file}")
                subprocess.run(f'pyfr partition {npart} {partition_file} {self.partition_dir}', shell=True, check=True)
                print(f"Partition created: {partition_file}")
            else:
                print(f"Partition  exists: {partition_file}")
