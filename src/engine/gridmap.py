from engine.coordinate import Point3D
from engine.gamemap import GameMap
from engine.mapgenerator import MapGenerator
from engine.polygon import Polygon
from engine.mapobjects.door import Door

from math import pi

class GridMap(GameMap):
    def __init__(self, gameManager, grid=None, edgeLength=1.0):
        '''
        grid example:
        ~~~~~~~~~~~~~~~~~~~~
               -----x/j--->

        grid = [[0,0,0,0,0],  |
                [0,2,2,2,0],  |
                [0,0,1,2,0],  z/i
                [0,0,2,2,0],  |
                [0,0,0,0,0]]  v
        
        grid[zIndex][xIndex]
        
        '''
        GameMap.__init__(self, gameManager)
        
        self.groundColor = '#7d7d7d'
        self.skyColor = '#515151'
        
        self.edgeLength = edgeLength
        self.startPosition = Point3D(0.0, 0.0, 0.0)
        self.wallBottom = -self.edgeLength / 2
        self.wallTop = self.edgeLength / 2
        
        self.grid = None
        
        if grid is None:
            self.mapGenerator = MapGenerator(30, 30, seed=1)
            #self.mapGenerator = MapGenerator(50, 50, seed=1)
            
            self.grid = self.mapGenerator.generateMap()
        else:
            self.grid = grid


        #DEBUG start
        #self.grid = [[1,1,1,1],
        #             [1,2,2,1],
        #             [1,1,2,1]]
        # 
        #DEBUG end


        # make walls towards these map grid values
        self.makeWallsTo = set([1, 's', '#'])
        
        for i in range(len(self.grid)):          # i corresponds to z axis
            for j in range(len(self.grid[i])):   # j corresponds to x axis
                if self.grid[i][j] == 2:     # wall
                    if i > 0 and self.grid[i-1][j] in self.makeWallsTo:
                        self.addWall((j + 1) * self.edgeLength,
                                     i * self.edgeLength,
                                     -self.edgeLength, 0)
                    if i < len(self.grid) - 1 and \
                            self.grid[i+1][j] in self.makeWallsTo:
                        self.addWall(j * self.edgeLength,
                                     (i + 1) * self.edgeLength,
                                     self.edgeLength, 0)

                    if j > 0 and self.grid[i][j-1] in self.makeWallsTo:
                        self.addWall(j * self.edgeLength,
                                     i * self.edgeLength,
                                     0, self.edgeLength)
                    if j < len(self.grid[i]) - 1 and\
                            self.grid[i][j+1] in self.makeWallsTo:
                        self.addWall((j + 1) * self.edgeLength,
                                     (i + 1) * self.edgeLength,
                                     0, -self.edgeLength)
                
                elif self.grid[i][j] == 1:     #floor and ceiling
                    self.addFloor(j, i)
                    self.addCeiling(j, i)

                elif self.grid[i][j] == '#':     #door
                    self.addFloor(j, i)
                    self.addCeiling(j, i)
                    rotation = 0
                    if self.grid[i-1][j] in self.makeWallsTo and \
                            self.grid[i+1][j] in self.makeWallsTo:
                        rotation = pi / 2
                    
                    self.mapObjectsManager.addMapObject(
                            Door(self.gameManager,
                                 self, (j, i), self.edgeLength, rotation))
                
                elif self.grid[i][j] == 's':     #start position
                    self.addFloor(j, i)
                    self.addCeiling(j, i)
                    self.startPosition = Point3D((0.5 + j) * self.edgeLength,
                                                 0.0,
                                                 (0.5 + i) * self.edgeLength)


    def addWall(self, x, z, xDelta, zDelta, fill='#805319', outline='#5e411c'):
        #print("new wall", x, z, xDelta, zDelta)
        point1 = Point3D(x, self.wallBottom, z)
        point2 = Point3D(x + xDelta, self.wallBottom, z + zDelta)
        
        point3 = Point3D(x + xDelta, self.wallTop, z + zDelta)
        point4 = Point3D(x, self.wallTop, z)
        
        newPolygon = Polygon('',
                             [point1, point2, point3, point4],
                             fill, outline)
        
        self.polygons.append(newPolygon)
    
    def addFloor(self, x, z):
        minX = x * self.edgeLength
        maxX = (x + 1) * self.edgeLength
        minZ = z * self.edgeLength
        maxZ = (z + 1) * self.edgeLength
        floorPolygon = Polygon('',
                   [
                    Point3D(minX, self.wallBottom, minZ),
                    Point3D(minX, self.wallBottom, maxZ),
                    Point3D(maxX, self.wallBottom, maxZ),
                    Point3D(maxX, self.wallBottom, minZ)
                   ],
                   self.groundColor)
        self.polygons.append(floorPolygon)
    
    def addCeiling(self, x, z):
        minX = x * self.edgeLength
        maxX = (x + 1) * self.edgeLength
        minZ = z * self.edgeLength
        maxZ = (z + 1) * self.edgeLength
        floorPolygon = Polygon('',
                   [
                    Point3D(minX, self.wallTop, minZ),
                    Point3D(maxX, self.wallTop, minZ),
                    Point3D(maxX, self.wallTop, maxZ),
                    Point3D(minX, self.wallTop, maxZ)
                   ],
                   self.skyColor)
        self.polygons.append(floorPolygon)
    
    def getPathBlockedPoint(self, point1, point2):
        '''TODO
        get the first point:Point3D where the path from point1 to point2
        intersects an object
        
        return none if no intersection'''
        i2 = int(point2.z / self.edgeLength)
        j2 = int(point2.x / self.edgeLength)
        
        distanceCellXM1 = point2.x % self.edgeLength
        distanceCellXP1 = self.edgeLength - point2.x % self.edgeLength
        distanceCellZM1 = point2.z % self.edgeLength
        distanceCellZP1 = self.edgeLength - point2.z % self.edgeLength
        
        minDistance = 0.2
        
        # check goal cell
        if self.grid[i2][j2] not in self.makeWallsTo:
            return Point3D(0.0, 0.0, 0.0)
        
        # check neighbouring cells
        if distanceCellZM1 < minDistance:
            if self.grid[i2 - 1][j2] not in self.makeWallsTo:
                return Point3D(0.0, 0.0, 0.0)
        elif distanceCellZP1 < minDistance:
            if self.grid[i2 + 1][j2] not in self.makeWallsTo:
                return Point3D(0.0, 0.0, 0.0)
        
        if distanceCellXM1 < minDistance:
            if self.grid[i2][j2 - 1] not in self.makeWallsTo:
                return Point3D(0.0, 0.0, 0.0)
        elif distanceCellXP1 < minDistance:
            if self.grid[i2][j2 + 1] not in self.makeWallsTo:
                return Point3D(0.0, 0.0, 0.0)
        
        return None

    def getStartPosition(self):
        return self.startPosition
