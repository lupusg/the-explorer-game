import math
import random
import sys
import time

import pygame as pg

from src.mob import Mob
from src.player import Player
from src.settings import *
from src.treasure import Treasure
from src.wall import Wall


class Game:
    def __init__(self):
        pg.init()  # Creaza fereastra cu jocul
        pg.font.init()  # Initializeaza modulul de font pentru a putea scrie pe ecran
        pg.mixer.get_init()  # Initializeaza modulul de sunet pentru gun shots.
        pg.display.set_caption('Exploratorul')  # Seteaza numele ferestre
        # Creaza un grup pentru fiecare tip de sprite: perete, jucator, monstru si comoara
        self.wall_group = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        self.mob_group = pg.sprite.Group()
        self.treasure_group = pg.sprite.Group()

        self.font = pg.font.SysFont('Arial', 24)  # Seteaza fontul 'Arial' cu marimea de 24.
        self.sound = pg.mixer.Sound(os.path.join(sounds_folder, 'shot.ogg'))  # Seteaza path-ul sunetului

        self.player = Player(self, 0,
                             HEIGHT // SQUARE_SIZE - 1)  # Creaza jucatorul pe harta cu pozitia de start stanga jos
        self.score = 0
        self.orientation = 2  # Directia in care jucatorul se uita, 1 - sus, 2 - dreapta, 3 - jos, 4 - stanga
        self.mobs_killed = 0  # Cati monstii a omorat
        self.treasures_found = 0  # Cate comori a gasit
        self.game_status = True  # Statusul pentru afisarea hartii in continuare sau a ecranului de finish.

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))  # Seteaza dimensiunea ferestrei
        self.clock = pg.time.Clock().tick(FPS)  # Seteaza refresh rate-ul jocului (FPS-ul)

    def draw_text(self):
        # Afiseaza punctele in partea din dreapta sus a ferestrei
        text = self.font.render('Points: ' + str(self.score), True, WHITE)
        self.screen.blit(text, (WIDTH - 140, 0))

    def draw_walls(self):
        # Matricea de pereti, 0 - nu exista perete, 1 - exista perete
        pereti = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0],
                  [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                  [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                  [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                  [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ]
        for i in range(HEIGHT // SQUARE_SIZE):
            for j in range(WIDTH // SQUARE_SIZE):
                if pereti[i][j] == 1:
                    Wall(self, j, i)

    def draw_mobs(self):
        """
        Adauga un numar de monstrii in fiecare patratica cu exceptia celor pe care se afla un perete sau pozitia de
        start a jucatorului.
        """
        mobs_number = MOBS_NUMBER
        while mobs_number:
            x = math.floor(random.random() * WIDTH // SQUARE_SIZE)
            y = math.floor(random.random() * HEIGHT // SQUARE_SIZE)
            if not self.check_wall_square(x, y) and (x != 0 or y != HEIGHT / SQUARE_SIZE - 1):
                Mob(self, x, y)
                mobs_number -= 1

    def draw_treasures(self):
        """
        Adauga un numar de comori in fiecare patratica in care nu se afla un perete, monstru sau pozitia de start a
        jucatorului.
        :return:
        """
        treasures_number = TREASURES_NUMBER
        while treasures_number:
            x = math.floor(random.random() * WIDTH // SQUARE_SIZE)
            y = math.floor(random.random() * HEIGHT // SQUARE_SIZE)
            if (not self.check_mob_square(x, y) and not self.check_wall_square(x, y)) and (
                    x != 0 or y != HEIGHT / SQUARE_SIZE - 1):
                Treasure(self, x, y)
                treasures_number -= 1

    def shoot(self):
        """
        Reda un sunet de fiecare data cand tragem si daca am in patratica in care ne uitam se afla un monstru atunci
        il scoate din grup si implicit il sterge de pe ecran si actualizeaza scorurile aferente.
        """
        self.sound.play()
        if self.orientation == self.player.mob_orientation:
            self.mob_group.remove(self.player.current_mob)
            self.player.mob_orientation = 0
            self.mobs_killed += 1
            self.score += 25
            return True
        else:
            self.score -= 25
            return False

    def end_screen(self):
        """
        Afiseaza ecranul de final dupa ce au fost omorati toti monstrii si adunate toate comorile.
        """
        self.screen.fill(DGREY)
        self.font = pg.font.SysFont('freesansbold', 40)
        text = self.font.render('Finished! Total points: ' + str(self.score), True, WHITE)
        self.screen.blit(text, (WIDTH / 2 - 210, HEIGHT / 2 - 10))
        pg.display.flip()
        time.sleep(3)
        self.quit()

    def start_screen(self):
        self.events()

        self.screen.fill(DGREY)
        self.font = pg.font.SysFont('freesansbold', 40)

        TEXT = ['E - Rotire spre stanga', 'R - Rotire spre dreapta', 'F - Trage',
                'Sageti - Deplasare', 'ESC - Quit']

        space = 50

        for line in TEXT:
            text = self.font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(WIDTH / 2, space))
            self.screen.blit(text, text_rect)
            space += 50

        pg.display.flip()

    def run(self):
        """
        Main loop-ul jocului.
        """
        while True:
            self.events()
            if self.game_status:
                self.font = pg.font.SysFont('Arial', 24)
                self.render()
            # Daca au fost omorati toti monstrii si adunate toate comorile, atunci jocul se incheie si se afiseaza
            # ecranul de finish
            if self.mobs_killed == MOBS_NUMBER and self.treasures_found == TREASURES_NUMBER:
                self.game_status = False
                time.sleep(1)
                self.end_screen()

    @staticmethod
    def quit():
        pg.quit()
        sys.exit()

    def draw_grid(self):
        """
        Traseaza liniile orizontale si verticale din cu SQUARE_SIZE spatii intre.
        """
        for x in range(0, WIDTH, SQUARE_SIZE):
            pg.draw.line(self.screen, LGREY, (x, 0), (x, HEIGHT))  # Traseaza o linie de la (x, 0) pana la (x, HEIGHT)
        for y in range(0, HEIGHT, SQUARE_SIZE):
            pg.draw.line(self.screen, LGREY, (0, y), (WIDTH, y))

    def render_sprites(self):
        """
        Afiseaza pe ecran, dupa stabilirea locatiilor, fiecare grup de sprite-uri si le actualizeaza pe cele dinamice.
        """
        self.player_group.draw(self.screen)
        self.wall_group.draw(self.screen)
        self.mob_group.draw(self.screen)
        self.treasure_group.draw(self.screen)

        self.player_group.update()
        self.mob_group.update()
        self.treasure_group.update()

    def render(self):
        """
        Render-ul final care creaza ecranul si afiseaza tot de la background pana la fiecare jucator, monstru, perete, comoara etc.
        """
        self.screen.fill(DGREY)  # Background-ul
        self.draw_grid()
        self.render_sprites()
        self.draw_text()
        pg.display.flip()  # Actualizeaza toate modificarile pe ecran (folosind double buffering)

    def events(self):
        """
        Event handling-ul jocului care stabileste ce se intampla de fiecare data cand este apasat un anumit buton, etc.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:  # Opreste jocul cand este apasat butonul de exit
                self.quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()  # Opreste jocul cand este apasat butonul ESC
                if event.key == pg.K_LEFT:
                    self.player.move(dx=-1)  # Deplaseaza jucatorul cu o patratica la stanga
                if event.key == pg.K_RIGHT:
                    self.player.move(dx=1)  # Deplaseaza jucatorul cu o patratica la dreapta
                if event.key == pg.K_UP:
                    self.player.move(dy=-1)  # Deplaseaza jucatorul cu o patratica in sus
                if event.key == pg.K_DOWN:
                    self.player.move(dy=1)  # Deplaseaza jucatorul cu o patratica in jos

                if event.key == pg.K_e:  # Schimba directia in care jucatorul se uita spre stanga
                    self.score -= 1
                    self.player.image = pg.transform.rotate(self.player.image, 90)
                    if self.orientation == 1:
                        self.orientation = 4
                    else:
                        self.orientation -= 1

                if event.key == pg.K_r:  # Schimba directia in care jucatorul se uita spre dreapta
                    self.score -= 1
                    self.player.image = pg.transform.rotate(self.player.image, -90)
                    if self.orientation == 4:
                        self.orientation = 1
                    else:
                        self.orientation += 1

                if event.key == pg.K_f:
                    self.shoot()

    def check_wall_square(self, x, y):
        """
        Verifica daca la coordonatele introduse se afla perete.
        """
        for wall in self.wall_group:
            if wall.x == x and wall.y == y:
                return True
        return False

    def check_mob_square(self, x, y):
        """
        Verifica daca la coordonatele introduse se afla un monstru.
        """
        for mob in self.mob_group:
            if mob.x == x and mob.y == y:
                return True
        return False
