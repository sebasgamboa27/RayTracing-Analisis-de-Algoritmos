import pygame

from numpy import array
from numpy import deg2rad
from numpy import linalg


from ray import *


class Particle:
    def __init__(self):
        self.pos = array([0, 0])

    def display(self, screen):
        #pygame.draw.circle(screen, (255, 255, 255), self.pos, 1, 1)

        for ray in self.rays:
            ray.display(screen)

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
