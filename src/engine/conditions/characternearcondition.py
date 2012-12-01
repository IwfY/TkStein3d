from engine.conditions.condition import Condition
from engine.mathhelper import getPointDistance

class CharacterNearCondition(Condition):
    def __init__(self, gameManager, position, radius):
        self.gameManager = gameManager
        self.position = position
        self.radius = radius
    
    def check(self):
        for character in self.gameManager.getCharacters():
            if getPointDistance(character.getPosition(), self.position) <= \
                    self.radius:
                return True

        return False
