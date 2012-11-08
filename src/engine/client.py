'''
Created on Nov 7, 2012

@author: Marcel Pfeiffer
'''


class Client(object):
    def __init__(self, gameManager, character):
        self.gameManager = gameManager
        self.character = character
        
        self.gameMap = self.gameManager.getMap()
        self.viewAndInput = None