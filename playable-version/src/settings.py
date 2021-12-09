import os
import pygame as pg

game_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

img_folder = os.path.join(game_folder, 'images')
sounds_folder = os.path.join(game_folder, 'sounds')

# Settings
WIDTH = 1024
HEIGHT = 768
FPS = 60
SQUARE_SIZE = 64

# Gameplay
MOBS_NUMBER = 3
TREASURES_NUMBER = 3

# Img paths
player_img = pg.image.load(os.path.join(img_folder, 'explorator.png'))
mob_img = pg.image.load(os.path.join(img_folder, 'mob.png'))
treasure_img = pg.image.load(os.path.join(img_folder, 'treasure.png'))

# Colors
DGREY = (30, 30, 30)
LGREY = (66, 66, 66)
YELLOW = (255, 191, 0)
ORANGE = (209, 125, 0)
WHITE = (255, 255, 255)
PURPLE = (81, 0, 135)
RED = (255, 0, 0)
DRED = (99, 0, 0)
GREEN = (0, 135, 43)
BGCOLOR = DGREY
