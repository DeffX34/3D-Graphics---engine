from math import sin, cos, pi, sqrt, tan, atan
from time import sleep, time
import pygame
import sys
from math_functions import *
import os
from matrices import rot_matrix
pygame.init()

WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3d engine mazafaka")
hweight = WIDTH/2
hheight = HEIGHT/2

asp_ratio = WIDTH/HEIGHT

clock = pygame.time.Clock()
FPS = 60
focal_length = 250
zblackout = 12
t = 0

camera_pos = [0,0,0]

class Cube:
    def __init__(self, a, pos):
        self.a = a / 2
        self.pos = pos
        self.rot = (0, 0, 0)
        self.xc = self.pos[0]
        self.yc = self.pos[1]
        self.zc = self.pos[2]
        self.zDepth = self.pos[2]
        self.xR = self.rot[0]
        self.yR = self.rot[1]
        self.zR = self.rot[2]
        self .matrix = []
        self.vc = []
        self.screen_vertices_dat = []
        self.edge_points = []
        self.vertices = []
        self.verices_amo = 8 #Указываем вершины для любой фигуры заранее (потом можно будет создавать фигуры с любым количеством вершин)
        self.cube_facesC = []
        self.screen_facesC = []
        self.cubes_to_draw = []
        self.faces_to_draw = []
        self.face_vertexesSCR = []
        self.zDepth = 0
        
    
    #Смотри - лучше обновлять матрицы и другие параметры в отдельной функции чем в draw - так и чище и расширяемее (Плюсом тестировать легче - одни каефы).
    def update(self,t):
        self.rot = (lerp(-pi, pi, (sin(t)+1)/2), lerp(-pi, pi, (sin(t+6)+1)/2), lerp(-pi, pi, (cos(t+2)+1)/2))
        self.xR = self.rot[0]
        self.yR = self.rot[1]
        self.zR = self.rot[2]
        self.matrix = rot_matrix(self.xR, self.yR, self.zR)
        
        self.vc = [ [-self.a, -self.a, -self.a],
                    [self.a, -self.a, -self.a],
                    [self.a, self.a, -self.a],
                    [-self.a, self.a, -self.a],
                    [-self.a, -self.a, self.a],
                    [self.a, -self.a, self.a],
                    [self.a, self.a, self.a],
                    [-self.a, self.a, self.a]]

        self.vertices = [[(self.vc[x][0]*self.matrix[0][0]) + (self.vc[x][1]*self.matrix[0][1]) + (self.vc[x][2]*self.matrix[0][2]) + self.xc, ((self.vc[x][0]*self.matrix[1][0]) + (self.vc[x][1]*self.matrix[1][1]) + (self.vc[x][2]*self.matrix[1][2])) + self.yc, (self.vc[x][0]*self.matrix[2][0]) + (self.vc[x][1]*self.matrix[2][1]) + (self.vc[x][2]*self.matrix[2][2]) + self.zc] for x in range(0, self.verices_amo)] #optimised   
        self.cube_facesC = [(self.vertices[0], self.vertices[1], self.vertices[2], self.vertices[3]),
                    (self.vertices[4], self.vertices[5], self.vertices[6], self.vertices[7]),
                    (self.vertices[0], self.vertices[1], self.vertices[5], self.vertices[4]),
                    (self.vertices[2], self.vertices[3], self.vertices[7], self.vertices[6]),
                    (self.vertices[0], self.vertices[3], self.vertices[7], self.vertices[4]),
                    (self.vertices[1], self.vertices[2], self.vertices[6], self.vertices[5])]

    #Твой draw - отрисовщик - не над там все матрицы переназначать если они константные   
    def draw(self):
        self.update(t)
        #Обнуляем прыдыдушие параметры (Хрен знает что это)
        self.faces_to_draw = []
        self.screen_vertices_dat = []
        self.edge_points = []
        self.screen_facesC = []
        self.face_vertexesSCR = []
        
        for i in self.vertices:
            self.Z = getZ(i, camera_pos, (0, 1, 0))
            screenXYZ = i[0] * focal_length / self.Z + hweight, i[2] * focal_length / self.Z + hheight
            self.screen_vertices_dat.append((screenXYZ[0], screenXYZ[1], self.Z))
        
        for i in self.screen_vertices_dat:
            colorvert = max(min(255, round(lerp(1, 0.2, (i[2]/zblackout)) * 255)), 0)
            pygame.draw.circle(screen, rgb_unit0_1(colorvert, False), (i[0], i[1]), 5)

        for i in self.cube_facesC:
            faceZ = getZ(((i[0][0]+i[2][0])/2, (i[0][1] + i[2][1])/2,(i[0][2] + i[2][2])/2), camera_pos, (0, 1, 0))
            distanceface = distance(camera_pos, ((i[0][0]+i[2][0])/2, (i[0][1] + i[2][1])/2,(i[0][2] + i[2][2])/2))
            facesscreenXYZ = ((i[0][0]+i[2][0])/2) * focal_length / faceZ + hweight, ((i[0][2] + i[2][2])/2) * focal_length / faceZ + hheight, distanceface
            self.screen_facesC.append((distanceface, facesscreenXYZ[0], facesscreenXYZ[1], self.cube_facesC.index(i)))
            coords = []
            for j in i:
                coords.append((j[0] * focal_length / getZ(j, camera_pos, (0, 1, 0)) + hweight, j[2] * focal_length / getZ(j, camera_pos, (0, 1, 0)) + hheight))

            self.face_vertexesSCR.append(tuple(coords))

        for i in self.vertices:
            self.edge_points.append((i[0], i[1]))

        for i in range(self.verices_amo):
            coloredge = max(min(255, round(lerp(1, 0.2, (self.screen_vertices_dat[i][2]/(zblackout+1))) * 255)), 0)
            start = (self.screen_vertices_dat[i][0], self.screen_vertices_dat[i][1])
            end = (self.screen_vertices_dat[i+1][0], self.screen_vertices_dat[i+1][1]) if i != 3 and i != 7 else (self.screen_vertices_dat[i - 3][0], self.screen_vertices_dat[i - 3][1])
            pygame.draw.line(screen, rgb_unit0_1(coloredge, False), start, end)
            
        for i in range(self.verices_amo):
            if i > 3:
                coloredge = max(min(255, round(lerp(1, 0.2, (self.screen_vertices_dat[i][2]/(zblackout+1))) * 255)), 0)
                start = (self.screen_vertices_dat[i-4][0], self.screen_vertices_dat[i-4][1])
                end = (self.screen_vertices_dat[i][0], self.screen_vertices_dat[i][1])
                pygame.draw.line(screen, rgb_unit0_1(coloredge, False), start, end)

        self.screen_facesC.sort(reverse=True)
        colors = [(255, 50, 100), (50, 255, 100), (100, 50, 255), (255, 255, 255), (80, 155, 20), (180, 10, 255)]

        for c in self.screen_facesC:
            colorface = coloredge = max(min(255, round(lerp(1, 0.2, (c[0]/(zblackout+4))) * 255)), 0)
            elem = self.face_vertexesSCR[c[3]]
            pygame.draw.polygon(screen, colors[c[3]], (elem[0], elem[1], elem[2], elem[3]))

cube = Cube(7, (8, 10, 9))      

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