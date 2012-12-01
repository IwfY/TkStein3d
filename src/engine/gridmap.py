from engine.coordinate import Point3D
from engine.gamemap import GameMap
from engine.mapgenerator import MapGenerator
from engine.polygon import Polygon
from engine.mapobjects.door import Door

class GridMap(GameMap):
    def __init__(self, gameManager):
        GameMap.__init__(self, gameManager)
        
        self.groundColor = '#7d7d7d'
        self.skyColor = '#515151'
        
        self.startPosition = Point3D(0.0, 0.0, 0.0)
        self.wallBottom = -7.5
        self.wallTop = 7.5
        
        self.edgeLength = 15
        
        # test input
        self.mapGenerator = MapGenerator(30, 30, seed=1)
        self.grid = self.mapGenerator.generateMap()
        #grid = [[0,0,0,0,0],
        #        [0,2,2,2,0],
        #        [0,0,1,2,0],
        #        [0,0,0,2,0],
        #        [0,0,0,0,0]]
        
        # make walls towards these map grid values
        self.makeWallsTo = set([1, 's', '#'])
        
        for i in range(len(self.grid)):          # i corresponds to x axis
            for j in range(len(self.grid[i])):   # j corresponds to z axis
                if self.grid[i][j] == 2:     # wall
                    if i > 0 and self.grid[i-1][j] in self.makeWallsTo:
                        self.addWall(i * self.edgeLength,
                                     j * self.edgeLength,
                                     0, self.edgeLength)
                    if i < len(self.grid) - 1 and \
                            self.grid[i+1][j] in self.makeWallsTo:
                        self.addWall((i+1) * self.edgeLength,
                                     (j+1) * self.edgeLength,
                                     0, -self.edgeLength)
                    
                    if j > 0 and self.grid[i][j-1] in self.makeWallsTo:
                        self.addWall((i+1) * self.edgeLength,
                                     j * self.edgeLength,
                                     -self.edgeLength, 0)
                    if j < len(self.grid[i]) - 1 and\
                            self.grid[i][j+1] in self.makeWallsTo:
                        self.addWall(i * self.edgeLength,
                                     (j+1) * self.edgeLength,
                                     self.edgeLength, 0)

                elif self.grid[i][j] == '#':     #door
                    rotation = 1
                    if self.grid[i-1][j] in self.makeWallsTo and \
                            self.grid[i+1][j] in self.makeWallsTo:
                        rotation = 0
                    self.mapObjectsManager.addMapObject(
                            Door(self.gameManager,
                                 self, (i, j), self.edgeLength, rotation))
                elif self.grid[i][j] == 's':     #start position
                    self.startPosition = Point3D((0.5 + i) * self.edgeLength,
                                                 0.0,
                                                 (0.5 + j) * self.edgeLength)
    


    def addWall(self, x, z, xDelta, zDelta, fill='#805319', outline='#5e411c'):
        #print("new wall", x, z, xDelta, zDelta)
        point1 = Point3D(x, self.wallBottom, z)
        point2 = Point3D(x + xDelta, self.wallBottom, z + zDelta)
        
        point3 = Point3D(x, self.wallTop, z)
        point4 = Point3D(x + xDelta, self.wallTop, z + zDelta)
        
        newPolygon = Polygon('',
                             [point1, point2, point4, point3],
                             fill, outline)
        
        self.polygons.append(newPolygon)
    
    def getPathBlockedPoint(self, point1, point2):
        '''TODO
        get the first point:Point3D where the path from point1 to point2
        intersects an object
        
        return none if no intersection'''
        i2 = int(point2.x / self.edgeLength)
        j2 = int(point2.z / self.edgeLength)
        
        distanceCellXM1 = point2.x % self.edgeLength
        distanceCellXP1 = self.edgeLength - point2.x % self.edgeLength
        distanceCellZM1 = point2.z % self.edgeLength
        distanceCellZP1 = self.edgeLength - point2.z % self.edgeLength
        
        minDistance = 3.0
        
        # check goal cell
        if self.grid[i2][j2] not in self.makeWallsTo:
            return Point3D(0.0, 0.0, 0.0)
        
        # check neighbouring cells
        if distanceCellXM1 < minDistance:
            if self.grid[i2 - 1][j2] not in self.makeWallsTo:
                return Point3D(0.0, 0.0, 0.0)
        elif distanceCellXP1 < minDistance:
            if self.grid[i2 + 1][j2] not in self.makeWallsTo:
                return Point3D(0.0, 0.0, 0.0)
        
        if distanceCellZM1 < minDistance:
            if self.grid[i2][j2 - 1] not in self.makeWallsTo:
                return Point3D(0.0, 0.0, 0.0)
        elif distanceCellZP1 < minDistance:
            if self.grid[i2][j2 + 1] not in self.makeWallsTo:
                return Point3D(0.0, 0.0, 0.0)
        
        return None

    def getStartPosition(self):
        return self.startPosition
