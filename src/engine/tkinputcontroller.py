from datetime import datetime, timedelta
from math import pi
from threading import Thread
from time import sleep

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
        
        self.player = self.client.getPlayer()
        self.keysPressed = set()
        self.millisecondsPerTick = 30
        self.running = False
        
        self.setBindings()
    
    def stop(self):
        self.running = False
    
    
    def run(self):
        self.running = True
        while self.running:
            stop = datetime.now() + \
                   timedelta(milliseconds=self.millisecondsPerTick)
            
            moveDeltaForward = 0.0
            moveDeltaLeft = 0.0
            rotation = 0.0
            # copy set because of error when set size changes during iteration
            tmpKeysPressed = set(self.keysPressed)
            for key in tmpKeysPressed:
                if key == 65363:    # right array
                    rotation += pi / 40
                elif key == 65361:  # left array
                    rotation -= pi / 40
                if key == 119:      # w
                    moveDeltaForward += 1.0
                elif key == 115:    # s
                    moveDeltaForward -= 1.0
                elif key == 97:     # a
                    moveDeltaLeft -= 1.0
                elif key == 100:    # d
                    moveDeltaLeft += 1.0
                elif key == 113:    # q -> stop
                    self.client.stop()
            self.client.moveRotateCharacter(self.player,
                                            moveDeltaForward,
                                            moveDeltaLeft,
                                            rotation)
            
            remaining = stop - datetime.now()
            if remaining.days < 0:  # input processing needed too long
                remaining = -1
            else:
                remaining = round(remaining.microseconds / 1000000, 3)
            if remaining > 0:
                sleep(remaining)
    
    
    def setBindings(self):
        self.window.bind('<KeyPress>', self.keyPressed)
        self.window.bind('<KeyRelease>', self.keyReleased)


    def keyPressed(self, event):
        self.keysPressed.add(event.keysym_num)


    def keyReleased(self, event):
        if event.keysym_num in self.keysPressed:
            self.keysPressed.remove(event.keysym_num)
