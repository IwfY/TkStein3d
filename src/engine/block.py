from engine.coordinate import Point3D
from engine.polygon import Polygon

class Block(object):
    
    def __init__(self, offsetX, offsetY, edgeLength):
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.edgeLength = edgeLength
        self.polygons = []
        
        self.initPolygons()
    
    def initPolygons(self):
        point1 = Point3D(self.offsetX, self.offsetY, 0)
        point2 = Point3D(self.offsetX + self.edgeLength, self.offsetY, 0)
        point3 = Point3D(self.offsetX + self.edgeLength,
                         self.offsetY + self.edgeLength, 0)
        point4 = Point3D(self.offsetX, self.offsetY + self.edgeLength, 0)
        
        point5 = Point3D(self.offsetX, self.offsetY, self.edgeLength)
        point6 = Point3D(self.offsetX + self.edgeLength,
                         self.offsetY,
                         self.edgeLength)
        point7 = Point3D(self.offsetX + self.edgeLength,
                         self.offsetY + self.edgeLength, self.edgeLength)
        point8 = Point3D(self.offsetX,
                         self.offsetY + self.edgeLength,
                         self.edgeLength)
        
        self.polygons.append(Polygon(point1, point2, point6, point5))
        self.polygons.append(Polygon(point2, point3, point7, point6))
        self.polygons.append(Polygon(point3, point4, point8, point7))
        self.polygons.append(Polygon(point4, point1, point5, point8))