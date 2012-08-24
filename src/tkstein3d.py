from engine.gamemanager import GameManager

from tkinter import Tk, Canvas

if __name__ == '__main__':
    window = Tk()
    canvas = Canvas(window, width=800, height=600)
    canvas.pack()
    
    engine = GameManager()
    player = engine.addCharacter()
    engine.addView(canvas, player)
    engine.start()

    window.mainloop()
