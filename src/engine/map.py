from engine.block import Block

class Map(object):
    def __init__(self):
        self.objects = []
        
        self.edgeLength = 15
        
        # test input
        grid = [[1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 1, 0, 0, 1],
                [1, 1, 0, 1, 0, 0, 1],
                [1, 0, 0, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1]                
                ]
        i = 0
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == 1:
                    self.objects.append(Block(i, j, self.edgeLength))
    
    
    def getObjects(self):
        return self.objects
