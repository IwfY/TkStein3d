import random

class MapGenerator(object):
    def __init__(self, width=40, height=40, seed=None):
        self.width = width
        self.height = height
        self.seed = seed
        
        self.clear()
    
    def clear(self):
        self.walls = []
        self.processed = []
    
    def addRectangle(self, start=False):
        x1 = random.randrange(1, self.width-1)
        x2 = random.randrange(1, self.width-1)
    
        y1 = random.randrange(1, self.height-1)
        y2 = random.randrange(1, self.height-1)
    
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
    
        if x2 - x1 < 3 or y2 - y1 < 3:
            self.addRectangle(start)
            return()
    
        for i in range(x1, x2):
            for j in range(y1, y2):
                # already taken
                if self.processed[i][j] == 1:
                    continue
    
                if i == x1 or i == x2-1 or j == y1 or j == y2-1:
                    self.walls[i][j] = 2
                else:
                    self.walls[i][j] = 1
                self.processed[i][j] = 1
    
        if start:
            self.walls[int((x2-x1) / 2) + x1][int((y2-y1) / 2) + y1] = 's'



    def addDoor(self):
        x = random.randrange(1, self.width-1)
        y = random.randrange(1, self.height-1)
    
        if self.walls[x][y] == 2 and \
            ((self.walls[x-1][y] == 1 and self.walls[x+1][y] == 1) or \
                (self.walls[x][y-1] == 1 and self.walls[x][y+1] == 1)):
                    self.walls[x][y] = '#'
        else:
            self.addDoor()

    def fillStatus(self):
        fill = 0
        for i in range(self.width):
            for j in range(self.height):
                fill += self.processed[i][j]
    
        return fill / (self.width * self.height)

    def generateMap(self):
        self.clear()
        random.seed(self.seed)

        # make blank 2 dimensional list
        for i in range(self.width):
            subList = []
            for j in range(self.height):
                subList.append(0)
            self.walls.append(subList)
            self.processed.append(subList[:])
        
        
        roomCount = 0
        self.addRectangle(start=True)
        while self.fillStatus() < 0.66:
            self.addRectangle()
            roomCount += 1
        
        for i in range(roomCount):
            self.addDoor()
        
        # show result
        #for i in range(self.width):
        #    for j in range(self.height):
        #        print(self.walls[i][j], end='')
        #    print()
        
        return self.walls