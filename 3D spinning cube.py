from math import sin, cos, pi, sqrt, tan, atan
from time import sleep, time
import sys
from math_functions import *
import os
from matrices import rot_matrix
import customtkinter as ctk
from files import *
import numpy as np
from geometry import *

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
shape_pos = [0, 20, 0]

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
sphere = Sphere(7, (shape_pos), enginescreen)

currentshape = sphere

shapes = {"Cube":cube, "Sphere":sphere}

def switchmodel(choice):
    global currentshape
    global shapes
    currentshape = shapes[choice]
    currentshape.set_pos(shape_pos)

def switchviewmode(choice):
    print(choice)

def switchcoords(event, axis, value):
    for i in value:
        axisvalue = str(value[value.index(i)].get())
        if axisvalue.lstrip("-").replace(".", "", 1).isdigit() and " " not in axisvalue:
            shape_pos[value.index(i)] = float(axisvalue)
            currentshape.set_pos(shape_pos)

    print(shape_pos)

#Shape choice UI
modelchoicetext = ctk.CTkLabel(settings_window, text = "Shape: ", font=enginefont)

modelchoicetext.grid(column = 1, row = 1, pady = 50)

modelchoicemenu = ctk.CTkOptionMenu(settings_window, values=["Sphere", "Pyramide", "Cylinder", "Cube"], command=switchmodel, 
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
        ctktext.grid(row=4+i, column=1, pady = 25)
        ctkentr = ctk.CTkEntry(settings_window, width=40, textvariable=entrycoord[i])
        ctkentr.grid(row=4+i, column=2, pady = 25, sticky = "w")
        ctkentr.bind("<Return>", lambda event, ax = entryaxis[i], axval = entrycoord: switchcoords(event, ax, axval))

def gameloop():
    t = (time() - start_time) * 0.5
    enginescreen.delete("all")
    currentshape.draw(t, camera_pos, focal_length, hweight, hheight)
    root.after(deltatime, gameloop)

enginescreen.configure(bg = rgb_to_hex((rgb0_1(0.68, 0.85, 0.90, 0)), 1))
gameloop()
root.mainloop()