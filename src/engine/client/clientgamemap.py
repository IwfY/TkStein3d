from engine.shared.utils import runAndWait

from numpy import array, float32, append
from threading import Thread


class ClientGameMap(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.client = client
        
        self.staticPolygons = self.client.getStaticPolygons()
        self.dynamicPolygonBuffers = [[], []]
        self.dynamicVertexBuffers = [array([], dtype=float32),
                                     array([], dtype=float32)]
        self.dynamicVertexColorBuffers = [array([], dtype=float32),
                                          array([], dtype=float32)]
        self.dynamicVertexUVBuffers = [array([], dtype=float32),
                                       array([], dtype=float32)]
        self.dynamicVertexCountBuffers = [0, 0]
        self.activeDynamicPolygonBuffer = 0
        
        self.groundColor = '#7d7d7d'
        self.skyColor = '#515151'
        
        self.millisecondsPerTick = 30
        self.running = True
        self.paused = False
        
    
    def getPolygons(self):
        out = []
        out.extend(self.staticPolygons)
        out.extend(self.dynamicPolygonBuffers[self.activeDynamicPolygonBuffer])
        
        return out

    def getDynamicPolygonArrays(self):
        '''return a tuple 
            (vertex array, color array, uv coordinate array, polygon count)
        of the dynamic polygons where every 4 entries represent a vertex/color
        and every 4 of these represent a polygon
        
        arrays are numpy arrays of float32 type'''
        return (self.dynamicVertexBuffers[
                                        self.activeDynamicPolygonBuffer],
                self.dynamicVertexColorBuffers[
                                        self.activeDynamicPolygonBuffer],
                self.dynamicVertexUVBuffers[
                                        self.activeDynamicPolygonBuffer],
                self.dynamicVertexCountBuffers[
                                        self.activeDynamicPolygonBuffer])
        
    
    def updateAndSwitchDynamicPolygonBuffers(self):
        '''get new dynamic polygon data from server, update the polygon,
        vertex, color and polygon count buffers accordingly and make it active
        '''
        
        unusedBuffer = int(not self.activeDynamicPolygonBuffer)
        
        # update polygon buffer
        self.dynamicPolygonBuffers[unusedBuffer] = \
                self.client.getDynamicPolygons()
        
        # update vertex and color buffers
        tmpVertexBuffer = []
        tmpVertexColorBuffer = []
        tmpVertexUVBuffer = []
        tmpVertexCount = 0
        
        for polygon in self.dynamicPolygonBuffers[unusedBuffer]:
            r, g, b = polygon.getFillColorTuple()
            for point in polygon.getTrianglePoints3D():
                tmpVertexBuffer.extend([point.x, point.y, point.z, 1.0])
                tmpVertexColorBuffer.extend(
                        [r/255.0, g/255.0, b/255.0, 1.0])
                tmpVertexCount += 1
            tmpVertexUVBuffer.extend(polygon.getTriangleUVCoordinates())
        
        self.dynamicVertexCountBuffers[unusedBuffer] = tmpVertexCount
        self.dynamicVertexBuffers[unusedBuffer] = \
                array(tmpVertexBuffer, dtype=float32)
        self.dynamicVertexColorBuffers[unusedBuffer] = \
                array(tmpVertexColorBuffer, dtype=float32)
        self.dynamicVertexUVBuffers[unusedBuffer] = \
                array(tmpVertexUVBuffer, dtype=float32)
        
        # make updated buffers active
        self.activeDynamicPolygonBuffer = unusedBuffer


    def getStaticPolygons(self):
        return self.staticPolygons
    
    def getDynamicPolygons(self):
        return self.dynamicPolygonBuffers[self.activeDynamicPolygonBuffer]

    def getGroundColor(self):
        return self.groundColor
    
    def getSkyColor(self):
        return self.skyColor
    
    
    def togglePaused(self):
        self.paused = not self.paused
    
    def stop(self):
        self.running = False
    
    def run(self):
        while self.running:
            runAndWait(self._run, self.millisecondsPerTick)
    
    def _run(self):
        if not self.paused:
            self.updateAndSwitchDynamicPolygonBuffers()
