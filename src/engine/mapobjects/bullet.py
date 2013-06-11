from engine.mapobjects.mapobject import MapObject
from engine.server.block import Block
from engine.shared.coordinate import Point3D

from math import atan2, pi
from engine.shared.polygon import Polygon

class Bullet(MapObject):
    def __init__(self, gameMap, position, moveVector):
        MapObject.__init__(self, gameMap)
        self.position = position
        self.moveVector = moveVector
        self.firstTick = None
        
        self.initPolygons()
    
    def initPolygons(self):
        block = Block(Point3D(self.position.x - 0.02,
                              self.position.y - 0.1,
                              self.position.z - 0.02),
                      Point3D(self.position.x + 0.02,
                              self.position.y - 0.06,
                              self.position.z + 0.02))
        blockPolygons = block.getPolygons()

        rotation = atan2(self.moveVector.z, self.moveVector.x) - pi / 2
        
        for polygon in blockPolygons:
            polygon.fill = '#405010'
            for point in polygon.getPoints3D():
                point.rotateAroundYAxisByAngle(self.position,
                                               rotation)
        self.polygons = blockPolygons

    def tick(self, count):
        if self.firstTick is None:
            self.firstTick = count
        
        for polygon in self.polygons:
            polygon.translate(self.moveVector.x,
                              self.moveVector.y,
                              self.moveVector.z)
        
        if (count - self.firstTick) > 100:
            self.gameMap.removeMapObject(self)
            self.polygons = []
