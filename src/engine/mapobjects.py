from engine.block import Block
from engine.coordinate import Point3D
from engine.polygon import Polygon

class Tree(Block):
    def __init__(self, gridX, gridZ, edgeLength):
        Block.__init__(self, gridX, gridZ, edgeLength)
        
    def initPolygons(self):
        halfEdgeLength = self.edgeLength / 2
        thirdEdgeLength = self.edgeLength / 3
        
        x1 = self.gridX * self.edgeLength
        x2 = self.gridX * self.edgeLength + thirdEdgeLength
        x3 = self.gridX * self.edgeLength + self.edgeLength - thirdEdgeLength
        x4 = self.gridX * self.edgeLength + self.edgeLength
        
        z1 = self.gridZ * self.edgeLength
        z2 = self.gridZ * self.edgeLength + thirdEdgeLength
        z3 = self.gridZ * self.edgeLength + self.edgeLength - thirdEdgeLength
        z4 = self.gridZ * self.edgeLength + self.edgeLength
        
        y1 = -halfEdgeLength
        y2 = halfEdgeLength
        y3 = self.edgeLength + halfEdgeLength
        
        #stem bottom
        stemPoint1 = Point3D(x2, y1, z2)
        stemPoint2 = Point3D(x3, y1, z2)
        stemPoint3 = Point3D(x3, y1, z3)
        stemPoint4 = Point3D(x2, y1, z3)
        
        #stem top
        stemPoint5 = Point3D(x2, y2, z2)
        stemPoint6 = Point3D(x3, y2, z2)
        stemPoint7 = Point3D(x3, y2, z3)
        stemPoint8 = Point3D(x2, y2, z3)
        
        #tree crown bottom
        crownPoint1 = Point3D(x1, y2, z1)
        crownPoint2 = Point3D(x4, y2, z1)
        crownPoint3 = Point3D(x4, y2, z4)
        crownPoint4 = Point3D(x1, y2, z4)
        
        #tree crown top
        crownPoint5 = Point3D(x1, y3, z1)
        crownPoint6 = Point3D(x4, y3, z1)
        crownPoint7 = Point3D(x4, y3, z4)
        crownPoint8 = Point3D(x1, y3, z4)
        
        self.polygons.append(
                 Polygon('{}p1'.format(self.blockId),
                         [stemPoint1, stemPoint2, stemPoint6, stemPoint5],
                         fill='#665223', outline='#453818'))
        self.polygons.append(
                 Polygon('{}p2'.format(self.blockId),
                         [stemPoint2, stemPoint3, stemPoint7, stemPoint6],
                         fill='#665223', outline='#453818'))
        self.polygons.append(
                 Polygon('{}p3'.format(self.blockId),
                         [stemPoint3, stemPoint4, stemPoint8, stemPoint7],
                         fill='#665223', outline='#453818'))
        self.polygons.append(
                 Polygon('{}p4'.format(self.blockId),
                         [stemPoint4, stemPoint1, stemPoint5, stemPoint8],
                         fill='#665223', outline='#453818'))
        
        
        self.polygons.append(
                 Polygon('{}p5'.format(self.blockId),
                         [crownPoint1, crownPoint2, crownPoint6, crownPoint5],
                         fill='#1c8d16', outline='#1c5c16'))
        self.polygons.append(
                 Polygon('{}p6'.format(self.blockId),
                         [crownPoint2, crownPoint3, crownPoint7, crownPoint6],
                         fill='#1c8d16', outline='#1c5c16'))
        self.polygons.append(
                 Polygon('{}p7'.format(self.blockId),
                         [crownPoint3, crownPoint4, crownPoint8, crownPoint7],
                         fill='#1c8d16', outline='#1c5c16'))
        self.polygons.append(
                 Polygon('{}p8'.format(self.blockId),
                         [crownPoint4, crownPoint1, crownPoint5, crownPoint8],
                         fill='#1c8d16', outline='#1c5c16'))
        
        self.polygons.append(
                 Polygon('{}p9'.format(self.blockId),
                         [crownPoint1, crownPoint2, crownPoint3, crownPoint4],
                         fill='#1c8d16', outline='#1c5c16'))


class Floor(Block):
    def __init__(self, gridX, gridZ, edgeLength):
        Block.__init__(self, gridX, gridZ, edgeLength)
        
    def initPolygons(self):
        x1 = self.gridX * self.edgeLength
        x2 = self.gridX * self.edgeLength + self.edgeLength
        
        z1 = self.gridZ * self.edgeLength
        z2 = self.gridZ * self.edgeLength + self.edgeLength
        
        halfEdgeLength = self.edgeLength / 2
        y1 = -halfEdgeLength
        
        point1 = Point3D(x1, y1, z1)
        point2 = Point3D(x2, y1, z1)
        point3 = Point3D(x2, y1, z2)
        point4 = Point3D(x1, y1, z2)
        
        self.polygons.append(Polygon('{}p1'.format(self.blockId),
                                     [point1, point2, point3, point4],
                                     fill='#9e9e9e', outline='#9e9e9e'))
