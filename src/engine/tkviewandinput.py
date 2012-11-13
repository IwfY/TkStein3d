from engine.tkview import TkView
from engine.tkinputcontroller import TkInputController
from engine.tkwindowmainloop import TkWindowMainLoop

class TkViewAndInput(object):
    '''
    class to handle the drawing and input processing using tk infrastructure
    '''


    def __init__(self, client):
        '''
        Constructor
        '''
        self.client = client
        
        self.running = False
        
        self.tkWindowMainLoop = TkWindowMainLoop(self.client)
        
        self.window = self.tkWindowMainLoop.getWindow()
        while self.window is None:      #wait until window is created
            self.window = self.tkWindowMainLoop.getWindow()
            
        self.canvas = self.tkWindowMainLoop.getCanvas()
        while self.canvas is None:      #wait until canvas is created
            self.canvas = self.tkWindowMainLoop.getCanvas()
        
        self.view = TkView(self.client, self.canvas)
        self.inputController = TkInputController(self.client, self.window)
    
    
    def start(self):
        if not self.running:
            self.view.start()
            self.inputController.start()
            self.running = True
    
    def stop(self):
        if self.running:
            self.view.stop()
            print("stopped view")
            self.inputController.stop()
            print("stopped inputcontroller")
            
            self.view.join()
            print("joined view")
            self.inputController.join()
            print("joined inputcontroller")
            
            self.tkWindowMainLoop.stop()
            print("stopped tkWindowMainLoop")
            self.tkWindowMainLoop.join()
            print("joined tkWindowMainLoop")
            
            self.running = False
