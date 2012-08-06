'''
Created on Aug 4, 2012

@author: marcel
'''
from engine.coordinate import Point2D

class Polygon(object):
    '''
    a 4 sided polygon
    '''

    def __init__(self, point1, point2, point3, point4):
        '''the blocks normal vector points towards you when you see the points
        from 1 to 4 in a counter-clockwise manner'''
        
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self.point4 = point4
    
    def getPoints3D(self):
        return [self.point1, self.point2, self.point3, self.point4]
    
    def getPoints2D(self, eye, player):
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
    
    def getNormalVector(self):
        '''for future use'''
        
        pass
