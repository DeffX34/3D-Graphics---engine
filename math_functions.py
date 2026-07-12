from math import sqrt, sin, cos, acos, asin, pi
def rgb0_1(r, g, b, multiplier=1, convertto255 = True):
    if convertto255:
        return (round((r*255)*multiplier), round((g*255)*multiplier), round((b*255)*multiplier))
    else:
        return (round(r*multiplier), round(g*multiplier), round(b*multiplier))

def rgb_unit0_1(unit, convertto255=True):
    if convertto255:
        return (round(unit*255), round(unit*255), round(unit*255))
    else:
        return(unit, unit, unit)
    
def rgb_to_hex(rgb, is255=False):
    if not is255:
        rgb255 = (round(rgb[0]*255), round(rgb[1]*255), round(rgb[2]*255))
    else:
        rgb255 = rgb
    return "#%02x%02x%02x" % rgb255

def lerp(min, max, alpha):
    return min + alpha * (max - min)

def dotproduct(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

def crossproduct(v1, v2):
    return (v1[1]*v2[2]-v1[2]*v2[1], v1[2]*v2[0]-v1[0]*v2[2], v1[0]*v2[1]-v1[1]*v2[0])

def normalize(v):
    length = sqrt(v[0]**2+v[1]**2+v[2]**2)
    
    return (v[0]/length,v[1]/length,v[2]/length) if length != 0 else (0, 0, 0)

def lengthsquared(v):
    return(v[0]**2, v[1]**2, v[2]**2)

def distance (v1, v2, oneaxis = None, axis = None):
    if oneaxis != True: 
        return sqrt((v2[0]-v1[0])**2 + (v2[1]-v1[1])**2 + (v2[2]-v1[2])**2)
    elif oneaxis == True and axis == "x":
        return sqrt((v2[0]-v1[0])**2)
    elif oneaxis == True and axis == "y":
        return sqrt((v2[1]-v1[1])**2)
    elif oneaxis == True and axis == "z":
        return sqrt((v2[2]-v1[2])**2)
    
def optimisedDistance(v1, v2):
    return (v2[0] - v1[0])**2 + (v2[1] - v1[1])**2 + (v2[2] - v1[2])**2

def minusV(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])

def distbetween2v(v1, v2):
    return sqrt(lengthsquared(minusV(v1, v2)))

def reflectionvector(v, normal):
    return v - 2 * dotproduct(v, normal) * normal

def anglebetweentwoV(v1, v2):
    return acos(dotproduct(v1, v2))

def getZ(point, cameraposition, forwardvector):
    v = minusV(point, cameraposition)
    return dotproduct(v, forwardvector)

def lerpV(v1, v2, alpha):
    x = v1[0] + alpha * (v2[0] - v1[0])
    y = v1[1] + alpha * (v2[1] - v1[1])
    z = v1[2] + alpha * (v2[2] - v1[2])
    return(x, y, z)

def degreeToRad(angle):
    return angle * pi / 180

def clamp(value, minv, maxv):
    return max(min(value, maxv), minv)