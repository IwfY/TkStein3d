from engine.coordinate import Point3D
from engine.polygon import Polygon

class Block(object):
    '''a block is represented by its 4 surrounding polygons'''
     
    def __init__(self, gridX, gridZ, edgeLength):
        self.gridX = gridX
        self.gridZ = gridZ
        self.edgeLength = edgeLength
        self.polygons = []
        
        self.initPolygons()
    
    def initPolygons(self):
        offsetX = self.gridX * self.edgeLength
        offsetZ = self.gridZ * self.edgeLength
        halfEdgeLength = self.edgeLength / 2
        
        point1 = Point3D(offsetX, -halfEdgeLength, offsetZ)
        point2 = Point3D(offsetX + self.edgeLength, -halfEdgeLength, offsetZ)
        point3 = Point3D(offsetX + self.edgeLength, -halfEdgeLength,
                         offsetZ + self.edgeLength)
        point4 = Point3D(offsetX, -halfEdgeLength, offsetZ + self.edgeLength)
        
        point5 = Point3D(offsetX, halfEdgeLength, offsetZ)
        point6 = Point3D(offsetX + self.edgeLength, halfEdgeLength, offsetZ)
        point7 = Point3D(offsetX + self.edgeLength, halfEdgeLength,
                         offsetZ + self.edgeLength)
        point8 = Point3D(offsetX, halfEdgeLength, offsetZ + self.edgeLength)
        
        self.polygons.append(Polygon(point1, point2, point6, point5))
        self.polygons.append(Polygon(point2, point3, point7, point6))
        self.polygons.append(Polygon(point3, point4, point8, point7))
        self.polygons.append(Polygon(point4, point1, point5, point8))
    
    def getPolygons(self):
        return self.polygons
