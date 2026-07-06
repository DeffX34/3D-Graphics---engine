from math import sin, cos, pi, sqrt
from time import sleep, time
import pygame
import sys
from math_functions import *
import os
pygame.init()

WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3d engine mazafaka")
hweight = WIDTH/2
hheight = HEIGHT/2

clock = pygame.Clock()
FPS = 60
focal_length = 250
yblackout = 4
t = 0

camera_pos = [0,-10,0]

class Cube:
    def __init__(self, a, pos):
        self.a = a / 2
        self.pos = pos
        self.rot = (0, 0, 0)
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.z = self.pos[2]
        self.xR = self.rot[0]
        self.yR = self.rot[1]
        self.zR = self.rot[2]
        self.matrix = []
        self.vc = []
        self.screen_vertices_dat = []
        self.Z = 0
        self.edge_points = []
        self.vertices = []
        self.cube_faces = []
        self.screen_verticesC = []
        
    def draw(self):
        self.screen_vertices_dat = []
        self.edge_points = []
        self.screen_verticesC = []
        self.rot = (lerp(-pi, pi, (sin(t)+1)/2), lerp(-pi, pi, (sin(t+6)+1)/2), lerp(-pi, pi, (cos(t+2)+1)/2))
        self.xR = self.rot[0]
        self.yR = self.rot[1]
        self.zR = self.rot[2]
        self.matrix = [[cos(self.yR)*cos(self.zR), sin(self.xR)*sin(self.yR)*cos(self.zR)-cos(self.xR)*sin(self.zR), cos(self.xR)*sin(self.yR)*cos(self.zR)+sin(self.xR)*sin(self.zR)],
                       [cos(self.yR)*sin(self.zR), sin(self.xR)*sin(self.yR)*sin(self.zR)+cos(self.xR)*cos(self.zR), cos(self.xR)*sin(self.yR)*sin(self.zR)-sin(self.xR)*cos(self.zR)],
                       [-sin(self.yR), sin(self.xR)*cos(self.yR), cos(self.xR)*cos(self.yR)]]
        
        self.vc = [ [-self.a, -self.a, -self.a],
                    [self.a, -self.a, -self.a],
                    [self.a, self.a, -self.a],
                    [-self.a, self.a, -self.a],
                    [-self.a, -self.a, self.a],
                    [self.a, -self.a, self.a],
                    [self.a, self.a, self.a],
                    [-self.a, self.a, self.a]]

        
        self.vertices = [
[(self.vc[0][0]*self.matrix[0][0]) + (self.vc[0][1]*self.matrix[0][1]) + (self.vc[0][2]*self.matrix[0][2]), ((self.vc[0][0]*self.matrix[1][0]) + (self.vc[0][1]*self.matrix[1][1]) + (self.vc[0][2]*self.matrix[1][2])), (self.vc[0][0]*self.matrix[2][0]) + (self.vc[0][1]*self.matrix[2][1]) + (self.vc[0][2]*self.matrix[2][2])],
[(self.vc[1][0]*self.matrix[0][0]) + (self.vc[1][1]*self.matrix[0][1]) + (self.vc[1][2]*self.matrix[0][2]), ((self.vc[1][0]*self.matrix[1][0]) + (self.vc[1][1]*self.matrix[1][1]) + (self.vc[1][2]*self.matrix[1][2])), (self.vc[1][0]*self.matrix[2][0]) + (self.vc[1][1]*self.matrix[2][1]) + (self.vc[1][2]*self.matrix[2][2])],
[(self.vc[2][0]*self.matrix[0][0]) + (self.vc[2][1]*self.matrix[0][1]) + (self.vc[2][2]*self.matrix[0][2]), ((self.vc[2][0]*self.matrix[1][0]) + (self.vc[2][1]*self.matrix[1][1]) + (self.vc[2][2]*self.matrix[1][2])), (self.vc[2][0]*self.matrix[2][0]) + (self.vc[2][1]*self.matrix[2][1]) + (self.vc[2][2]*self.matrix[2][2])],
[(self.vc[3][0]*self.matrix[0][0]) + (self.vc[3][1]*self.matrix[0][1]) + (self.vc[3][2]*self.matrix[0][2]), ((self.vc[3][0]*self.matrix[1][0]) + (self.vc[3][1]*self.matrix[1][1]) + (self.vc[3][2]*self.matrix[1][2])), (self.vc[3][0]*self.matrix[2][0]) + (self.vc[3][1]*self.matrix[2][1]) + (self.vc[3][2]*self.matrix[2][2])],
[(self.vc[4][0]*self.matrix[0][0]) + (self.vc[4][1]*self.matrix[0][1]) + (self.vc[4][2]*self.matrix[0][2]), ((self.vc[4][0]*self.matrix[1][0]) + (self.vc[4][1]*self.matrix[1][1]) + (self.vc[4][2]*self.matrix[1][2])), (self.vc[4][0]*self.matrix[2][0]) + (self.vc[4][1]*self.matrix[2][1]) + (self.vc[4][2]*self.matrix[2][2])],
[(self.vc[5][0]*self.matrix[0][0]) + (self.vc[5][1]*self.matrix[0][1]) + (self.vc[5][2]*self.matrix[0][2]), ((self.vc[5][0]*self.matrix[1][0]) + (self.vc[5][1]*self.matrix[1][1]) + (self.vc[5][2]*self.matrix[1][2])), (self.vc[5][0]*self.matrix[2][0]) + (self.vc[5][1]*self.matrix[2][1]) + (self.vc[5][2]*self.matrix[2][2])],
[(self.vc[6][0]*self.matrix[0][0]) + (self.vc[6][1]*self.matrix[0][1]) + (self.vc[6][2]*self.matrix[0][2]), ((self.vc[6][0]*self.matrix[1][0]) + (self.vc[6][1]*self.matrix[1][1]) + (self.vc[6][2]*self.matrix[1][2])), (self.vc[6][0]*self.matrix[2][0]) + (self.vc[6][1]*self.matrix[2][1]) + (self.vc[6][2]*self.matrix[2][2])],
[(self.vc[7][0]*self.matrix[0][0]) + (self.vc[7][1]*self.matrix[0][1]) + (self.vc[7][2]*self.matrix[0][2]), ((self.vc[7][0]*self.matrix[1][0]) + (self.vc[7][1]*self.matrix[1][1]) + (self.vc[7][2]*self.matrix[1][2])), (self.vc[7][0]*self.matrix[2][0]) + (self.vc[7][1]*self.matrix[2][1]) + (self.vc[7][2]*self.matrix[2][2])]]
  
        for i in self.vertices:
            screenXYZ = i[0] * focal_length / distance(0,camera_pos[1],0,0,i[1],0, True, "y") + hweight, i[2] * focal_length / distance(0,camera_pos[1],0,0,i[1],0, True, "y") + hheight
            self.screen_vertices_dat.append((screenXYZ[0], screenXYZ[1], distance(0,camera_pos[1],0,0,i[1],0, True, "y"), i[1]))
            self.screen_verticesC.append((screenXYZ[0], screenXYZ[1]))

        for i in self.vertices:
            self.edge_points.append((i[0], i[1]))

        for i in self.screen_vertices_dat:
            colorvert = max(min(255, round(lerp(1, 0.2, (i[3]/yblackout)) * 255)), 0)
            pygame.draw.circle(screen, rgb_unit0_1(colorvert, False), (i[0], i[1]), 5)

        self.cube_faces = [(self.screen_verticesC[0], self.screen_verticesC[1], self.screen_verticesC[2], self.screen_verticesC[3]),
                           (self.screen_verticesC[4], self.screen_verticesC[5], self.screen_verticesC[6], self.screen_verticesC[7]),
                           (self.screen_verticesC[0], self.screen_verticesC[1], self.screen_verticesC[5], self.screen_verticesC[4]),
                           (self.screen_verticesC[2], self.screen_verticesC[3], self.screen_verticesC[7], self.screen_verticesC[6]),
                           (self.screen_verticesC[0], self.screen_verticesC[3], self.screen_verticesC[7], self.screen_verticesC[4]),
                           (self.screen_verticesC[1], self.screen_verticesC[2], self.screen_verticesC[6], self.screen_verticesC[5]),                        
                           ]
        
        for i in range(8):
            coloredge = max(min(255, round(lerp(1, 0.2, (self.screen_vertices_dat[i][3]/(yblackout+1))) * 255)), 0)
            start = (self.screen_vertices_dat[i][0], self.screen_vertices_dat[i][1])
            end = (self.screen_vertices_dat[i+1][0], self.screen_vertices_dat[i+1][1]) if i != 3 and i != 7 else (self.screen_vertices_dat[i - 3][0], self.screen_vertices_dat[i - 3][1])
            pygame.draw.line(screen, rgb_unit0_1(coloredge, False), start, end)
            
        for i in range(8):
            if i > 3:
                coloredge = max(min(255, round(lerp(1, 0.2, (self.screen_vertices_dat[i][3]/(yblackout+1))) * 255)), 0)
                start = (self.screen_vertices_dat[i-4][0], self.screen_vertices_dat[i-4][1])
                end = (self.screen_vertices_dat[i][0], self.screen_vertices_dat[i][1])
                pygame.draw.line(screen, rgb_unit0_1(coloredge, False), start, end)

        colorface = 0

        points = []
        for i in self.cube_faces: 
            colorface = max(min(255, round(lerp(1, 0.2, (self.screen_vertices_dat[self.cube_faces.index(i)][3] /(yblackout+1))) * 255)), 0)
            pygame.draw.polygon(screen, rgb_unit0_1(colorface, False), i)


cube = Cube(7, (0, 0, 0))        
cube.draw()

running = True
start_time = time()

r = 100

while running:
    t = (time() - start_time) * 0.5
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(rgb0_1(0.68, 0.85, 0.90, 0))

    scrVert = cube.screen_vertices_dat
    scrDrawEdges = cube.edge_points

    
        

    cube.draw()
    pygame.display.flip()
    os.system("cls")
else:
    pygame.quit()
    sys.exit()