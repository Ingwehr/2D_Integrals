#preamble
import numpy as np 
import matplotlib.pyplot as plt 
import numpy.linalg as la

#naming convention: camelCase
#no unnamed or undocumented variables or functions please 

#documentation of variables
point = tuple[float, float] | np.ndarray
#edge  = tuple[point, point] | np.ndarray # on the form (node,node,norm(node,node))

#init and methods pertaining to a single element in the mesh
class Triangle: 
    
    #the triangle is initialized with its three corners and the corresponding edges (they might be unnecessary dunno)
    def __init__(self, corner1: point, corner2: point, corner3: point): 
        self.corner1 = corner1
        self.corner2 = corner2
        self.corner3 = corner3

    #check if a point p is inside the instance or outside
    def PointInTriangle(self,p: point) -> bool: 
        v1 = (self.corner2[1] - self.corner1[1],-self.corner2[0] + self.corner1[0])
        v2 = (self.corner3[1] - self.corner2[1],-self.corner3[0] + self.corner2[0])
        v3 = (self.corner1[1] - self.corner3[1],-self.corner1[0] + self.corner3[0])

        v_1 = (p[0] - self.corner1[0], p[1] - self.corner1[1])
        v_2 = (p[0] - self.corner2[0], p[1] - self.corner2[1])
        v_3 = (p[0] - self.corner3[0], p[1] - self.corner3[1])

        #if the signs match, then return True, else False
        return np.sign(np.dot(v1,v_1)) == np.sign(np.dot(v2,v_2)) == np.sign(np.dot(v3,v_3))

    #task 2, write a method that calculates the jacobian for one elements transformation
    def JacobianOfTransformation(self) -> float: 
        return abs(la.matrix.det(np.array([self.corner2[0] - self.corner1[0], self.corner3[0] - self.corner1[0]],
                                          [self.corner2[1] - self.corner1[1], self.corner3[1] - self.corner1[1]])))

    #task 3, compute minimum angle between edges and determine whether it is too small or not
    def IsMinimumAngleInTriangleSmol() -> bool: 
        pass 
    
    #printing the insteance returns '(c1,c2,c3)'
    def __str__(self) -> None: 
        print(f'({self.corner1},{self.corner2},{self.corner3})')

    def AreaOfTriangle(self) -> float: 
        pass

#init and methods pertaining to all the elements in the mesh
class Mesh: 
    
    #initialized with the meshlayers points and triangles
    def __init__(self,nodePath,coordPath):
        self.points = ReadCoordFile(coordPath)
        self.triangles = ReadNodeFile(nodePath,self.points)

    def InsideArea(self,p: point) -> bool:
        for t in self.triangles: 
            if t.PointInTriangle(p): 
                return True
        return False

    #task 5, method which computes I_omega for any given function f
    def IntegralOfOmega(): 
        pass

    #task 6, method which computes the sum of all triangles in a mesh
    def TotalTriangleArea() -> float:
        pass

    def __str__(self): 
        print(f'({self.points},{self.triangles})')

#task 7, draw the mesh as in figure 1  (see instruction, extension pdf preview might be needed if in vscode)
def DrawMesh(mesh): 
    pass
    
#task 8, call relevant methods and initialize classes to calculate the areas of the files provided in ./meshes (in particular dolfin) 

def ReadCoordFile(path: str) -> list: 
    with open(path,'r') as f: 
        x,y = f.readlines()
    coordinates = []
    for ind,element in x: 
        coordinates.append(tuple(x[ind],y[ind]))
    return(coordinates)

def ReadNodeFile(path: str, coordinates: list) -> list:
    with open(path,'r') as f: 
        p1,p2,p3 = f.readlines()
    triangles = []        
    for ind,element in p1: 
        triangles.append(Triangle(coordinates[p1[ind+1]],coordinates[p2[ind+1]],coordinates[p3[ind+1]]))
    return(triangles)


#main, initialising instances etc is done here 
def main(): 
    pass

if __name__ == '__main__': 
    main()
