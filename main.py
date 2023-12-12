#preamble
import numpy as np 
import matplotlib.pyplot as plt 
import numpy.linalg as la

#naming convention: camelCase
#no unnamed or undocumented variables or functions please 

#documentation of variables
point = tuple[float, float] | np.ndarray
edge  = tuple[point, point] | np.ndarray


#init and methods pertaining to a single element in the mesh
class Triangle: 
    
    #the triangle is initialized with its three corners and the corresponding edges (they might be removed dunno)
    def __init__(self, corner1: point, corner2: point, corner3: point): 
        self.corner1 = corner1
        self.corner2 = corner2
        self.corner3 = corner3

        self.edge1 = (self.corner1, self.corner2)
        self.edge2 = (self.corner2, self.corner3)
        self.edge3 = (self.corner3, self.corner1)


    #method for transforming a triangle to it's equivalent unit triangle, not sure if this will be needed
    def TransformToUnitTriangle(): 
        pass

    #task 2, write a method that calculates the jacobian for one elements transformation
    def JacobianOfTransformation(self) -> float: 
        return la.matrix.det(np.array([self.corner2[0] - self.corner1[0], self.corner3[0] - self.corner1[0]],
                                      [self.corner2[1] - self.corner1[1], self.corner3[1] - self.corner1[1]]))

    #task 3, compute minimum angle between edges and determine whether it is too small or not
    def IsMinimumAngleInTriangleSmol() -> bool: 
        pass

#init and methods pertaining to all the elements in the mesh
class Mesh: 
    
    #should we read the file here or what? separate method for reading the file in the class maybe 
    def __init__():
        pass

    #task 5, method which computes I_omega for any given function f
    def IntegralOfOmega(): 
        pass

    #task 6, method which computes the sum of all triangles in a mesh
    def TriangleArea() -> float:
        pass


#task 7, draw the mesh as in figure 1  (see instruction, extension pdf preview might be needed if in vscode)
def DrawMesh(mesh): 
    pass
    
#task 8, call relevant methods and initialize classes to calculate the areas of the files provided in ./meshes (in particular dolfin) 

#main, initialising instances etc is done here 
def main(): 
    pass

if __name__ == '__main__': 
    main()