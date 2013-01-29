from OpenGL.GL import *
from OpenGL.GLU import *

class ShaderProgram(object):
    def __init__(self, vertexShaderFilename, fragmentShaderFilename,
                 attributeList, uniformList):
        '''
        @param attributeList
                list of tuples (attribute name : string, type : string)
        @param uniformList
                list of tuples (uniform name : string, type :string)        
        '''
        self.vertexShaderFilename = vertexShaderFilename
        self.fragmentShaderFilename = fragmentShaderFilename
        self.attributeList = attributeList
        self.uniformList = uniformList
        
        # dictionary of attribute locations {attribute name -> location id}
        self.attributeLocations = dict()
        # dictionary of attribute types {attribute name -> type}
        self.attributeTypes = dict()
        
        # dictionary of uniform locations {uniform name -> location id}
        self.uniformLocations = dict()
        # dictionary of uniform types {uniform name -> type}
        self.uniformTypes = dict()
        
        self.vertexShaderId = None
        self.fragmentShaderId = None
        self.programId = None
        
        self.initProgram()
        self.initAttributesAndUniforms()


    def destroy(self):
        errorCheckValue = glGetError()
     
        self.unUse()
     
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


    def initProgram(self):
        '''create the shader program, compile shader and link them to the
        program'''
        
        errorCheckValue = glGetError()
        
        # vertex shader
        vertexShaderString = \
                [self.__getShaderStringFromFile(self.vertexShaderFilename)]
        self.vertexShaderId = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(self.vertexShaderId, vertexShaderString)
        glCompileShader(self.vertexShaderId)

        log = glGetShaderInfoLog(self.vertexShaderId)
        if log:
            print('Vertex Shader: ', log)
        
        # fragment shader
        fragmentShaderString = \
                [self.__getShaderStringFromFile(self.fragmentShaderFilename)]

        self.fragmentShaderId = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(self.fragmentShaderId, fragmentShaderString)
        glCompileShader(self.fragmentShaderId)

        log = glGetShaderInfoLog(self.fragmentShaderId)
        if log:
            print('Fragment Shader: ', log)

        # shader program creation 
        self.programId = glCreateProgram()
        glAttachShader(self.programId, self.vertexShaderId)
        glAttachShader(self.programId, self.fragmentShaderId)
        glLinkProgram(self.programId)


    def initAttributesAndUniforms(self):
        '''extract locations of attributes and uniforms'''
        assert(self.programId is not None)
        
        # process attributes
        for name, dataType in self.attributeList:
            self.attributeLocations[name] = \
                    glGetAttribLocation(self.programId,
                                        name.encode('ascii'))
            self.attributeTypes[name] = dataType
        
        
        # process uniforms
        for name, dataType in self.uniformList:
            self.uniformLocations[name] = \
                    glGetUniformLocation(self.programId,
                                         name.encode('ascii'))
            self.uniformTypes[name] = dataType
            


    def __getShaderStringFromFile(self, filename):
        try:
            file = open(filename, 'r')
            string = file.read()
        finally:
            file.close()
        
        return string
    
    def getProgramId(self):
        return self.programId
    
    
    def getAttributeLocation(self, attributeName):
        if attributeName in self.attributeLocations:
            return self.attributeLocations[attributeName]


    def getUniformLocation(self, uniformName):
        if uniformName in self.uniformLocations:
            return self.uniformLocations[uniformName]


    def use(self):
        glUseProgram(self.programId)


    def unUse(self):
        glUseProgram(0)


    def setUniform(self, uniformName, data):
        assert(uniformName in self.uniformLocations)
        assert(uniformName in self.uniformTypes)
        
        location = self.uniformLocations[uniformName]
        dataType = self.uniformTypes[uniformName]
        
        if dataType == 'Matrix4fv':
            glUniformMatrix4fv(location, 1, GL_FALSE, data)
        