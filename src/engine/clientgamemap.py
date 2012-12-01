from datetime import datetime, timedelta
from threading import Thread
from time import sleep


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

    def getGroundColor(self):
        return self.groundColor
    
    def getSkyColor(self):
        return self.skyColor

    
    def stop(self):
        self.running = False
    
    def run(self):
        while self.running:
            stop = datetime.now() + \
                   timedelta(milliseconds=self.millisecondsPerTick)
            
            unusedBuffer = int(not self.activeDynamicPolygonBuffer)
            self.dynamicPolygonBuffers[unusedBuffer] = \
                    self.client.getDynamicPolygons()
            self.activeDynamicPolygonBuffer = unusedBuffer
            
            #wait until quota runs out
            remaining = stop - datetime.now()
            if remaining.days < 0:  # input processing needed too long
                remaining = -1
            else:
                remaining = round(remaining.microseconds / 1000000, 3)
            if remaining > 0:
                sleep(remaining)