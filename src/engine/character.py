from engine.coordinate import Point3D
class Character(object):
    def __init__(self, position=None):
        if position is not None:
            self.position = position
        else:
            self.position = Point3D(0.0, 0.0, 0.0)
    
    def getPosition(self):
        return self.position
