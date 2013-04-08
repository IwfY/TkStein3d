from engine.shared.coordinate import Vector3D, Point3D
from engine.shared.polygon import moveAndRotatePolygon
from engine.shared.utils import runAndWait, mixColors

from numpy import append, array, float32
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

from math import pi
from threading import Thread
import cProfile
from engine.shared.mathhelper import getPointDistance, getSquaredPointDistance
from engine.shared.matrixhelper import createPerspectiveMatrix,\
    createLookAtAngleViewMatrix
from engine.client.pygameviewandinput.shader import ShaderProgram
from engine.shared.actions import ACTION_ROTATE_RIGHT, ACTION_ROTATE_LEFT,\
    ACTION_FORWARD, ACTION_BACK, ACTION_LEFT, ACTION_RIGHT, ACTION_WALK
from engine.client.pygameviewandinput.renderunit import RenderUnit


class PygameViewAndInput(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        
        self.client = client
        self.gameMap = self.client.getGameMap()
        
        self.millisecondsPerFrame = 100/6
        self.running = False
        self.keysPressed = []
        
        self.eye = Point3D(0.0, 0.0, -2.0)
        
        self.shaderProgram = None
        
        self.renderUnits = []
        
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
        
        errorCheck = self.createShaders()
        if not errorCheck:
            return False
        self.initStaticPolygonVBO()
        self.initDynamicPolygonVBO()
        
        return True


    def cleanup(self):
        self.destroyVBOs()
        self.destroyShaders()        
    
    def createShaders(self):
        try:
            self.shaderProgram = ShaderProgram('data/shader/vertexshader.vert',
                                               'data/shader/fragmentshader.frag',
                                               [('in_color', '4fv'),
                                                ('uv', '2fv')],
                                               [('projection_matrix', 'Matrix4fv'),
                                                ('view_matrix', 'Matrix4fv')])
        except Exception as e:
            print('Error creating Shader:', e)
            return False
        
        self.shaderProgram.use()
        
        self.shaderProgram.setUniform('projection_matrix',
                                      self.projectionMatrix)
        self.shaderProgram.setUniform('view_matrix',
                                      self.viewMatrix)
        
        return True


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
        
        for polygon in self.gameMap.getStaticPolygons():
            r, g, b = polygon.getFillColorTuple()
            for point in polygon.getTrianglePoints3D():
                vertices.extend([point.x, point.y, point.z, 1.0])
                colors.extend([r/255.0, g/255.0, b/255.0, 1.0])
            uvCoordinates.extend(polygon.getTriangleUVCoordinates())
        
        newRenderUnit = RenderUnit(self.shaderProgram,
                                   [0, 'in_color', 'uv'],
                                   [vertices, colors, uvCoordinates])
        self.renderUnits.append(newRenderUnit)


    def destroyVBOs(self):
        errorCheckValue = glGetError()
     
        glBindBuffer(GL_ARRAY_BUFFER, 0)
     
        glDeleteBuffers(1, [self.colorBufferIdDynamic])
        glDeleteBuffers(1, [self.vboIdDynamic])
     
        glBindVertexArray(0)
        
        glDeleteVertexArrays(1, [self.vaoIdDynamic])
        
        for renderUnit in self.renderUnits:
            renderUnit.destroyVertexArrayObject()
     
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
        
        glBindVertexArray(self.vaoIdDynamic)
        glDrawArrays(GL_TRIANGLES, 0, self.dynamicVerticesCount)
        
        self.shaderProgram.unUse()
        
        
        for renderUnit in self.renderUnits:
            renderUnit.setShaderUniform('projection_matrix',
                                        self.projectionMatrix)
            renderUnit.setShaderUniform('view_matrix',
                                        self.viewMatrix)
            renderUnit.render()
        
        
        self.updateDynamicPolygonVBO()
        
        errorCheckValue = glGetError()
        if errorCheckValue != GL_NO_ERROR:
            print('draw error',
                  gluErrorString(errorCheckValue))
            exit(-1);

    
    def processEvents(self, events):
        actions = 0
        
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
                actions += ACTION_ROTATE_RIGHT
            elif key == K_LEFT:
                actions += ACTION_ROTATE_LEFT
            elif key == K_w:
                actions += ACTION_FORWARD
            elif key == K_s:    # s
                actions += ACTION_BACK
            elif key == K_a:     # a
                actions += ACTION_LEFT
            elif key == K_d:    # d
                actions += ACTION_RIGHT
            elif key == K_LSHIFT:
                actions += ACTION_WALK
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
                
        self.client.setActions(actions)
    
    
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
        
        resolutionTuple = (800, 600)
        
        video_flags = OPENGL | DOUBLEBUF
        pygame.display.set_mode(resolutionTuple, video_flags)
        
        self.resize(resolutionTuple)
        errorCheck = self.init()
        
        if not errorCheck:
            self.client.stop()
            pygame.quit()
            return
        
        self.running = True
        while self.running:
            runAndWait(self.runBody, self.millisecondsPerFrame)
        
        self.cleanup()
        
        pygame.quit()
