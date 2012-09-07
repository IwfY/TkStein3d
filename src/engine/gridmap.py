from engine.coordinate import Point3D
from engine.map import Map
from engine.mapobjects import Floor, Tree
from engine.mapgenerator import MapGenerator
from engine.polygon import Polygon

class GridMap(Map):
    def __init__(self):
        Map.__init__(self)
        self.objects = []
        self.startPosition = Point3D(0.0, 0.0, 0.0)
        self.wallBottom = -7.5
        self.wallTop = 7.5
        
        self.edgeLength = 15
        
        # test input
        self.mapGenerator = MapGenerator(30, 20, seed=1)
        grid = self.mapGenerator.generateMap()
        
        # make walls towards these map grid values
        makeWallsTo = set([1, 's', '#'])
        
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == 2:
                    if i > 0 and grid[i-1][j] in makeWallsTo:
                        self.addWall(i * self.edgeLength, j * self.edgeLength,
                                     0, self.edgeLength)
                    if i < len(grid) - 1 and grid[i+1][j] in makeWallsTo:
                        self.addWall((i+1) * self.edgeLength,
                                     j * self.edgeLength,
                                     0, self.edgeLength)
                    
                    if j > 0 and grid[i][j-1] in makeWallsTo:
                        self.addWall(i * self.edgeLength, j * self.edgeLength,
                                     self.edgeLength, 0)
                    if j < len(grid[i]) - 1 and grid[i][j+1] in makeWallsTo:
                        self.addWall(i * self.edgeLength,
                                     (j+1) * self.edgeLength,
                                     self.edgeLength, 0)
                    
                    
                elif grid[i][j] == 's':     #start position
                    self.startPosition = Point3D((0.5 + i) * self.edgeLength,
                                                 0.0,
                                                 (0.5 + j) * self.edgeLength)
    


    def addWall(self, x, z, xDelta, zDelta, fill='grey', outline='darkgrey'):
        point1 = Point3D(x, self.wallBottom, z)
        point2 = Point3D(x + xDelta, self.wallBottom, z + zDelta)
        
        point3 = Point3D(x, self.wallTop, z)
        point4 = Point3D(x + xDelta, self.wallTop, z + zDelta)
        
        newPolygon = Polygon('',
                             [point1, point2, point4, point3],
                             fill, outline)
        
        self.polygons.append(newPolygon)

    def getStartPosition(self):
        return self.startPosition
    
    
    def getObjects(self):
        return self.objects
