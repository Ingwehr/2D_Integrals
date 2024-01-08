#preamble
import numpy as np 
import matplotlib.pyplot as plt 
import numpy.linalg as la
from matplotlib.patches import *

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
            raise Exception('Triangle too thin')

    def JacobianDeterminant(self) -> float: 
        return abs(la.det(np.array([[self.corner2[0] - self.corner1[0], self.corner3[0] - self.corner1[0]],
                                    [self.corner2[1] - self.corner1[1], self.corner3[1] - self.corner1[1]]])))

    def TooSmallAngle(self) -> bool: 
        edges = [np.sqrt((self.corner1[0] - self.corner2[0])**2 + (self.corner1[1] - self.corner2[1])**2),
                 np.sqrt((self.corner2[0] - self.corner3[0])**2 + (self.corner2[1] - self.corner3[1])**2),
                 np.sqrt((self.corner3[0] - self.corner1[0])**2 + (self.corner3[1] - self.corner1[1])**2)]
        
        edges.sort()
        
        return np.arccos(((edges[2] * edges[2]) + edges[1] * edges[1] - edges[0] * edges[0]) / (2 * edges[1] * edges[2])) < (np.pi / 32)
    
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
def ReadNodeForPlot(path: str):
    with open(path, 'r') as f: 
        p1,p2,p3 = f.readlines()
        p1,p2,p3 = p1.split(),p2.split(),p3.split()
        
    nodes = []

    for ind,_ in enumerate(p1): 
        nodes.append((int(float(p1[ind])),int(float(p2[ind])),int(float(p3[ind]))))
    
    return nodes

def plot(nodess:str , coordinatess:str) -> None:
    coords_plot=ReadCoordFile(coordinatess)
    nodes_plot=ReadNodeForPlot(nodess)
    pre_final_points=[]
    for i in range(len(nodes_plot)):
        plot_points=[]
        for j in range(3):
            points=coords_plot[nodes_plot[i][j]-1]
            if (points[0]<1e-10 and points[0]>0) or (points[0]>-1e-10 and points[0]<0):
                points=list(points)
                points[0]=0
                points=tuple(points)
            if (points[1]<1e-10 and points[1]>0) or (points[1]>-1e-10 and points[1]<0):
                points=list(points)
                points[1]=0
                points=tuple(points)
            plot_points.append(points)
        pre_final_points.append(plot_points)
    final_points=[]
    for i in pre_final_points:
        x_c=(i[0][0]+i[1][0]+i[2][0])/3
        y_c=(i[0][1]+i[1][1]+i[2][1])/3
        if (x_c<1e-5 and x_c>0) or (x_c>-1e-5 and x_c<0):
            x_c=0
        if (y_c<1e-5 and y_c>0) or (y_c>-1e-5 and y_c<0):
            y_c=0
        centroid=[x_c,y_c]
        resized_points=[]
        for j in i:
            if j[1]!=centroid[1]:
                #change number for different resolution
                if j[1]<centroid[1]:
                    y=j[1]-((j[1]-centroid[1])/10)
                elif j[1]>centroid[1]:
                    y=j[1]-((j[1]-centroid[1])/10)
                x_1=centroid[0]
                x_2=j[0]
                y_1=centroid[1]
                y_2=j[1]
                x=((y*x_1 - y*x_2 - x_1*y_1 + x_2*y_1)/(y_1 - y_2))+x_1
            else:
                if j[0]>centroid[0]:
                    x=j[0]-.02
                else:
                    x=j[0]+.02
                y=centroid[1]
            tupled_points=(x,y)
            resized_points.append(tupled_points)
        final_points.append(resized_points)
    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')
    colors = np.random.rand(len(final_points), 3)
    for triangle_points,color in zip(final_points,colors):
        triangle = Polygon(triangle_points, edgecolor=color, linewidth=1, facecolor='None')
        ax.add_patch(triangle)
    ax.set_xlim(-1,1)
    ax.set_ylim(-1,1)
    plt.rcParams['figure.dpi'] = 500
    plt.show()

def main(): 
    f = lambda x, y : 1
    mesh = Mesh('meshes/nodes_unitcircle_10000.txt', 'meshes/coordinates_unitcircle_10000.txt', f)
    print(np.pi * 2 - mesh.TotalTriangleArea())

if __name__ == '__main__': 
    main()
