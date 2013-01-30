from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
from time import time

from math import cos, pi, sin, sqrt, tan
from numpy import array, float32
from engine.shared.matrixhelper import createLookAtAngleViewMatrix,\
    createLookAtViewMatrix, createPerspectiveMatrix
from engine.shared.coordinate import Point3D


class Triangle(object):
    def __init__(self):
        self.running = False

        self.attributeColorIndex = None
        self.vertexShaderId = None
        self.fragmentShaderId = None
        self.programId = None
        
        self.vao1Id = None
        self.vao2Id = None
        
        self.vbo1Id = None
        self.colorBuffer1Id = None
        
        self.vbo2Id = None
        self.colorBuffer2Id = None
        
        self.projectionMatrixUniformLocation = None
        self.viewMatrixUniformLocation = None
        self.projectionMatrix = [1, 0, 0, 0,
                                 0, 1, 0, 0,
                                 0, 0, 1, 0,
                                 0, 0, 0, 1]  # is set in resize()
        self.viewMatrix = [1, 0, 0, 0,
                           0, 1, 0, 0,
                           0, 0, 1, 0,
                           0, 0, 0, 1]
        
        self.vertexShader120 = ['''
#version 120

uniform mat4 projection_matrix;
uniform mat4 view_matrix;
attribute vec4 in_color;
varying vec4 ex_color;

void main(void) {
    gl_Position = projection_matrix * view_matrix * gl_Vertex;
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
    
    def resize(self, width, height):
        if height == 0:
            height = 1
        glViewport(0, 0, width, height)
        self.projectionMatrix = \
                createPerspectiveMatrix(60,
                                        width / height,
                                        0.1,
                                        1000.0)
    
    def init(self):
        print('GL_SHADING_LANGUAGE_VERSION',
              glGetString(GL_SHADING_LANGUAGE_VERSION))
        print('GL_VERSION', glGetString(GL_VERSION))
        
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        
        self.createShaders()
        self.createVBO1()
        self.createVBO2()
        
        glClearColor(0.2, 0.0, 0.0, 1.0)
    
    def cleanup(self):
        self.destroyShaders()
        self.destroyVBO()
    
    def createVBO1(self):
        vertices = array([
                          -0.5, -0.5, -2.0, 1.0,
                           0.5, -0.5, -2.0, 1.0,
                           0.5,  0.5, -5.0, 1.0,
                          -0.5,  0.5, -5.0, 1.0
                         ],
                         dtype=float32)
        
        colors = array([
                           1.0, 1.0, 1.0, 1.0,
                           1.0, 1.0, 1.0, 1.0,
                           0.5, 0.5, 0.5, 1.0,
                           0.5, 0.5, 0.5, 1.0
                        ],
                        dtype=float32)
        
        errorCheckValue = glGetError()
         
        self.vao1Id = glGenVertexArrays(1)
        glBindVertexArray(self.vao1Id)
     
        self.vbo1Id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo1Id)
        glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, vertices,
                     GL_STATIC_DRAW)
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
        
        self.colorBuffer1Id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.colorBuffer1Id)
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
    
    def switchVBO2(self):
        glBindBuffer(GL_ARRAY_BUFFER, 0)
     
        glDeleteBuffers(1, [self.colorBuffer2Id])
        glDeleteBuffers(1, [self.vbo2Id])
     
        glBindVertexArray(0)
        glDeleteVertexArrays(1, [self.vao2Id])
        
        self.createVBO2()
    
    
    def createVBO2(self):
        tmp = int(time()) % 60 / 30
        vertices = array([
                          2.0 - tmp, -2.0, -4.0, 1.0,
                          4.0 - tmp, -2.0, -4.0, 1.0,
                          4.0 - tmp,  0.0, -4.0, 1.0,
                          2.0 - tmp,  0.0, -4.0, 1.0
                         ],
                         dtype=float32)
        
        colors = array([
                           1.0, 0.0, 0.0, 1.0,
                           0.0, 1.0, 0.0, 1.0,
                           0.0, 0.0, 1.0, 1.0,
                           1.0, 0.0, 1.0, 1.0
                        ],
                        dtype=float32)
        
        errorCheckValue = glGetError()
         
        self.vao2Id = glGenVertexArrays(1)
        glBindVertexArray(self.vao2Id)
     
        self.vbo2Id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo2Id)
        glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, vertices,
                     GL_STATIC_DRAW)
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
        
        self.colorBuffer2Id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.colorBuffer2Id)
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
        
    
    def destroyVBO(self):
        errorCheckValue = glGetError()
     
        glDisableVertexAttribArray(self.attributeColorIndex)
        glDisableVertexAttribArray(0)
         
        glBindBuffer(GL_ARRAY_BUFFER, 0)
     
        glDeleteBuffers(1, [self.colorBuffer1Id])
        glDeleteBuffers(1, [self.vbo1Id])
        glDeleteBuffers(1, [self.colorBuffer2Id])
        glDeleteBuffers(1, [self.vbo2Id])
     
        glBindVertexArray(0)
        glDeleteVertexArrays(1, [self.vao1Id])
        glDeleteVertexArrays(1, [self.vao2Id])
     
        errorCheckValue = glGetError()
        if errorCheckValue != GL_NO_ERROR:
            print('error destroying VBOs',
                  gluErrorString(errorCheckValue))
            exit(-1);
    
    
    def createShaders(self):
        errorCheckValue = glGetError()
         
        self.vertexShaderId = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(self.vertexShaderId, self.vertexShader120)
        glCompileShader(self.vertexShaderId)
        
        log = glGetShaderInfoLog(self.vertexShaderId)
        if log: print('Vertex Shader: ', log)
     
        self.fragmentShaderId = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(self.fragmentShaderId, self.fragmentShader120)
        glCompileShader(self.fragmentShaderId)
        
        log = glGetShaderInfoLog(self.fragmentShaderId)
        if log: print('Fragment Shader: ', log)
     
        self.programId = glCreateProgram()
        glAttachShader(self.programId, self.vertexShaderId)
        glAttachShader(self.programId, self.fragmentShaderId)
        glLinkProgram(self.programId)
        
        self.attributeColorIndex = glGetAttribLocation(self.programId,
                                                       b'in_color')
        
        self.projectionMatrixUniformLocation = \
                glGetUniformLocation(self.programId,
                                     b"projection_matrix");
        self.viewMatrixUniformLocation = \
                glGetUniformLocation(self.programId,
                                     b"view_matrix");
        
        log = glGetProgramInfoLog(self.programId)
        if log:
            print('Program:', log)

        glUseProgram(self.programId)
        
        glUniformMatrix4fv(self.projectionMatrixUniformLocation,
                           1, GL_FALSE, self.projectionMatrix)
        glUniformMatrix4fv(self.viewMatrixUniformLocation,
                           1, GL_FALSE, self.viewMatrix)
     
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

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.viewMatrix = createLookAtViewMatrix(Point3D(0, 0, 0),
                                                 Point3D(0, 0, -1))
        
        glUniformMatrix4fv(self.viewMatrixUniformLocation,
                           1, GL_FALSE, self.viewMatrix)
        
        glBindVertexArray(self.vao1Id)
        glDrawArrays(GL_QUADS, 0, 4)
        
        glBindVertexArray(self.vao2Id)
        glDrawArrays(GL_QUADS, 0, 4)
        
        self.switchVBO2()
        
        errorCheckValue = glGetError()
        if errorCheckValue != GL_NO_ERROR:
            print('error drawing',
                  gluErrorString(errorCheckValue))
            exit(-1)

    
    def processEvents(self, events):
        for event in events:
            if event.type == QUIT or \
               (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.stop()
            
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    self.stop()
    
    def stop(self):
        '''stop the loop from running'''
        self.running = False
    
    def run(self):
        pygame.init()
        
        video_flags = OPENGL | DOUBLEBUF
        pygame.display.set_mode((800, 600), video_flags)
        
        self.resize(800, 600)
        self.init()
        
        self.running = True
        while self.running:
            self.processEvents(pygame.event.get())
            self.draw()
            pygame.display.flip()
        
        self.cleanup()
        pygame.quit()


if __name__ == '__main__':
    t = Triangle()
    t.run()

