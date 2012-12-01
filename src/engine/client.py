'''
Created on Nov 7, 2012

@author: Marcel Pfeiffer
'''
from time import sleep
from engine.clientgamemap import ClientGameMap

class Client(object):
    def __init__(self, gameManager, player):
        self.gameManager = gameManager
        self.player = player
        
        self.gameMap = ClientGameMap(self)
        self.viewAndInput = None
        self.running = True
    
    
    def getGameMap(self):
        return self.gameMap

    def getPlayer(self):
        return self.player
    
    def getStaticPolygons(self):
        return self.gameManager.getStaticPolygons()
    
    def getDynamicPolygons(self):
        return self.gameManager.getDynamicPolygons()
    
    def moveRotateCharacter(self,
                            moveDeltaForward, moveDeltaLeft,
                            rotation):
        '''wrapper for GameManager method'''
        self.gameManager.moveRotateCharacter(self.player,
                                             moveDeltaForward, moveDeltaLeft,
                                             rotation)
    
    def start(self):
        self.gameMap.start()
        self.viewAndInput.start()
        
        while self.running:
            sleep(0.25)

        self.viewAndInput.stop()
        self.gameMap.stop()
        print("stopped client::gameMap")
        self.gameMap.join()
        print("joined client::gameMap")
        
    
    
    def stop(self):
        self.running = False
