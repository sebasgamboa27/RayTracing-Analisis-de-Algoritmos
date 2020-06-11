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
                points=[]
                points.append(self.rays[i].pos)
                points.append(self.rays[i].end)
                points.append(self.rays[i+1].end)

                texture = pygame.image.load("img/light_350_hard.png").convert()
                pygame.transform.scale(texture,(100,100))

                pygame.gfxdraw.textured_polygon(game.fog,points,texture,0,0)


        screen.blit(game.fog, (0, 0), special_flags=pygame.BLEND_MULT)





    def look(self, screen, walls,startAngle):
        self.rays = []
        for i in range(int(-startAngle), int(-startAngle+40), 7):
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
                pygame.draw.line(screen, (255, 255, 255), self.pos, array(closestpt, int), 2)
                ray.end=closestpt
                ray.dis = dis
