from engine.gamemanager import GameManager
from engine import clientfactory



if __name__ == '__main__':
    engine = GameManager()
    player = engine.addCharacter()
    
    client = clientfactory.createTkClient(engine, player)
    client.start()
