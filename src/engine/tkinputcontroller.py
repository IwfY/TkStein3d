from engine.shared.utils import runAndWait

from math import pi
from threading import Thread

class TkInputController(Thread):
    '''
    class to handle input for the game manager
    runs in a thread
    '''

    def __init__(self, client, window):
        '''
        Constructor
        '''
        Thread.__init__(self)
        
        self.client = client
        self.window = window
        
        self.keysPressed = set()
        self.millisecondsPerTick = 30
        self.running = False
        
        self.setBindings()
    
    def stop(self):
        self.running = False
    
    
    def run(self):
        self.running = True
        while self.running:
            runAndWait(self._run, self.millisecondsPerTick)
    
    def _run(self):
        moveDeltaForward = 0.0
        moveDeltaLeft = 0.0
        rotationClockwise = 0.0
        # copy set because of error when set size changes during iteration
        tmpKeysPressed = set(self.keysPressed)
        for key in tmpKeysPressed:
            if key == 65363:    # right array
                rotationClockwise += pi / 40
            elif key == 65361:  # left array
                rotationClockwise -= pi / 40
            if key == 119:      # w
                moveDeltaForward += 1.0
            elif key == 115:    # s
                moveDeltaForward -= 1.0
            elif key == 97:     # a
                moveDeltaLeft += 1.0
            elif key == 100:    # d
                moveDeltaLeft -= 1.0
            elif key == 113:    # q -> stop
                self.client.stop()
        self.client.moveRotateCharacter(moveDeltaForward,
                                        moveDeltaLeft,
                                        rotationClockwise)
    
    def setBindings(self):
        self.window.bind('<KeyPress>', self.keyPressed)
        self.window.bind('<KeyRelease>', self.keyReleased)


    def keyPressed(self, event):
        self.keysPressed.add(event.keysym_num)


    def keyReleased(self, event):
        if event.keysym_num in self.keysPressed:
            self.keysPressed.remove(event.keysym_num)
