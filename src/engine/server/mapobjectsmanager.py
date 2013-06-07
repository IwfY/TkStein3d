from engine.shared.utils import runAndWait

from threading import Thread


class MapObjectsManager(Thread):    
    def __init__(self, gameManager):
        Thread.__init__(self)
        
        self.gameManager = gameManager
        
        self.millisecondsPerTick = 40
        
        self.mapObjects = []
        self.running = True
        self.currentTick = 0
    
    
    def addMapObject(self, mapObject):
        self.mapObjects.append(mapObject)
    
    def removeMapObject(self, mapObject):
        if mapObject in self.mapObjects:
            self.mapObjects.remove(mapObject)

    
    def run(self):
        while self.running:
            runAndWait(self._run, self.millisecondsPerTick)
    
    def _run(self):
        for mapObject in self.mapObjects:
                mapObject.tick(self.currentTick)
        self.currentTick += 1
    
    
    def stop(self):
        self.running = False
    

    def getPolygons(self):
        outPolygons = []
        for mapObject in self.mapObjects:
            outPolygons.extend(mapObject.getPolygons())
        
        return outPolygons
