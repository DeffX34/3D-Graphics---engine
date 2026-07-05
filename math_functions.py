from math import sqrt
def rgb0_1(r, g, b):
    return (r*255, g*255, b*255)

def rgb_unit0_1(unit):
    return (unit*255, unit*255, unit*255)

def lerp(min, max, a):
    return min + a * (max - min)

def distance (x1, y1, z1, x2, y2, z2, oneaxis = None, axis = None):
    if oneaxis != True: 
        return sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
    elif oneaxis == True and axis == "x":
        return sqrt((x2-x1)**2)
    elif oneaxis == True and axis == "y":
        return sqrt((y2-y1)**2)
    elif oneaxis == True and axis == "z":
        return sqrt((z2-z1)**2)