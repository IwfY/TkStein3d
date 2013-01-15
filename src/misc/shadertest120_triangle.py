from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

from math import pi
from numpy import array, float32


class Triangle(object):
    def __init__(self):
        self.running = False

        self.attributeColorIndex = None
        self.vertexShaderId = None
        self.fragmentShaderId = None
        self.programId = None
        self.vaoId = None
        self.vboId = None
        self.colorBufferId = None
        
        self.vertexShader120 = ['''
#version 120

attribute vec4 in_color;
varying vec4 ex_color;

void main(void) {
    gl_Position = gl_Vertex;
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
    
    def init(self):
        print('GL_SHADING_LANGUAGE_VERSION',
              glGetString(GL_SHADING_LANGUAGE_VERSION))
        print('GL_VERSION', glGetString(GL_VERSION))
        
        self.createShaders()
        self.createVBO()
        
        glClearColor(0.2, 0.0, 0.0, 0.0)
    
    def cleanup(self):
        self.destroyShaders()
        self.destroyVBO()
    
    def createVBO(self):
        vertices = array([
                          -0.8, -0.8, 0.0, 1.0,
                           0.0,  0.8, 0.0, 1.0,
                           0.8, -0.8, 0.0, 1.0
                         ],
                         dtype=float32)
        
        colors = array([
                           1.0, 0.0, 0.0, 1.0,
                           0.0, 1.0, 0.0, 1.0,
                           0.0, 0.0, 1.0, 1.0
                        ],
                        dtype=float32)
        
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
        
    
    def destroyVBO(self):
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
        
        log = glGetProgramInfoLog(self.programId)
        if log:
            print('Program:', log)

        glUseProgram(self.programId)
     
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
        
        glDrawArrays(GL_TRIANGLES, 0, 3)
        
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
