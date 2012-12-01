from datetime import datetime, timedelta
from threading import Thread
from time import sleep

class MapObjectsManager(Thread):    
    def __init__(self, gameManager):
        Thread.__init__(self)
        
        self.gameManager = gameManager
        
        self.millisecondsPerTick = 100
        
        self.mapObjects = []
        self.running = True
    
    
    def addMapObject(self, mapObject):
        self.mapObjects.append(mapObject)
    
    def removeMapObject(self, mapObject):
        if mapObject in self.mapObjects:
            self.mapObjects.remove(mapObject)

    
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
            outPolygons.extend(mapObject.getPolygons())
        
        return outPolygons
