import pyglet as pg
import os

def load_font(file_name):
    if os.path.exists(file_name):
        try:
            pg.font.add_file(file_name)
        except Exception as e:
            print(e)
            return None
    else:
        return None