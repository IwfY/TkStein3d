from threading import Thread
from tkinter import Canvas, Tk

class TkWindowMainLoop(Thread):
    '''class for thread that handles Tk window creation and main loop''' 
    
    def __init__(self, client):
        Thread.__init__(self)
        
        self.window = None
        self.canvas = None
        self.client = client
        
        self.start()

    
    def callbackDeleteWindow(self):
        self.client.stop()
        
    def stop(self):
        self.window.quit()
        
    
    def run(self):
        self.window = Tk()
        self.canvas = Canvas(self.window, width=1024, height=768)
        self.canvas.pack()
        
        self.window.protocol("WM_DELETE_WINDOW", self.callbackDeleteWindow)
        
        self.window.mainloop()

    def getWindow(self):
        return self.window
    
    def getCanvas(self):
        return self.canvas
