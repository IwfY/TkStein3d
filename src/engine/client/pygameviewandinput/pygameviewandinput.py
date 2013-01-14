from engine.coordinate import Vector3D, Point3D
from engine.polygon import moveAndRotatePolygon
from engine.shared.utils import runAndWait, mixColors

from numpy import append, array, float32
from OpenGL.GL import *
from OpenGL.GL.ARB.shader_objects import *
from OpenGL.GL.ARB.vertex_shader import *
from OpenGL.GL.ARB.fragment_shader import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

from math import pi
from threading import Thread
import cProfile
from engine.mathhelper import getPointDistance, getSquaredPointDistance


class PygameViewAndInput(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        
        self.client = client
        self.gameMap = self.client.getGameMap()
        
        self.millisecondsPerFrame = 100/6
        self.running = False
        self.keysPressed = []
        
        self.eye = Point3D(0.0, 0.0, -2.0)
        
        self.staticVerticesCount = 0
        self.attributeColorIndex = None
        self.vertexShaderId = None
        self.fragmentShaderId = None
        self.programId = None
        self.vaoId = None
        self.vboId = None
        self.colorBufferId = None
        
        self.vertexShader120 = '''
#version 120

attribute vec4 in_color;
varying vec4 ex_color;

void main(void) {
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    ex_color = in_color;
}
'''

        self.fragmentShader120 = '''
#version 120

varying vec4 ex_color;

void main() {
    gl_FragColor = ex_color;
}
'''
    
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
        
        self.createShaders()
        self.initStaticPolygonVBO()
    
    def cleanup(self):
        self.destroyShaders()
        self.destroyStaticPolygonsVBO()
    
    def createShaders(self):
        errorCheckValue = glGetError()
         
        self.vertexShaderId = glCreateShaderObjectARB(GL_VERTEX_SHADER)
        glShaderSourceARB(self.vertexShaderId, [self.vertexShader120])
        glCompileShaderARB(self.vertexShaderId)
        
        log = glGetInfoLogARB(self.vertexShaderId)
        if log: print('Vertex Shader:', log)
     
        self.fragmentShaderId = glCreateShaderObjectARB(GL_FRAGMENT_SHADER)
        glShaderSourceARB(self.fragmentShaderId, [self.fragmentShader120])
        glCompileShaderARB(self.fragmentShaderId)
        
        log = glGetInfoLogARB(self.fragmentShaderId)
        if log: print('Fragment Shader:', log)
     
        self.programId = glCreateProgramObjectARB()
        glAttachObjectARB(self.programId, self.vertexShaderId)
        glAttachObjectARB(self.programId, self.fragmentShaderId)
        glLinkProgramARB(self.programId)
        
        log = glGetInfoLogARB(self.programId)
        if log:
            print('Program:', log)
        glUseProgramObjectARB(self.programId)
     
        errorCheckValue = glGetError()
        if errorCheckValue != GL_NO_ERROR:
            print('error creating shaders',
                  gluErrorString(errorCheckValue))
            exit(-1)
    
    def destroyShaders(self):
        errorCheckValue = glGetError()
     
        glUseProgramObjectARB(0)
     
        glDetachObjectARB(self.programId, self.vertexShaderId)
        glDetachObjectARB(self.programId, self.fragmentShaderId)
     
        glDeleteObjectARB(self.fragmentShaderId)
        glDeleteObjectARB(self.vertexShaderId)
     
        glDeleteObjectARB(self.programId)
     
        errorCheckValue = glGetError()
        if errorCheckValue != GL_NO_ERROR:
            print('error destroying shaders',
                  gluErrorString(errorCheckValue))
            exit(-1)
        
    
    def initStaticPolygonVBO(self):
        '''create and fill buffer objects for static polygons'''
        
        # create vertex and color arrays
        vertices = array([], dtype=float32)        
        colors = array([], dtype=float32)
        
        self.staticVerticesCount = 0
        #for polygon in self.gameMap.getStaticPolygons():
        for polygon in self.gameMap.getPolygons():
            if len(polygon.getPoints3D()) == 4:
                r, g, b = polygon.getFillColorTuple()
                for point in polygon.getPoints3D():
                    append(vertices, [point.x, point.y, point.z])
                    append(colors, [r/255, g/255, b/255])
                    self.staticVerticesCount += 1
        
        errorCheckValue = glGetError()
         
        self.vaoId = glGenVertexArrays(1)
        glBindVertexArray(self.vaoId)
     
        self.vboId = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vboId)
        glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, vertices,
                     GL_STATIC_DRAW)
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
        

        self.attributeColorIndex = glGetAttribLocation(self.programId,
                                                       b'in_color')
        
        self.colorBufferId = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.colorBufferId)
        glBufferData(GL_ARRAY_BUFFER, len(colors) * 4, colors,
                     GL_STATIC_DRAW)
        glVertexAttribPointer(self.attributeColorIndex,
                              4, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(self.attributeColorIndex)
     
        errorCheckValue = glGetError()
        if errorCheckValue != GL_NO_ERROR:
            print('error creating VBOs',
                  gluErrorString(errorCheckValue))
            exit(-1)
    
    def destroyStaticPolygonsVBO(self):
        errorCheckValue = glGetError()
     
        glDisableVertexAttribArray(self.attributeColorIndex)
        glDisableVertexAttribArray(0)
         
        glBindBuffer(GL_ARRAY_BUFFER, 0)
     
        glDeleteBuffers(1, [self.colorBufferId])
        glDeleteBuffers(1, [self.vboId])
     
        glBindVertexArray(0)
        glDeleteVertexArrays(1, [self.vaoId])
     
        errorCheckValue = glGetError()
        if errorCheckValue != GL_NO_ERROR:
            print('error destroying VBOs',
                  gluErrorString(errorCheckValue))
            exit(-1);

    def draw(self):
        player = self.client.getPlayer()
        playerPostion = player.getPosition()
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glLoadIdentity()

        glRotatef((player.getViewAngle() + pi/2) * 180 / pi, 0.0, 1.0, 0.0)
        glTranslatef(-playerPostion.x, -playerPostion.y, -playerPostion.z)
        
        glDrawArrays(GL_QUADS, 0, self.staticVerticesCount)

    
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
        
        self.cleanup()
        
        pygame.quit()
