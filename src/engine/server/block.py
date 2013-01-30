from engine.shared.coordinate import Point3D
from engine.shared.polygon import Polygon

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
                                     [point4, point3, point2, point1]))
        self.polygons.append(Polygon('',
                                     [point3, point7, point6, point2]))
        self.polygons.append(Polygon('',
                                     [point7, point8, point5, point6]))
        self.polygons.append(Polygon('',
                                     [point8, point4, point1, point5]))
    
    def getPolygons(self):
        return self.polygons
