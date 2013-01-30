from engine.shared.coordinate import Point3D
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
    
    def addMapObject(self, mapObject):
        self.mapObjectsManager.addMapObject(mapObject)

    def getMaxX(self):
        maxX = None
        for polygon in self.polygons:
            for point in polygon.getPoints3D():
                if maxX is None:
                    maxX = point.x
                    continue
                maxX = max(maxX, point.x)        
        return maxX
    
    def getMinX(self):
        minX = None
        for polygon in self.polygons:
            for point in polygon.getPoints3D():
                if minX is None:
                    minX = point.x
                    continue
                minX = min(minX, point.x)        
        return minX
                
    def getMaxY(self):
        maxY = None
        for polygon in self.polygons:
            for point in polygon.getPoints3D():
                if maxY is None:
                    maxY = point.y
                    continue
                maxY = max(maxY, point.y)        
        return maxY
    
    def getMinY(self):
        minY = None
        for polygon in self.polygons:
            for point in polygon.getPoints3D():
                if minY is None:
                    minY = point.y
                    continue
                minY = min(minY, point.y)        
        return minY
    
    def getMaxZ(self):
        maxZ = None
        for polygon in self.polygons:
            for point in polygon.getPoints3D():
                if maxZ is None:
                    maxZ = point.z
                    continue
                maxZ = max(maxZ, point.z)        
        return maxZ
    
    def getMinZ(self):
        minZ = None
        for polygon in self.polygons:
            for point in polygon.getPoints3D():
                if minZ is None:
                    minZ = point.z
                    continue
                minZ = min(minZ, point.z)        
        return minZ

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
