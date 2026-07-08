from math import sin, cos
import numpy as np

def rot_matrix(xR, yR,zR):
    return np.array([[cos(yR)*cos(zR), sin(xR)*sin(yR)*cos(zR)-cos(xR)*sin(zR), cos(xR)*sin(yR)*cos(zR)+sin(xR)*sin(zR)],
            [cos(yR)*sin(zR), sin(xR)*sin(yR)*sin(zR)+cos(xR)*cos(zR), cos(xR)*sin(yR)*sin(zR)-sin(xR)*cos(zR)],
            [-sin(yR), sin(xR)*cos(yR), cos(xR)*cos(yR)]])