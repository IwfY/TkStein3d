from engine.block import Block

class Map(object):
    def __init__(self):
        self.objects = []
        
        self.edgeLength = 15
        # test input
        self.objects.append(Block(2, 3, self.edgeLength))
        self.objects.append(Block(1, 3, self.edgeLength))
        self.objects.append(Block(-2, 3, self.edgeLength))
        self.objects.append(Block(-1, 3, self.edgeLength))
        self.objects.append(Block(0, 3, self.edgeLength))
        self.objects.append(Block(2, 2, self.edgeLength))
        self.objects.append(Block(-2, 2, self.edgeLength))
        self.objects.append(Block(-2, 1, self.edgeLength))
    
    
    def getObjects(self):
        return self.objects
