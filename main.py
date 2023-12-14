#preamble
import numpy as np 
import matplotlib.pyplot as plt 
import numpy.linalg as la

#naming convention: camelCase
#no unnamed or undocumented variables or functions please 

#documentation of variables
point = tuple[float, float] | np.ndarray
edge  = tuple[point, point] | np.ndarray # on the form (node,node,norm(node,node))

#init and methods pertaining to a single element in the mesh
class Triangle: 
    
    #the triangle is initialized with its three corners and the corresponding edges (they might be unnecessary dunno)
    def __init__(self, corner1: point, corner2: point, corner3: point, func): 
        self.corner1 = corner1
        self.corner2 = corner2
        self.corner3 = corner3

        self.func = func

        if not self.MinimumAngle(): 
            raise Exception('Angle in triangle too small')

    #task 2, write a method that calculates the absolute of the jacobian determinant for one self's transformation
    def JacobianOfTransformationDeterminant(self) -> float: 
        return abs(la.det(np.array([[self.corner2[0] - self.corner1[0], self.corner3[0] - self.corner1[0]],
                                    [self.corner2[1] - self.corner1[1], self.corner3[1] - self.corner1[1]]])))

    #task 3, compute minimum angle between edges and determine whether it is too small or not
    def MinimumAngle(self) -> bool: 
        return True
    
    def VolumeOfPrism(self) -> float: 
        return (
        self.JacobianOfTransformationDeterminant() *
        sum((self.func(*self.corner1),  
             self.func(*self.corner2), 
             self.func(*self.corner3))) * 
        (1/6)) 

    def __add__(self, other) -> float: 
        return self.VolumeOfPrism() + other

    def __radd__(self, other) -> float: 
        return self.VolumeOfPrism() + other

#init and methods pertaining to all the elements in the mesh
class Mesh: 
    
    #initialized with the meshlayers points and triangles
    def __init__(self, nodePath: str, coordPath: str, func):
        self.func = func
        self.points = ReadCoordFile(coordPath)
        self.triangles = ReadNodeFile(nodePath,self.points,self.func)
        

    #task 6, method which computes the sum of all triangles in a function f(x,y) describing an area
    def TotalTriangleArea(self) -> float:
        return sum(self.triangles)

#task 7, draw the mesh as in figure 1  (see instruction, extension pdf preview might be needed if in vscode)
def DrawMesh(mesh): 
    pass
    
#task 8, call relevant methods and initialize classes to calculate the areas of the files provided in ./meshes (in particular dolfin) 

def ReadCoordFile(path: str) -> list: 
    with open(path,'r') as f: 
        x,y = f.readlines()
        x,y = x.split(),y.split()

        coordinates = []

        for ind,_ in enumerate(x): 
            coordinates.append((float(x[ind]),float(y[ind])))
        
        return coordinates

def ReadNodeFile(path: str, coordinates: list, func) -> list:
    with open(path, 'r') as f: 
        p1,p2,p3 = f.readlines()
        p1,p2,p3 = p1.split(),p2.split(),p3.split()

        triangles = []

        for ind,_ in enumerate(p1): 
            triangles.append(Triangle(
                coordinates[int(float(p1[ind])) - 1],
                coordinates[int(float(p2[ind])) - 1],
                coordinates[int(float(p3[ind])) - 1],
                func
            ))
        return triangles

#main, initialising instances etc is done here 
def main(): 
    f = lambda x, y : 1
    mesh = Mesh('meshes/nodes_dolphin_coarse.txt', 'meshes/coordinates_dolphin_coarse.txt', f)
    print(1 - mesh.TotalTriangleArea())

if __name__ == '__main__': 
    main()
