from src.settings import *
import pygame as pg


class Mob(pg.sprite.Sprite):
    def __init__(self, game_class, x, y):
        pg.sprite.Sprite.__init__(self, game_class.mob_group)
        self.image = mob_img  # Seteaza path-ul imaginii
        self.rect = self.image.get_rect()  # Creaza o patratica cu imaginea cu coordonatele (0, 0)
        self.x = x
        self.y = y
        # Actualizeaza coordonatele patratului cu unele in functie de marimea patratului in matricea jocului
        self.rect.x = x * SQUARE_SIZE
        self.rect.y = y * SQUARE_SIZE