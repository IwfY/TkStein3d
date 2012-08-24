from engine.block import Block

class Map(object):
    def __init__(self):
        self.blocks = []
        
        self.edgeLength = 15
        # test input
        self.blocks.append(Block(2, 3, self.edgeLength))
        self.blocks.append(Block(1, 3, self.edgeLength))
        self.blocks.append(Block(-2, 3, self.edgeLength))
        self.blocks.append(Block(-1, 3, self.edgeLength))
        self.blocks.append(Block(0, 3, self.edgeLength))
        self.blocks.append(Block(2, 2, self.edgeLength))
        self.blocks.append(Block(-2, 2, self.edgeLength))
        self.blocks.append(Block(-2, 1, self.edgeLength))
    
    
    def getBlocks(self):
        return self.blocks
