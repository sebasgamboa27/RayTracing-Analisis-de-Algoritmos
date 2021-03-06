import pygame as pg
import numpy as np
from PIL import Image

vec = pg.math.Vector2

segments = []
light = np.array([1, 1, 0.75])
i = Image.new("RGB", (1024, 768), (0, 0, 0) )
px = np.array(i)


# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_SPEED = 280
PLAYER_ROT_SPEED = 200
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10)

# Effects
NIGHT_COLOR = (20, 20, 20)
LIGHT_RADIUS = (500, 500)
LIGHT_MASK = "light_350_soft.png"
LIGHT_MODE = [1,2,3]
LIGHT_CURRENT_MODE = 1

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
EFFECTS_LAYER = 4

LIGHT_MAX_DISTANCE = 400

MAX_REFLECTION_LENGHT = 100
MAX_REFLECTION_BRIGHTNESS = 45

#Colors

WHITE = [255,255,255,0]
ORANGE = [255,128,0,0]
RED = [255,102,102,0]
BLUE = [0,128,255,0]
GREEN = [102,255,102,0]