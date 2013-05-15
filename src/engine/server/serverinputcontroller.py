from engine.shared.actions import *
from engine.shared.coordinate import Vector3D, Point3D
from engine.shared.utils import runAndWait

from math import pi
from threading import Thread
from engine.mapobjects.bullet import Bullet


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
                                ACTION_WALK,
                                ACTION_SHOOT]
        
        self.millisecondsPerTick = 20
        self.running = False


    def setActions(self, characterId, actions):
        self.characterActionMap[characterId] = actions


    def stop(self):
        self.running = False


    def run(self):
        self.running = True
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
        #print('ServerInputController::applyActions',
        #      characterId, characterActionList)
        movementPerTick = 0.05
        movementWalkModifier = 0.5
        rotationPerTick = pi / 60
        movementVector = Vector3D(0.0, 0.0, 0.0) # +z ... forward; +x ... left
        rotateClockwise = 0.0
        
        if (ACTION_FORWARD in characterActionList):
            movementVector.z += movementPerTick
        if (ACTION_BACK in characterActionList):
            movementVector.z -= movementPerTick
        if (ACTION_LEFT in characterActionList):
            movementVector.x += movementPerTick
        if (ACTION_RIGHT in characterActionList):
            movementVector.x -= movementPerTick
        
        # don't let character walk diagonally faster
        movementVector.normalize()
        movementVector.multiplyByScalar(movementPerTick)
        
        if (ACTION_WALK in characterActionList):
            movementVector.multiplyByScalar(movementWalkModifier)
        
        if (ACTION_ROTATE_LEFT in characterActionList):
            rotateClockwise -= rotationPerTick
        if (ACTION_ROTATE_RIGHT in characterActionList):
            rotateClockwise += rotationPerTick

        if (ACTION_SHOOT in characterActionList):
            character = self.gameManager.getCharacterInfo(characterId)
            self.gameManager.getGameMap().\
                    addMapObject(
                        Bullet(self.gameManager.getGameMap(),
                               character.getPosition(),
                               Point3D(1.0, 0, 0)))
        
        self.gameManager.moveRotateCharacter(characterId,
                                             movementVector.z,
                                             movementVector.x,
                                             rotateClockwise)
