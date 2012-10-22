from engine.coordinate import Point3D
from engine.mapobjects import MapObjectManager

class Map(object):
    def __init__(self):
        self.polygons = []
        
        self.groundColor = ''
        self.skyColor = ''
        self.mapObjectManager = MapObjectManager()
    
    def getPolygons(self):
        return self.polygons

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
