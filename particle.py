import pygame
import pygame.gfxdraw


from numpy import array
from numpy import deg2rad
from numpy import linalg


from ray import *


class Particle:
    def __init__(self):
        self.pos = array([0, 0])

    def displayLights(self, screen,game):


        game.fog.fill((20, 20, 20))

        for i in range(0,len(self.rays)):

            if i<len(self.rays)-1:
                points_first_half=[]
                points_second_half = []
                points_end = []

                half_start_x1 = self.rays[i].end[0] - (((self.rays[i].end[0]-self.rays[i].pos[0])/ 3)*1 )
                half_start_y1= self.rays[i].end[1] - (((self.rays[i].end[1]-self.rays[i].pos[1])/ 3)*1 )

                half_start_x2 = self.rays[i+1].end[0] - (((self.rays[i+1].end[0]-self.rays[i+1].pos[0])/ 3)*1 )
                half_start_y2 = self.rays[i+1].end[1] - (((self.rays[i+1].end[1]-self.rays[i+1].pos[1])/ 3)*1 )

                half_end_x1 = self.rays[i].end[0] - (((self.rays[i].end[0]-self.rays[i].pos[0])/ 3)*2 )
                half_end_y1 = self.rays[i].end[1] - (((self.rays[i].end[1]-self.rays[i].pos[1])/ 3)*2 )

                half_end_x2 = self.rays[i+1].end[0] - (((self.rays[i+1].end[0]-self.rays[i+1].pos[0])/ 3)*2 )
                half_end_y2 = self.rays[i+1].end[1] - (((self.rays[i+1].end[1]-self.rays[i+1].pos[1])/ 3)*2 )


                half_start1=[half_start_x1,half_start_y1]
                half_start2 = [half_start_x2, half_start_y2]

                half_end1 = [half_end_x1,half_end_y1]
                half_end2 = [half_end_x2, half_end_y2]

                points_first_half.append(self.rays[i].pos)
                points_first_half.append(half_end1)
                points_first_half.append(half_end2)

                points_second_half.append(half_start2)
                points_second_half.append(half_start1)
                points_second_half.append(half_end1)
                points_second_half.append(half_end2)


                points_end.append(half_start1)
                points_end.append(half_start2)
                points_end.append(self.rays[i+1].end)
                points_end.append(self.rays[i].end)


                texture = pygame.image.load("img/light_small.png").convert_alpha()
                pygame.transform.scale(texture,(100,100))

                texture_dim = pygame.image.load("img/dimmer3.png").convert_alpha()
                pygame.transform.scale(texture_dim, (100, 100))

                texture_dim2 = pygame.image.load("img/dimmer4.png").convert_alpha()
                pygame.transform.scale(texture_dim2, (100, 100))

                pygame.gfxdraw.textured_polygon(game.fog,points_first_half,texture,0,0)
                pygame.gfxdraw.textured_polygon(game.fog, points_second_half, texture_dim, 0, 0)
                pygame.gfxdraw.textured_polygon(game.fog, points_end, texture_dim2, 0, 0)

        screen.blit(game.fog, (0, 0), special_flags=pygame.BLEND_MULT)






    def look(self, screen, walls,startAngle):
        self.rays = []
        for i in range(int(-startAngle-20), int(-startAngle+20), 6):
            self.rays.append(Ray(self.pos[0], self.pos[1], deg2rad(i)))

        for ray in self.rays:
            closest = 1000
            closestpt = None
            for wall in walls:
                pt = ray.cast(wall)

                if pt is not None:
                    dis = linalg.norm(pt - self.pos)
                    if (dis < closest):
                        closest = dis
                        closestpt = pt

            if closestpt is not None:
                ray.end=closestpt
                ray.dis = dis
                #pygame.draw.line(screen, (255, 255, 255), self.pos, array(closestpt, int), 2)

                '''if (wall.type == 1):
                    print("normal")
                elif (wall.type == 2):
                    print("Modo refracción")
                    #self.look(screen,walls,startAngle-180)
                elif (wall.type == 3):
                    print("Modo reflejo")'''
