from itertools import product
import numpy as np
import os

class MeshMaker:
    def __init__(self,):
        pass

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
    
    def gmsh_boundaries_tet(self, nx, nele = 0):
        ele = ''
        ind = lambda i, j, k: self.grid_index(nx, nx, i, j, k)

        for i1 in range(nx-1):
            for i2 in range(nx-1):
                # WEST 1: i=0
                nele += 1
                n = [ind(0, i2+0, i1+0),
                    ind(0, i2+1, i1+0),
                    ind(0, i2+0, i1+1)]

                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 2 2 2 2 {n_str}\n'

                # WEST 2: i=0
                nele += 1
                n = [ind(0, i2+0, i1+1),
                    ind(0, i2+1, i1+0),
                    ind(0, i2+1, i1+1)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 2 2 2 2 {n_str}\n'

                # EAST 1: i=nx-1
                nele += 1
                n = [ind(nx-1, i2+0, i1+0),
                    ind(nx-1, i2+0, i1+1),
                    ind(nx-1, i2+1, i1+0)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 2 2 5 5 {n_str}\n'

                # EAST 2: i=nx-1
                nele += 1
                n = [ind(nx-1, i2+0, i1+1),
                    ind(nx-1, i2+1, i1+1),
                    ind(nx-1, i2+1, i1+0)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 2 2 5 5 {n_str}\n'

                # SOUTH 1: j=0
                nele += 1
                n = [ind(i2+0, 0, i1+0),
                    ind(i2+0, 0, i1+1),
                    ind(i2+1, 0, i1+0)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 2 2 3 3 {n_str}\n'

                # SOUTH 2: j=0
                nele += 1
                n = [ind(i2+1, 0, i1+0),
                    ind(i2+0, 0, i1+1),
                    ind(i2+1, 0, i1+1)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 2 2 3 3 {n_str}\n'

                # NORTH 1: j=nx-1
                nele += 1
                n = [ind(i2+0, nx-1, i1+0),
                    ind(i2+1, nx-1, i1+0),
                    ind(i2+0, nx-1, i1+1)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 2 2 6 6 {n_str}\n'

                # NORTH 2: j=nx-1
                nele += 1
                n = [ind(i2+1, nx-1, i1+0),
                    ind(i2+1, nx-1, i1+1),
                    ind(i2+0, nx-1, i1+1)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 2 2 6 6 {n_str}\n'

                # BOTTOM 1: k=0
                nele += 1
                n = [ind(i2+0, i1+0, 0),
                    ind(i2+1, i1+0, 0),
                    ind(i2+0, i1+1, 0)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 2 2 4 4 {n_str}\n'

                # BOTTOM 2: k=0
                nele += 1
                n = [ind(i2+1, i1+0, 0),
                    ind(i2+1, i1+1, 0),
                    ind(i2+0, i1+1, 0)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 2 2 4 4 {n_str}\n'

                # TOP 1: k=nx-1
                nele += 1
                n = [ind(i2+0, i1+0, nx-1),
                    ind(i2+0, i1+1, nx-1),
                    ind(i2+1, i1+0, nx-1)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 2 2 7 7 {n_str}\n'

                # TOP 2: k=nx-1
                nele += 1
                n = [ind(i2+1, i1+0, nx-1),
                    ind(i2+0, i1+1, nx-1),
                    ind(i2+1, i1+1, nx-1)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 2 2 7 7 {n_str}\n'

        return nele, ele

    def gmsh_boundaries_pyr(self, nx, nele = 0):
        ele = ''

        ind = lambda i, j, k: self.grid_index(nx, nx, i, j, k)
        for i1 in range(nx-1):
            for i2 in range(nx-1):
                # WEST: i=0
                nele += 1
                n = [ind(0, i2+0, i1+0),
                    ind(0, i2+0, i1+1),
                    ind(0, i2+1, i1+1),
                    ind(0, i2+1, i1+0)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 3 2 2 2 {n_str}\n'

                # EAST: i=nx-1
                nele += 1
                n = [ind(nx-1, i2+0, i1+0),
                    ind(nx-1, i2+0, i1+1),
                    ind(nx-1, i2+1, i1+1),
                    ind(nx-1, i2+1, i1+0)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 3 2 5 5 {n_str}\n'

                # SOUTH: j=0
                nele += 1
                n = [ind(i2+0, 0, i1+0),
                    ind(i2+1, 0, i1+0),
                    ind(i2+1, 0, i1+1),
                    ind(i2+0, 0, i1+1)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 3 2 3 3 {n_str}\n'

                # NORTH: j=nx-1
                nele += 1
                n = [ind(i2+0, nx-1, i1+0),
                    ind(i2+1, nx-1, i1+0),
                    ind(i2+1, nx-1, i1+1),
                    ind(i2+0, nx-1, i1+1)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 3 2 6 6 {n_str}\n'

                # BOTTOM: k=0
                nele += 1
                n = [ind(i2+0, i1+0, 0),
                    ind(i2+1, i1+0, 0),
                    ind(i2+1, i1+1, 0),
                    ind(i2+0, i1+1, 0)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 3 2 4 4 {n_str}\n'

                # TOP: k=nx-1
                nele += 1
                n = [ind(i2+0, i1+0, nx-1),
                    ind(i2+1, i1+0, nx-1),
                    ind(i2+1, i1+1, nx-1),
                    ind(i2+0, i1+1, nx-1)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 3 2 7 7 {n_str}\n'

        return nele, ele

    def gmsh_boundaries_pri(self, nx, nele = 0):
        ele = ''
        ind = lambda i, j, k: self.grid_index(nx, nx, i, j, k)

        for i1 in range(nx-1):
            for i2 in range(nx-1):
                # i=0
                nele += 1
                n = [ind(0, i2+0, i1+0), ind(0, i2+1, i1+0),
                    ind(0, i2+1, i1+1), ind(0, i2+0, i1+1)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 3 2 2 2 {n_str}\n'

                # i=nx-1
                nele += 1
                n = [ind(nx-1, i2+0, i1+0), ind(nx-1, i2+1, i1+0),
                    ind(nx-1, i2+1, i1+1), ind(nx-1, i2+0, i1+1)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 3 2 5 5 {n_str}\n'

                # j=0
                nele += 1
                n = [ind(i2+0, 0, i1+0), ind(i2+1, 0, i1+0),
                    ind(i2+1, 0, i1+1), ind(i2+0, 0, i1+1)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 3 2 3 3 {n_str}\n'

                # j=nx-1
                nele += 1
                n = [ind(i2+0, nx-1, i1+0), ind(i2+1, nx-1, i1+0),
                    ind(i2+1, nx-1, i1+1), ind(i2+0, nx-1, i1+1)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 3 2 6 6 {n_str}\n'

                # k=0
                nele += 1
                n = [ind(i2+0, i1+0, 0), 
                    ind(i2+0, i1+1, 0),
                    ind(i2+1, i1+0, 0)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 2 2 4 4 {n_str}\n'

                nele += 1
                n = [ind(i2+1, i1+1, 0), 
                    ind(i2+0, i1+1, 0),
                    ind(i2+1, i1+0, 0)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 2 2 4 4 {n_str}\n'

                # k=nx-1
                nele += 1
                n = [ind(i2+0, i1+0, nx-1), 
                    ind(i2+0, i1+1, nx-1),
                    ind(i2+1, i1+0, nx-1)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 2 2 7 7 {n_str}\n'

                nele += 1
                n = [ind(i2+1, i1+1, nx-1), 
                    ind(i2+0, i1+1, nx-1),
                    ind(i2+1, i1+0, nx-1)]
                # Id Type NumTags PhysGrp ElemGrp IndexList
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 2 2 7 7 {n_str}\n'
        
        return nele, ele

    def gmsh_boundaries_hex(self, nx, nele = 0):
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

    def gmsh_elements_pri(self, nx):
        nele, ele = self.gmsh_boundaries_pri(nx)

        ind = lambda i, j, k: self.grid_index(nx, nx, i, j, k)

        # elm-number elm-type number-of-tags < tag > & node-number-list
        for k in range(nx - 1):
            for j in range(nx - 1):
                for i in range(nx - 1):
                    nele += 1
                    n = [ind(i+0, j+0, k+0),
                        ind(i+0, j+1, k+0),
                        ind(i+1, j+0, k+0),
                        ind(i+0, j+0, k+1),
                        ind(i+0, j+1, k+1),
                        ind(i+1, j+0, k+1)]
                    n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                    ele += f'{nele} 6 2 1 1 {n_str} \n'
                    nele += 1
                    n = [ind(i+1, j+1, k+0),
                        ind(i+0, j+1, k+0),
                        ind(i+1, j+0, k+0),
                        ind(i+1, j+1, k+1),
                        ind(i+0, j+1, k+1),
                        ind(i+1, j+0, k+1)]
                    n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                    ele += f'{nele} 6 2 1 1 {n_str} \n'

        return f'$Elements\n{nele}\n' + ele + '$EndElements\n'

    def gmsh_elements_pyr(self, nx):
        nele, ele = self.gmsh_boundaries_pyr(nx)
        moff = nx*nx*nx

        ind = lambda i, j, k: self.grid_index(nx, nx, i, j, k)
        mind = lambda i, j, k: moff + self.grid_index(nx-1, nx-1, i, j, k)

        # elm-number elm-type number-of-tags < tag > & node-number-list
        for k in range(nx - 1):
            for j in range(nx - 1):
                for i in range(nx - 1):
                    # Bottom
                    nele += 1
                    n = [ind(i+0, j+0, k),
                        ind(i+1, j+0, k),
                        ind(i+1, j+1, k),
                        ind(i+0, j+1, k),
                        mind(i, j, k)]
                    n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                    ele += f'{nele} 7 2 1 1 {n_str} \n'

                    # Top
                    nele += 1
                    n = [ind(i+0, j+0, k+1),
                        ind(i+1, j+0, k+1),
                        ind(i+1, j+1, k+1),
                        ind(i+0, j+1, k+1),
                        mind(i, j, k)]
                    n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                    ele += f'{nele} 7 2 1 1 {n_str} \n'

                    # East
                    nele += 1
                    n = [ind(i+1, j+0, k+0),
                        ind(i+1, j+0, k+1),
                        ind(i+1, j+1, k+1),
                        ind(i+1, j+1, k+0),
                        mind(i, j, k)]
                    n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                    ele += f'{nele} 7 2 1 1 {n_str} \n'

                    # West
                    nele += 1
                    n = [ind(i+0, j+0, k+0),
                        ind(i+0, j+0, k+1),
                        ind(i+0, j+1, k+1),
                        ind(i+0, j+1, k+0),
                        mind(i, j, k)]
                    n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                    ele += f'{nele} 7 2 1 1 {n_str} \n'

                    # South
                    nele += 1
                    n = [ind(i+0, j+0, k+0),
                        ind(i+1, j+0, k+0),
                        ind(i+1, j+0, k+1),
                        ind(i+0, j+0, k+1),
                        mind(i, j, k)]
                    n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                    ele += f'{nele} 7 2 1 1 {n_str} \n'

                    # North
                    nele += 1
                    n = [ind(i+0, j+1, k+0),
                        ind(i+1, j+1, k+0),
                        ind(i+1, j+1, k+1),
                        ind(i+0, j+1, k+1),
                        mind(i, j, k)]
                    n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                    ele += f'{nele} 7 2 1 1 {n_str} \n'

        return f'$Elements\n{nele}\n' + ele + '$EndElements\n'
 
    def gmsh_elements_tet(self, nx):
        nele, ele = self.gmsh_boundaries_tet(nx)
        moff = nx*nx*nx

        ind = lambda i, j, k: self.grid_index(nx, nx, i, j, k)
        mind = lambda i, j, k: moff + self.grid_index(nx-1, nx-1, i, j, k)

        # elm-number elm-type number-of-tags < tag > & node-number-list
        for k in range(nx - 1):
            for j in range(nx - 1):
                for i in range(nx - 1):
                    # Bottom 1
                    nele += 1
                    n = [ind(i+0, j+0, k+0),
                        ind(i+1, j+0, k+0),
                        ind(i+0, j+1, k+0),
                        mind(i, j, k)]
                    n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                    ele += f'{nele} 4 2 1 1 {n_str} \n'

                    # Bottom 2
                    nele += 1
                    n = [ind(i+1, j+0, k+0),
                        ind(i+1, j+1, k+0),
                        ind(i+0, j+1, k+0),
                        mind(i, j, k)]
                    n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                    ele += f'{nele} 4 2 1 1 {n_str} \n'

                    # Top 1
                    nele += 1
                    n = [ind(i+0, j+0, k+1),
                        ind(i+0, j+1, k+1),
                        ind(i+1, j+0, k+1),
                        mind(i, j, k)]
                    n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                    ele += f'{nele} 4 2 1 1 {n_str} \n'

                    # Top 2
                    nele += 1
                    n = [ind(i+1, j+0, k+1),
                        ind(i+0, j+1, k+1),
                        ind(i+1, j+1, k+1),
                        mind(i, j, k)]
                    n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                    ele += f'{nele} 4 2 1 1 {n_str} \n'

                    # East 1
                    nele += 1
                    n = [ind(i+1, j+0, k+0),
                        ind(i+1, j+0, k+1),
                        ind(i+1, j+1, k+0),
                        mind(i, j, k)]
                    n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                    ele += f'{nele} 4 2 1 1 {n_str} \n'

                    # East 2
                    nele += 1
                    n = [ind(i+1, j+0, k+1),
                        ind(i+1, j+1, k+1),
                        ind(i+1, j+1, k+0),
                        mind(i, j, k)]
                    n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                    ele += f'{nele} 4 2 1 1 {n_str} \n'

                    # West 1
                    nele += 1
                    n = [ind(i+0, j+0, k+0),
                        ind(i+0, j+1, k+0),
                        ind(i+0, j+0, k+1),
                        mind(i, j, k)]
                    n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                    ele += f'{nele} 4 2 1 1 {n_str} \n'

                    # West 2
                    nele += 1
                    n = [ind(i+0, j+0, k+1),
                        ind(i+0, j+1, k+0),
                        ind(i+0, j+1, k+1),
                        mind(i, j, k)]
                    n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                    ele += f'{nele} 4 2 1 1 {n_str} \n'

                    # South 1
                    nele += 1
                    n = [ind(i+0, j+0, k+0),
                        ind(i+0, j+0, k+1),
                        ind(i+1, j+0, k+0),
                        mind(i, j, k)]
                    n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                    ele += f'{nele} 4 2 1 1 {n_str} \n'

                    # South 2
                    nele += 1
                    n = [ind(i+1, j+0, k+0),
                        ind(i+0, j+0, k+1),
                        ind(i+1, j+0, k+1),
                        mind(i, j, k)]
                    n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                    ele += f'{nele} 4 2 1 1 {n_str} \n'

                    # North 1
                    nele += 1
                    n = [ind(i+0, j+1, k+0),
                        ind(i+1, j+1, k+0),
                        ind(i+0, j+1, k+1),
                        mind(i, j, k)]
                    n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                    ele += f'{nele} 4 2 1 1 {n_str} \n'

                    # North 2
                    nele += 1
                    n = [ind(i+1, j+1, k+0),
                        ind(i+1, j+1, k+1),
                        ind(i+0, j+1, k+1),
                        mind(i, j, k)]
                    n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                    ele += f'{nele} 4 2 1 1 {n_str} \n'

        return f'$Elements\n{nele}\n' + ele + '$EndElements\n'

    def gmsh_elements_hex(self, nx):
        nele, ele = self.gmsh_boundaries_hex(nx)
        elements = []

        # elm-number elm-type number-of-tags < tag > â¦ node-number-list
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

    def make_mesh(self, etype, nx):
        R = np.linspace(0, self.l, nx)
        header = self.gmsh_header()

        if etype == 'tet':    

            dx = R[1] - R[0]
            M = np.linspace(0.5*dx, self.l - 0.5*dx, nx-1)

            X = np.zeros((nx*nx*nx + (nx-1)*(nx-1)*(nx-1), 3))
            i = 0
            for rz in R:
                for ry in R:
                    for rx in R:
                        X[i,:] = [rx, ry, rz]
                        i += 1

            for mz in M:
                for my in M:
                    for mx in M:
                        X[i,:] = [mx, my, mz]
                        i += 1

            nodes = self.gmsh_nodes(X)
            elements = self.gmsh_elements_tet(nx)

        elif etype == 'pyr':

            dx = R[1] - R[0]
            M = np.linspace(0.5*dx, self.l - 0.5*dx, nx-1)

            X = np.zeros((nx*nx*nx + (nx-1)*(nx-1)*(nx-1), 3))

            i = 0
            for rz in R:
                for ry in R:
                    for rx in R:
                        X[i,:] = [rx, ry, rz]
                        i += 1

            for mz in M:
                for my in M:
                    for mx in M:
                        X[i,:] = [mx, my, mz]
                        i += 1

            header = self.gmsh_header()
            nodes = self.gmsh_nodes(X)
            elements = self.gmsh_elements_pyr(nx)

        elif etype == 'pri':
            X = np.zeros((nx*nx*nx, 3))

            i = 0
            for rz in R:
                for ry in R:
                    for rx in R:
                        X[i,:] = [rx, ry, rz]
                        i += 1
            
            header = self.gmsh_header()
            nodes = self.gmsh_nodes(X)
            elements = self.gmsh_elements_pri(nx)

        elif etype == 'hex':
            X = np.array([np.array([rx, ry, rz]) for rz, ry, rx in product(R, repeat=3)])
            nodes = self.gmsh_nodes(X)
            elements = self.gmsh_elements_hex(nx)

        else:
            raise ValueError(f"Mesh type {etype} not recognized")

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

    def make_meshes(self, nx_values, netype):

        os.system("mkdir -p meshes")

        for nx, etype in zip(nx_values, netype):

            if etype in ['tet', 'pyr', 'pri', 'hex',]:
                pass
            else:
                raise ValueError(f"Mesh type {etype} not recognized")

            self.l = 6.28318530718
            filename = f'meshes/{etype}{nx}.msh'

            if not os.path.isfile(filename):
            
                try:
                    msh = self.make_mesh(etype, nx)
                    self.write_mesh_to_file(msh, filename)
                except Exception as e:
                    print(f"An error occurred while creating the mesh for nx={nx}: {e}")
            else:
                print(f"Mesh  exists: {filename}")                
