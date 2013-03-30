from engine.shared.utils import runAndWait
from engine.shared.coordinate import Vector3D
from engine.shared.actions import ACTION_FORWARD, ACTION_BACK, ACTION_RIGHT,\
    ACTION_LEFT, ACTION_ROTATE_RIGHT, ACTION_ROTATE_LEFT

from math import pi
import random
from threading import Thread


class Bot(Thread):
    def __init__(self, gameManager, characterId):
        Thread.__init__(self)
        self.gameManager = gameManager
        self.characterId = characterId
        
        self.millisecondsPerTick = 100
        self.running = False
        
        self.moveVector = Vector3D(0.0, 0.0, 0.0)
        self.lastRotation = 0.0
    
    
    def run(self):
        self.running = True
        while self.running:
            runAndWait(self._run, self.millisecondsPerTick)
    
    def _run(self):
        self.moveVector.x += (random.randrange(0, 21) - 10) / 40
        self.moveVector.z += (random.randrange(0, 21) - 10) / 40
        
        self.moveVector.normalize()
        self.moveVector.x *= 0.3
        self.moveVector.z *= 0.3
        
        self.lastRotation = ((random.randrange(0, 9) - 4) * 0.017 + \
                    self.lastRotation) / 2
        
        actions = 0
        if self.moveVector.z > 0.01:
            actions += ACTION_FORWARD
        elif self.moveVector.z < -0.01:
            actions += ACTION_BACK
        
        if self.moveVector.x > 0.01:
            actions += ACTION_RIGHT
        elif self.moveVector.z < -0.01:
            actions += ACTION_LEFT
        
        if self.lastRotation > pi / 120:
            actions += ACTION_ROTATE_RIGHT
        elif self.lastRotation < -pi / 120:
            actions += ACTION_ROTATE_LEFT
        
        self.gameManager.setActions(self.characterId, actions)
        
        #player = self.gameManager.getCharacterInfo(self.characterId)
        #print('Bot::_run: position', player.getPosition())
        #print('Bot::_run: rotation', player.getViewAngle())
    
    
    def stop(self):
        self.running = False