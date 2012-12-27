from engine.coordinate import Vector3D, Point3D
from engine.polygon import moveAndRotatePolygon
from engine.shared.utils import runAndWait

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

from math import pi
from threading import Thread
import cProfile
from engine.mathhelper import getPointDistance


class PygameViewAndInput(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        
        self.client = client
        self.gameMap = self.client.getGameMap()
        
        self.millisecondsPerFrame = 100/6
        self.running = False
        self.keysPressed = []
        
        self.eye = Point3D(0.0, 0.0, -2.0)
    
    def resize(self, tuple_wh):
        width, height = tuple_wh
        if height==0:
            height=1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1.0*width/height, 2.0, 1000.0)
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
        player = self.client.getPlayer()
        playerPostion = player.getPosition()
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glLoadIdentity()

        glRotatef((player.getViewAngle() + pi/2) * 180 / pi, 0.0, 1.0, 0.0)
        glTranslatef(-playerPostion.x, -playerPostion.y, -playerPostion.z)
        
        for polygon in self.gameMap.getPolygons():
            if polygon.facesPoint(playerPostion) and \
                getPointDistance(playerPostion, polygon.getCenter()) < 300:
                r, g, b = polygon.getFillColorTuple()
                glBegin(GL_QUADS)
                for point in polygon.getPoints3D():
                    glColor3f(r/255, g/255, b/255)
                    glVertex3f(point.x, point.y, point.z)
                glEnd()

    
    def processEvents(self, events):
        moveDeltaForward = 0.0
        moveDeltaLeft = 0.0
        rotation = 0.0
        
        for event in events:
            if event.type == QUIT or \
               (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.client.stop()
                
            elif event.type == KEYDOWN:
                self.keysPressed.append(event.key)
            elif event.type == KEYUP:
                if event.key in self.keysPressed:
                    self.keysPressed.remove(event.key)
        
        for key in self.keysPressed:
            if key == K_RIGHT:
                rotation += pi / 60
            elif key == K_LEFT:
                rotation -= pi / 60
            elif key == K_w:
                moveDeltaForward += 0.6
            elif key == K_s:    # s
                moveDeltaForward -= 0.6
            elif key == K_a:     # a
                moveDeltaLeft += 0.6
            elif key == K_d:    # d
                moveDeltaLeft -= 0.6
            elif key == K_q:    # q -> stop
                self.client.stop()
            elif key == K_p:
                player = self.client.getPlayer()
                print('pos:{}; angle:{}/{}'.format(
                                player.getPosition(),
                                player.getViewAngle(),
                                player.getViewAngle()*180/3.14))
                
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
        pygame.display.flip()
    
    def run(self):
        pygame.init()
        
        video_flags = OPENGL | DOUBLEBUF
        pygame.display.set_mode((1440, 900), video_flags)
        
        self.resize((1440, 900))
        self.init()
        
        self.running = True
        while self.running:
            runAndWait(self.runBody, self.millisecondsPerFrame)
        
        pygame.quit()