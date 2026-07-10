from math import sin, cos, pi
from matrices import rot_matrix
from math_functions import *
import customtkinter as ctk

class Cube:
    def __init__(self, a, pos, screen):
        self.a = a / 2
        self.pos = pos
        self.rot = (0, 0, 0)
        self.xc = self.pos[0]
        self.yc = self.pos[1]
        self.zc = self.pos[2]
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
        self.zDepth = 0
        self.drawscreen = screen

        
    def set_pos(self, newpos):
        self.pos = newpos
        self.xc = self.pos[0]
        self.yc = self.pos[1]
        self.zc = self.pos[2]

    #Смотри - лучше обновлять матрицы и другие параметры в отдельной функции чем в draw - так и чище и расширяемее (Плюсом тестировать легче - одни каефы).
    def update(self,t):
        self.rot = (((sin(t)+1)/2)*360, ((cos(t+6)+1)/2)*360, ((cos(t+2)+1)/2)*360)
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
    def draw(self, t, camera_pos, focal_length, hweight, hheight):
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
            self.drawscreen.create_aa_circle(i[0], i[1], 5, fill=rgb_to_hex((1, 1, 1), 0))

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
            self.drawscreen.create_line(start[0], start[1], end[0], end[1], fill = rgb_to_hex((1, 1, 1)))
            
        for i in range(self.verices_amo):
            if i > 3:
                start = (self.screen_vertices_dat[i-4][0], self.screen_vertices_dat[i-4][1])
                end = (self.screen_vertices_dat[i][0], self.screen_vertices_dat[i][1])
                self.drawscreen.create_line(start[0], start[1], end[0], end[1], fill = rgb_to_hex((1, 1, 1)))

        self.screen_facesC.sort(reverse=True)
        colors = [(255, 50, 100), (50, 255, 100), (100, 50, 255), (255, 255, 255), (80, 155, 20), (180, 10, 255)]

        for c in self.screen_facesC:
            elem = self.face_vertexesSCR[c[3]]
            self.drawscreen.create_polygon(elem[0], elem[1], elem[2], elem[3], fill = rgb_to_hex(colors[c[3]], 1))


class Sphere:
    def __init__(self, r, pos, screen = ctk.CTkCanvas):
        self.pos = pos
        self.r = r
        self.rot = (0, 0, 0)
        self.xc = self.pos[0]
        self.yc = self.pos[1]
        self.zc = self.pos[2]
        self.xR = self.rot[0]
        self.yR = self.rot[1]
        self.zR = self.rot[2]
        self .matrix = []
        self.vc = []
        self.screen_vertices_dat = []
        self.edge_points = []
        self.vertices = []
        self.verices_amo = 8 #Указываем вершины для любой фигуры заранее (потом можно будет создавать фигуры с любым количеством вершин)
        self.sphere_facesC = []
        self.screen_facesC = []
        self.screen_verticesC = []
        self.faces_to_draw = []
        self.face_vertexesSCR = []
        self.zDepth = 0
        self.drawscreen = screen
        self.detalization = 10
        
    def set_pos(self, newpos):
        self.pos = newpos
        self.xc = self.pos[0]
        self.yc = self.pos[1]
        self.zc = self.pos[2]

    #Смотри - лучше обновлять матрицы и другие параметры в отдельной функции чем в draw - так и чище и расширяемее (Плюсом тестировать легче - одни каефы).
    def update(self,t):
        self.rot = (((sin(t)+1)/2)*360, ((cos(t+6)+1)/2)*360, ((cos(t+2)+1)/2)*360)
        self.xR = self.rot[0]
        self.yR = self.rot[1]
        self.zR = self.rot[2]
        self.matrix = rot_matrix(self.xR, self.yR, self.zR)
        
        self.vc = []
        for i in range(0, self.detalization):
            phi = degreeToRad((i / self.detalization) * 360)
            for j in range(0, self.detalization):
                tetha = degreeToRad((j / (self.detalization-1)) * 180)
                x = self.r * sin(tetha) * cos(phi)
                y = self.r * cos(tetha)
                z = self.r * sin(tetha) * sin(phi)
                self.vc.append([x, y, z])

        self.vertices = [[(self.vc[x][0]*self.matrix[0][0]) + (self.vc[x][1]*self.matrix[0][1]) + (self.vc[x][2]*self.matrix[0][2]) + self.xc, ((self.vc[x][0]*self.matrix[1][0]) + (self.vc[x][1]*self.matrix[1][1]) + (self.vc[x][2]*self.matrix[1][2])) + self.yc, (self.vc[x][0]*self.matrix[2][0]) + (self.vc[x][1]*self.matrix[2][1]) + (self.vc[x][2]*self.matrix[2][2]) + self.zc] for x in range(0, len(self.vc))] #optimised   
        self.sphere_facesC = []

    #Твой draw - отрисовщик - не над там все матрицы переназначать если они константные   
    def draw(self, t, camera_pos, focal_length, hweight, hheight):
        self.update(t)
        #Обнуляем прыдыдушие параметры (Хрен знает что это)
        self.faces_to_draw = []
        self.screen_vertices_dat = []
        self.edge_points = []
        self.screen_facesC = []
        self.screen_verticesC = []

        self.face_vertexesSCR = []
        oldverts = []

        for i in self.vertices:
            self.Z = getZ(i, camera_pos, (0, 1, 0))
            screenXYZ = i[0] * focal_length / self.Z + hweight, i[2] * focal_length / self.Z + hheight
            self.screen_vertices_dat.append((screenXYZ[0], screenXYZ[1], self.Z))
            self.screen_verticesC.append((screenXYZ[0], screenXYZ[1]))

        # for i in self.screen_vertices_dat:
        #     self.drawscreen.create_aa_circle(i[0], i[1], 5, fill=rgb_to_hex((1, 1, 1), 0))

        for i in range(0, self.detalization):  
            # Horizontal edges (Tetha)
            for tethaC in range(0, self.detalization):

                oldcoordPhi01 = self.screen_verticesC[tethaC + i * self.detalization]
                newcoordPhi01 = self.screen_verticesC[tethaC + (i+1) * self.detalization] if i != self.detalization-1 else self.screen_verticesC[tethaC]

                self.drawscreen.create_line(oldcoordPhi01[0], oldcoordPhi01[1], newcoordPhi01[0], newcoordPhi01[1], fill=rgb_to_hex((1,1,1)))

            # Vertical edges (Phi)
            for phiC in range(0, self.detalization):
                oldcoordTheta01 = self.screen_verticesC[i + phiC * self.detalization]
                newcoordTheta01 = self.screen_verticesC[(i+1) + phiC * self.detalization] if i != self.detalization-1 else self.screen_verticesC[i]
                self.drawscreen.create_line(oldcoordTheta01[0], oldcoordTheta01[1], newcoordTheta01[0], newcoordTheta01[1], fill=rgb_to_hex((1,1,1)))


                oldcoordTheta02 = self.screen_verticesC[(i + phiC * self.detalization) - self.detalization]
                newcoordTheta02 = self.screen_verticesC[((i+1) + phiC * self.detalization) - self.detalization]
                self.sphere_facesC.append((self.vertices[self.screen_verticesC.index(oldcoordTheta01)], self.vertices[self.screen_verticesC.index(newcoordTheta01)], self.vertices[self.screen_verticesC.index(newcoordTheta02)], self.vertices[self.screen_verticesC.index(oldcoordTheta02)]))


        for i in self.sphere_facesC:
            centercoord = (i[0][0]+i[2][0])/2, (i[0][1] + i[2][1])/2,(i[0][2] + i[2][2])/2
            faceZ = getZ(centercoord, camera_pos, (0, 1, 0))
            distanceface = optimisedDistance(camera_pos, centercoord)
            facesscreenXYZ = centercoord[0] * focal_length / faceZ + hweight, centercoord[2] * focal_length / faceZ + hheight, distanceface
            self.faces_to_draw.append((distanceface, facesscreenXYZ[0], facesscreenXYZ[1], self.sphere_facesC.index(i), faceZ))
            coords = []
            for j in i:
                coords.append((j[0] * focal_length / getZ(j, camera_pos, (0, 1, 0)) + hweight, j[2] * focal_length / getZ(j, camera_pos, (0, 1, 0)) + hheight))

            self.face_vertexesSCR.append(tuple(coords))

        self.faces_to_draw.sort(reverse=True)

        for c in self.faces_to_draw:
            elem = self.face_vertexesSCR[c[3]]
            self.drawscreen.create_polygon(elem, fill = rgb_to_hex((round(abs(sin(c[3]))*255), round(abs(cos(c[3])*255)), round(abs(sin(c[3]+4)*255))), 1))

class Pyramide:
    def __init__(self, a, pos, screen):
        self.a = a / 2
        self.pos = pos
        self.rot = (0, 0, 0)
        self.xc = self.pos[0]
        self.yc = self.pos[1]
        self.zc = self.pos[2]
        self.xR = self.rot[0]
        self.yR = self.rot[1]
        self.zR = self.rot[2]
        self .matrix = []
        self.vc = []
        self.screen_vertices_dat = []
        self.edge_points = []
        self.vertices = []
        self.verices_amo = 5
        self.pyramide_facesC = []
        self.screen_facesC = []
        self.faces_to_draw = []
        self.zDepth = 0
        self.drawscreen = screen
        
    def set_pos(self, newpos):
        self.pos = newpos
        self.xc = self.pos[0]
        self.yc = self.pos[1]
        self.zc = self.pos[2]

    #Смотри - лучше обновлять матрицы и другие параметры в отдельной функции чем в draw - так и чище и расширяемее (Плюсом тестировать легче - одни каефы).
    def update(self,t):
        self.rot = (((sin(t)+1)/2)*360, ((cos(t+6)+1)/2)*360, ((cos(t+2)+1)/2)*360)
        self.xR = self.rot[0]
        self.yR = self.rot[1]
        self.zR = self.rot[2]
        self.matrix = rot_matrix(self.xR, self.yR, self.zR)
        
        self.vc = [ [-self.a, -self.a, -self.a],
                    [self.a, -self.a, -self.a],
                    [self.a, self.a, -self.a],
                    [-self.a, self.a, -self.a],
                    [0, 0, self.a]]

        self.vertices = [[(self.vc[x][0]*self.matrix[0][0]) + (self.vc[x][1]*self.matrix[0][1]) + (self.vc[x][2]*self.matrix[0][2]) + self.xc, ((self.vc[x][0]*self.matrix[1][0]) + (self.vc[x][1]*self.matrix[1][1]) + (self.vc[x][2]*self.matrix[1][2])) + self.yc, (self.vc[x][0]*self.matrix[2][0]) + (self.vc[x][1]*self.matrix[2][1]) + (self.vc[x][2]*self.matrix[2][2]) + self.zc] for x in range(0, self.verices_amo)] #optimised   
        self.pyramide_facesC = [(self.vertices[0], self.vertices[1], self.vertices[2], self.vertices[3]),
                            (self.vertices[4], self.vertices[0], self.vertices[1]),
                            (self.vertices[4], self.vertices[1], self.vertices[2]),
                            (self.vertices[4], self.vertices[2], self.vertices[3]),
                            (self.vertices[4], self.vertices[3], self.vertices[0]),]

    #Твой draw - отрисовщик - не над там все матрицы переназначать если они константные   
    def draw(self, t, camera_pos, focal_length, hweight, hheight):
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
            self.drawscreen.create_aa_circle(i[0], i[1], 5, fill=rgb_to_hex((1, 1, 1), 0))

        for i in self.pyramide_facesC:
            centercoord = ((i[0][0]+i[2][0])/2, (i[0][1] + i[2][1])/2, (i[0][2] + i[2][2])/2) if self.pyramide_facesC.index(i) < 1 else lerpV(lerpV(i[1], i[2], 0.5), (i[0]), 0.5)
            faceZ = getZ(centercoord, camera_pos, (0, 1, 0))
            distanceface = optimisedDistance(camera_pos, (centercoord))
            facesscreenXYZ = ((i[0][0]+i[2][0])/2) * focal_length / faceZ + hweight, ((i[0][2] + i[2][2])/2) * focal_length / faceZ + hheight, distanceface
            self.screen_facesC.append((distanceface, facesscreenXYZ[0], facesscreenXYZ[1], self.pyramide_facesC.index(i)))
            coords = []
            for j in i:
                coords.append((j[0] * focal_length / getZ(j, camera_pos, (0, 1, 0)) + hweight, j[2] * focal_length / getZ(j, camera_pos, (0, 1, 0)) + hheight))

            self.face_vertexesSCR.append(tuple(coords))

        for i in self.vertices:
            self.edge_points.append((i[0], i[1]))

        for i in range(self.verices_amo):
            if i != 4:
                start = (self.screen_vertices_dat[i][0], self.screen_vertices_dat[i][1])
                end = (self.screen_vertices_dat[i+1][0], self.screen_vertices_dat[i+1][1]) if i != 3 else (self.screen_vertices_dat[0][0], self.screen_vertices_dat[0][1])
                self.drawscreen.create_line(start[0], start[1], end[0], end[1], fill = rgb_to_hex((1, 1, 1)))
            else:
                for j in self.vertices:
                    self.drawscreen.create_line(j[0], j[1], self.vertices[4][0], self.vertices[4][1], fill = rgb_to_hex((1, 1, 1)))

        self.screen_facesC.sort(reverse=True)
        colors = [(255, 50, 100), (50, 255, 100), (100, 50, 255), (255, 255, 255), (80, 155, 20), (180, 10, 255)]

        for c in self.screen_facesC:
            elem = self.face_vertexesSCR[c[3]]
            self.drawscreen.create_polygon(elem, fill = rgb_to_hex(colors[c[3]], 1))



class Cylinder:
    def __init__(self, width, height, pos, screen = ctk.CTkCanvas):
        self.pos = pos
        self.width = width
        self.height = height
        self.rot = (0, 0, 0)
        self.xc = self.pos[0]
        self.yc = self.pos[1]
        self.zc = self.pos[2]
        self.xR = self.rot[0]
        self.yR = self.rot[1]
        self.zR = self.rot[2]
        self .matrix = []
        self.vc = []
        self.screen_vertices_dat = []
        self.edge_points = []
        self.vertices = []
        self.verices_amo = 8 #Указываем вершины для любой фигуры заранее (потом можно будет создавать фигуры с любым количеством вершин)
        self.cylinder_facesC = []
        self.screen_facesC = []
        self.screen_verticesC = []
        self.faces_to_draw = []
        self.face_vertexesSCR = []
        self.zDepth = 0
        self.drawscreen = screen
        self.detalization = 10
        
    def set_pos(self, newpos):
        self.pos = newpos
        self.xc = self.pos[0]
        self.yc = self.pos[1]
        self.zc = self.pos[2]

    #Смотри - лучше обновлять матрицы и другие параметры в отдельной функции чем в draw - так и чище и расширяемее (Плюсом тестировать легче - одни каефы).
    def update(self,t):
        self.rot = (((sin(t)+1)/2)*360, ((cos(t+6)+1)/2)*360, ((cos(t+2)+1)/2)*360)
        self.xR = self.rot[0]
        self.yR = self.rot[1]
        self.zR = self.rot[2]
        self.matrix = rot_matrix(self.xR, self.yR, self.zR)
        self.vc = []

        for i in range(2):
            for j in range(0, self.detalization):
                tetha = degreeToRad((j / (self.detalization)) * 360)
                x = self.width * sin(tetha)
                y = self.width * cos(tetha)
                z = self.height - self.height*2*i
                self.vc.append([x, y, z])

        for i in range(2):
            self.vc.append([0, 0, self.height - self.height*2*i])


        self.vertices = [[(self.vc[x][0]*self.matrix[0][0]) + (self.vc[x][1]*self.matrix[0][1]) + (self.vc[x][2]*self.matrix[0][2]) + self.xc, ((self.vc[x][0]*self.matrix[1][0]) + (self.vc[x][1]*self.matrix[1][1]) + (self.vc[x][2]*self.matrix[1][2])) + self.yc, (self.vc[x][0]*self.matrix[2][0]) + (self.vc[x][1]*self.matrix[2][1]) + (self.vc[x][2]*self.matrix[2][2]) + self.zc] for x in range(0, len(self.vc))] #optimised   
        self.cylinder_facesC = []

    #Твой draw - отрисовщик - не над там все матрицы переназначать если они константные   
    def draw(self, t, camera_pos, focal_length, hweight, hheight):
        self.update(t)
        #Обнуляем прыдыдушие параметры (Хрен знает что это)
        self.faces_to_draw = []
        self.screen_vertices_dat = []
        self.edge_points = []
        self.screen_facesC = []
        self.screen_verticesC = []
        otherverteces = []
        self.face_vertexesSCR = []
        top_bottom_faces = []

        for i in self.vertices:
            if self.vertices.index(i) < self.detalization*2:
                self.Z = getZ(i, camera_pos, (0, 1, 0))
                screenXYZ = i[0] * focal_length / self.Z + hweight, i[2] * focal_length / self.Z + hheight
                self.screen_vertices_dat.append((screenXYZ[0], screenXYZ[1], self.Z))
                self.screen_verticesC.append((screenXYZ[0], screenXYZ[1]))

        for i in self.screen_vertices_dat:
            self.drawscreen.create_aa_circle(i[0], i[1], 5, fill=rgb_to_hex((1, 1, 1), 0))

        
        for i in range(2):  
            for j in range(0, self.detalization+1):

                oldcoord = self.screen_verticesC[(j-1) + i * self.detalization if j != 0 else i * self.detalization]
                newcoord = self.screen_verticesC[j + i * self.detalization] if j != self.detalization else self.screen_verticesC[0 + i * self.detalization]

                self.drawscreen.create_line(oldcoord[0], oldcoord[1], newcoord[0], newcoord[1], fill=rgb_to_hex((1,1,1)))


            for l in range(0, self.detalization+1):
                if l != self.detalization:
                    otherverteces.append(self.vertices[l + i * self.detalization])
                if i > 0:
                    oldcoordF02 = self.screen_verticesC[l] if l != self.detalization else self.screen_verticesC[0]
                    newcoordF02 = self.screen_verticesC[l + self.detalization] if l != self.detalization else self.screen_verticesC[self.detalization]
                    
                    self.drawscreen.create_line(oldcoordF02[0], oldcoordF02[1], newcoordF02[0], newcoordF02[1], fill=rgb_to_hex((1,1,1)))

                    if l > 0:
                        self.cylinder_facesC.append((self.vertices[l-1], self.vertices[l if l != self.detalization else 0], self.vertices[(l + self.detalization) if l != self.detalization else self.detalization], self.vertices[l + self.detalization - 1]))


            top_bottom_faces.append(otherverteces)
            otherverteces = []



        for i in self.cylinder_facesC: 

            centercoord = (i[0][0]+i[2][0])/2, (i[0][1] + i[2][1])/2, (i[0][2] + i[2][2])/2

            faceZ = getZ(centercoord, camera_pos, (0, 1, 0))
            distanceface = optimisedDistance(camera_pos, centercoord)
            facesscreenXYZ = (centercoord[0]) * focal_length / faceZ + hweight, (centercoord[2]) * focal_length / faceZ + hheight, distanceface

            self.faces_to_draw.append((distanceface, facesscreenXYZ[0], facesscreenXYZ[1], self.cylinder_facesC.index(i), faceZ))
            coords = []

            for j in i:
                coords.append((j[0] * focal_length / getZ(j, camera_pos, (0, 1, 0)) + hweight, j[2] * focal_length / getZ(j, camera_pos, (0, 1, 0)) + hheight))

            self.face_vertexesSCR.append(tuple(coords))

        for t in range(0, 2):
            centercoord = self.vertices[self.detalization*2+t]


            facesscreenXYZ = (centercoord[0]) * focal_length / faceZ + hweight, (centercoord[2]) * focal_length / faceZ + hheight, distanceface


            faceZ = getZ(centercoord, camera_pos, (0, 1, 0))
            distanceface = optimisedDistance(camera_pos, centercoord)
            
            self.faces_to_draw.append((distanceface, facesscreenXYZ[0], facesscreenXYZ[1], self.detalization+t, faceZ))
            
            coords = []

            for j in top_bottom_faces[t]:
                coords.append((j[0] * focal_length / getZ(j, camera_pos, (0, 1, 0)) + hweight, j[2] * focal_length / getZ(j, camera_pos, (0, 1, 0)) + hheight))


            self.face_vertexesSCR.append(tuple(coords))

        self.faces_to_draw.sort(reverse=True)

        for c in self.faces_to_draw:
            elem = self.face_vertexesSCR[c[3]]
            self.drawscreen.create_polygon(elem, fill = rgb_to_hex((round(abs(sin(c[3]))*255), round(abs(cos(c[3])*255)), round(abs(sin(c[3]+4)*255))), 1))  