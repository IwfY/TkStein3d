from engine.client import Client
from engine.tkviewandinput import TkViewAndInput

def createTkClient(gameManager, character):
    client = Client(gameManager, character)
    
    client.viewAndInput = TkViewAndInput(client)
    
    return client
