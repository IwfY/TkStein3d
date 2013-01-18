from math import cos, pi, sin, tan
from engine.coordinate import Vector3D, Point3D
from engine.mathhelper import getVectorDotProduct

def createPerspectiveMatrix(fieldOfView, aspect, nearDistance, farDistance):
    '''reference:
    http://stackoverflow.com/questions/3498581/in-opengl-what-is-the-simplest-way-to-create-a-perspective-view-using-only-open?rq=1
    '''
    matrix = [1, 0, 0, 0,
              0, 1, 0, 0,
              0, 0, 1, 0,
              0, 0, 0, 1]
    
    angle = (fieldOfView / 180.0) * pi
    f = 1.0 / tan(angle * 0.5)

    matrix[0] = f / aspect
    matrix[5] = f
    matrix[10] = (farDistance + nearDistance) / (nearDistance - farDistance)
    matrix[11] = -1.0
    matrix[14] = (2.0 * farDistance * nearDistance) / \
                 (nearDistance - farDistance)

    return matrix



def createLookAtViewMatrix(cameraPosition, lookAtPosition,
                           upVector=Vector3D(0.0, 1.0, 0.0)):
    '''create a view matrix (column major) representing the translation
    and rotation in a look at transformation
    
    @param cameraPosition : const Point3D    position of the camera
    @param lookAtPosition : const Point3D    position the camera is looking at
    @param upVector       : const Vector3D   normalized vector that points up
    
    @return 4x4 matrix values in a list in column major order
    '''
    
    lookAtVector = Vector3D(lookAtPosition.x - cameraPosition.x,
                            lookAtPosition.y - cameraPosition.y,
                            lookAtPosition.z - cameraPosition.z)
    lookAtVector.normalize()
    
    normalizedUpVector = upVector.getNormalizedVector()
    
    horizonatalVector = lookAtVector.getCrossProduct(normalizedUpVector)
    
    downVector = horizonatalVector.getCrossProduct(lookAtVector)

    matrix = [1, 0, 0, 0,
              0, 1, 0, 0,
              0, 0, 1, 0,
              0, 0, 0, 1]
    
    matrix[0] = horizonatalVector.x
    matrix[4] = horizonatalVector.y
    matrix[8] = horizonatalVector.z
    matrix[1] = downVector.x
    matrix[5] = downVector.y
    matrix[9] = downVector.z
    matrix[2] = -lookAtVector.x
    matrix[6] = -lookAtVector.y
    matrix[10] = -lookAtVector.z
    matrix[12] = -getVectorDotProduct(horizonatalVector, cameraPosition)
    matrix[13] = -getVectorDotProduct(downVector, cameraPosition)
    matrix[14] = -getVectorDotProduct(lookAtVector, cameraPosition)

    return matrix;



def createLookAtAngleViewMatrix(cameraPosition, viewAngle,
                                upVector=Vector3D(0.0, 1.0, 0.0)):
    '''create a view matrix (column major) representing the translation
    and rotation in a look at transformation
    
    @param cameraPosition : const Point3D   position of the camera
    @param viewAngle      : const float     angle between look at vector and
                                            negative z axis; grows clockwise
    @param upVector       : const Vector3D  normalized vector that points up
    
    @return 4x4 matrix values in a list in column major order
    '''
    
    lookAtPosition = Point3D(cameraPosition.x + sin(viewAngle),
                             cameraPosition.y,
                             cameraPosition.z - cos(viewAngle))

    return createLookAtViewMatrix(cameraPosition, lookAtPosition, upVector)
