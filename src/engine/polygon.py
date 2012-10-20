'''
Created on Aug 4, 2012

@author: marcel
'''
from engine.coordinate import Point2D, Point3D, Vector3D


def moveAndRotatePolygon(polygon,
                         movementVector,
                         rotationCenter,
                         rotationAngle):
    '''return a new polygon that is moved and rotated
    the polygon is first moved, rotated afterwards
    the rotation center is not moved'''
    newPolygonPoints = []
    
    for point in polygon.getPoints3D():
        newPoint = Point3D(point.x, point.y, point.z)
        newPoint.moveByVector(movementVector)
        newPoint.rotateAroundYAxisToAngle(rotationCenter, rotationAngle)
        newPolygonPoints.append(newPoint)

    newPolygon = getPolygonCopy(polygon)
    newPolygon.points = newPolygonPoints
    return newPolygon


def rotateAndMovePolygon(polygon,
                         movementVector,
                         rotationCenter,
                         rotationAngle):
    '''return a new polygon that is rotated and moved
    the polygon is first rotated, moved afterwards'''
    newPolygonPoints = []
    
    for point in polygon.getPoints3D():
        newPoint = Point3D(point.x, point.y, point.z)
        newPoint.rotateAroundYAxisToAngle(rotationCenter, rotationAngle)
        newPoint.moveByVector(movementVector)
        newPolygonPoints.append(newPoint)

    newPolygon = getPolygonCopy(polygon)
    newPolygon.points = newPolygonPoints
    return newPolygon


def getPolygonCopy(polygon):
    newPolygon = Polygon(polygon.polygonId,
                         polygon.points,
                         polygon.fill,
                         polygon.outline)
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
            return Point3D(self.points[2].x + \
                                (self.points[0].x - self.points[2].x) / 2,
                           self.points[2].y + \
                                (self.points[0].y - self.points[2].y) / 2,
                           self.points[2].z + \
                                (self.points[0].z - self.points[2].z) / 2)
    
    def getNormalVectorXZ(self):
        '''get the normal vector when considering the polygon as a line on the
        x-z-plane
        
        points 1 and 3 are used to calculate the the line v
        
        v = (p3.x) - (p1.x)
            (p3.z)   (p1.z)
            
        normal n = ( v.z)
                   (-v.x)
        '''
        
        vX = self.points[2].x - self.points[0].x
        vZ = self.points[2].z - self.points[0].z
        
        return Vector3D(-vZ, 0, vX)
        
        pass
