import sys
from os import path
import time

import numpy as np

import vectorOperation
from Pixel import Point
from sprites import *
from tilemap import *
from Limits import *
import threading


# HUD functions

class Game:
    def __init__(self, objectType):
        pg.mixer.pre_init(44100, -16, 4, 2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.objectType = objectType
        self.pixelMap = []
        self.pathTracerDone = False
        self.animation = True

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.map_folder = path.join(game_folder, 'maps')
        self.title_font = path.join(img_folder, 'ZOMBIE.TTF')
        self.hud_font = path.join(img_folder, 'Impacted2.0.ttf')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()

        # lighting effect
        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pg.image.load(path.join(img_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()

    def new(self):

        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.map = TiledMap(path.join(self.map_folder, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()

        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)

            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)

            if tile_object.name == 'wall' and (tile_object.x < 1050 or tile_object.y < 800):

                obstacle = Obstacle(self, tile_object.x, tile_object.y,
                                    tile_object.width, tile_object.height, self.objectType)

                if (tile_object.x > 621 and tile_object.x < 660):
                    print(0)
                else:

                    self.map.RayWalls.append(Limits(tile_object.x, tile_object.y,
                                                    tile_object.x + tile_object.width, tile_object.y, obstacle.type))

                    self.map.RayWalls.append(Limits(tile_object.x, tile_object.y + tile_object.height,
                                                    tile_object.x + tile_object.width,
                                                    tile_object.y + tile_object.height, obstacle.type))

                    self.map.RayWalls.append(Limits(tile_object.x, tile_object.y,
                                                    tile_object.x, tile_object.y + tile_object.height, obstacle.type))

                    self.map.RayWalls.append(Limits(tile_object.x + tile_object.width, tile_object.y,
                                                    tile_object.x + tile_object.width,
                                                    tile_object.y + tile_object.height, obstacle.type))

                    segments.append([Point(tile_object.x, tile_object.y),
                                     Point(tile_object.x + tile_object.width, tile_object.y)])

                    segments.append([Point(tile_object.x, tile_object.y + tile_object.height),
                                     Point(tile_object.x + tile_object.width, tile_object.y + tile_object.height)])

                    segments.append([Point(tile_object.x, tile_object.y),
                                     Point(tile_object.x, tile_object.y + tile_object.height)])

                    segments.append([Point(tile_object.x + tile_object.width, tile_object.y),
                                     Point(tile_object.x + tile_object.width, tile_object.y + tile_object.height)])

        self.map.RayWalls.append(Limits(0, 0, 1024, 0))
        self.map.RayWalls.append(Limits(0, 0, 1024, 0))
        self.map.RayWalls.append(Limits(0, 768, 1024, 768))
        self.map.RayWalls.append(Limits(1024, 768, 1024, 0))

        segments.append([Point(0, 0), Point(1024, 0)])
        segments.append([Point(0, 0), Point(1024, 0)])
        segments.append([Point(0, 768), Point(1024, 768)])
        segments.append([Point(1024, 768), Point(1024, 0)])

        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.night = True

    def pathTracer(self):

        minW = self.player.pos[0] - LIGHT_MAX_DISTANCE
        if (minW < 0):
            minW = 0

        maxW = self.player.pos[0] + LIGHT_MAX_DISTANCE
        if (maxW > WIDTH):
            maxW = WIDTH

        minH = self.player.pos[1] - LIGHT_MAX_DISTANCE
        if (minH < 0):
            minH = 0

        maxH = self.player.pos[1] + LIGHT_MAX_DISTANCE
        if (maxH > HEIGHT):
            maxH = HEIGHT

        for i in range(int(minW), int(maxW)):
            for j in range(int(minH), int(maxH)):

                alpha = 0
                point = Point(i, j)

                source = Point(self.player.pos[0], self.player.pos[1])

                angle = self.player.particle.getAngle([point.x, point.y], [source.x, source.y],
                                                      self.player.particle.rays[2].end)

                if 40 >= angle >= 0:

                    if point.x != source.x or point.y != source.y:
                        point = Point(i, j)

                        dir = source - point

                        length = vectorOperation.length(dir)
                        length2 = vectorOperation.length(vectorOperation.normalize(dir))

                        free = True
                        for seg in segments:

                            dist = vectorOperation.raySegmentIntersect(point, dir, seg[0], seg[1])

                            if dist > 0 and length2 > dist:
                                free = False
                                break

                        if free:

                            newAngle = self.player.particle.getAngle([point.x, point.y], [source.x, source.y],
                                                                     self.player.particle.rays[1].end)

                            if newAngle < 20:
                                angleDim = (20 - newAngle) / 20

                            else:
                                newAngle = abs(newAngle - 360)
                                angleDim = (20 - newAngle) / 20

                            alpha = round((((LIGHT_MAX_DISTANCE - length) / LIGHT_MAX_DISTANCE) * angleDim) * 255)

                        else:
                            # reflexion
                            intersectionPoint = self.getIntersectionPoint(point, dir, seg)
                            reflectionSpace = self.getReflectionSpace(seg, source) #relacion de lados del rectangulo(0-1,0-2,1-3,2-3)
                            pygame.draw.line(self.screen,(255,255,255),reflectionSpace[0],reflectionSpace[1],2)
                            pygame.draw.line(self.screen, (255, 255, 255), reflectionSpace[0], reflectionSpace[2], 2)
                            pygame.draw.line(self.screen, (255, 255, 255), reflectionSpace[1], reflectionSpace[3], 2)
                            pygame.draw.line(self.screen, (255, 255, 255), reflectionSpace[2], reflectionSpace[3], 2)

                            #Aqui iria for que pinta con los respectivos calculos del alpha


                    if alpha < 0 or alpha > 255:
                        alpha = 0

                    WHITE[3] = alpha
                    if (self.animation):
                        self.pixelMap += [[i, j, alpha]]
                        time.sleep(0.0000000000000000001)
                    else:
                        pygame.gfxdraw.pixel(self.fog, i, j, WHITE)

        # self.screen.blit(self.fog, (0, 0), special_flags=pygame.BLEND_MULT)
        self.pathTracerDone = True
        print("terminado")

    def getReflectionSpace(self, seg, source):
        point1 = [seg[0].x,seg[0].y]  # Establece valor de recta pero será modificado
        point2 = [seg[1].x,seg[1].y] # Establece valor de recta pero será modificado
        point3 = [seg[0].x,seg[0].y]
        point4 = [seg[1].x,seg[1].y]

        print([point1,point2,point3,point4])

        if (source.y > seg[0].y and source.y < seg[1].y):
            if (source.x < seg[0].x or source.x < seg[1].x):
                point1[0] -= 100
                point2[0] -= 100
            else:
                point1[0] += 100
                point2[0] += 100
        else:
            if (source.y < seg[0].y or source.y < seg[1].y):
                point1[1] -= 100
                point2[1] -= 100
            else:
                point1[1] += 100
                point2[1] += 100
        return [point1,point2,point3,point4]

    def getIntersectionPoint(self, point, dir, seg):

        # start point
        x1 = seg[0].x
        y1 = seg[0].y
        # end point
        x2 = seg[1].x
        y2 = seg[1].y

        # position of the ray
        x3 = point.x
        y3 = point.y
        x4 = x3 + dir.x
        y4 = y3 + dir.y

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

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        self.player.particle.on = False

        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0

            self.pathTracerTrhead = threading.Thread(target=self.pathTracer)

            self.player.particle.pos[0] = self.player.pos.x
            self.player.particle.pos[1] = self.player.pos.y

            self.events()
            if not self.paused:
                self.update()

            if (self.player.particle.on):
                if (self.animation):
                    self.player.particle.look(self.screen, self.map.RayWalls, self.player.rot)
                    self.pathTracerTrhead.start()
                else:
                    self.drawIllumination()
                    time.sleep(20)
                self.player.particle.on = False

            self.draw()

            if self.pathTracerDone and self.animation:
                print("terminado")
                time.sleep(20)
                self.pixelMap = []
                self.pathTracerDone = not self.pathTracerDone

            pg.display.update()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        # self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def render_fog(self):
        # draw the light mask (gradient) onto fog image
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

    def pixelPainter(self):
        for pixel in self.pixelMap:
            WHITE[3] = pixel[2]
            pygame.gfxdraw.pixel(self.fog, pixel[0], pixel[1], WHITE)

    def draw(self):

        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply(self.map))
        self.fog.fill((20, 20, 20))

        self.pixelPainter()
        self.screen.blit(self.fog, (0, 0), special_flags=pygame.BLEND_MULT)

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)

        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")
        pg.display.flip()
        self.player.particle.on = False

    def drawIllumination(self):

        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply(self.map))
        self.fog.fill((20, 20, 20))

        self.player.particle.look(self.screen, self.map.RayWalls, self.player.rot)
        self.pathTracer()
        # self.player.particle.displayLights(self.screen,self)
        # self.player.particle.displayResponseLights(self.screen,self)
        self.screen.blit(self.fog, (0, 0), special_flags=pygame.BLEND_MULT)

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)

        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")
        pg.display.flip()
        self.player.particle.on = False

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_p:
                    self.paused = not self.paused
                if event.key == pg.K_t:
                    self.player.particle.switchParticle()


# create the game object
g = Game(1)
while True:
    g.new()
    g.run()
