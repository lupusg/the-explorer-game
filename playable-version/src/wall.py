import pygame as pg
from src.settings import *


class Wall(pg.sprite.Sprite):
    def __init__(self, game_class, x, y):
        pg.sprite.Sprite.__init__(self, game_class.wall_group)
        self.image = pg.Surface((SQUARE_SIZE, SQUARE_SIZE))  # Creaza un patrat de SQUARE_SIZE x SQUARE_SIZE
        self.image.fill(DRED)  # Umple patratul creat cu DARK RED
        self.rect = self.image.get_rect()  # Creaza patratul cu coordonate (0,0)
        self.x = x
        self.y = y
        self.rect.x = x * SQUARE_SIZE  # Actualizeaza coordonatele patratului cu unele in functie de marimea patratului
        self.rect.y = y * SQUARE_SIZE  # in matricea jocului
