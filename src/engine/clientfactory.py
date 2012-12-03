from engine.client.client import Client
from engine.tkviewandinput import TkViewAndInput

def createTkClient(gameManager, characterID):
    client = Client(gameManager, characterID)
    
    client.viewAndInput = TkViewAndInput(client)
    
    return client
