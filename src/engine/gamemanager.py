from engine.character import Character
from engine.gridmap import GridMap
from engine.inputcontrol import InputControl
from engine.svgmap import SVGMap
from engine.view import View


from math import cos, pi, sin
from threading import Thread


class GameManager(Thread):
    def __init__(self):
        Thread.__init__(self)
        
        self.characters = []
        self.gameMap = GridMap()
        #self.gameMap = SVGMap("data/maps/map_city.svg")
        self.views = []
        self.isStarted = False
        self.inputController = []
    
    def addView(self, window, canvas, character):
        # don't start two views on same canvas
        for view in self.views:
            if view.getCanvas() == canvas:
                return
        
        newView = View(self, self.gameMap, character, window, canvas)
        self.views.append(newView)
        
        if self.isStarted:
            newView.start()
    
    def addInputControl(self, window, character):
        newInputControl = InputControl(self, character, window)
        self.inputController.append(newInputControl)
        
        if self.isStarted:
            newInputControl.start()
    
    
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
        
        for inputControl in self.inputController:
            inputControl.start()
        
        for view in self.views:
            view.start()