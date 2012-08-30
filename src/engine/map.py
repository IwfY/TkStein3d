from engine.coordinate import Point3D

class Map(object):
    def __init__(self):
        self.polygons = []
    
    def getPolygons(self):
        return self.polygons

    def getStartPosition(self):
        return Point3D(0.0, 0.0, 0.0)
    
    def getGroundColor(self):
        return '#339900'
    
    def getSkyColor(self):
        return '#b3defd'
