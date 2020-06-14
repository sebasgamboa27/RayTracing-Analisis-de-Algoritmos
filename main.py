import sys
from os import path
import numpy as np
from sprites import *
from tilemap import *
from Limits import *
from Point import *
import rt

# HUD functions

class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 4, 2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()



    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)

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

        segments.append([Point(0, 0), Point(WIDTH, 0)])
        segments.append([Point(0, 0), Point(0, HEIGHT)])
        segments.append([Point(0, HEIGHT),Point(WIDTH, HEIGHT)])
        segments.append([Point(WIDTH, 0), Point(WIDTH, HEIGHT)])

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

            if tile_object.name == 'wall' and (tile_object.x<1050 or tile_object.y<800):

                obstacle = Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height,1)

                self.map.RayWalls.append(Limits(tile_object.x,tile_object.y,
                                            tile_object.x+tile_object.width,tile_object.y,obstacle.type))

                self.map.RayWalls.append(Limits(tile_object.x, tile_object.y+tile_object.height,
                                            tile_object.x + tile_object.width, tile_object.y+tile_object.height,obstacle.type))

                self.map.RayWalls.append(Limits(tile_object.x, tile_object.y,
                                            tile_object.x, tile_object.y+tile_object.height,obstacle.type))

                self.map.RayWalls.append(Limits(tile_object.x + tile_object.width, tile_object.y ,
                                            tile_object.x + tile_object.width, tile_object.y + tile_object.height,obstacle.type))

                segments.append([Point(tile_object.x, tile_object.y),
                                 Point(tile_object.x + tile_object.width, tile_object.y)])

                segments.append([Point(tile_object.x, tile_object.y + tile_object.height),
                                                Point(tile_object.x + tile_object.width, tile_object.y + tile_object.height)])

                segments.append([Point(tile_object.x, tile_object.y),
                                                Point(tile_object.x, tile_object.y + tile_object.height)])

                segments.append([Point(tile_object.x + tile_object.width, tile_object.y),
                                                Point(tile_object.x + tile_object.width, tile_object.y + tile_object.height)])


        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.night = True

    def changeWallState(self):
        global LIGHT_CURRENT_MODE

        if(LIGHT_CURRENT_MODE >= 2):
            LIGHT_CURRENT_MODE = 1
        else:
            LIGHT_CURRENT_MODE += 1

        for wall in self.map.RayWalls:
            wall.type = LIGHT_CURRENT_MODE



    def run(self):

        self.playing = True

        #self.player.pos.x = 600
        #self.player.pos.y = 580

        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            if not self.paused:
                self.update()
            self.player.particle.pos[0] = self.player.pos.x
            self.player.particle.pos[1] = self.player.pos.y
            self.draw()
            pg.display.update()




    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        

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


    def draw(self):

        self.screen.blit(self.map_img, self.camera.apply(self.map))

        self.fog.fill((20, 20, 20))


        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)

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

        count = 0

        for i in range(int(minW),int(maxW)):
            for j in range(int(minH),int(maxH)):
                alpha = 0
                point = Point(i, j)

                source = Point(self.player.pos[0], self.player.pos[1])

                if(point.x != source.x or point.y != source.y ):
                    point = Point(i,j)

                    source = Point(self.player.pos[0],self.player.pos[1])
                    dir = source - point

                    length = rt.length(dir)
                    length2 = rt.length(rt.normalize(dir))

                    free = True
                    for seg in segments:

                        dist = rt.raySegmentIntersect(point, dir, seg[0], seg[1])
                        
                        if dist > 0 and length2 > dist:
                            free = False
                            break

                    if free:
                        alpha = round(((LIGHT_MAX_DISTANCE - length) / LIGHT_MAX_DISTANCE) * 255)

                if(alpha<0):
                    alpha = 0
                print(count)
                count = count + 1
                pygame.gfxdraw.pixel(self.fog, i, j,(255,255,255,alpha))


        self.screen.blit(self.fog, (0, 0), special_flags=pygame.BLEND_MULT)


    def find_collision(self,ray):
        closest = 1000
        closestpt = None
        for wall in self.map.RayWalls:
            pt = ray.cast(wall)
            if pt is not None:
                dis = linalg.norm(pt - self.player.pos)
                if (dis < closest):
                    closest = dis
                    closestpt = pt

        if closestpt is not None:

            return Ray(ray.pos[0],ray.pos[1],closestpt[0],closestpt[1])

        return None


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
                    self.changeWallState()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.title_font, 100, RED,
                       WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("Press a key to start", self.title_font, 75, WHITE,
                       WIDTH / 2, HEIGHT * 3 / 4, align="center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

# create the game object
g = Game()
g.show_start_screen()
g.new()
while True:
    g.run()


