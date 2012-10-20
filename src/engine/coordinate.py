from engine.mathhelper import getPointDistance

from math import atan2, cos, pi, sin

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
        return '{} ({}, {}, {})'.format(id(self), self.x, self.y, self.z)
    
    def moveByVector(self, vector):
        self.x += vector.x
        self.y += vector.y
        self.z += vector.z
    
    def rotateAroundYAxisToAngle(self, rotationCenter, angle):
        '''see http://mathworld.wolfram.com/SphericalCoordinates.html
        (z and y are switched here)'''
        length = getPointDistance(Point3D(self.x, 0.0, self.z),
                                  Point3D(rotationCenter.x,
                                          0.0,
                                          rotationCenter.z))
        vector = Vector3D(self.x - rotationCenter.x,
                          0,
                          self.z - rotationCenter.z)
        
        azimuthal = atan2(vector.z, vector.x)
        azimuthal += angle
        polar = pi/2
        
        self.x = length * cos(azimuthal) * sin(polar) + rotationCenter.x
        self.z = length * sin(azimuthal) * sin(polar) + rotationCenter.z

class Vector3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return '{} ({}, {}, {})'.format(id(self), self.x, self.y, self.z)
