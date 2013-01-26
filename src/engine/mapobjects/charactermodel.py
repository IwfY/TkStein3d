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
        block = Block(Point3D(characterPosition.x - 0.15,
                              characterPosition.y - 0.5,
                              characterPosition.z - 0.15),
                      Point3D(characterPosition.x + 0.15,
                              characterPosition.y + 0.2,
                              characterPosition.z + 0.15))
        self.polygons = block.getPolygons()