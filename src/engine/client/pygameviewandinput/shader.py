class ShaderProgram(object):
    def __init__(self, vertexShaderFilename, fragmentShaderFilename,
                 attributeList, uniformList):
        '''
        @param attributeList ... list of tuples (attribute name, type)
        @param uniformList   ... list of tuples (uniform name, type)        
        '''
        self.vertexShaderFilename = vertexShaderFilename
        self.fragmentShaderFilename = fragmentShaderFilename
        self.attributeList = attributeList
        self.uniformList = uniformList
        
        self.vertexShaderId = None
        self.fragmentShaderId = None
    
    def destroy(self):
        pass
    
    def __getShaderStringFromFile(self, filename):
        pass
    
    def getProgramId(self):
        pass
    
    def use(self):
        pass
    
    def unUse(self):
        pass
    
    def setUniform(self, uniformName, data):
        pass