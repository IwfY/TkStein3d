from engine.shared.coordinate import Point3D
from engine.server.wavefrontobjloader import WavefrontObjLoader

class Model(object):
    '''
    a model represented by a couple of polygons
    '''


    def __init__(self, polygons=[]):
        self.polygons = polygons
    
    
    def loadFromObjFile(self, filename):
        objLoader = WavefrontObjLoader(filename)
        self.polygons = objLoader.getPolygons()

    
    def getPolygons(self):
        return self.polygons


    def translate(self, dx, dy, dz):
        for polygon in self.polygons:
            polygon.translate(dx, dy, dz)

    def scale(self, scaleOrigin=Point3D(0.0, 0.0, 0.0), sx=1.0, sy=1.0, sz=1.0):
        for polygon in self.polygons:
            polygon.scale(scaleOrigin, sx, sy, sz)