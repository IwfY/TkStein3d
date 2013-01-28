from engine.ai.bot import Bot
from engine.gamemanager import GameManager
from engine import clientfactory

from time import sleep


if __name__ == '__main__':
    engine = GameManager()
    engine.start()
    player = engine.addCharacter()
    player2 = engine.addCharacter()
    player3 = engine.addCharacter()
    
    bot = Bot(engine, player2)
    bot.start()
    bot2 = Bot(engine, player3)
    bot2.start()
    
    client = clientfactory.createPygameClient(engine, player)
    #client = clientfactory.createTkClient(engine, player)
    client.start()

    while client.running:
        sleep(0.25)
    
    bot.stop()
    bot2.stop()
    
    engine.stop()