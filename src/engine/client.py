'''
Created on Nov 7, 2012

@author: Marcel Pfeiffer
'''


class Client(object):
    def __init__(self, gameManager, player):
        self.gameManager = gameManager
        self.player = player
        
        self.gameMap = self.gameManager.getGameMap()
        self.viewAndInput = None
    
    
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
    
    
    def stop(self):
        self.viewAndInput.stop()
