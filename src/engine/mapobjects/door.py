from engine.conditions.characternearcondition import CharacterNearCondition
from engine.shared.coordinate import Point3D
from engine.mapobjects.mapobject import MapObject
from engine.polygon import Polygon



class Door(MapObject):
    '''a door that slides down if a character is near'''
    STATE_OPENING = 1
    STATE_CLOSING = 2
    
    def __init__(self, gameManager, gameMap, coordinate, edgeLength, rotation):
        '''create a door
        
        @param coordinate is a tuple (i, j) where i represents the x index and
                          j the z index in the grid map
        @param rotation : float represents the rotation of the door around the
                          y axis
        '''
        MapObject.__init__(self, gameMap)
        
        self.state = Door.STATE_CLOSING
        self.edgeLength = edgeLength
        self.height = - self.edgeLength / 2
        self.rotation = rotation
        
        i, j = coordinate
        self.characterNearCondition = CharacterNearCondition(
                          gameManager,
                          Point3D((i + 0.5) * self.edgeLength,
                                  0,
                                  (j + 0.5) * self.edgeLength),
                          self.edgeLength * 2)
        
        self.createPolygons(coordinate, self.edgeLength)
    
    def tick(self):
        '''is called periodically. used to check for conditions and transform
        polygons'''
        if self.characterNearCondition.check():
            self.state = Door.STATE_OPENING
        else:
            self.state = Door.STATE_CLOSING
        
        if self.state == Door.STATE_OPENING:
            if self.height < self.edgeLength / 2 - self.edgeLength / 10:
                self.height += self.edgeLength / 10
        elif self.state == Door.STATE_CLOSING:
            if self.height > -self.edgeLength / 2:
                self.height -= self.edgeLength / 10
        
        self.updatePolygons()


    def updatePolygons(self):
        self.polygons[0].points[0].y = self.height
        self.polygons[0].points[1].y = self.height
        self.polygons[1].points[0].y = self.height
        self.polygons[1].points[1].y = self.height
        self.polygons[2].points[0].y = self.height
        self.polygons[2].points[1].y = self.height
        self.polygons[2].points[2].y = self.height
        self.polygons[2].points[3].y = self.height



    def createPolygons(self, coordinate, edgeLength):
        i, j = coordinate
        
        self.addWall((i + 0.5) * self.edgeLength - (self.edgeLength / 8),
                     j * self.edgeLength,
                     0, self.edgeLength)
        self.addWall((i + 0.5) * self.edgeLength + (self.edgeLength / 8),
                     (j + 1) * self.edgeLength,
                     0, -self.edgeLength)
        
        # horizontal part
        point1 = Point3D((i + 0.5) * self.edgeLength - (self.edgeLength / 8),
                         self.height,
                         j * self.edgeLength)
        point2 = Point3D((i + 0.5) * self.edgeLength - (self.edgeLength / 8),
                         self.height,
                         (j + 1) * self.edgeLength)            
        point3 = Point3D((i + 0.5) * self.edgeLength + (self.edgeLength / 8),
                         self.height,
                         (j + 1) * self.edgeLength)
        point4 = Point3D((i + 0.5) * self.edgeLength + (self.edgeLength / 8),
                         self.height,
                         j * self.edgeLength)
        newPolygon = Polygon('',
                         [point4, point3, point2, point1],
                         '#298b94', '#2a6a70')
        self.polygons.append(newPolygon)
        
        if self.rotation != 0.0:
            for polygon in self.polygons:
                for point in polygon.getPoints3D():
                    point.rotateAroundYAxisByAngle(
                            Point3D((i + 0.5) * self.edgeLength,
                                    0,
                                    (j + 0.5) * self.edgeLength),
                            self.rotation)


    def addWall(self, x, z, xDelta, zDelta, fill='#298b94', outline='#2a6a70'):
        wallBottom = -self.edgeLength / 2
        wallTop = self.edgeLength / 2
        point1 = Point3D(x, wallBottom, z)
        point2 = Point3D(x + xDelta, wallBottom, z + zDelta)
        
        point3 = Point3D(x + xDelta, wallTop, z + zDelta)
        point4 = Point3D(x, wallTop, z)
        
        newPolygon = Polygon('',
                             [point1, point2, point3, point4],
                             fill, outline)
        
        self.polygons.append(newPolygon)

