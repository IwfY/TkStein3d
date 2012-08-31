from engine.coordinate import Point3D, Vector3D
from engine.map import Map
from engine.polygon import Polygon

import re
from threading import Lock
import xml.dom.minidom as dom

class SVGMap(Map):
    count = 0
    mutex = Lock()
    
    def __init__(self, svgFilename):
        Map.__init__(self)
        
        self.wallBottom = -7.5
        self.wallTop = 7.5
        self.startPosition = Point3D(0.0, 0.0, 0.0)
        
        
        self.loadMap(svgFilename)
    
    def loadMap(self, svgFilename):
        xml = dom.parse(svgFilename)
        
        reFillColor = re.compile('.*fill:#([0-9a-f]{6}|none).*')
        reStrokeColor = re.compile('.*stroke:#([0-9a-f]{6}|none).*')
        rePathTranslate = re.compile('translate\(([0-9.-]+),([0-9.-]+)\)')
        
        # sky and ground color
        for rect in xml.getElementsByTagName('rect'):
            if rect.getAttribute('id') == 'sky':
                styleString = rect.getAttribute('style')
                if styleString is not None:
                    matches = reFillColor.match(styleString)
                    if matches is not None:
                        if matches.groups()[0] == 'none':
                            self.skyColor = ''
                        else:
                            self.skyColor = '#{}'.format(matches.groups()[0])
            
            if rect.getAttribute('id') == 'ground':
                styleString = rect.getAttribute('style')
                if styleString is not None:
                    matches = reFillColor.match(styleString)
                    if matches is not None:
                        if matches.groups()[0] == 'none':
                            self.groundColor = ''
                        else:
                            self.groundColor = '#{}'.format(matches.groups()[0])
        
        for path in xml.getElementsByTagName('path'):
            coordinateString = path.getAttribute('d')
            
            # parse translate transform
            translateVector = Vector3D(0.0, 0.0, 0.0)
            transformString = path.getAttribute('transform')
            if transformString is not None:
                if transformString.startswith('translate'):                    
                    matches = rePathTranslate.match(transformString)
                    if matches is not None:
                        matchGroups = matches.groups()
                        translateVector.x = float(matchGroups[0])
                        translateVector.z = -float(matchGroups[1])
            
            # arcs
            if path.getAttribute('sodipodi:type') == 'arc':
                # start position
                if path.getAttribute('id') == 'startposition':
                    x = float(path.getAttribute('sodipodi:cx'))
                    z = -float(path.getAttribute('sodipodi:cy'))
                    self.startPosition = Point3D(x + translateVector.x,
                                                 0.0,
                                                 z + translateVector.z)
                    continue
                
                # map objects
                if path.getAttribute('inkscape:label') is not None:
                    labelParts =  path.getAttribute('inkscape:label').split(':')
                    if labelParts[0] == 'mo':
                        x = float(path.getAttribute('sodipodi:cx'))
                        z = -float(path.getAttribute('sodipodi:cy'))
                        y = 0.0
                        if len(labelParts) >= 3:
                            y = float(labelParts[2])
                        movementVector = Vector3D(x + translateVector.x,
                                                  y,
                                                  z + translateVector.z)
                        rotationAngle = 0.0
                        if len(labelParts) >= 4:
                            rotationAngle = float(labelParts[3])
                        polygons = self.mapObjectManager. \
                                getPolygonsForMapObjectRotateMove(
                                          labelParts[1],
                                          rotationAngle,
                                          movementVector)
                        if polygons is not None:
                            self.polygons.extend(polygons)
                continue
            
            # wall coordinates
            parts = coordinateString.split(' ')
            x = float(parts[1].split(',')[0]) + translateVector.x
            z = -float(parts[1].split(',')[1]) + translateVector.z
            if parts[0] == 'm':     #relative move
                xDelta = float(parts[2].split(',')[0])
                zDelta = -float(parts[2].split(',')[1])
            elif parts[0] == 'M':     #absolute move
                xDelta = float(parts[2].split(',')[0]) - x + translateVector.x
                zDelta = -float(parts[2].split(',')[1]) - z + translateVector.z
            else:
                print('something went horribly wrong')
                continue
            
            #parse color
            fill = 'grey'
            outline = 'darkgrey'
            styleString = path.getAttribute('style')
            if styleString is not None:
                matches = reFillColor.match(styleString)
                if matches is not None:
                    if matches.groups()[0] == 'none':
                        fill = ''
                    else:
                        fill = '#{}'.format(matches.groups()[0])
                
                matches = reStrokeColor.match(styleString)
                if matches is not None:
                    if matches.groups()[0] == 'none':
                        outline = ''
                    else:
                        outline = '#{}'.format(matches.groups()[0])
            
            self.addWall(x, z, xDelta, zDelta, fill, outline)
        
        
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
    
    def getStartPosition(self):
        return self.startPosition
