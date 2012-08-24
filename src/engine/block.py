from engine.coordinate import Point3D
from engine.polygon import Polygon

from threading import Lock

class Block(object):
    '''a block is represented by its 4 surrounding polygons'''
    count = 0
    mutex = Lock()
     
    def __init__(self, gridX, gridZ, edgeLength):
        self.gridX = gridX
        self.gridZ = gridZ
        self.edgeLength = edgeLength
        self.polygons = []
        
        # using mutex for unique IDs if several threads try to create blocks
        Block.mutex.acquire()
        try:
            self.blockId = 'b{}'.format(Block.count)
            Block.count += 1
        finally:
            Block.mutex.release()
        
        
        
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
        
        self.polygons.append(Polygon('{}p1'.format(self.blockId),
                                     point1, point2, point6, point5))
        self.polygons.append(Polygon('{}p2'.format(self.blockId),
                                     point2, point3, point7, point6))
        self.polygons.append(Polygon('{}p3'.format(self.blockId),
                                     point3, point4, point8, point7))
        self.polygons.append(Polygon('{}p4'.format(self.blockId),
                                     point4, point1, point5, point8))
    
    def getPolygons(self):
        return self.polygons
