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
              0, 0, 0, 0]
    
    angleRad = (fieldOfView / 180.0) * pi
    f = 1.0 / tan(angleRad * 0.5)      # == 1 for fieldOfView == 90°

    matrix[0] = f / aspect
    matrix[5] = f
    matrix[10] = (farDistance + nearDistance) / (nearDistance - farDistance)
    matrix[11] = -1.0
    matrix[14] = (2.0 * farDistance * nearDistance) / \
                 (nearDistance - farDistance)
    
    return matrix


def createOrthogonalProjectionMatrixWidthHeight(width, height,
                                                nearDistance, farDistance):
    '''source:
    http://stackoverflow.com/questions/688240/formula-for-a-orthogonal-projection-matrix?rq=1'''
    matrix = [1, 0, 0, 0,
              0, 1, 0, 0,
              0, 0, 1, 0,
              0, 0, 0, 1]
    
    matrix[0] = 2.0 / width
    matrix[5] = 2.0 / height
    matrix[10] = 1.0 / (farDistance - nearDistance)
    matrix[11] = -nearDistance / (farDistance - nearDistance) # or at [15]?
    
    return matrix



def createLookAtViewMatrix(cameraPosition, lookAtPosition,
                           worldUpVector=Vector3D(0.0, 1.0, 0.0)):
    '''create a view matrix (column major) representing the translation
    and rotation in a look at transformation
    
    @param cameraPosition : const Point3D    position of the camera
    @param lookAtPosition : const Point3D    position the camera is looking at
    @param worldUpVector  : const Vector3D   normalized vector representing
                                             the worlds up direction
    
    @return 4x4 matrix values in a list in column major order
    '''
    
    lookVector = Vector3D(lookAtPosition.x - cameraPosition.x,
                            lookAtPosition.y - cameraPosition.y,
                            lookAtPosition.z - cameraPosition.z)
    lookVector.normalize()
    
    normalizedWorldUpVector = worldUpVector.getNormalizedVector()
    
    horizonatalVector = lookVector.getCrossProduct(normalizedWorldUpVector)
    
    upVector = horizonatalVector.getCrossProduct(lookVector)

    matrix = [1, 0, 0, 0,
              0, 1, 0, 0,
              0, 0, 1, 0,
              0, 0, 0, 1]
    
    matrix[0] = horizonatalVector.x
    matrix[4] = horizonatalVector.y
    matrix[8] = horizonatalVector.z
    matrix[1] = upVector.x
    matrix[5] = upVector.y  
    matrix[9] = upVector.z
    matrix[2] = lookVector.x
    matrix[6] = lookVector.y
    matrix[10] = lookVector.z
    matrix[12] = -getVectorDotProduct(horizonatalVector, cameraPosition)
    matrix[13] = -getVectorDotProduct(upVector, cameraPosition)
    matrix[14] = -getVectorDotProduct(lookVector, cameraPosition)

    return matrix;



def createLookAtAngleViewMatrix(cameraPosition, viewAngle,
                                worldUpVector=Vector3D(0.0, 1.0, 0.0)):
    '''create a view matrix (column major) representing the translation
    and rotation in a look at transformation
    
    @param cameraPosition : const Point3D    position of the camera
    @param lookAtPosition : const Point3D    position the camera is looking at
    @param worldUpVector  : const Vector3D   normalized vector representing
                                             the worlds up direction
    
    @return 4x4 matrix values in a list in column major order
    '''
    
    lookAtPosition = Point3D(cameraPosition.x + sin(viewAngle),
                             cameraPosition.y,
                             cameraPosition.z - cos(viewAngle))

    return createLookAtViewMatrix(cameraPosition, lookAtPosition, worldUpVector)