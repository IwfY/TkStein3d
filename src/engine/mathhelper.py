def getPointDistance(point1, point2):
    '''get the distance between 2 points'''
    return pow(pow(point1.x - point2.x, 2.0) + \
               pow(point1.y - point2.y, 2.0) + \
               pow(point1.z - point2.z, 2.0),
               0.5)

def getIntersectionXYPlane(point1, point2):
    '''get the intersection of the x-y plane of the line between two given
    points
    
    using equation:
    x = x1 + a * (x2 - x1)
    y = y1 + a * (y2 - y1)
    z = z1 + a * (z2 - z1)
    
    for z = 0
    
    @return tuple (x, y, z)
    '''
    a = - point1.z / (point2.z - point1.z)
    x = point1.x + a * (point2.x - point1.x)
    y = point1.y + a * (point2.y - point1.y)
    
    return (x, y, 0.0)
