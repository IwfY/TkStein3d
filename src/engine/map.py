from engine.block import Block

class Map(object):
    def __init__(self):
        self.blocks = []
        
        # test input
        self.blocks.append(Block(2, 3, 15))
        self.blocks.append(Block(1, 3, 15))
        self.blocks.append(Block(2, 2, 15))
        self.blocks.append(Block(-1, 1, 15))
        
    
    
    def getBlocks(self):
        return self.blocks
