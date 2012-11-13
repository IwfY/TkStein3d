from threading import Thread

class TkWindowMainLoop(Thread):
    '''class for thread that handles Tk window main loop''' 
    
    def __init__(self, window):
        Thread.__init__(self)
        
        self.window = window
    
    
    def run(self):
        self.window.mainloop()
