class Point2D(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Point3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def moveByVector(self, vector):
        self.x += vector.x
        self.y += vector.y
        self.z += vector.z

class Vector3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
