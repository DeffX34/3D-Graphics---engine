from math import sin, cos, pi, sqrt, tan, atan
from time import sleep, time
import sys
from math_functions import *
import os
from matrices import rot_matrix
import customtkinter as ctk
from files import *
import numpy as np

WIDTH = 1920
HEIGHT = 1080

settings_width = 400

RENDER_WIDTH = WIDTH-settings_width 
RENDER_HEIGHT = HEIGHT
hweight = RENDER_WIDTH/2
hheight = RENDER_HEIGHT/2

load_font("Rajdhani-Medium.ttf")

enginefont = ("Rajdhani", 20)

asp_ratio = RENDER_WIDTH/RENDER_HEIGHT

FPS = 144
deltatime = round(1000 / FPS)
print(deltatime)
focal_length = 300
zblackout = 2
start_time = time()
t = 0

camera_pos = (0,0,0)
shape_pos = [0, 0, 0]

class Cube:
    def __init__(self, a, pos, screen):
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
        self.drawscreen = screen
        
    def set_pos(self, newpos):
        self.pos = newpos
        self.xc = self.pos[0]
        self.yc = self.pos[1]
        self.zc = self.pos[2]

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
    def draw(self, t):
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
            colorvert = round(max(min(255, lerp(0, 40, i[2]/zblackout)), 0))
            enginescreen.create_aa_circle(i[0], i[1], 5, fill=rgb_to_hex((1, 1, 1), 0))

        for i in self.cube_facesC:
            faceZ = getZ(((i[0][0]+i[2][0])/2, (i[0][1] + i[2][1])/2,(i[0][2] + i[2][2])/2), camera_pos, (0, 1, 0))
            distanceface = optimisedDistance(camera_pos, ((i[0][0]+i[2][0])/2, (i[0][1] + i[2][1])/2,(i[0][2] + i[2][2])/2))
            facesscreenXYZ = ((i[0][0]+i[2][0])/2) * focal_length / faceZ + hweight, ((i[0][2] + i[2][2])/2) * focal_length / faceZ + hheight, distanceface
            self.screen_facesC.append((distanceface, facesscreenXYZ[0], facesscreenXYZ[1], self.cube_facesC.index(i)))
            coords = []
            for j in i:
                coords.append((j[0] * focal_length / getZ(j, camera_pos, (0, 1, 0)) + hweight, j[2] * focal_length / getZ(j, camera_pos, (0, 1, 0)) + hheight))

            self.face_vertexesSCR.append(tuple(coords))

        for i in self.vertices:
            self.edge_points.append((i[0], i[1]))

        for i in range(self.verices_amo):
            start = (self.screen_vertices_dat[i][0], self.screen_vertices_dat[i][1])
            end = (self.screen_vertices_dat[i+1][0], self.screen_vertices_dat[i+1][1]) if i != 3 and i != 7 else (self.screen_vertices_dat[i - 3][0], self.screen_vertices_dat[i - 3][1])
            enginescreen.create_line(start[0], start[1], end[0], end[1], fill = rgb_to_hex((1, 1, 1)))
            
        for i in range(self.verices_amo):
            if i > 3:
                start = (self.screen_vertices_dat[i-4][0], self.screen_vertices_dat[i-4][1])
                end = (self.screen_vertices_dat[i][0], self.screen_vertices_dat[i][1])
                enginescreen.create_line(start[0], start[1], end[0], end[1], fill = rgb_to_hex((1, 1, 1)))

        self.screen_facesC.sort(reverse=True)
        colors = [(255, 50, 100), (50, 255, 100), (100, 50, 255), (255, 255, 255), (80, 155, 20), (180, 10, 255)]

        for c in self.screen_facesC:
            elem = self.face_vertexesSCR[c[3]]
            enginescreen.create_polygon(elem[0], elem[1], elem[2], elem[3], fill = rgb_to_hex(colors[c[3]], 1))






r = 100
root = ctk.CTk()
root.title("3D---engine")
root.resizable(0, 0)
root.geometry(f"{WIDTH}x{HEIGHT}")
root.attributes("-topmost", 1)
settings_window = ctk.CTkFrame(root, bg_color=rgb_to_hex((140, 140, 140)), width=settings_width, corner_radius=0)

settings_window.grid_rowconfigure(0, weight=0)
settings_window.grid_rowconfigure(7, weight=1)
settings_window.grid_columnconfigure(0, weight=1)
settings_window.grid_columnconfigure(4, weight=1)
settings_window.grid_propagate(0)

settings_window.pack(side="right", fill = "y")
enginescreen = ctk.CTkCanvas(root, width = WIDTH, height = HEIGHT, highlightthickness=0, bg=rgb_to_hex((40, 40, 40)))
enginescreen.pack(expand=1, fill="both")
cube = Cube(7, (shape_pos), enginescreen)


def switchmodel(choice):
    print(choice)

def switchviewmode(choice):
    print(choice)

def switchcoords(event, axis, value):
    
    for i in value:
        axisvalue = str(value[value.index(i)].get())
        if axisvalue.lstrip("-").replace(".", "", 1).isdigit() and " " not in axisvalue:
            shape_pos[value.index(i)] = float(axisvalue)
            cube.set_pos(shape_pos)

    print(shape_pos)

#Shape choice UI
modelchoicetext = ctk.CTkLabel(settings_window, text = "Shape: ", font=enginefont)

modelchoicetext.grid(column = 1, row = 1, pady = 50)

modelchoicemenu = ctk.CTkOptionMenu(settings_window, values=["Cube", "Pyramide", "Cylinder", "Sphere"], command=switchmodel, 
                                    fg_color=rgb_to_hex((80,80,80), 1), 
                                    button_color=rgb_to_hex((130,130,130), 1), 
                                    button_hover_color=rgb_to_hex((170,170,170), 1),
                                    width=250, height=50,
                                    font=enginefont, dropdown_font=enginefont)

modelchoicemenu.grid(row=1, column = 2, columnspan = 2, pady = 50)

# View mode choice UI
modelviewmodetext = ctk.CTkLabel(settings_window, text = "View mode: ", font=enginefont)

modelviewmodetext.grid(column = 1, row = 2)

modelviewmodemenu = ctk.CTkOptionMenu(settings_window, values=["lit", "unlit", "edges", "vertex"], command=switchviewmode, 
                                    fg_color=rgb_to_hex((80,80,80), 1), 
                                    button_color=rgb_to_hex((130,130,130), 1), 
                                    button_hover_color=rgb_to_hex((170,170,170), 1),
                                    width=250, height=50,
                                    font=enginefont, dropdown_font=enginefont)

modelviewmodemenu.grid(row=2, column = 2)

# Coordinates UI
entryaxis = ["X:", "Y:", "Z:"]
xve, yve, zve = ctk.StringVar(), ctk.StringVar(), ctk.StringVar()
entrycoord = [xve, yve, zve]

for i in range(3):
    for j in range(2):
        ctktext = ctk.CTkLabel(settings_window, text=entryaxis[i], font=enginefont)
        ctktext.grid(row=3+i, column=1, pady = 25)
        ctkentr = ctk.CTkEntry(settings_window, width=40, textvariable=entrycoord[i])
        ctkentr.grid(row=3+i, column=2, pady = 25, sticky = "w")

        ctkentr.bind("<Return>", lambda event, ax = entryaxis[i], axval = entrycoord: switchcoords(event, ax, axval))




def gameloop():
    t = (time() - start_time) * 0.5
    enginescreen.delete("all")
    cube.draw(t)
    enginescreen.configure(bg = rgb_to_hex((rgb0_1(0.68, 0.85, 0.90, 0)), 1))

    root.after(deltatime, gameloop)

gameloop()
root.mainloop()