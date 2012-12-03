from engine.coordinate import Point3D
from engine.polygon import Polygon

class Block(object):
    '''a block is represented by its 4 surrounding polygons'''
     
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.polygons = []
        
        self.initPolygons()
    
    def initPolygons(self):
        x1 = self.point1.x
        y1 = self.point1.y
        z1 = self.point1.z
        
        x2 = self.point2.x
        y2 = self.point2.y
        z2 = self.point2.z
        
        point1 = Point3D(x1, y1, z1)
        point2 = Point3D(x2, y1, z1)
        point3 = Point3D(x2, y2, z1)
        point4 = Point3D(x1, y2, z1)
        point5 = Point3D(x1, y1, z2)
        point6 = Point3D(x2, y1, z2)
        point7 = Point3D(x2, y2, z2)
        point8 = Point3D(x1, y2, z2)
        
        self.polygons.append(Polygon('',
                                     [point1, point2, point3, point4]))
        self.polygons.append(Polygon('',
                                     [point2, point6, point7, point3]))
        self.polygons.append(Polygon('',
                                     [point6, point5, point8, point7]))
        self.polygons.append(Polygon('',
                                     [point5, point1, point4, point8]))
    
    def getPolygons(self):
        return self.polygons
