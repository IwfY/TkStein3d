from engine.client.pygameviewandinput.vertexarrayobject import VertexArrayObject

from OpenGL.GL import *

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
