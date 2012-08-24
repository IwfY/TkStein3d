from engine.character import Character
from engine.map import Map
from engine.view import View

from threading import Thread


class GameManager(Thread):
    def __init__(self):
        Thread.__init__(self)
        
        self.characters = []
        self.gameMap = Map()
        self.views = []
        self.isStarted = False
    
    def addView(self, canvas, character):
        # don't start two views on same canvas
        for view in self.views:
            if view.getCanvas() == canvas:
                return
        
        newView = View(self, self.gameMap, character, canvas)
        self.views.append(newView)
        
        if self.isStarted:
            newView.start()
    
    def addCharacter(self):
        character = Character()
        self.characters.append(character)
        
        return character
    
    def moveCharacter(self, character, vector):
        character.position.x += vector.x
        character.position.y += vector.y
        character.position.z += vector.z
    
    def run(self):
        self.isStarted = True
        
        for view in self.views:
            view.start()