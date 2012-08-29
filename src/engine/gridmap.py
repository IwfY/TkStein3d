from engine.block import Block
from engine.map import Map
from engine.mapobjects import Floor, Tree

class GridMap(Map):
    def __init__(self):
        Map.__init__(self)
        self.objects = []
        
        self.edgeLength = 15
        
        # test input
        grid = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 1, 0, 0, 0, 1],
                [1, 1, 0, 1, 0, 0, 0, 1],
                [1, 0, 0, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 2, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 2, 1],
                [1, 0, 2, 0, 2, 0, 0, 1],
                [1, 0, 0, 2, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]
                ]
        i = 0
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == 1:
                    self.objects.append(Block(i, j, self.edgeLength))
                elif grid[i][j] == 2:
                    self.objects.append(Tree(i, j, self.edgeLength))
                #elif grid[i][j] == 0:
                #    self.objects.append(Floor(i, j, self.edgeLength))
    
    def getPolygons(self):
        tmp = []
        for mapObject in self.objects:
            tmp.extend(mapObject.getPolygons())
        
        return tmp
    
    
    def getObjects(self):
        return self.objects
