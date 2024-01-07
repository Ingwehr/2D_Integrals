#preamble
import numpy as np 
import matplotlib.pyplot as plt 
import numpy.linalg as la

#naming convention: camelCase
#no unnamed or undocumented variables or functions please 

point = tuple[float, float] | np.ndarray

class Triangle: 
    
    def __init__(self, corner1: point, corner2: point, corner3: point, func): 
        self.corner1 = corner1
        self.corner2 = corner2
        self.corner3 = corner3

        self.func = func

    def JacobianDeterminant(self) -> float:  #height of prism
        return abs(la.det(np.array([[self.corner2[0] - self.corner1[0], self.corner3[0] - self.corner1[0]],
                                    [self.corner2[1] - self.corner1[1], self.corner3[1] - self.corner1[1]]])))
    
class Mesh: 
    def __init__(self, nodePath: str, coordPath: str, func) -> None:
        self.func = func
        self.points = ReadCoordFile(coordPath)
        self.triangles = ReadNodeFile(nodePath,self.points,self.func)
        
    def WriteCoords(self, path: str) -> None:
        #read triangles and get height of each triangle, thi
        with open(path, 'a') as f: 
            
            coordinates = [[],[],[]]
            
            for triangle in self.triangles:
                coordinates[0].extend((triangle.corner1[0],triangle.corner2[0],triangle.corner3[0]))
                coordinates[1].extend((triangle.corner1[1],triangle.corner2[1],triangle.corner3[1]))
                coordinates[2].extend((triangle.JacobianDeterminant(),triangle.JacobianDeterminant(),triangle.JacobianDeterminant()))

            for coordList in coordinates: 
                f.write(','.join(str(element) for element in coordList) + '\n')

                

def ReadCoordFile(path: str) -> list: 
    with open(path,'r') as f: 
        x,y = f.readlines()
        x,y = x.split(), y.split()

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
            func))
    return triangles

def main(): 
    f = lambda x, y : x + y
    mesh = Mesh('exampleMeshes/elementnode1.txt', 'exampleMeshes/coord1.txt', f)
    mesh.WriteCoords('Presentation/Visualisations/visualisation.txt')

main()
