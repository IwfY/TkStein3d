'''
Created on Nov 7, 2012

@author: Marcel Pfeiffer
'''
from time import sleep

class Client(object):
    def __init__(self, gameManager, player):
        self.gameManager = gameManager
        self.player = player
        
        self.gameMap = self.gameManager.getGameMap()
        self.viewAndInput = None
        self.running = True
    
    
    def getGameMap(self):
        return self.gameMap

    def getPlayer(self):
        return self.player
    
    def moveRotateCharacter(self, character,
                            moveDeltaForward, moveDeltaLeft,
                            rotation):
        '''wrapper for GameManager method'''
        self.gameManager.moveRotateCharacter(character,
                                             moveDeltaForward, moveDeltaLeft,
                                             rotation)
    
    def start(self):
        self.viewAndInput.start()
        
        while self.running:
            sleep(0.25)
        self.viewAndInput.stop()
    
    
    def stop(self):
        self.running = False
