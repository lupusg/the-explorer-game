import pygame as pg
import os


game_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
img_folder = os.path.join(game_folder, 'images')

# Settings
WIDTH = 16 * 64
HEIGHT = 12 * 64
FPS = 60
SQUARE_SIZE = 64

# Gameplay
MOBS_NUMBER = 20
TREASURES_NUMBER = 10

# Colors
DGREY = (30, 30, 30)
LGREY = (66, 66, 66)
WHITE = (255, 255, 255)
BGCOLOR = DGREY

# Img paths
mob_img = pg.image.load(os.path.join(img_folder, 'mob.png'))
treasure_img = pg.image.load(os.path.join(img_folder, 'treasure.png'))
path_img = pg.image.load(os.path.join(img_folder, 'drum2.png'))
player_img = pg.image.load(os.path.join(img_folder, 'explorator.png'))
