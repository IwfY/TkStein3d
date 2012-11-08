from engine.tkview import TkView
from engine.tkinputcontroller import TkInputController

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
        
        self.view = TkView(self.client, window, view)
        self.inputController = TkInputController(self.client, windows)
        