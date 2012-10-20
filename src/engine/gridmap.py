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
        self.mapGenerator = MapGenerator(20, 20, seed=1)
        grid = self.mapGenerator.generateMap()
        
        # make walls towards these map grid values
        makeWallsTo = set([1, 's', '#'])
        
        for i in range(len(grid)):          # i corresponds to x axis
            for j in range(len(grid[i])):   # j corresponds to z axis
                if grid[i][j] == 2:     # wall
                    if i > 0 and grid[i-1][j] in makeWallsTo:
                        self.addWall(i * self.edgeLength,
                                     j * self.edgeLength,
                                     0, self.edgeLength)
                    if i < len(grid) - 1 and grid[i+1][j] in makeWallsTo:
                        self.addWall((i+1) * self.edgeLength,
                                     (j+1) * self.edgeLength,
                                     0, -self.edgeLength)
                    
                    if j > 0 and grid[i][j-1] in makeWallsTo:
                        self.addWall((i+1) * self.edgeLength,
                                     j * self.edgeLength,
                                     -self.edgeLength, 0)
                    if j < len(grid[i]) - 1 and grid[i][j+1] in makeWallsTo:
                        self.addWall(i * self.edgeLength,
                                     (j+1) * self.edgeLength,
                                     self.edgeLength, 0)

                elif grid[i][j] == '#':     #door
                    if grid[i-1][j] in makeWallsTo and \
                            grid[i+1][j] in makeWallsTo:
                        self.addWall((i + 0.5) * self.edgeLength - 2,
                                     j * self.edgeLength,
                                     0 ,self.edgeLength,
                                     fill='brown')
                        self.addWall((i + 0.5) * self.edgeLength + 2,
                                     (j + 1) * self.edgeLength,
                                     0 ,-self.edgeLength,
                                     fill='brown')
                    else:
                        self.addWall((i + 1) * self.edgeLength,
                                     (j + 0.5) * self.edgeLength - 2,
                                     -self.edgeLength, 0,
                                     fill='brown')
                        self.addWall(i * self.edgeLength,
                                     (j + 0.5) * self.edgeLength + 2,
                                     self.edgeLength, 0,
                                     fill='brown')
                    
                    
                elif grid[i][j] == 's':     #start position
                    self.startPosition = Point3D((0.5 + i) * self.edgeLength,
                                                 0.0,
                                                 (0.5 + j) * self.edgeLength)
    


    def addWall(self, x, z, xDelta, zDelta, fill='', outline='darkgrey'):
        #print("new wall", x, z, xDelta, zDelta)
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
