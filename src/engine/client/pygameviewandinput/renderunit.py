from engine.client.pygameviewandinput.vertexarrayobject import VertexArrayObject

from OpenGL.GL import *
from engine.shared.coordinate import Point3D, AABoundingBox

class RenderUnit(object):
    '''this class provides an easy access to a single vertex array object
    connected to a shader program'''
    
    def __init__(self, shaderProgram, attributeList, arrayList):
        self.shaderProgram = shaderProgram
        
        self.vertexArrayObject = VertexArrayObject(attributeList, arrayList)
        #TODO check if attribute list of shader and vertex array match
        
        self.enableVertexAttributes()
        
        # every 4 floats represent a vertex
        self.vertices = arrayList[0].copy()
        self.verticesCount = int(len(self.vertices) / 4)
        
        self.boundingBox = None
        self.calculateBoundingBox()
        #TODO calculate bounding box
    
    
    def enableVertexAttributes(self):
        vertexBufferDict = self.vertexArrayObject.getVertexBufferObjectsDict()
        
        #vertex data
        glBindBuffer(GL_ARRAY_BUFFER, vertexBufferDict[0])
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
        
        for attributeName in vertexBufferDict.keys():
            if (attributeName == 0):
                continue
            
            glBindBuffer(GL_ARRAY_BUFFER, vertexBufferDict[attributeName])
            
            attributeLocation = self.shaderProgram.getAttributeLocation(
                                        attributeName)
            attributeType = self.shaderProgram.getAttributeType(
                                        attributeName)
            numberOfComponents = 4
            if attributeType == '2fv':
                numberOfComponents = 2
            
            glVertexAttribPointer(attributeLocation,
                    numberOfComponents, GL_FLOAT, GL_FALSE, 0, None)
            glEnableVertexAttribArray(attributeLocation)


    def setShaderUniform(self, uniformName, data):
        self.shaderProgram.setUniform(uniformName, data)
    
    
    def updateVertexBufferObjectData(self, attributeName, data):
        self.vertexArrayObject.\
                updateVertexBufferObjectData(attributeName, data)
        
        if attributeName == 0:
            self.vertices = data.copy()
            self.verticesCount = int(len(self.vertices) / 4)
            self.calculateBoundingBox()

    
    def calculateBoundingBox(self):
        minX = None
        maxX = None
        minY = None
        maxY = None
        minZ = None
        maxZ = None
        first = True
        
        for i in range(int(len(self.vertices) / 4)):
            if first:
                minX = self.vertices[i * 4]
                maxX = self.vertices[i * 4]
                minY = self.vertices[i * 4 + 1]
                maxY = self.vertices[i * 4 + 1]
                minZ = self.vertices[i * 4 + 2]
                maxZ = self.vertices[i * 4 + 2]
                first = False
                continue
            
            minX = min(minX, self.vertices[i * 4])
            maxX = max(maxX, self.vertices[i * 4])
            minY = min(minY, self.vertices[i * 4 + 1])
            maxY = max(maxY, self.vertices[i * 4 + 1])
            minZ = min(minZ, self.vertices[i * 4 + 2])
            maxZ = max(maxZ, self.vertices[i * 4 + 2])
        
        point1 = Point3D(minX, minY, minZ)
        point2 = Point3D(maxX, maxY, maxZ)
        
        self.boundingBox = AABoundingBox(point1, point2)


    def destroyVertexArrayObject(self):
        self.vertexArrayObject.destroy()
    
    
    def destroyAll(self):
        self.vertexArrayObject.destroy()
        self.shaderProgram.destroy()


    def render(self):
        self.shaderProgram.use()
        
        glBindVertexArray(self.vertexArrayObject.getVertexArrayId())
        glDrawArrays(GL_TRIANGLES, 0, self.verticesCount)
        
        self.shaderProgram.unUse() 
