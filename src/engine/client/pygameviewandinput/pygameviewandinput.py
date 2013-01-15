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
from engine.shared.matrixhelper import createPerspectiveMatrix
from OpenGL.raw.GL.VERSION.GL_2_0 import glUniform3f


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
        
        self.projectionMatrixUniformLocation = None
        self.playerPositionUniformLocation = None
        self.playerRotationUniformLocation = None
        self.projectionMatrixUniformLocation = None
        
        self.projectionMatrix = [1, 0, 0, 0,
                                 0, 1, 0, 0,
                                 0, 0, 1, 0,
                                 0, 0, 0, 1]  # is set in resize()
        
        
        
        self.vertexShader120 = ['''
#version 120

uniform mat4 projection_matrix;
uniform vec3 player_position;
uniform float player_rotation;
attribute vec4 in_color;
varying vec4 ex_color;

void main(void) {
    float pi = 3.1416;
    vec4 vertex = gl_Vertex + vec4(player_position, 1.0);
    
    float rotation = -player_rotation - pi/2;
    
    float vectorLength = sqrt(vertex[0] * vertex[0] + vertex[2] * vertex[2]);
    
    float currentAngle = atan(vertex[2], vertex[0]);
    float newAngle = currentAngle + rotation;
    
    vertex[0] = vectorLength * cos(newAngle);
    vertex[2] = vectorLength * sin(newAngle);
     
    gl_Position = projection_matrix * vertex;
    ex_color = in_color;
}
''']

        self.fragmentShader120 = ['''
#version 120

varying vec4 ex_color;

void main() {
    gl_FragColor = ex_color;
}
''']
    
    def resize(self, tuple_wh):
        width, height = tuple_wh
        if height==0:
            height=1
        glViewport(0, 0, width, height)
        self.projectionMatrix = createPerspectiveMatrix(90, width / height,
                                                        0.1, 1000.0)
        
    
    def init(self):
        glClearColor(0.2, 0.0, 0.0, 0.0)
        
        self.createShaders()
        self.initStaticPolygonVBO()
    
    def cleanup(self):
        self.destroyShaders()
        self.destroyStaticPolygonsVBO()
    
    def createShaders(self):
        errorCheckValue = glGetError()
         
        # vertex shader
        self.vertexShaderId = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(self.vertexShaderId, self.vertexShader120)
        glCompileShader(self.vertexShaderId)
        
        log = glGetShaderInfoLog(self.vertexShaderId)
        if log: print('Vertex Shader: ', log)
     
        # fragment shader
        self.fragmentShaderId = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(self.fragmentShaderId, self.fragmentShader120)
        glCompileShader(self.fragmentShaderId)
        
        log = glGetShaderInfoLog(self.fragmentShaderId)
        if log: print('Fragment Shader: ', log)
     
        # program creation
        self.programId = glCreateProgram()
        glAttachShader(self.programId, self.vertexShaderId)
        glAttachShader(self.programId, self.fragmentShaderId)
        glLinkProgram(self.programId)
        
        self.projectionMatrixUniformLocation = \
                glGetUniformLocation(self.programId,
                                     b"projection_matrix");
        self.playerPositionUniformLocation = \
                glGetUniformLocation(self.programId,
                                     b"player_position");
        self.playerRotationUniformLocation = \
                glGetUniformLocation(self.programId,
                                     b"player_rotation");

        glUseProgram(self.programId)
        
        glUniformMatrix4fv(self.projectionMatrixUniformLocation,
                           1, GL_FALSE, self.projectionMatrix)
     
        errorCheckValue = glGetError()
        if errorCheckValue != GL_NO_ERROR:
            print('error creating shaders',
                  gluErrorString(errorCheckValue))
            exit(-1)


    def destroyShaders(self):
        errorCheckValue = glGetError()
     
        glUseProgram(0)
     
        glDetachShader(self.programId, self.vertexShaderId)
        glDetachShader(self.programId, self.fragmentShaderId)
     
        glDeleteShader(self.fragmentShaderId)
        glDeleteShader(self.vertexShaderId)
     
        glDeleteProgram(self.programId)
     
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
        
        #vertices = array([
        #                  -0.8, -0.8, -2.0, 1.0,
        #                   0.8,  -0.8, -2.0, 1.0,
        #                   0.8, 0.8, -2.0, 1.0,
        #                   -0.8, 0.8, -2.0, 1.0
        #                 ],
        #                 dtype=float32)
        
        #colors = array([
        #                   1.0, 0.0, 0.0, 1.0,
        #                   0.0, 1.0, 0.0, 1.0,
        #                   0.0, 0.0, 1.0, 1.0,
        #                   1.0, 0.0, 1.0, 1.0
        #                ],
        #                dtype=float32)
        
        self.staticVerticesCount = 0
        #for polygon in self.gameMap.getStaticPolygons():
        for polygon in self.gameMap.getPolygons():
            if len(polygon.getPoints3D()) == 4:
                r, g, b = polygon.getFillColorTuple()
                for point in polygon.getPoints3D():
                    vertices = append(vertices, [point.x, point.y, point.z])
                    colors = append(colors, [r/255, g/255, b/255])
                    self.staticVerticesCount += 1
                    #pass
        
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
            exit(-1)

    def draw(self):
        player = self.client.getPlayer()
        playerPostion = player.getPosition()
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glUniform3f(self.playerPositionUniformLocation,
                    -playerPostion.x, -playerPostion.y, -playerPostion.z)
        glUniform1f(self.playerRotationUniformLocation,
                    player.getViewAngle())
        
        glUniformMatrix4fv(self.projectionMatrixUniformLocation,
                           1, GL_FALSE, self.projectionMatrix)
        
        glDrawArrays(GL_QUADS, 0, self.staticVerticesCount)
        
        errorCheckValue = glGetError()
        if errorCheckValue != GL_NO_ERROR:
            print('draw error',
                  gluErrorString(errorCheckValue))
            exit(-1);

    
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
