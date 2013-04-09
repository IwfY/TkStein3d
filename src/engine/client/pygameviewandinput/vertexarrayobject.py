from numpy import array, float32
from OpenGL.GL import *
from OpenGL.GLU import *


class VertexArrayObject(object):
    def __init__(self, attributeList, arrayList):
        '''
        @param attributeList
            list of strings with the corresponding attribute names for the data
            arrays (first is ignored as this is for vertex data)
        @param list of arrays containing the data; in the same order as
            specified by attribute list
        '''
        
        # first array is for vertex data --> attribute 0
        attributeList[0] = 0
        
        # a dict that maps attribute names to vertex buffer object ids
        self.vertexBufferObjectDict = dict([])
        
        self.vertexArrayId = None
        
        self.init(attributeList, arrayList)
    
    
    def init(self, attributeList, arrayList):        
        errorCheckValue = glGetError()
        
        self.vertexArrayId = glGenVertexArrays(1)
        glBindVertexArray(self.vertexArrayId)
        
        for i in range(len(attributeList)):
            # transform data array to numpy array
            arrayList[i] = array(arrayList[i], dtype=float32)
            
            newVertexBufferId = glGenBuffers(1)
            self.vertexBufferObjectDict[attributeList[i]] = newVertexBufferId
            
            glBindBuffer(GL_ARRAY_BUFFER,
                         newVertexBufferId)
            
            glBufferData(GL_ARRAY_BUFFER,
                         len(arrayList[i]) * 4,
                         arrayList[i],
                         GL_STATIC_DRAW)
        
        errorCheckValue = glGetError()
        if errorCheckValue != GL_NO_ERROR:
            print('error creating VBOs',
                  gluErrorString(errorCheckValue))
            exit(-1)
    
    
    def destroy(self):
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        
        for vertexBufferObjectTuple in self.vertexBufferObjectDict.items():
            glDeleteBuffers(1, [vertexBufferObjectTuple[1]])
     
        glBindVertexArray(0)
        glDeleteVertexArrays(1, [self.vertexArrayId])


    def getVertexArrayId(self):
        return self.vertexArrayId


    def getVertexBufferObjectsDict(self):
        return self.vertexBufferObjectDict


    def updateVertexBufferObjectData(self, attributeName, data):
        vertexBufferObjectId = self.vertexBufferObjectDict[attributeName]
        
        data = array(data, dtype=float32)
        
        glBindBuffer(GL_ARRAY_BUFFER, vertexBufferObjectId)
        glBufferData(GL_ARRAY_BUFFER, len(data) * 4, data,
                     GL_STATIC_DRAW)
