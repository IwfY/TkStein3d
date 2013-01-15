from math import cos, pi, sin, tan

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
