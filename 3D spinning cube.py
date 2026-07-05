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

clock = pygame.Clock()
FPS = 60
focal_length = 250

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
        self.screen_vertices = []
        self.Z = 0
        
        self.vertices = [[-self.a, -self.a, -self.a],
                         [self.a, -self.a, -self.a],
                         [self.a, self.a, -self.a],
                         [-self.a, self.a, -self.a],
                         [-self.a, -self.a, self.a],
                         [self.a, -self.a, self.a],
                         [self.a, self.a, self.a],
                         [-self.a, self.a, self.a]]
        
    def draw(self):
        self.screen_vertices = []
        self.rot = (lerp(-pi/2, pi/2, (sin(t)+1)/2), lerp(-pi, pi, (sin(t+6)+1)/2), lerp(-pi, pi, (cos(t+2)+1)/2))
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
            self.screen_vertices.append((i[0] * focal_length / distance(0,camera_pos[1],0,0,i[1],0, True, "y"), i[2] * focal_length / distance(0,camera_pos[1],0,0,i[1],0, True, "y"), i[1]))


cube = Cube(5, (0, 0, 0))        
cube.draw()

running = True
start_time = time()

r = 100

while running:
    t = (time() - start_time) * 1
    clock.tick(FPS)
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))

    scrVert = cube.screen_vertices
    for i in scrVert:
        pygame.draw.circle(screen, rgb_unit0_1(1), (i[0]+WIDTH/2, i[1]+HEIGHT/2), 5)
    
    pygame.display.flip()
    os.system("cls")
    cube.draw()
    print("\n",t)
else:
    pygame.quit()
    sys.exit()