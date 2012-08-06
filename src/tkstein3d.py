from engine.engine import Engine

from tkinter import Tk, Canvas

if __name__ == '__main__':
    window = Tk()
    canvas = Canvas(window, width=800, height=600)
    canvas.pack()
    
    engine = Engine(canvas)
    engine.start()

    window.mainloop()
