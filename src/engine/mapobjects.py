from engine.block import Block
from engine.coordinate import Point3D
from engine.polygon import Polygon, rotateAndMovePolygon

from os import path
from threading import Lock

class MapObjectManager(object):
    count = 0
    mutex = Lock()
    
    def __init__(self):
        self.mapObjectPath = 'engine/resources/mapobjects/'  #TODO make portable
    
    def getPolygonsForMapObjectRotateMove(self,
                                          mapObjectName,
                                          rotationAngle,
                                          movementVector):
        filename = '{}{}.txt'.format(self.mapObjectPath, mapObjectName)
        fileContent = ''
        if path.isfile(filename):
            try:
                file = open(filename, 'r')
                fileContent = file.readlines()        
            finally:
                file.close()
            
            
            # using mutex for unique IDs if several threads try to create
            MapObjectManager.mutex.acquire()
            try:
                mapObjectId = 'mo{}'.format(MapObjectManager.count)
                MapObjectManager.count += 1
            finally:
                MapObjectManager.mutex.release()
                
            colors = {}
            points = {'rotationCenter' : Point3D(0.0, 0.0, 0.0)}
            polygons = []
            
            for line in fileContent:
                parts = line.split()
                if len(parts) > 0:
                    if parts[0] == 'color':
                        colors[parts[1]] = parts[2]
                    elif parts[0] == 'c':
                        points[parts[1]] = Point3D(float(parts[2]),
                                                   float(parts[3]),
                                                   float(parts[4]))
                    elif parts[0] == 'p':
                        newPolygonId = '{}{}'.format(mapObjectId, parts[1])
                        newPolygonPoints = []
                        for i in range(2, len(parts) - 2):
                            if parts[i] in points:
                                newPolygonPoints.append(points[parts[i]])
                        fillColor = ''
                        outlineColor = ''
                        if parts[-2] in colors:
                            fillColor = colors[parts[-2]]
                        if parts[-1] in colors:
                            outlineColor = colors[parts[-1]]
                        newPolygon =  Polygon(newPolygonId,
                                              newPolygonPoints,
                                              fillColor,
                                              outlineColor)
                        polygons.append(newPolygon)
            
            newPolygons = []
            for polygon in polygons:
                transformedPolygon = \
                        rotateAndMovePolygon(polygon,
                                             movementVector,
                                             points['rotationCenter'],
                                             rotationAngle)
                newPolygons.append(transformedPolygon)
            
            return newPolygons
        else:
            return None

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
        
        colorStemFill = '#665223'
        colorStemOutline = '#453818'
        colorCrownFill = '#1c8d16'
        colorCrownOutline = '#1c5c16'
        
        self.polygons.append(
                 Polygon('{}p1'.format(self.blockId),
                         [stemPoint1, stemPoint2, stemPoint6, stemPoint5],
                         fill=colorStemFill, outline=colorStemOutline))
        self.polygons.append(
                 Polygon('{}p2'.format(self.blockId),
                         [stemPoint2, stemPoint3, stemPoint7, stemPoint6],
                         fill=colorStemFill, outline=colorStemOutline))
        self.polygons.append(
                 Polygon('{}p3'.format(self.blockId),
                         [stemPoint3, stemPoint4, stemPoint8, stemPoint7],
                         fill=colorStemFill, outline=colorStemOutline))
        self.polygons.append(
                 Polygon('{}p4'.format(self.blockId),
                         [stemPoint4, stemPoint1, stemPoint5, stemPoint8],
                         fill=colorStemFill, outline=colorStemOutline))
        
        
        self.polygons.append(
                 Polygon('{}p5'.format(self.blockId),
                         [crownPoint1, crownPoint2, crownPoint6, crownPoint5],
                         fill=colorCrownFill, outline=colorCrownOutline))
        self.polygons.append(
                 Polygon('{}p6'.format(self.blockId),
                         [crownPoint2, crownPoint3, crownPoint7, crownPoint6],
                         fill=colorCrownFill, outline=colorCrownOutline))
        self.polygons.append(
                 Polygon('{}p7'.format(self.blockId),
                         [crownPoint3, crownPoint4, crownPoint8, crownPoint7],
                         fill=colorCrownFill, outline=colorCrownOutline))
        self.polygons.append(
                 Polygon('{}p8'.format(self.blockId),
                         [crownPoint4, crownPoint1, crownPoint5, crownPoint8],
                         fill=colorCrownFill, outline=colorCrownOutline))
        
        self.polygons.append(
                 Polygon('{}p9'.format(self.blockId),
                         [crownPoint1, crownPoint2, crownPoint3, crownPoint4],
                         fill=colorCrownFill, outline=colorCrownOutline))


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

class Hut(Block):
    def __init__(self, gridX, gridZ, edgeLength):
        Block.__init__(self, gridX, gridZ, edgeLength)
    
    def initPolygons(self):
        offsetX = self.gridX
        offsetZ = self.gridZ
        
        colorWallFill = '#855223'
        colorWallOutline = '#69411c'
        colorRoofFill = '#d19640'
        colorRoofOutline = '#725223'
        
        #bottom wall points
        pb1 = Point3D(10 + offsetX,
                      -7.5,
                      0 + offsetZ)
        pb2 = Point3D(25 + offsetX,
                      -7.5,
                      0 + offsetZ)
        pb3 = Point3D(35 + offsetX,
                      -7.5,
                      10 + offsetZ)
        pb4 = Point3D(35 + offsetX,
                      -7.5,
                      25 + offsetZ)
        pb5 = Point3D(25 + offsetX,
                      -7.5,
                      35 + offsetZ)
        pb6 = Point3D(10 + offsetX,
                      -7.5,
                      35 + offsetZ)
        pb7 = Point3D(0 + offsetX,
                      -7.5,
                      25 + offsetZ)
        pb8 = Point3D(0 + offsetX,
                      -7.5,
                      10 + offsetZ)
        
        #top wall points
        pt1 = Point3D(10 + offsetX,
                      7.5,
                      0 + offsetZ)
        pt2 = Point3D(25 + offsetX,
                      7.5,
                      0 + offsetZ)
        pt3 = Point3D(35 + offsetX,
                      7.5,
                      10 + offsetZ)
        pt4 = Point3D(35 + offsetX,
                      7.5,
                      25 + offsetZ)
        pt5 = Point3D(25 + offsetX,
                      7.5,
                      35 + offsetZ)
        pt6 = Point3D(10 + offsetX,
                      7.5,
                      35 + offsetZ)
        pt7 = Point3D(0 + offsetX,
                      7.5,
                      25 + offsetZ)
        pt8 = Point3D(0 + offsetX,
                      7.5,
                      10 + offsetZ)
        
        #top wall points expanded
        pte1 = Point3D(10 + offsetX,
                      7.0,
                      0 - 5 + offsetZ)
        pte2 = Point3D(25 + offsetX,
                      7.0,
                      0 - 5 + offsetZ)
        pte3 = Point3D(35 + 5 + offsetX,
                      7.0,
                      10 + offsetZ)
        pte4 = Point3D(35 + 5 + offsetX,
                      7.0,
                      25 + offsetZ)
        pte5 = Point3D(25 + offsetX,
                      7.0,
                      35 + 5 + offsetZ)
        pte6 = Point3D(10 + offsetX,
                      7.0,
                      35 + 5 + offsetZ)
        pte7 = Point3D(0 - 5 + offsetX,
                      7.0,
                      25 + offsetZ)
        pte8 = Point3D(0 - 5 + offsetX,
                      7.0,
                      10 + offsetZ)
        
        #roof point
        pr = Point3D(17.5 + offsetX,
                     17.5,
                     17.5 + offsetZ)
        
        self.polygons.append(Polygon('{}p1'.format(self.blockId),
                                     [pb1, pb2, pt2, pt1],
                                     fill=colorWallFill, outline=colorWallOutline))
        self.polygons.append(Polygon('{}p2'.format(self.blockId),
                                     [pb2, pb3, pt3, pt2],
                                     fill=colorWallFill, outline=colorWallOutline))
        self.polygons.append(Polygon('{}p3'.format(self.blockId),
                                     [pb3, pb4, pt4, pt3],
                                     fill=colorWallFill, outline=colorWallOutline))
        self.polygons.append(Polygon('{}p4'.format(self.blockId),
                                     [pb4, pb5, pt5, pt4],
                                     fill=colorWallFill, outline=colorWallOutline))
        self.polygons.append(Polygon('{}p5'.format(self.blockId),
                                     [pb5, pb6, pt6, pt5],
                                     fill=colorWallFill, outline=colorWallOutline))
        self.polygons.append(Polygon('{}p6'.format(self.blockId),
                                     [pb6, pb7, pt7, pt6],
                                     fill=colorWallFill, outline=colorWallOutline))
        self.polygons.append(Polygon('{}p7'.format(self.blockId),
                                     [pb7, pb8, pt8, pt7],
                                     fill=colorWallFill, outline=colorWallOutline))
        self.polygons.append(Polygon('{}p8'.format(self.blockId),
                                     [pb8, pb1, pt1, pt8],
                                     fill=colorWallFill, outline=colorWallOutline))
        
        self.polygons.append(Polygon('{}p9'.format(self.blockId),
                                     [pte1, pte2, pr],
                                     fill=colorRoofFill, outline=colorRoofOutline))
        self.polygons.append(Polygon('{}p10'.format(self.blockId),
                                     [pte2, pte3, pr],
                                     fill=colorRoofFill, outline=colorRoofOutline))
        self.polygons.append(Polygon('{}p11'.format(self.blockId),
                                     [pte3, pte4, pr],
                                     fill=colorRoofFill, outline=colorRoofOutline))
        self.polygons.append(Polygon('{}p12'.format(self.blockId),
                                     [pte4, pte5, pr],
                                     fill=colorRoofFill, outline=colorRoofOutline))
        self.polygons.append(Polygon('{}p13'.format(self.blockId),
                                     [pte5, pte6, pr],
                                     fill=colorRoofFill, outline=colorRoofOutline))
        self.polygons.append(Polygon('{}p14'.format(self.blockId),
                                     [pte6, pte7, pr],
                                     fill=colorRoofFill, outline=colorRoofOutline))
        self.polygons.append(Polygon('{}p15'.format(self.blockId),
                                     [pte7, pte8, pr],
                                     fill=colorRoofFill, outline=colorRoofOutline))
        self.polygons.append(Polygon('{}p16'.format(self.blockId),
                                     [pte8, pte1, pr],
                                     fill=colorRoofFill, outline=colorRoofOutline))
