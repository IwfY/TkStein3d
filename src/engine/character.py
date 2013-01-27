from engine.coordinate import Point3D
from engine.shared.characterinfo import CharacterInfo

class Character(object):
    def __init__(self, characterID,
                 position=Point3D(0.0, 0.0, 0.0), viewAngle=0.0):
        self.characterID = characterID
        self.position = position
        self.viewAngle = viewAngle
        self.clipping = True
    
    def getCharacterID(self):
        return self.characterID
    
    def getViewAngle(self):
        return self.viewAngle

    def setViewAngle(self, viewAngle):
        self.viewAngle = viewAngle        
    
    def getPosition(self):
        return self.position
    
    def setPositionXYZ(self, x, y, z):
        self.position = Point3D(x, y, z)
    
    def setPosition(self, point3d):
        self.position = point3d
    
    def getCharacterInfo(self):
        out = CharacterInfo(self.position, self.viewAngle)
        
        return out
