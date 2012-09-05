from engine.block import Block
from engine.coordinate import Point3D
from engine.map import Map
from engine.mapobjects import Floor, Tree
from engine.mapgenerator import MapGenerator

class GridMap(Map):
    def __init__(self):
        Map.__init__(self)
        self.objects = []
        self.startPosition = Point3D(0.0, 0.0, 0.0)
        
        self.edgeLength = 15
        
        # test input
        self.mapGenerator = MapGenerator(30, 20, 1)
        grid = self.mapGenerator.generateMap()
        
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == 2:
                    self.objects.append(Block(i, j, self.edgeLength))
                #elif grid[i][j] == 2:
                #    self.objects.append(Tree(i, j, self.edgeLength))
                #elif grid[i][j] == 0:
                #    self.objects.append(Floor(i, j, self.edgeLength))
                elif grid[i][j] == 's':     #start position
                    self.startPosition = Point3D((0.5 + i) * self.edgeLength,
                                                 0.0,
                                                 (0.5 + j) * self.edgeLength)
    
    def getPolygons(self):
        tmp = []
        for mapObject in self.objects:
            tmp.extend(mapObject.getPolygons())
        
        return tmp

    def getStartPosition(self):
        return self.startPosition
    
    
    def getObjects(self):
        return self.objects
