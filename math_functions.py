from math import sqrt
def rgb0_1(r, g, b, multiplier=1, convertto255 = True):
    if convertto255:
        return ((r*255)*multiplier, (g*255)*multiplier, (b*255)*multiplier)
    else:
        return (r*multiplier, g*multiplier, b*multiplier)

def rgb_unit0_1(unit, convertto255=True):
    if convertto255:
        return (unit*255, unit*255, unit*255)
    else:
        return(unit, unit, unit)
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
    
