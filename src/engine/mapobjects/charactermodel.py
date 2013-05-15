from engine.mapobjects.mapobject import MapObject
from engine.server.block import Block
from engine.shared.coordinate import Point3D

class CharacterModel(MapObject):
    def __init__(self, gameMap, character):
        MapObject.__init__(self, gameMap)
        self.character = character
        
        self.tick()
    
    def tick(self):
        characterPosition = self.character.getPosition()
        characterRotation = self.character.getViewAngle()
        block = Block(Point3D(characterPosition.x - 0.2,
                              characterPosition.y - 0.5,
                              characterPosition.z - 0.2),
                      Point3D(characterPosition.x + 0.2,
                              characterPosition.y + 0.2,
                              characterPosition.z + 0.2),
                      True)
        blockPolygons = block.getPolygons()
        
        for polygon in blockPolygons:
            polygon.fill = '#101018'
            for point in polygon.getPoints3D():
                point.rotateAroundYAxisByAngle(characterPosition,
                                               characterRotation)
        self.polygons = blockPolygons
