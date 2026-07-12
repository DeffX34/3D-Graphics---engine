from math import sin, cos, pi, sqrt, tan, atan, atan2
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

settings_window.grid_propagate(0)

settings_window.pack(side="right", fill = "y")

xrot = 0
yrot = 0
zrot = 0

mousex = None
mousey = None 

mouse_rotation = (0, 0, 0)
is_mouse_rotation = False

def rotateshape(event):
    global mouse_rotation, xrot, yrot, zrot, mousex, mousey
    if is_mouse_rotation:
        if mousex != None:

            xrot -= clamp(event.y-mousey, -1, 1) * 50

            # yrot -= clamp(event.x-mousex, -1, 1) * 50

            zrot += clamp(event.x-mousex, -1, 1) * 50

        mousex = event.x
        mousey = event.y

        mouse_rotation = (degreeToRad(xrot), degreeToRad(yrot), degreeToRad(zrot))


enginescreen = ctk.CTkCanvas(root, width = RENDER_WIDTH, height = RENDER_HEIGHT, highlightthickness=0, bg=rgb_to_hex((40, 40, 40)))
enginescreen.bind("<Motion>", lambda event: rotateshape(event))
enginescreen.pack(side="left", fill="both", expand=1)

camera_pos = (0,0,0)
shape_pos = [0, 40, 0]

zblackout = 30
cube = Cube(8, (shape_pos), enginescreen)
sphere = Sphere(7, (shape_pos), enginescreen)
pyramide = Pyramide(10, (shape_pos), enginescreen)
cylinder = Cylinder(6,9, (shape_pos), enginescreen)

currentshape = cube

viewmodes = {"Lit" : True, "Unlit" : False, "Depth" : False, "Index of faces" : False, "Only edges" : False, "Only verteces" : False}
shapes = {"Cube" : cube, "Sphere" : sphere, "Pyramide" : pyramide, "Cylinder" : cylinder}

focal_length = ctk.DoubleVar()
focal_length_min = 150
focal_length_max = 650

scale = ctk.DoubleVar()
scale_min = 2
scale_max = 20

rotation_phase_multiplier = ctk.DoubleVar()
rotation_phase_multiplier_min = 0.1
rotation_phase_multiplier_max = 3

directional_light_pos = (30, 10, 15)

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

def rotationchange(button = ctk.CTkButton):
    global is_mouse_rotation

    if not is_mouse_rotation:
        button.configure(text="Mouse rotation: ON", fg_color = rgb_to_hex(rgb0_1(0.3, 0.5, 0.3))) 
        is_mouse_rotation = True
    else:
        is_mouse_rotation = False
        button.configure(text="Mouse rotation: OFF", fg_color = rgb_to_hex(rgb0_1(0.5, 0.3, 0.3)))

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
    ctktext.grid(row=3, column=(i*2), pady = 25, padx = 5)
    ctkentr = ctk.CTkEntry(settings_window, width=70, textvariable=entrycoord[i])
    ctkentr.grid(row=3, column=(i*2+1), pady = 25)
    ctkentr.bind("<Return>", lambda event, ax = entryaxis[i], axval = entrycoord: switchcoords(event, ax, axval))

#Focal length slidebar
focal_length_text = ctk.CTkLabel(settings_window, font=enginefont, text = "Focal length")
focal_length_text.grid(row = 4, column = 1)

focal_length_slidebar = ctk.CTkSlider(settings_window, from_=focal_length_min, to=focal_length_max, variable=focal_length)
focal_length_slidebar.set(lerp(focal_length_min, focal_length_max, 0.5))
focal_length_slidebar.grid(row = 4, column = 2, columnspan = 5)

# Shape scale slidebar
size_text = ctk.CTkLabel(settings_window, font=enginefont, text = "Shape size")
size_text.grid(row = 5, column = 1, pady = 20)

size_slidebar = ctk.CTkSlider(settings_window, from_=scale_min, to=scale_max, variable=scale)
size_slidebar.set(lerp(scale_min, scale_max, 0.5))
size_slidebar.grid(row = 5, column = 2, columnspan = 5, pady = 20)

# Rotation settings
rotation_phase_text = ctk.CTkLabel(settings_window, font=enginefont, text = "Rotation speed")
rotation_phase_text.grid(row = 6, column = 1, pady = 15)

rotation_phase_slidebar = ctk.CTkSlider(settings_window, from_=rotation_phase_multiplier_min, to=rotation_phase_multiplier_max, variable=rotation_phase_multiplier)
rotation_phase_slidebar.set(lerp(rotation_phase_multiplier_min, rotation_phase_multiplier_max, 0.2))
rotation_phase_slidebar.grid(row = 6, column = 2, columnspan = 5, pady = 15)

mouse_rotation_button = ctk.CTkButton(settings_window, text = "Mouse rotation: OFF", font = enginefont, fg_color= rgb_to_hex(rgb0_1(0.5, 0.3, 0.3)), hover_color=rgb_to_hex(rgb_unit0_1(0.5)))
mouse_rotation_button.bind("<Button-1>", lambda ev: rotationchange(mouse_rotation_button))
mouse_rotation_button.grid(row = 7, column = 1, columnspan = 7)

deltatimeinseconds = 0
deltatimebef = 0

enginescreen.grid_propagate(0)
enginescreen.grid_columnconfigure(0, weight=1)

fpstext = ctk.CTkLabel(enginescreen, text = "", bg_color="transparent", font=enginefont)
fpstext.grid(column = 1, row = 0)


def gameloop():
    global deltatimebef, deltatimeinseconds
    
    current_time = time()
    
    deltatimeinseconds = current_time - deltatimebef

    deltatimebef = current_time

    fpstext.configure(text=f"FPS: {round(1/deltatimeinseconds)}")

    t = (time() - start_time) * rotation_phase_multiplier.get()

    enginescreen.delete("mesh")

    currentshape.draw(t, camera_pos, focal_length.get(), hweight, hheight, viewmodes, zblackout, directional_light_pos, normalize(minusV(directional_light_pos, shape_pos)), scale.get(), mouse_rotation, is_mouse_rotation, deltatimeinseconds)

    print(deltatimeinseconds)

    root.after(deltatime, gameloop)


enginescreen.configure(bg = rgb_to_hex((rgb0_1(0.68, 0.85, 0.90, 0)), 1))
gameloop()
root.mainloop()