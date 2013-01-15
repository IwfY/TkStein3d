from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

from math import pi
from numpy import array, float32


class Triangle(object):
    def __init__(self):
        self.running = False

        self.vertexShaderId = None
        self.fragmentShaderId = None
        self.programId = None
        self.vaoId = None
        self.vboId = None
        self.colorBufferId = None

        self.vertexShader400 = '''
#version 400

layout(location=0) in vec4 in_Position;
layout(location=1) in vec4 in_Color;
out vec4 ex_Color;

void main(void)
{
    gl_Position = in_Position;
    ex_Color = in_Color;
}
'''

        self.fragmentShader400 = '''
#version 400

in vec4 ex_Color;
out vec4 out_Color;

void main(void)
{
    out_Color = ex_Color;
}
'''
    
    def resize(self, width, height):
        if height == 0:
            height = 1
        glViewport(0, 0, width, height)
    
    def init(self):
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
        

        self.colorBufferId = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.colorBufferId)
        glBufferData(GL_ARRAY_BUFFER, len(colors) * 4, colors,
                     GL_STATIC_DRAW)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)
     
        errorCheckValue = glGetError()
        if errorCheckValue != GL_NO_ERROR:
            print('error creating VBOs',
                  gluErrorString(errorCheckValue))
            exit(-1)
        
    
    def destroyVBO(self):
        errorCheckValue = glGetError()
     
        glDisableVertexAttribArray(1)
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
        glShaderSource(self.vertexShaderId, self.vertexShader400)
        glCompileShader(self.vertexShaderId)
        
        log = glGetShaderInfoLog(self.vertexShaderId)
        if log: print('Vertex Shader: ', log)
     
        self.fragmentShaderId = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(self.fragmentShaderId, self.fragmentShader400)
        glCompileShader(self.fragmentShaderId)
        
        log = glGetShaderInfoLog(self.fragmentShaderId)
        if log: print('Fragment Shader: ', log)
     
        self.programId = glCreateProgram()
        glAttachShader(self.programId, self.vertexShaderId)
        glAttachShader(self.programId, self.fragmentShaderId)
        glLinkProgram(self.programId)
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