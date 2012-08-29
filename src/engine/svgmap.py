from engine.coordinate import Point3D
from engine.map import Map
from engine.polygon import Polygon

from threading import Lock
import xml.dom.minidom as dom

class SVGMap(Map):
    count = 0
    mutex = Lock()
    
    def __init__(self, svgFilename):
        Map.__init__(self)
        
        self.wallBottom = -7.5
        self.wallTop = 7.5
        
        self.loadMap(svgFilename)
    
    def loadMap(self, svgFilename):
        xml = dom.parse(svgFilename)
        
        for path in xml.getElementsByTagName('path'):
            coordinateString = path.getAttribute('d')
            parts = coordinateString.split(' ')
            x = float(parts[1].split(',')[0])
            z = float(parts[1].split(',')[1])
            if parts[0] == 'm':     #relative move
                xDelta = float(parts[2].split(',')[0])
                zDelta = float(parts[2].split(',')[1])
            elif parts[0] == 'M':     #absolute move
                xDelta = float(parts[2].split(',')[0]) - x
                zDelta = float(parts[2].split(',')[1]) - z
            else:
                print('something went horribly wrong')
                continue
            
            print(x, z, xDelta, zDelta)
            self.addWall(x, -z, xDelta, -zDelta)
        
        
    def addWall(self, x, z, xDelta, zDelta, fill='grey', outline='darkgrey'):
        point1 = Point3D(x, self.wallBottom, z)
        point2 = Point3D(x + xDelta, self.wallBottom, z + zDelta)
        
        point3 = Point3D(x, self.wallTop, z)
        point4 = Point3D(x + xDelta, self.wallTop, z + zDelta)
        
        # using mutex for unique IDs if several threads try to create walls
        SVGMap.mutex.acquire()
        try:
            newPolygonId = 'p{}'.format(SVGMap.count)
            SVGMap.count += 1
        finally:
            SVGMap.mutex.release()
        
        newPolygon = Polygon(newPolygonId,
                             [point1, point2, point4, point3],
                             fill, outline)
        
        self.polygons.append(newPolygon)