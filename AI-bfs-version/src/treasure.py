from src.settings import *
import pygame as pg


class Treasure(pg.sprite.Sprite):
    def __init__(self, game_class, x, y):
        pg.sprite.Sprite.__init__(self, game_class.treasure_group)
        self.image = treasure_img  # Seteaza path-ul imaginiii
        self.rect = self.image.get_rect()  # Creaza o patratica cu imaginea cu coordonatele (0, 0)
        self.x = x
        self.y = y
        # Actualizeaza coordonatele patratului cu unele in functie de marimea patratului in matricea jocului
        self.rect.x = x * SQUARE_SIZE
        self.rect.y = y * SQUARE_SIZE
