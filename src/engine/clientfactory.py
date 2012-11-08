from engine.client import Client
from engine.tkviewandinput import TkViewAndInput

from tkinter import Canvas, Tk

def createTkClient(gameManager, character):
    client = Client(gameManager, character)
    
    window = Tk()
    canvas = Canvas(window, width=1024, height=768)
    canvas.pack()
    
    client.viewAndInput = TkViewAndInput(window, canvas)
    
    return client
    
    