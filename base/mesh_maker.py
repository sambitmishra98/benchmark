from itertools import product
import numpy as np
import os

class MeshMaker:
    def __init__(self, suffix):
        self.suffix = suffix

    def gmsh_header(self):
        return '''
$MeshFormat
2.2 0 8
$EndMeshFormat
$PhysicalNames
7
3 1 "fluid"
2 2 "periodic_0_l"
2 3 "periodic_1_l"
2 4 "periodic_2_l"
2 5 "periodic_0_r"
2 6 "periodic_1_r"
2 7 "periodic_2_r"
$EndPhysicalNames
'''

    def gmsh_nodes(self, X):
        nodes = '\n'.join(f'{i+1} {" ".join(map(str, x))}' for i, x in enumerate(X))
        return f'$Nodes\n{len(X)}\n{nodes}\n$EndNodes\n'
    
    def gmsh_boundaries(self, nx, nele = 0):
        ele = ''
        ind = lambda i, j, k: self.grid_index(nx, nx, i, j, k)

        for i1 in range(nx-1):
            for i2 in range(nx-1):
                # i=0
                nele += 1
                n = [ind(0, i2, i1), ind(0, i2+1, i1),
                    ind(0, i2+1, i1+1), ind(0, i2, i1+1)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 3 2 2 2 {n_str}\n'

                # i=nx-1
                nele += 1
                n = [ind(nx-1, i2, i1), ind(nx-1, i2+1, i1),
                    ind(nx-1, i2+1, i1+1), ind(nx-1, i2, i1+1)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 3 2 5 5 {n_str}\n'

                # j=0
                nele += 1
                n = [ind(i2, 0, i1), ind(i2+1, 0, i1),
                    ind(i2+1, 0, i1+1), ind(i2, 0, i1+1)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 3 2 3 3 {n_str}\n'

                # j=nx-1
                nele += 1
                n = [ind(i2, nx-1, i1), ind(i2+1, nx-1, i1),
                    ind(i2+1, nx-1, i1+1), ind(i2, nx-1, i1+1)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 3 2 6 6 {n_str}\n'

                # k=0
                nele += 1
                n = [ind(i2, i1, 0), ind(i2, i1+1, 0),
                    ind(i2+1, i1+1, 0), ind(i2+1, i1, 0)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 3 2 4 4 {n_str}\n'

                # k=nx-1
                nele += 1
                n = [ind(i2, i1, nx-1), ind(i2, i1+1, nx-1),
                    ind(i2+1, i1+1, nx-1), ind(i2+1, i1, nx-1)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 3 2 7 7 {n_str}\n'
        
        return nele, ele

    def gmsh_elements(self, nx):
        nele, ele = self.gmsh_boundaries(nx)
        elements = []

        # elm-number elm-type number-of-tags < tag > … node-number-list
        for k in range(nx - 1):
            for j in range(nx - 1):
                for i in range(nx - 1):
                    nele += 1
                    n = [
                        self.grid_index(nx, nx, i+dx, j+dy, k+dz) 
                        for dx, dy, dz in [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0),
                                            (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]
                    ]
                    n_str = ' '.join(str(ni) for ni in n)
                    elements.append(f'{nele} 5 2 1 1 {n_str} \n')

        ele += ''.join(elements)
        return f'$Elements\n{nele}\n{ele}$EndElements\n'

    def make_mesh(self):
        R = np.linspace(0, self.l, self.nx)
        X = np.array([np.array([rx, ry, rz]) for rz, ry, rx in product(R, repeat=3)])

        header = self.gmsh_header()
        nodes = self.gmsh_nodes(X)
        elements = self.gmsh_elements(self.nx)

        return header + nodes + elements

    def grid_index(self, nx, ny, i, j, k):
        return k*nx*ny + j*nx + i + 1

    def write_mesh_to_file(self, msh, filename):
        try:
            with open(filename, 'w') as f:
                f.write(msh)
            print(f"Mesh successfully written to {filename}")
        except Exception as e:
            print(f"An error occurred while writing the mesh to file: {e}")

    def make_meshes(self, nx_values):

        os.system("mkdir -p meshes")

        for nx in nx_values:
            self.l = 6.28318530718
            self.nx = nx
            filename = f'meshes/{self.suffix}{nx}.msh'

            if not os.path.isfile(filename):
            
                try:
                    msh = self.make_mesh()
                    self.write_mesh_to_file(msh, filename)
                except Exception as e:
                    print(f"An error occurred while creating the mesh for nx={nx}: {e}")
            else:
                print(f"Mesh for nx={nx} already exists")                
                