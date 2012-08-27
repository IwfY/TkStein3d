'''
Created on Aug 4, 2012

@author: marcel
'''
from engine.coordinate import Point2D, Point3D


def moveAndRotatePolygon(polygon,
                         movementVector,
                         rotationCenter,
                         rotationAngle):
    '''return a new polygon that is moved and rotated'''
    newPolygonPoints = []
    
    for point in polygon.getPoints3D():
        newPoint = Point3D(point.x, point.y, point.z)
        newPoint.moveByVector(movementVector)
        newPoint.rotateAroundYAxisToAngle(rotationCenter, rotationAngle)
        newPolygonPoints.append(newPoint)

    newPolygon = Polygon(polygon.getPolygonId(), newPolygonPoints)
    return newPolygon

class Polygon(object):
    '''
    a N sided polygon with all points on one plane
    '''

    def __init__(self, pId, points, fill='grey', outline='darkgrey'):
        '''the blocks normal vector points towards you when you see the points
        from 1 to N in a counter-clockwise manner'''
        
        self.points = points
        self.polygonId = pId
        self.fill = fill
        self.outline = outline
    
    def getPolygonId(self):
        return self.polygonId

    def setPolygonId(self, polygonId):
        self.polygonId = polygonId
    
    def getPoints3D(self):
        return self.points
    
    def getPoints2D(self, eye, player):
        '''transform 3d points to 2d representations on view plane'''
        outPoints = []
        for point in self.getPoints3D():
            if eye.z - point.z == 0.0:
                x = 0.0 #TODO
                y = 0.0
            else:
                x = (eye.z * point.x) / (eye.z - point.z)
                y = (eye.z * point.y) / (eye.z - point.z)
            outPoints.append(Point2D(x, y))
        
        return outPoints
        
    
    def getCenter(self):
        '''get the point at the center of the polygone'''
        if len(self.points) >= 3:
            return Point3D(self.points[3].x + \
                                (self.points[1].x - self.points[3].x) / 2,
                           self.points[3].y + \
                                (self.points[1].y - self.points[3].y) / 2,
                           self.points[3].z + \
                                (self.points[1].z - self.points[3].z) / 2)
    
    def getNormalVector(self):
        '''for future use'''
        
        pass
