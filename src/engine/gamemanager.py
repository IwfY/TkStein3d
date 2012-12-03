from engine.charactermanager import CharacterManager
from engine.gridmap import GridMap
#from engine.svgmap import SVGMap


from math import cos, pi, sin
from engine.coordinate import Point3D



class GameManager():
    def __init__(self):        
        self.characters = []
        self.characterManager = CharacterManager(self)
        self.gameMap = GridMap(self)
        #self.gameMap = SVGMap("data/maps/map_city.svg")
    
    def getGameMap(self):
        return self.gameMap
    
    def addCharacter(self):
        '''adds a new character to the game and returns its ID'''
        return self.characterManager.addCharacter()
    
    def getCharacterInfo(self, characterID):
        character = self.characterManager.getCharacterByID(characterID)
        if character is None:
            print('GameManager::getCharacterInfo character not found.',
                  characterID)
            return None

        return character.getCharacterInfo()
    
    def getCharacters(self):
        return self.characterManager.getCharacters()
    
    def getStaticPolygons(self):
        return self.gameMap.getStaticPolygons()
    
    def getDynamicPolygons(self):
        return self.gameMap.getDynamicPolygons()


    def moveRotateCharacter(self, characterID,
                            moveDeltaForward, moveDeltaLeft,
                            rotation):
        character = self.characterManager.getCharacterByID(characterID)
        if character is None:
            print('GameManager::moveRotateCharacter: character not found',
                  characterID)
            return
        
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
