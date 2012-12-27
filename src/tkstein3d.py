from engine.gamemanager import GameManager
from engine import clientfactory

from time import sleep

if __name__ == '__main__':
    engine = GameManager()
    engine.start()
    player = engine.addCharacter()
    player2 = engine.addCharacter()
    
    client = clientfactory.createPygameClient(engine, player)
    #client = clientfactory.createTkClient(engine, player)
    client.start()

    while client.running:
        sleep(0.25)
    
    engine.stop()