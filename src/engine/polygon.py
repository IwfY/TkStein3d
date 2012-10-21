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


    def polygonFacesPoint(self, point):
        '''returns true if polygon faces a point so it can be seen from it
        
        mathematical background
        ~~~~~~~~~~~~~~~~~~~~~~
        v ... the vector (x, z) from polygon point0 to point2
        n ... normal (x, z) of vector v using the following formula:
                n = ( v.z)
                    (-v.x)
        p ... point
        
        pp0 ... polygon point 0
        
        p can be expressed as linear combination of v, n and pp0:
        
        p = pp0 + a*v + b*n
        
        normal faces the eye if b < 0
        
        b = ((p.x  - pp0.x) * v.z / v.x + pp0.z - p.z) / (n.x * v.z / v.x - n.z)
        
        return true if b >= 0, false otherwise
        '''
        v = Vector3D(self.points[2].x - self.points[0].x,
                     0,
                     self.points[2].z - self.points[0].z)
        n = self.getNormalVectorXZ()
        
        if v.x == 0.0:
            b = -0.1
        elif (n.x * v.z / v.x - n.z) == 0.0:
            b = -0.1
        else:
            b = ((point.x  - self.points[0].x) * v.z / v.x + \
                  self.points[0].z - point.z) / (n.x * v.z / v.x - n.z)
        
        #print(id(self), self.points[0], self.points[2], '\n  v ', v, \
        # '\n  n ', n, '\n  p ', point, '\n  b ', b)
        
        
        if b < 0.0:
            return True
        
        return False
