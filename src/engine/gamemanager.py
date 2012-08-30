from engine.character import Character
from engine.gridmap import GridMap
from engine.view import View

from math import cos, pi, sin
from threading import Thread
from engine.svgmap import SVGMap


class GameManager(Thread):
    def __init__(self):
        Thread.__init__(self)
        
        self.characters = []
        #self.gameMap = GridMap()
        self.gameMap = SVGMap("/home/marcel/projects/programming/python/TkStein3d/docs/map_samples/map2.svg")
        self.views = []
        self.isStarted = False
    
    def addView(self, window, canvas, character):
        # don't start two views on same canvas
        for view in self.views:
            if view.getCanvas() == canvas:
                return
        
        newView = View(self, self.gameMap, character, window, canvas)
        self.views.append(newView)
        
        if self.isStarted:
            newView.start()
    
    def addCharacter(self):
        character = Character()
        character.setPosition(self.gameMap.getStartPosition())
        self.characters.append(character)
        
        return character
    
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
        
        character.position.x -= moveDeltaX
        character.position.z -= moveDeltaZ
        
    
    def run(self):
        self.isStarted = True
        
        for view in self.views:
            view.start()