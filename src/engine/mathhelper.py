def getPointDistance(point1, point2):
    '''get the distance between 2 points'''
    return pow(pow(point1.x - point2.x, 2.0) + \
               pow(point1.y - point2.y, 2.0) + \
               pow(point1.z - point2.z, 2.0),
               0.5)