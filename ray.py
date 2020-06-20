import pygame

from numpy import *
from Limits import *


class Ray:
    def __init__(self, x, y, radius):
        self.pos = [x, y]
        self.dir = array([cos(radius), sin(radius)])
        self.end = [x, y]
        self.dis = 0
        self.radius = radius
        self.responseRay = None

    def display(self, screen):
        pygame.draw.line(screen, (255, 255, 255), self.pos, self.pos + self.dir, 1)

    def setResponseRay(self, x, y, radius):
        self.responseRay = Ray(x, y, -radius)

    def refract(self, startPoint):
        self.responseRay = Ray(startPoint[0], startPoint[1], self.radius)

    def reflect(self, startPoint, cont, totalRays):
        if (cont < totalRays // 2):
            self.responseRay = Ray(startPoint[0], startPoint[1], self.radius - deg2rad(100))

        else:
            self.responseRay = Ray(startPoint[0], startPoint[1], self.radius + deg2rad(100))

    def cast(self, wall):
        # start point
        x1 = wall.a[0]
        y1 = wall.a[1]
        # end point
        x2 = wall.b[0]
        y2 = wall.b[1]

        # position of the ray
        x3 = self.pos[0]
        y3 = self.pos[1]
        x4 = self.pos[0] + self.dir[0]
        y4 = self.pos[1] + self.dir[1]

        # denominator
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        # numerator
        num = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
        if den == 0:
            return None

        # formulars
        t = num / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

        if t > 0 and t < 1 and u > 0:
            # Px, Py
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            pot = array([x, y])
            return pot

    def closestWall(self, walls, Startwall):
        closest = 10000000000
        finalWall = None
        for wall in walls:
            if (wall == Startwall):
                continue
            pt = self.cast(wall)

            if pt is not None:
                dis = linalg.norm(pt - self.pos)
                if (dis < closest):
                    closest = dis
                    finalWall = wall

        return finalWall

    def createReflectionWall(self, wall, castPt):

        if (self.pos[0] > wall.a[0] and self.pos[0] < wall.b[0]):

            if (self.pos[1] < castPt[1]):
                return Limits(wall.a[0], wall.a[1] - 25, wall.b[0], wall.b[1] - 25)
            else:
                return Limits(wall.a[0], wall.a[1] + 25, wall.b[0], wall.b[1] + 25)
        else:

            if (self.pos[1] < castPt[1]):
                return Limits(wall.a[0] - 25, wall.a[1], wall.b[0] - 25, wall.b[1])
            else:
                return Limits(wall.a[0] + 25, wall.a[1], wall.b[0] + 25, wall.b[1])
