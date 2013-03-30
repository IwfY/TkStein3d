from engine.shared.actions import ACTION_FORWARD, ACTION_BACK, ACTION_LEFT,\
    ACTION_RIGHT, ACTION_SHOOT, ACTION_ROTATE_LEFT, ACTION_ROTATE_RIGHT
from engine.shared.utils import runAndWait

from math import pi
from threading import Thread


class ServerInputController(Thread):
    '''
    server thread to handle incoming input commands from client
    '''

    def __init__(self, gameManager):
        Thread.__init__(self)
        
        self.gameManager = gameManager
        
        # map of characterId -> integer for actions
        self.characterActionMap = dict()
        
        self.acceptedActions = [ACTION_FORWARD,
                                ACTION_BACK,
                                ACTION_LEFT,
                                ACTION_RIGHT,
                                ACTION_ROTATE_LEFT,
                                ACTION_ROTATE_RIGHT,
                                ACTION_SHOOT]
        
        self.millisecondsPerTick = 30
        self.running = True


    def setActions(self, characterId, actions):
        if characterId in self.characterActionMap:
            self.characterActionMap[characterId] = actions


    def stop(self):
        self.running = False


    def run(self):
        while self.running:
            runAndWait(self._run, self.millisecondsPerTick)


    def _run(self):
        # split and check actions
        for character in self.gameManager.getCharacters():
            characterId = character.getCharacterID()
            if characterId in self.characterActionMap.keys():
                #characterActions is an integer
                characterActions = self.characterActionMap[characterId]
                characterActionList = []
                for acceptedAction in self.acceptedActions:
                    actionId = acceptedAction & characterActions 
                    if actionId:
                        characterActionList.append(actionId)
                self.applyActions(characterId, characterActionList)


    def applyActions(self, characterId, characterActionList):
        movementPerTick = 0.05
        rotationPerTick = pi / 60
        moveForward = 0.0
        moveLeft = 0.0
        rotateClockwise = 0.0
        
        if (ACTION_FORWARD in characterActionList):
            moveForward += movementPerTick
        if (ACTION_BACK in characterActionList):
            moveForward -= movementPerTick
        if (ACTION_LEFT in characterActionList):
            moveLeft += movementPerTick
        if (ACTION_RIGHT in characterActionList):
            moveLeft -= movementPerTick
        if (ACTION_ROTATE_LEFT in characterActionList):
            rotateClockwise -= rotationPerTick
        if (ACTION_ROTATE_RIGHT in characterActionList):
            rotateClockwise += rotationPerTick
        if (ACTION_SHOOT in characterActionList):
            pass
        
        self.gameManager.moveRotateCharacter(characterId,
                                             moveForward,
                                             moveLeft,
                                             rotateClockwise)
