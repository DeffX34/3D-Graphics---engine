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
zblackout = 2
start_time = time()
t = 0



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
settings_window.grid_columnconfigure(7, weight=1)
settings_window.grid_propagate(0)

settings_window.pack(side="right", fill = "y")
enginescreen = ctk.CTkCanvas(root, width = WIDTH, height = HEIGHT, highlightthickness=0, bg=rgb_to_hex((40, 40, 40)))
enginescreen.pack(expand=1, fill="both")

camera_pos = (0,0,0)
shape_pos = [0, 25, 0]

zblackout = 30
cube = Cube(8, (shape_pos), enginescreen)
sphere = Sphere(7, (shape_pos), enginescreen)
pyramide = Pyramide(10, (shape_pos), enginescreen)
cylinder = Cylinder(6,9, (shape_pos), enginescreen)

currentshape = cube

viewmodes = {"Lit" : True, "Unlit" : False, "Depth" : False, "Index of faces" : False, "Only edges" : False, "Only verteces" : False}
shapes = {"Cube" : cube, "Sphere" : sphere, "Pyramide" : pyramide, "Cylinder" : cylinder}

focal_length = ctk.IntVar()
focal_length_min = 150
focal_length_max = 650

directional_light_pos = (30, 10, 15)
normalized_light_dir = normalize(minusV(shape_pos, directional_light_pos))

def switchmodel(choice):
    global currentshape
    global shapes
    currentshape = shapes[choice]
    currentshape.settings_apply(shape_pos)

def switchviewmode(choice):
    for i in list(viewmodes):
        viewmodes[i] = False

    viewmodes[choice] = True

def switchcoords(event, axis, value):
    for i in value:
        axisvalue = str(value[value.index(i)].get())
        if axisvalue.lstrip("-").replace(".", "", 1).isdigit() and " " not in axisvalue:
            shape_pos[value.index(i)] = float(axisvalue)
            currentshape.settings_apply(shape_pos)

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

modelchoicemenu.grid(row=1, column = 2, columnspan = 5, pady = 50)

# View mode choice UI
modelviewmodetext = ctk.CTkLabel(settings_window, text = "View mode: ", font=enginefont)

modelviewmodetext.grid(column = 1, row = 2)



modelviewmodemenu = ctk.CTkOptionMenu(settings_window, values=list(viewmodes), command=switchviewmode, 
                                    fg_color=rgb_to_hex((80,80,80), 1), 
                                    button_color=rgb_to_hex((130,130,130), 1), 
                                    button_hover_color=rgb_to_hex((170,170,170), 1),
                                    width=250, height=50,
                                    font=enginefont, dropdown_font=enginefont)

modelviewmodemenu.grid(row=2, column = 2, columnspan = 5)

# Coordinates UI
entryaxis = ["X:", "Y:", "Z:"]
xve, yve, zve = ctk.StringVar(), ctk.StringVar(), ctk.StringVar()
entrycoord = [xve, yve, zve]

for i in range(3):
    ctktext = ctk.CTkLabel(settings_window, text=entryaxis[i], font=enginefont)
    ctktext.grid(row=3, column=(i+1)+i, pady = 25)
    ctkentr = ctk.CTkEntry(settings_window, width=10, textvariable=entrycoord[i])
    ctkentr.grid(row=3, column=(i+2)+i, pady = 25, sticky = "w")
    ctkentr.bind("<Return>", lambda event, ax = entryaxis[i], axval = entrycoord: switchcoords(event, ax, axval))

#Focal length slidebar
focal_length_slidebar = ctk.CTkSlider(settings_window, from_=focal_length_min, to=focal_length_max, variable=focal_length)
focal_length_slidebar.set(lerp(focal_length_min, focal_length_max, 0.5))
focal_length_slidebar.grid(row = 4, column = 2, columnspan = 5)

def gameloop():
    t = (time() - start_time) * 0.5
    enginescreen.delete("all")
    currentshape.draw(t, camera_pos, focal_length.get(), hweight, hheight, viewmodes, zblackout, directional_light_pos, normalized_light_dir)
    root.after(deltatime, gameloop)


enginescreen.configure(bg = rgb_to_hex((rgb0_1(0.68, 0.85, 0.90, 0)), 1))
gameloop()
root.mainloop()