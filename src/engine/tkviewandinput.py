from engine.tkview import TkView
from engine.tkinputcontroller import TkInputController
from engine.tkwindowmainloop import TkWindowMainLoop

class TkViewAndInput(object):
    '''
    class to handle the drawing and input processing using tk infrastructure
    '''


    def __init__(self, client, window, canvas):
        '''
        Constructor
        '''
        self.client = client
        self.window = window
        self.canvas = canvas
        
        self.running = False
        
        self.tkWindowMainLoop = TkWindowMainLoop(self.window)
        self.view = TkView(self.client, self.canvas)
        self.inputController = TkInputController(self.client, self.window)
    
    
    def start(self):
        if not self.running:
            self.tkWindowMainLoop.start()
            self.view.start()
            self.inputController.start()
            self.running = True
    
    def stop(self):
        if self.running:
            self.view.stop()
            self.inputController.stop()
            
            self.view.join()
            self.inputController.join()
            
            self.running = False
