from engine.character import Character
from engine.gridmap import GridMap
#from engine.svgmap import SVGMap


from math import cos, pi, sin
from engine.coordinate import Point3D


class GameManager():
    def __init__(self):        
        self.characters = []
        self.gameMap = GridMap()
        #self.gameMap = SVGMap("data/maps/map_city.svg")
    
    
    def addCharacter(self):
        character = Character()
        character.setPosition(self.gameMap.getStartPosition())
        self.characters.append(character)
        
        return character
    
    def getStaticPolygons(self):
        return self.gameMap.getStaticPolygons()
    
    def getDynamicPolygons(self):
        return self.gameMap.getDynamicPolygons()


    def moveRotateCharacter(self, character,
                            moveDeltaForward, moveDeltaLeft,
                            rotation):
        character.viewAngle += rotation
        
        # forward/backward
        moveDeltaX = -sin(character.viewAngle) * moveDeltaForward
        moveDeltaZ = -cos(character.viewAngle) * moveDeltaForward
        
        # left/right
        moveDeltaX += -cos(character.viewAngle) * moveDeltaLeft
        moveDeltaZ += sin(character.viewAngle) * moveDeltaLeft
        
        newPosition = Point3D(character.position.x - moveDeltaX,
                              character.position.y,
                              character.position.z - moveDeltaZ)
        
        if character.clipping == False:
            character.position = newPosition
        else:
            if self.gameMap.getPathBlockedPoint(character.position,
                    newPosition) is None:
                character.position = newPosition

    def start(self):
        self.gameMap.start()
    
    def stop(self):
        self.gameMap.stop()
