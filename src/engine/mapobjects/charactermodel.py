from engine.mapobjects.mapobject import MapObject
from engine.server.block import Block
from engine.coordinate import Point3D

class CharacterModel(MapObject):
    def __init__(self, gameMap, character):
        MapObject.__init__(self, gameMap)
        self.character = character
        
        self.tick()
    
    def tick(self):
        characterPosition = self.character.getPosition()
        block = Block(Point3D(characterPosition.x - 3,
                              characterPosition.y - 7.5,
                              characterPosition.z - 3),
                      Point3D(characterPosition.x + 3,
                              characterPosition.y + 2,
                              characterPosition.z + 3))
        self.polygons = block.getPolygons()