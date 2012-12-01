from engine.coordinate import Point3D
from engine.mapobjectsmanager import MapObjectsManager

class GameMap(object):
    def __init__(self, gameManager):
        self.gameManager = gameManager
        
        self.polygons = []
        
        self.groundColor = ''
        self.skyColor = ''
        self.mapObjectsManager = MapObjectsManager(self.gameManager)
    
    def getPolygons(self):
        outPolygons = [x for x in self.polygons]
        outPolygons.extend(self.mapObjectsManager.getPolygons())
        
        return outPolygons
    
    def getStaticPolygons(self):
        return self.polygons
    
    def getDynamicPolygons(self):
        return self.mapObjectsManager.getPolygons()


    def getStartPosition(self):
        return Point3D(0.0, 0.0, 0.0)
    
    def getGroundColor(self):
        return self.groundColor
    
    def getSkyColor(self):
        return self.skyColor

    def getPathBlockedPoint(self, point1, point2):
        '''get the first point:Point3D where the path from point1 to point2
        intersects an object
        
        return none if no intersection'''
        
        return None

    def start(self):
        self.mapObjectsManager.start()
    
    def stop(self):
        self.mapObjectsManager.stop()
