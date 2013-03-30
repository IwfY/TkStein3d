'''
Created on Nov 7, 2012

@author: Marcel Pfeiffer
'''
from time import sleep
from engine.client.clientgamemap import ClientGameMap

class Client(object):
    def __init__(self, gameManager, playerID):
        self.gameManager = gameManager
        self.playerID = playerID
        
        self.gameMap = ClientGameMap(self)
        self.viewAndInput = None
        self.running = True
    
    
    def getGameMap(self):
        return self.gameMap

    def getPlayer(self):
        return self.gameManager.getCharacterInfo(self.playerID)
    
    
    def getStaticPolygons(self):
        return self.gameManager.getStaticPolygons()
    
    def getDynamicPolygons(self):
        return self.gameManager.getDynamicPolygons()
    
    def setActions(self, actionInteger):
        self.gameManager.setActions(self.playerID, actionInteger)
    
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
