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
                points1=[]
                points2 = []
                points3 = []
                points4 = []
                points_end = []


                half_start_x1 = self.rays[i].end[0] - (((self.rays[i].end[0]-self.rays[i].pos[0])/ 5)*1 )
                half_start_y1= self.rays[i].end[1] - (((self.rays[i].end[1]-self.rays[i].pos[1])/ 5)*1 )
                half_start_x2 = self.rays[i+1].end[0] - (((self.rays[i+1].end[0]-self.rays[i+1].pos[0])/ 5)*1 )
                half_start_y2 = self.rays[i+1].end[1] - (((self.rays[i+1].end[1]-self.rays[i+1].pos[1])/ 5)*1 )

                half_end_x1 = self.rays[i].end[0] - (((self.rays[i].end[0]-self.rays[i].pos[0])/ 5)*2 )
                half_end_y1 = self.rays[i].end[1] - (((self.rays[i].end[1]-self.rays[i].pos[1])/ 5)*2 )
                half_end_x2 = self.rays[i+1].end[0] - (((self.rays[i+1].end[0]-self.rays[i+1].pos[0])/ 5)*2 )
                half_end_y2 = self.rays[i+1].end[1] - (((self.rays[i+1].end[1]-self.rays[i+1].pos[1])/ 5)*2 )

                pointx3_1 = self.rays[i].end[0] - (((self.rays[i].end[0] - self.rays[i].pos[0]) / 5) * 3)
                pointy3_1 = self.rays[i].end[1] - (((self.rays[i].end[1] - self.rays[i].pos[1]) / 5) * 3)
                pointx3_2 = self.rays[i + 1].end[0] - (((self.rays[i + 1].end[0] - self.rays[i + 1].pos[0]) / 5) * 3)
                pointy3_2 = self.rays[i + 1].end[1] - (((self.rays[i + 1].end[1] - self.rays[i + 1].pos[1]) / 5) * 3)

                pointx4_1 = self.rays[i].end[0] - (((self.rays[i].end[0] - self.rays[i].pos[0]) / 5) * 4)
                pointy4_1 = self.rays[i].end[1] - (((self.rays[i].end[1] - self.rays[i].pos[1]) / 5) * 4)
                pointx4_2 = self.rays[i + 1].end[0] - (((self.rays[i + 1].end[0] - self.rays[i + 1].pos[0]) / 5) * 4)
                pointy4_2 = self.rays[i + 1].end[1] - (((self.rays[i + 1].end[1] - self.rays[i + 1].pos[1]) / 5) * 4)

                half_start1 = [half_start_x1, half_start_y1]
                half_start2 = [half_start_x2, half_start_y2]

                half_end1 = [half_end_x1,half_end_y1]
                half_end2 = [half_end_x2, half_end_y2]

                point3_1 = [pointx3_1, pointy3_1]
                point3_2 = [pointx3_2, pointy3_2]

                point4_1 = [pointx4_1, pointy4_1]
                point4_2 = [pointx4_2, pointy4_2]

                points1.append(self.rays[i].pos)
                points1.append(point4_1)
                points1.append(point4_2)

                points2.append(point3_2)
                points2.append(point3_1)
                points2.append(point4_1)
                points2.append(point4_2)

                points3.append(point3_2)
                points3.append(point3_1)
                points3.append(half_end1)
                points3.append(half_end2)

                points4.append(half_start2)
                points4.append(half_start1)
                points4.append(half_end1)
                points4.append(half_end2)

                points_end.append(half_start1)
                points_end.append(half_start2)
                points_end.append(self.rays[i+1].end)
                points_end.append(self.rays[i].end)

                first_color = pygame.Color(255,255,255,120)
                second_color = pygame.Color(255, 255, 255, 100)
                third_color = pygame.Color(255, 255, 255, 80)
                fourth_color =pygame.Color(255, 255, 255, 60)
                fifth_color = pygame.Color(255, 255, 255, 40)

                pygame.gfxdraw.filled_polygon(game.fog,points1,first_color)
                pygame.gfxdraw.filled_polygon(game.fog, points2, second_color)
                pygame.gfxdraw.filled_polygon(game.fog, points3, third_color)
                pygame.gfxdraw.filled_polygon(game.fog, points4, fourth_color)
                pygame.gfxdraw.filled_polygon(game.fog, points_end, fifth_color)

        #screen.blit(game.fog, (0, 0), special_flags=pygame.BLEND_MULT)

    def displayResponseLights(self, screen, game):

        for i in range(0, len(self.ResponseRays)):

            if i < len(self.ResponseRays) - 1:
                points = []

                points.append(self.ResponseRays[i].pos)
                points.append(self.ResponseRays[i+1].pos)
                points.append(self.ResponseRays[i + 1].end)
                points.append(self.ResponseRays[i].end)


                first_color = pygame.Color(255, 255, 255, 25)

                pygame.gfxdraw.filled_polygon(game.fog, points, first_color)


        screen.blit(game.fog, (0, 0), special_flags=pygame.BLEND_MULT)






    def look(self, screen, walls,startAngle):
        self.rays = []
        self.ResponseRays = []
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
                        finalWall = wall

            if closestpt is not None:
                ray.end=closestpt
                ray.dis = dis
                #pygame.draw.line(screen, (255, 255, 255), self.pos, array(closestpt, int), 2)

                if (finalWall.type == 2):
                    ray.refract(finalWall, closestpt)
                    endWall = ray.closestWall(walls, finalWall)
                    castPt = ray.responseRay.cast(endWall)
                    if castPt is not None:
                        self.ResponseRays.append(ray.responseRay)
                        ray.responseRay.end = castPt
                        #pygame.draw.line(screen, (255, 255, 255), ray.responseRay.pos, array(castPt, int), 2)


                elif (finalWall.type == 3):
                    ray.reflect(finalWall, closestpt)
                    endWall = ray.closestWall(walls, finalWall)
                    castPt = ray.responseRay.cast(endWall)
                    if castPt is not None:
                        self.ResponseRays.append(ray.responseRay)
                        ay.responseRay.end = castPt
                        #pygame.draw.line(screen, (255, 255, 255), ray.responseRay.pos, array(castPt, int), 2)
