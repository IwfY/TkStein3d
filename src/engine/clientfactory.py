from engine.client.client import Client
from engine.client.tkviewandinput.tkviewandinput import TkViewAndInput
from engine.client.pygameviewandinput.pygameviewandinput import \
    PygameViewAndInput

def createTkClient(gameManager, characterID):
    client = Client(gameManager, characterID)
    
    client.viewAndInput = TkViewAndInput(client)
    
    return client

def createPygameClient(gameManager, characterID):
    client = Client(gameManager, characterID)
    
    client.viewAndInput = PygameViewAndInput(client)
    
    return client
