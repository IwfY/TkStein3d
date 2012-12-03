from engine.character import Character

from threading import Lock

class CharacterManager(object):
    lastID = 0    
    idLock = Lock()
    
    def __init__(self, gameManager):
        self.gameManager = gameManager
        
        self.characters = []
    
    def addCharacter(self):
        newCharacterID = self.getNewCharacterId()
        character = Character(newCharacterID)
        character.setPosition(self.gameManager.getGameMap().getStartPosition())
        self.characters.append(character)
        
        print('CharacterManager::addCharacter: character created; id',
              newCharacterID)
        return newCharacterID
    
    def getNewCharacterId(self):
        out = -1
        CharacterManager.idLock.acquire()
        try:
            CharacterManager.lastID += 1
            out = CharacterManager.lastID
        finally:
            CharacterManager.idLock.release()
        
        return out
    
    def removeCharacter(self, character):
        if character in self.characters:
            self.characters.remove(character)
            return True
        
        return False
    
    def removeCharacterByID(self, characterID):
        toRemove = None
        for character in self.characters:
            if character.getCharacterID == characterID:
                toRemove = character
                break
        if toRemove is not None:
            self.characters.remove(toRemove)
            return True
        
        return False
    
    def getCharacters(self):
        return self.characters
    
    def getCharacterByID(self, characterID):
        out = None
        for character in self.characters:
            if character.getCharacterID() == characterID:
                out = character
                break
        
        return out
