import pygame as pg
from src.settings import *


class Player(pg.sprite.Sprite):
    def __init__(self, game_class, x, y):  #
        pg.sprite.Sprite.__init__(self, game_class.player_group)  # Apelare constructor clasa mostenita
        self.game_class = game_class  # Importa variabilele din clasa Game
        self.image = player_img  # Seteaza path-ul imaginii jucatorului
        self.rect = self.image.get_rect()  # Creaza o patratica cu imaginea
        self.mob_orientation = -1  # Salveaza pozitia monstrului fata de jucator. 1-sus, 2-dreapta, 3-jos, 4-stanga
        self.current_mob = -1  # Salveaza monstru cu care s-a intrat in contact ultima oara
        self.x = x
        self.y = y

    def move(self, dx=0, dy=0):
        self.game_class.score -= 1  # Scade scorul cu o unitate la fiecare mutare

        self.check_mob_colision(dx, dy)

        # Dupa fiecare mutare verificam daca ne aflam intr-o patratica cu un monstru sau o comoara
        if self.check_mob_square(dx, dy):
            self.game_class.score -= 1000
            self.game_class.mobs_killed += 1
        if self.check_treasure_square(dx, dy):
            self.game_class.score += 100
            self.game_class.treasures_found += 1

        # dx, dy, directia in care se misca. -1 spate, 1 fata.
        # Verifica daca pozitia jucatorului se incadreaza in fereastra si nu trece prin perete
        if 0 <= self.x + dx <= WIDTH // SQUARE_SIZE - 1 and self.check_wall_colision(dx, dy):
            self.x += dx
        if 0 <= self.y + dy <= HEIGHT // SQUARE_SIZE - 1 and self.check_wall_colision(dx, dy):
            self.y += dy

    # Metoda din clasa mostenita pg.sprite.Sprite
    def update(self):
        self.rect.x = self.x * SQUARE_SIZE
        self.rect.y = self.y * SQUARE_SIZE

    def check_mob_square(self, dx, dy):
        """
        Verifica daca jucatorul a intrat intr-o celula cu un monstru viu.
        Daca coordonatele monstrului sunt egale cu pozitia curenta a jucatorului + miscarea pe care o face, monstrul
        este eliminat din grup si implicit de pe ecran.
        :param dx: Miscarea jucatorului pe axa x (-1 in stanga, 1 in dreapta)
        :param dy: Miscarea jucatorului pe axa y (-1 in sus, 1 in jos)
        """
        for mob in self.game_class.mob_group:
            if mob.x == self.x + dx and mob.y == self.y + dy:
                self.game_class.mob_group.remove(mob)
                return True
        return False

    def check_treasure_square(self, dx, dy):
        """
        Verifica daca jucatorul a intrat intr-o celula cu o comoara
        Daca coordonatele comorii sunt egale cu pozitia curenta a jucatorului + miscarea pe care o face, comoara este
        eliminata din grup si implicit de pe ecran.
        :param dx: Miscarea jucatorului pe axa x (-1 in stanga, 1 in dreapta)
        :param dy: Miscarea jucatorului pe axa y (-1 in sus, 1 in jos)
        """
        for treasure in self.game_class.treasure_group:
            if treasure.x == self.x + dx and treasure.y == self.y + dy:
                self.game_class.treasure_group.remove(treasure)
                return True
        return False

    def check_wall_colision(self, dx, dy):
        """
        Verifica daca jucatorul a intrat intr-un perete
        Daca coordonatele peretelui sunt egale cu pozitia curenta a jucatorului + miscarea pe care o face
        """
        for wall in self.game_class.wall_group:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return False
        return True

    def check_mob_colision(self, dx, dy):
        """
        Returneaza pozitia pe care se afla un mob, 1 - sus, 2 - dreapta, 3 - jos, 4 - stanga.
        Pentru fiecare parte din care se poate ajunge in perimetrul unui monstru se verifica
        EX: 0 este monstrul
                                                         1. se poate intra de sus in perimetrul sau
                                                         |
                                                         V
                                                         ###
         3. se poate intra din stanga in perimetrul sau->#0#
                                                         ###
                                                         ^
                                                         |
                                                         2. se poate intra de jos in perimetrul sau
        Se repeta metoda pentru fiecare latura.
        """
        self.mob_orientation = -1
        for mob in self.game_class.mob_group:
            if self.x + 1 == mob.x and ((self.y - 1 == mob.y and dy == -1) or (self.y + 1 == mob.y and dy == 1)):
                self.mob_orientation = 2
                self.current_mob = mob
            if self.x + 2 == mob.x and self.y == mob.y and dx == 1:
                self.mob_orientation = 2
                self.current_mob = mob

            if self.y - 1 == mob.y and ((self.x + 1 == mob.x and dx == 1) or (self.x - 1 == mob.x and dx == -1)):
                self.mob_orientation = 1
                self.current_mob = mob
            if self.y - 2 == mob.y and self.x == mob.x and dy == -1:
                self.mob_orientation = 1
                self.current_mob = mob

            if self.y + 1 == mob.y and ((self.x + 1 == mob.x and dx == 1) or (self.x - 1 == mob.x and dx == -1)):
                self.mob_orientation = 3
                self.current_mob = mob
            if self.y + 2 == mob.y and self.x == mob.x and dy == 1:
                self.mob_orientation = 3
                self.current_mob = mob

            if self.x - 1 == mob.x and ((self.y - 1 == mob.y and dy == -1) or (self.y + 1 == mob.y and dy == 1)):
                self.mob_orientation = 4
                self.current_mob = mob
            if self.x - 2 == mob.x and self.y == mob.y and dx == -1:
                self.mob_orientation = 4
                self.current_mob = mob
