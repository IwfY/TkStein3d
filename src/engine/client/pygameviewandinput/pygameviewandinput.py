from engine.shared.utils import runAndWait

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

from threading import Thread
import cProfile

class PygameViewAndInput(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        
        self.client = client
        
        self.millisecondsPerFrame = 10
        self.running = False
    
    def resize(self, tuple_wh):
        width, height = tuple_wh
        if height==0:
            height=1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1.0*width/height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
    def init(self):
        glShadeModel(GL_SMOOTH)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
    
        glTranslatef(-1.5, 0.0, -6.0)
    
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.0, 1.0, 0.0)
        glVertex3f(-1.0, -1.0, 0)
        glVertex3f(1.0, -1.0, 0)
        glEnd()
    
        glTranslatef(3.0, 0.0, 0.0)
    
        glBegin(GL_QUADS)
        glVertex3f(-1.0, 1.0, 0)
        glVertex3f(1.0, 1.0, 0)
        glVertex3f(1.0, -1.0, 0)
        glVertex3f(-1.0, -1.0, 0)
        glEnd()
        
        pygame.display.flip()
    
    def processEvents(self, events):
        moveDeltaForward = 0.0
        moveDeltaLeft = 0.0
        rotation = 0.0
        
        for event in events:
            if event.type == QUIT or \
               (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.client.stop()
                
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    rotation += pi / 40
                elif event.key == K_LEFT:
                    rotation -= pi / 40
                elif event.key == K_w:
                    moveDeltaForward += 1.0
                elif event.key == K_s:    # s
                    moveDeltaForward -= 1.0
                elif event.key == K_a:     # a
                    moveDeltaLeft -= 1.0
                elif event.key == K_d:    # d
                    moveDeltaLeft += 1.0
                elif event.key == K_q:    # q -> stop
                    self.client.stop()
                
        self.client.moveRotateCharacter(moveDeltaForward,
                                        moveDeltaLeft,
                                        rotation)
    
    
    def stop(self):
        '''stop the loop from running'''
        self.running = False
    
    def run2(self):
        '''rename this to run and run to _run for profiling output'''
        profiler = cProfile.Profile()
        try:
            return profiler.runcall(self._run)
        finally:
            profiler.print_stats()
    
    def runBody(self):
        self.processEvents(pygame.event.get())
        self.draw()
    
    def run(self):
        pygame.init()
        
        video_flags = OPENGL | DOUBLEBUF
        pygame.display.set_mode((800, 600), video_flags)
        
        self.resize((800,600))
        self.init()
        
        self.running = True
        while self.running:
            runAndWait(self.runBody, self.millisecondsPerFrame)
        
        pygame.quit()