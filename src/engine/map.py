from engine.coordinate import Point3D

class Map(object):
    def __init__(self):
        self.polygons = []
        
        self.groundColor = ''
        self.skyColor = ''
    
    def getPolygons(self):
        return self.polygons

    def getStartPosition(self):
        return Point3D(0.0, 0.0, 0.0)
    
    def getGroundColor(self):
        return self.groundColor
    
    def getSkyColor(self):
        return self.skyColor
