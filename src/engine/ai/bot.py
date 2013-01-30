from engine.shared.utils import runAndWait

import random
from threading import Thread
from engine.shared.coordinate import Vector3D

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
        
        self.gameManager.moveRotateCharacter(self.characterId,
                            self.moveVector.z, -self.moveVector.x,
                            self.lastRotation)
        
        #player = self.gameManager.getCharacterInfo(self.characterId)
        #print('Bot::_run: position', player.getPosition())
        #print('Bot::_run: rotation', player.getViewAngle())
    
    
    def stop(self):
        self.running = False