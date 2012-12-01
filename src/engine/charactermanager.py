from engine.character import Character

class CharacterManager(object):
    def __init__(self, gameManager):
        self.gameManager = gameManager
        
        self.characters = []
    
    def addCharacter(self):
        character = Character()
        character.setPosition(self.gameManager.getGameMap().getStartPosition())
        self.characters.append(character)
        
        return character
    
    def removeCharacter(self, character):
        if character in self.characters:
            self.characters.remove(character)
    
    def getCharacters(self):
        return self.characters