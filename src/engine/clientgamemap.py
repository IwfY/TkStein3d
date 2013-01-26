from engine.shared.utils import runAndWait

from threading import Thread


class ClientGameMap(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.client = client
        
        self.staticPolygons = self.client.getStaticPolygons()
        self.dynamicPolygonBuffers = [[], []]
        self.activeDynamicPolygonBuffer = 0
        
        self.groundColor = '#7d7d7d'
        self.skyColor = '#515151'
        
        self.millisecondsPerTick = 30
        self.running = True
        
    
    def getPolygons(self):
        out = []
        out.extend(self.staticPolygons)
        out.extend(self.dynamicPolygonBuffers[self.activeDynamicPolygonBuffer])
        
        return out

    def getStaticPolygons(self):
        return self.staticPolygons
    
    def getDynamicPolygons(self):
        return self.dynamicPolygonBuffers[self.activeDynamicPolygonBuffer]

    def getGroundColor(self):
        return self.groundColor
    
    def getSkyColor(self):
        return self.skyColor

    
    def stop(self):
        self.running = False
    
    def run(self):
        while self.running:
            runAndWait(self._run, self.millisecondsPerTick)
    
    def _run(self):
        unusedBuffer = int(not self.activeDynamicPolygonBuffer)
        self.dynamicPolygonBuffers[unusedBuffer] = \
                self.client.getDynamicPolygons()
        self.activeDynamicPolygonBuffer = unusedBuffer