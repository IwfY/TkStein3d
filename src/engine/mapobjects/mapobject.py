class MapObject(object):
    '''a dynamic object in the game world'''
    def __init__(self, gameMap):
        self.gameMap = gameMap
        self.polygons = []
    
    def tick(self, count):
        '''is called periodically. used to check for conditions and transform
        polygons'''
        pass
    
    
    def getPolygons(self):
        return self.polygons
