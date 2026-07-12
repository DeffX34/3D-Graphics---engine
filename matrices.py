from math import sin, cos, pi
import numpy as np

def rot_matrix(xrot, yrot, zrot):
    xR, yR, zR = xrot * pi / 180, yrot * pi / 180, zrot * pi / 180
    return np.array([[cos(yR)*cos(zR), sin(xR)*sin(yR)*cos(zR)-cos(xR)*sin(zR), cos(xR)*sin(yR)*cos(zR)+sin(xR)*sin(zR)],
            [cos(yR)*sin(zR), sin(xR)*sin(yR)*sin(zR)+cos(xR)*cos(zR), cos(xR)*sin(yR)*sin(zR)-sin(xR)*cos(zR)],
            [-sin(yR), sin(xR)*cos(yR), cos(xR)*cos(yR)]])

def multiplymatrices(m1, m2):
    return [m1[0][0]*m2[0][0] + m1[0][1]*m2[1][0] + m1[0][2]*m2[2][0],
            m1[0][0]*m2[0][1] + m1[0][1]*m2[1][1] + m1[0][2]*m2[2][1],
            m1[0][0]*m2[0][2] + m1[0][1]*m2[1][2] + m1[0][2]*m2[2][2]]

def indentity_matrix():
    return [[1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]]