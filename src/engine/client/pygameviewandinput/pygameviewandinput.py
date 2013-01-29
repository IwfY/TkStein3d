from engine.coordinate import Vector3D, Point3D
from engine.polygon import moveAndRotatePolygon
from engine.shared.utils import runAndWait, mixColors

from numpy import append, array, float32
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

from math import pi
from threading import Thread
import cProfile
from engine.mathhelper import getPointDistance, getSquaredPointDistance
from engine.shared.matrixhelper import createPerspectiveMatrix,\
    createLookAtAngleViewMatrix
from engine.client.pygameviewandinput.shader import ShaderProgram


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
        
        self.shaderProgram = None
        
        self.vaoId = None
        self.vboId = None
        self.colorBufferId = None
        self.uvBufferId = None
        
        self.vaoIdDynamic = None
        self.vboIdDynamic = None
        self.colorBufferIdDynamic = None
        self.uvBufferIdDynamic = None
        self.dynamicVerticesCount = 0
        
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

    
    def resize(self, tuple_wh):
        width, height = tuple_wh
        if height==0:
            height=1
        glViewport(0, 0, width, height)
        self.projectionMatrix = createPerspectiveMatrix(60, width / height,
                                                        0.01, 100.0)
        
    
    def init(self):
        glClearColor(0.2, 0.0, 0.0, 0.0)
        
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        
        self.createShaders()
        self.initStaticPolygonVBO()
        self.initDynamicPolygonVBO()


    def cleanup(self):
        self.destroyVBOs()
        self.destroyShaders()        
    
    def createShaders(self):
        self.shaderProgram = ShaderProgram('data/shader/vertexshader.vert',
                                           'data/shader/fragmentshader.frag',
                                           [('in_color', '4fv'),
                                            ('uv', '2fv')],
                                           [('projection_matrix', 'Matrix4fv'),
                                            ('view_matrix', 'Matrix4fv')])
        
        self.shaderProgram.use()
        
        self.shaderProgram.setUniform('projection_matrix',
                                      self.projectionMatrix)
        self.shaderProgram.setUniform('view_matrix',
                                      self.viewMatrix)


    def destroyShaders(self):
        self.shaderProgram.destroy()
        self.shaderProgram = None


    def updateDynamicPolygonVBO(self):
        vertices, colors, uvCoordinates, count = \
                self.gameMap.getDynamicPolygonArrays()
        
        self.dynamicVerticesCount = count
        
        glBindVertexArray(self.vaoIdDynamic)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.vboIdDynamic)
        glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, vertices,
                     GL_STATIC_DRAW)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.colorBufferIdDynamic)
        glBufferData(GL_ARRAY_BUFFER, len(colors) * 4, colors,
                     GL_STATIC_DRAW)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.uvBufferIdDynamic)
        glBufferData(GL_ARRAY_BUFFER, len(uvCoordinates) * 4, uvCoordinates,
                     GL_STATIC_DRAW)


    def initDynamicPolygonVBO(self):
        errorCheckValue = glGetError()
        
        vertices, colors, uvCoordinates, count = \
                self.gameMap.getDynamicPolygonArrays()
        
        self.dynamicVerticesCount = count
         
        self.vaoIdDynamic = glGenVertexArrays(1)
        glBindVertexArray(self.vaoIdDynamic)
     
        self.vboIdDynamic = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vboIdDynamic)
        glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, vertices,
                     GL_STATIC_DRAW)
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
        
        self.colorBufferIdDynamic = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.colorBufferIdDynamic)
        glBufferData(GL_ARRAY_BUFFER, len(colors) * 4, colors,
                     GL_STATIC_DRAW)
        glVertexAttribPointer(
                self.shaderProgram.getAttributeLocation('in_color'),
                4, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(
                self.shaderProgram.getAttributeLocation('in_color'))
        
        self.uvBufferIdDynamic = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.uvBufferIdDynamic)
        glBufferData(GL_ARRAY_BUFFER, len(uvCoordinates) * 4, uvCoordinates,
                     GL_STATIC_DRAW)
        glVertexAttribPointer(
                self.shaderProgram.getAttributeLocation('uv'),
                2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(
                self.shaderProgram.getAttributeLocation('uv'))
     
        errorCheckValue = glGetError()
        if errorCheckValue != GL_NO_ERROR:
            print('error creating VBOs',
                  gluErrorString(errorCheckValue))
            exit(-1)


    def initStaticPolygonVBO(self):
        '''create and fill buffer objects for static polygons'''
        
        # create vertex and color arrays
        vertices = []
        colors = []
        uvCoordinates = []
        
        self.staticVerticesCount = 0
        for polygon in self.gameMap.getStaticPolygons():
            if len(polygon.getPoints3D()) == 4:
                r, g, b = polygon.getFillColorTuple()
                for point in polygon.getPoints3D():
                    vertices.extend([point.x, point.y, point.z, 1.0])
                    colors.extend([r/255.0, g/255.0, b/255.0, 1.0])
                    self.staticVerticesCount += 1
                uvCoordinates.extend([0.0, 0.0,
                                      1.0, 0.0,
                                      1.0, 1.0,
                                      0.0, 1.0])
        
        vertices = array(vertices, dtype=float32)        
        colors = array(colors, dtype=float32)
        uvCoordinates = array(uvCoordinates, dtype=float32)
        
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
        glVertexAttribPointer(
                self.shaderProgram.getAttributeLocation('in_color'),
                4, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(
                self.shaderProgram.getAttributeLocation('in_color'))
        
        self.uvBufferId = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.uvBufferId)
        glBufferData(GL_ARRAY_BUFFER, len(uvCoordinates) * 4, uvCoordinates,
                     GL_STATIC_DRAW)
        glVertexAttribPointer(
                self.shaderProgram.getAttributeLocation('uv'),
                2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(
                self.shaderProgram.getAttributeLocation('uv'))
     
        errorCheckValue = glGetError()
        if errorCheckValue != GL_NO_ERROR:
            print('error creating VBOs',
                  gluErrorString(errorCheckValue))
            exit(-1)
    
    def destroyVBOs(self):
        errorCheckValue = glGetError()
     
        glDisableVertexAttribArray(
                self.shaderProgram.getAttributeLocation('in_color'))
        glDisableVertexAttribArray(0)
         
        glBindBuffer(GL_ARRAY_BUFFER, 0)
     
        glDeleteBuffers(1, [self.colorBufferId])
        glDeleteBuffers(1, [self.vboId])
        glDeleteBuffers(1, [self.colorBufferIdDynamic])
        glDeleteBuffers(1, [self.vboIdDynamic])
     
        glBindVertexArray(0)
        glDeleteVertexArrays(1, [self.vaoId])
        glDeleteVertexArrays(1, [self.vaoIdDynamic])
     
        errorCheckValue = glGetError()
        if errorCheckValue != GL_NO_ERROR:
            print('error destroying VBOs',
                  gluErrorString(errorCheckValue))
            exit(-1)


    def draw(self):
        player = self.client.getPlayer()
        playerPostion = player.getPosition()
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.viewMatrix = createLookAtAngleViewMatrix(
                                    Point3D(playerPostion.x,
                                            playerPostion.y,
                                            playerPostion.z),
                                    player.getViewAngle())
        
        # set uniforms
        self.shaderProgram.use()
        self.shaderProgram.setUniform('projection_matrix',
                                      self.projectionMatrix)
        self.shaderProgram.setUniform('view_matrix',
                                      self.viewMatrix)
        
        glBindVertexArray(self.vaoId)
        glDrawArrays(GL_QUADS, 0, self.staticVerticesCount)
        
        glBindVertexArray(self.vaoIdDynamic)
        glDrawArrays(GL_QUADS, 0, self.dynamicVerticesCount)
        
        self.shaderProgram.unUse()
        
        self.updateDynamicPolygonVBO()
        
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
                moveDeltaForward += 0.05
            elif key == K_s:    # s
                moveDeltaForward -= 0.05
            elif key == K_a:     # a
                moveDeltaLeft += 0.05
            elif key == K_d:    # d
                moveDeltaLeft -= 0.05
            elif key == K_q:    # q -> stop
                self.client.stop()
            elif key == K_p:
                player = self.client.getPlayer()
                print('PygameViewAndInput::processEvents:',
                      'pos:{}; angle:{}r/{}d'.format(
                                player.getPosition(),
                                round(player.getViewAngle(), 3),
                                round((player.getViewAngle()*180/3.14) % 180,
                                      2)))
                
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
        
        resolutionTuple = (1800, 1100)
        
        video_flags = OPENGL | DOUBLEBUF
        pygame.display.set_mode(resolutionTuple, video_flags)
        
        self.resize(resolutionTuple)
        self.init()
        
        self.running = True
        while self.running:
            runAndWait(self.runBody, self.millisecondsPerFrame)
        
        self.cleanup()
        
        pygame.quit()
