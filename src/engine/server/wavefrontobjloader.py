from engine.shared.coordinate import Point3DColorUV
from engine.shared.polygon import Polygon

class WavefrontObjLoader(object):
    def __init__(self, objFilename):
        self.objFilename = objFilename
        
        self.vertices = []
        self.faces = []
        self.normals = []
        self.uvCoordinates = []
        
        self.polygons = []
        
        self.parseFile()
        self.createPolygons()


    def parseFile(self):
        content = None
        file = open(self.objFilename,  'r')
        try:
            content = file.readlines()
        finally:
            file.close()
            
        if content is not None:
            for line in content:
                values = line.split()
                if values[0] == 'v':    # vertices (x, y, z)
                    if len(values) >= 4:
                        self.vertices.append((float(values[1]),
                                              float(values[2]),
                                              float(values[3])
                                              )
                                             )
                        
                elif values[0] == 'f':
                    faceCorners = []
                    for i in range(1, len(values)):
                        indices = values[i].split('/')
                        faceCorner = [int(indices[0]), None, None]
                        
                        if len(indices) > 1 and indices[1] != '': # uv index
                            faceCorner[1] = int(indices[1])
                        if len(indices) > 2 and indices[2] != '': # normal index
                            faceCorner[2] = int(indices[2])

                        faceCorners.append(faceCorner)
                    self.faces.append(faceCorners)

                elif values[0] == 'vt':     # texture coordinates (u, v)
                    if len(values) >= 3:
                        self.uvCoordinates.append((float(values[1]),
                                                   float(values[2])))
                elif values[0] == 'vn':     # normal vector (dx, dy, dz)
                    if len(values) >= 4:
                        self.normals.append((float(values[1]),
                                             float(values[2]),
                                             float(values[3])
                                             )
                                            )
    
    def createPolygons(self):
        for face in self.faces:
            points = []
            for cornerPoint in face:
                vertex = self.vertices[cornerPoint[0] - 1]
                point = Point3DColorUV(vertex)
                points.append(point)
            polygon = Polygon('', points)
            self.polygons.append(polygon)

    def getPolygons(self):
        return self.polygons
