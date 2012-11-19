from datetime import datetime, timedelta
from threading import Thread
from time import sleep

class MapObjectsManager(Thread):    
    def __init__(self):
        Thread.__init__(self)
        self.millisecondsPerTick = 30
        
        self.mapObjects = []
        self.running = True

    
    def run(self):
        while self.running:
            stop = datetime.now() + \
                   timedelta(milliseconds=self.millisecondsPerTick)
            
            for mapObject in self.mapObjects:
                mapObject.tick()
            
            remaining = stop - datetime.now()
            if remaining.days < 0:  # input processing needed too long
                remaining = -1
            else:
                remaining = round(remaining.microseconds / 1000000, 3)
            if remaining > 0:
                sleep(remaining)
    
    
    def stop(self):
        self.running = False
    

    def getPolygons(self):
        outPolygons = []
        for mapObject in self.mapObjects:
            outPolygons.extend(mapObject.getPolygons)
        
        return outPolygons


class MapObject(object):
    '''a dynamic object in the game world'''
    def __init__(self, gameMap):
        self.gameMap = gameMap
        self.polygons = []
    
    def tick(self):
        '''is called periodically. used to check for conditions and transform
        polygons'''
        pass
    
    
    def getPolygons(self):
        return self.polygons


