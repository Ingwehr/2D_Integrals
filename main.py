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

        if self.TooSmallAngle(): 
            raise Exception('Angle in triangle too small')

    def JacobianDeterminant(self) -> float: 
        return abs(la.det(np.array([[self.corner2[0] - self.corner1[0], self.corner3[0] - self.corner1[0]],
                                    [self.corner2[1] - self.corner1[1], self.corner3[1] - self.corner1[1]]])))

    def TooSmallAngle(self) -> bool: 
        return False
    
    def VolumeOfPrism(self) -> float: 
        return self.JacobianDeterminant() * (1/6) * (self.func(*self.corner1) + self.func(*self.corner2) + self.func(*self.corner3)) 

    def __add__(self, other) -> float: 
        return self.VolumeOfPrism() + other

    def __radd__(self, other) -> float: 
        return self.VolumeOfPrism() + other

class Mesh: 
    def __init__(self, nodePath: str, coordPath: str, func) -> None:
        self.func = func
        self.points = ReadCoordFile(coordPath)
        self.triangles = ReadNodeFile(nodePath,self.points,self.func)
        
    def TotalTriangleArea(self) -> float:
        return sum(self.triangles)

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
            func))
    return triangles

def main(): 
    f = lambda x, y : 1
    mesh = Mesh('meshes/nodes_unitcircle_10000.txt', 'meshes/coordinates_unitcircle_10000.txt', f)
    print(np.pi * 2 - mesh.TotalTriangleArea())

if __name__ == '__main__': 
    main()