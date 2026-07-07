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

clock = pygame.time.Clock()
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
        self.verices_amo = 8 #Указываем вершины для любой фигуры заранее (потом можно будет создавать фигуры с любым количеством вершин)
        self.cube_facesC = []
        self.screen_facesC = []
        self.cubes_to_draw = []
        self.faces_to_draw = []
        self.face_vertexesSCR = []
        
    
    #Смотри - лучше обновлять матрицы и другие параметры в отдельной функции чем в draw - так и чище и расширяемее (Плюсом тестировать легче - одни каефы).
    def update(self,t):
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

        self.vertices = [[(self.vc[x][0]*self.matrix[0][0]) + (self.vc[x][1]*self.matrix[0][1]) + (self.vc[x][2]*self.matrix[0][2]), ((self.vc[x][0]*self.matrix[1][0]) + (self.vc[x][1]*self.matrix[1][1]) + (self.vc[x][2]*self.matrix[1][2])), (self.vc[x][0]*self.matrix[2][0]) + (self.vc[x][1]*self.matrix[2][1]) + (self.vc[x][2]*self.matrix[2][2])] for x in range(0, self.verices_amo)] #optimised   
        self.cube_facesC = [(self.vertices[0], self.vertices[1], self.vertices[2], self.vertices[3]),
                    (self.vertices[4], self.vertices[5], self.vertices[6], self.vertices[7]),
                    (self.vertices[0], self.vertices[1], self.vertices[5], self.vertices[4]),
                    (self.vertices[2], self.vertices[3], self.vertices[7], self.vertices[6]),
                    (self.vertices[0], self.vertices[3], self.vertices[7], self.vertices[4]),
                    (self.vertices[1], self.vertices[2], self.vertices[6], self.vertices[5])]

    #Твой draw - отрисовщик - не над там все матрицы переназначать если они константные   
    def draw(self):
        #Обнуляем прыдыдушие параметры (Хрен знает что это)
        self.faces_to_draw = []
        self.screen_vertices_dat = []
        self.edge_points = []
        self.screen_facesC = []
        self.face_vertexesSCR = []
        
        for i in self.vertices:
            screenXYZ = i[0] * focal_length / distance(0,camera_pos[1],0,0,i[1],0, True, "y") + hweight, i[2] * focal_length / distance(0,camera_pos[1],0,0,i[1],0, True, "y") + hheight
            self.screen_vertices_dat.append((screenXYZ[0], screenXYZ[1], distance(0,camera_pos[1],0,0,i[1],0, True, "y"), i[1]))
            

        for i in self.cube_facesC:
            faceZ = distance(0,camera_pos[1],0,0,(i[0][1]+i[2][1])/2,0, True, "y")
            facesscreenXYZ = ((i[0][0]+i[2][0])/2) * focal_length / faceZ + hweight, ((i[0][2] + i[2][2])/2) * focal_length / faceZ + hheight, faceZ
            self.screen_facesC.append((faceZ, facesscreenXYZ[0], facesscreenXYZ[1], self.cube_facesC.index(i)))
            coords = []
            for j in i:
                coords.append(((j[0]) * focal_length / distance(0,camera_pos[1],0,0,j[1],0, True, "y") + hweight, (j[2]) * focal_length / distance(0,camera_pos[1],0,0,j[1],0, True, "y") + hheight))

            self.face_vertexesSCR.append(tuple(coords))

        for i in self.vertices:
            self.edge_points.append((i[0], i[1]))

        for i in self.screen_vertices_dat:
            colorvert = max(min(255, round(lerp(1, 0.2, (i[3]/yblackout)) * 255)), 0)
            pygame.draw.circle(screen, rgb_unit0_1(colorvert, False), (i[0], i[1]), 5)

        for i in range(self.verices_amo):
            coloredge = max(min(255, round(lerp(1, 0.2, (self.screen_vertices_dat[i][3]/(yblackout+1))) * 255)), 0)
            start = (self.screen_vertices_dat[i][0], self.screen_vertices_dat[i][1])
            end = (self.screen_vertices_dat[i+1][0], self.screen_vertices_dat[i+1][1]) if i != 3 and i != 7 else (self.screen_vertices_dat[i - 3][0], self.screen_vertices_dat[i - 3][1])
            pygame.draw.line(screen, rgb_unit0_1(coloredge, False), start, end)
            
        for i in range(self.verices_amo):
            if i > 3:
                coloredge = max(min(255, round(lerp(1, 0.2, (self.screen_vertices_dat[i][3]/(yblackout+1))) * 255)), 0)
                start = (self.screen_vertices_dat[i-4][0], self.screen_vertices_dat[i-4][1])
                end = (self.screen_vertices_dat[i][0], self.screen_vertices_dat[i][1])
                pygame.draw.line(screen, rgb_unit0_1(coloredge, False), start, end)
    
        self.screen_facesC.sort(reverse=True)
        for c in self.screen_facesC:
            colorface = coloredge = max(min(255, round(lerp(1, 0.2, (c[0]/(yblackout+4))) * 255)), 0)
            elem = self.face_vertexesSCR[c[3]]
            pygame.draw.polygon(screen, rgb_unit0_1(colorface, False), (elem[0], elem[1], elem[2], elem[3]))

cube = Cube(7, (0, 0, 0))        

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
    cube.update(t) #Каждый раз просчитываем новые параметры матриц уже в функции
    cube.draw()
    pygame.display.flip()
    os.system("cls")
else:
    pygame.quit()
    sys.exit()