from engine.gamemanager import GameManager

from tkinter import Tk, Canvas

if __name__ == '__main__':
    window = Tk()
    canvas = Canvas(window, width=400, height=300)
    canvas.pack()
    #canvas2 = Canvas(window, width=400, height=300)
    #canvas2.pack()
    #canvas3 = Canvas(window, width=600, height=100)
    #canvas3.pack()
    #canvas4 = Canvas(window, width=600, height=100)
    #canvas4.pack()
    
    engine = GameManager()
    player = engine.addCharacter()
    #player2 = engine.addCharacter()
    #player2.setPosition(10, 0, 10)
    engine.addView(canvas, player)
    #engine.addView(canvas2, player2)
    #engine.addView(canvas3, player2)
    #engine.addView(canvas4, player2)
    engine.start()

    window.mainloop()
