from engine.shared.actions import ACTION_FORWARD, ACTION_BACK, ACTION_LEFT,\
    ACTION_RIGHT, ACTION_SHOOT
from engine.shared.utils import runAndWait

from threading import Thread


class ServerInputController(Thread):
    '''
    server thread to handle incoming input commands from client
    '''

    def __init__(self):
        Thread.__init__(self)
        self.characterActionMap = dict() # map of characterId -> list of actions
        
        self.acceptedActions = [ACTION_FORWARD,
                                ACTION_BACK,
                                ACTION_LEFT,
                                ACTION_RIGHT,
                                ACTION_SHOOT]
        
        self.millisecondsPerTick = 30
        self.running = True


    def addCharacter(self, characterId):
        if characterId not in self.characterActionMap:
            self.characterActionMap[characterId] = []


    def removeCharacter(self, characterId):
        if characterId in self.characterActionMap:
            self.characterActionMap.pop(characterId)


    def setActions(self, characterId, actions):
        for action in actions:
            if action not in self.acceptedActions:
                return

        if characterId in self.characterActionMap:
            self.characterActionMap[characterId] = actions


    def stop(self):
        self.running = False


    def run(self):
        while self.running:
            runAndWait(self._run, self.millisecondsPerTick)


    def _run(self):
        for characterId in self.characterActionMap.keys():
            for action in self.characterActionMap[characterId]:
                pass
            
            self.characterActionMap[characterId] = []
