from math import atan2, cos, pi, sin, sqrt

class Point2D(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return '{} ({}, {})'.format(id(self), self.x, self.y)

class Point3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return '{} ({}, {}, {})'.format(id(self), round(self.x, 2), round(self.y, 2), round(self.z, 2))
    
    def __add__(self, other):
        return Vector3D(self.x + other.x,
                        self.y + other.y,
                        self.z + other.z)
    
    def __sub__(self, other):
        return Vector3D(self.x - other.x,
                        self.y - other.y,
                        self.z - other.z)
    
    def moveByVector(self, vector):
        self.x += vector.x
        self.y += vector.y
        self.z += vector.z
    
    def rotateAroundYAxisToAngle(self, rotationCenter, angle):
        # points shifted to have rotation center at (0, 0, 0)
        tmpPoint = Point3D(self.x - rotationCenter.x,
                           0,
                           self.z - rotationCenter.z)
        tmpLength = sqrt(tmpPoint.x * tmpPoint.x + tmpPoint.z * tmpPoint.z)
        
        tmpPoint.x = tmpLength * cos(angle)
        tmpPoint.z = tmpLength * sin(angle)
        
        # shift back to rotation center
        self.x = tmpPoint.x + rotationCenter.x
        self.z = tmpPoint.z + rotationCenter.z


    def rotateAroundYAxisByAngle(self, rotationCenter, angle):
        # points shifted to have rotation center at (0, 0, 0)
        tmpPoint = Point3D(self.x - rotationCenter.x,
                           0,
                           self.z - rotationCenter.z)
        tmpLength = sqrt(tmpPoint.x * tmpPoint.x + tmpPoint.z * tmpPoint.z)
        
        currentAngle = atan2(tmpPoint.z, tmpPoint.x)
        newAngle = currentAngle + angle
        
        tmpPoint.x = tmpLength * cos(newAngle)
        tmpPoint.z = tmpLength * sin(newAngle)
        
        # shift back to rotation center
        self.x = tmpPoint.x + rotationCenter.x
        self.z = tmpPoint.z + rotationCenter.z


class Point3DColorUV(Point3D):
    def __init__(self, positionTuple = [None, None, None],
                 colorTuple = [None, None, None],
                 uvTuple = [None,None]):
        Point3D.__init__(self,
                         positionTuple[0],
                         positionTuple[1],
                         positionTuple[2])
        
        self.r = colorTuple[0]
        self.g = colorTuple[1]
        self.b = colorTuple[2]
        
        self.u = uvTuple[0]
        self.v = uvTuple[1]

class Vector3D(Point3D):
    def __init__(self, x, y, z):
        Point3D.__init__(self, x, y, z)
    
    def __add__(self, other):
        return Vector3D(self.x + other.x,
                        self.y + other.y,
                        self.z + other.z)
    
    def __sub__(self, other):
        return Vector3D(self.x - other.x,
                        self.y - other.y,
                        self.z - other.z)

    
    def getLength(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def getNormalizedVector(self):
        length = self.getLength()
        if length == 0.0:
            return Vector3D(0, 0, 0)
        
        return Vector3D(self.x / length,
                        self.y / length,
                        self.z / length)


    def multiplyByScalar(self, scalar):
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar


    def normalize(self):
        length = self.getLength()
        if length == 0.0 or length == 1.0:
            return
        
        self.x /= length
        self.y /= length
        self.z /= length
    
    def getCrossProduct(self, vector):
        result = Vector3D((self.y * vector.z) - (self.z * vector.y),
                          (self.z * vector.x) - (self.x * vector.z),
                          (self.x * vector.y) - (self.y * vector.x))
        return result