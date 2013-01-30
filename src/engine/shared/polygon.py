'''
Created on Aug 4, 2012

@author: marcel
'''
from engine.shared.coordinate import Point2D, Point3D, Vector3D
from engine.shared.mathhelper import getVectorDotProduct, getAngleBetweenVectors

from math import pi


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
        newPoint.rotateAroundYAxisByAngle(rotationCenter, rotationAngle)
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

    def __init__(self, pId, points, fill='#505050', outline='#101010'):
        '''the blocks normal vector points towards you when you see the points
        from 1 to N in a counter-clockwise manner'''
        
        self.points = points
        self.polygonId = pId
        self.fill = fill
        self.outline = outline
    
    def getFillColorTuple(self):
        r = int(self.fill[1:3], 16)
        g = int(self.fill[3:5], 16)
        b = int(self.fill[5:7], 16)
        return r, g, b
    
    def getOutlineColorTuple(self):
        r = int(self.outline[1:3], 16)
        g = int(self.outline[3:5], 16)
        b = int(self.outline[5:7], 16)
        return r, g, b
    
    def getPolygonId(self):
        return self.polygonId

    def setPolygonId(self, polygonId):
        self.polygonId = polygonId
    
    def getPoints3D(self):
        return self.points
    

    def getTrianglePoints3D(self):
        return [self.points[0], self.points[1], self.points[2],
                self.points[0], self.points[2], self.points[3]]

    
    def getTriangleUVCoordinates(self):
        return [0.0, 0.0, 1.0, 0.0, 1.0, 1.0,
               0.0, 0.0, 1.0, 1.0, 0.0, 1.0]


    def getPoints2D(self, eye):
        '''transform 3d points to 2d representations on view plane (z = 0)'''
        outPoints = []
        for point in self.getPoints3D():
            if point.z - eye.z == 0.0:
                x = 0.0 #TODO
                y = 0.0
            else:
                x = abs(eye.z) * point.x / abs(point.z - eye.z)
                y = abs(eye.z) * point.y / abs(point.z - eye.z)
            outPoints.append(Point2D(x, y))
        
        return outPoints
        
    
    def getCenter(self):
        '''get the point in the middle of diagonal between point 0 and 2'''
        if len(self.points) >= 3:
            return Point3D(self.points[2].x + \
                                (self.points[0].x - self.points[2].x) / 2,
                           self.points[2].y + \
                                (self.points[0].y - self.points[2].y) / 2,
                           self.points[2].z + \
                                (self.points[0].z - self.points[2].z) / 2)
    
    def getPlaneParameters(self):
        '''return tuple (a, b, c, d) for plane that represents the polygon as
        ax + by + cz + d = 0'''
        normal = self.getNormalVector()
        #d = -ax - by - cz
        d = - normal.x * self.points[0].x - \
            normal.y * self.points[0].y - \
            normal.z * self.points[0].z
        
        return (normal.x, normal.y, normal.z, d)

    
    def getNormalVector(self):
        '''get the normalized normal vector of the polygon'''
        vector1 = Vector3D(self.points[1].x - self.points[0].x,
                           self.points[1].y - self.points[0].y,
                           self.points[1].z - self.points[0].z)
        vector2 = Vector3D(self.points[2].x - self.points[0].x,
                           self.points[2].y - self.points[0].y,
                           self.points[2].z - self.points[0].z)
        
        normal = vector1.getCrossProduct(vector2)
        
        return normal.getNormalizedVector()



    def facesPoint(self, point):
        '''returns true if polygon faces a point so it can be seen from it'''
        a, b, c, d = self.getPlaneParameters()
        
        distancePointPlane = a * point.x + b * point.y + c * point.z + d
        
        if distancePointPlane >= 0.0: 
            return True
        
        return False
