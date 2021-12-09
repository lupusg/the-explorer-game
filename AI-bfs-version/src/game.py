import math
import random
import sys

import numpy as np

from src.mob import Mob
from src.path import Path
from src.player import Player
from src.settings import *
import pygame as pg

from src.treasure import Treasure


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Exploratorul')
        pg.font.init()  # Initializeaza modulul de font pentru a putea scrie pe ecran
        self.font = pg.font.SysFont('Arial', 24)  # Seteaza fontul 'Arial' cu marimea de 24.
        self.wall_group = pg.sprite.Group()  # Grupeaza toate sprite-urile pe care le folosim ca pereti
        self.mob_group = pg.sprite.Group()  # Grupeaza toate sprite-urile pe care le folosim ca monstriii
        self.treasure_group = pg.sprite.Group()  # Grupeaza toate sprite-urile pe care le folosim ca si comori
        # Adauga jucatorul intr-un grup, nu era necesar deoarece nu avem mai multi, dar pentru a evita adaugarea lui
        # manuala il vom grupa.
        self.player_group = pg.sprite.Group()
        self.score = 0
        self.rows = HEIGHT // SQUARE_SIZE  # Numarul de linii din matrice
        self.cols = WIDTH // SQUARE_SIZE  # Numarul de coloane din matrice
        self.monsters_arr = np.zeros(self.rows * self.cols, int)  # Lista cu nodurile care vor fi monstrii
        self.treasure_arr = np.zeros(self.rows * self.cols, int)  # Lista cu nodurile care vor fi comori
        self.ga_matrix = np.zeros(
            (self.rows * self.cols, self.rows * self.cols))  # Matricea de adiacenta a celor rows*col noduri
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))  # Seteaza dimensiunea ferestrei
        self.clock = pg.time.Clock().tick(FPS)  # Seteaza rata de refresh a jocului (FPS)
        # Genereaza matricea de adiacenta a celor rows*cols noduri, matrice ce are un anumit pattern fiind vorba
        # despre un graf 'grid'
        create_grid_graph(self.ga_matrix, self.rows, self.cols)
        Player(self, 0, 0)  # Genereaza jucatorul pe harta la pozitia 0 0

    def breadth_first_search(self, start=0):
        vizited = [False] * self.rows * self.cols  # Marcam toate nodurile initial nevizitate
        parent = [-1] * self.rows * self.cols  # Initializam lista de parinti cu -1 initial
        queue = [start]  # Adaugam nodul de start in queue
        vizited[start] = True  # Vizitam nodul de start
        # Pastram ultima comoara gasita pentru a putea realua cautarea atunci cand gasim o noua comoara pentru a crea
        # drumul intre cele 2
        last_treasure = start

        while queue:
            if self.check_monsters(queue[0]):  # Verifica daca nodul este monstru, daca da il scoate din lista
                queue.pop(0)
            else:
                if self.check_treasure(queue[0]):  # Verifica daca nodul este comoara, daca da
                    # Prima data creaza drumul intre nodul de start si prima comoara gasita, apoi actualizand ultima
                    # comoara gasita creaza drum intre ea si comoara gasita actual
                    self.create_path(last_treasure, queue[0], parent)
                    last_treasure = queue[0]
                    self.score += 100  # Actualizeaza scorul
                    self.treasure_arr[last_treasure] = 0  # Excludem nodul ca fiind comoara in continuare
                    # Apelam recursiv cautarea in adancime pentru a gasi o noua comoara de la comoara actuala.
                    self.breadth_first_search(last_treasure)

                current_node = queue.pop(0)  # Retinem primul nod din lista si il scoatem din lista

                for node in range(self.rows * self.cols):  # Pentru fiecare nod
                    # Verificam daca este ascendent si nevizitat
                    if self.ga_matrix[node][current_node] and not vizited[node]:
                        vizited[node] = True  # Daca am gasit un nod ascendent il vizitatam
                        parent[node] = current_node  # Parintele nodului gasit este nodul curent
                        # queue.insert(0, node)  # Adaugam nodul in lista la inceput DFS
                        queue.append(node)  # Adaugam nodul in lista la final BFS

    def draw_text(self):
        # Afiseaza punctele in partea din dreapta sus a ferestrei
        text = self.font.render('Points: ' + str(self.score), True, WHITE)
        self.screen.blit(text, (WIDTH - 140, 0))

    def check_monsters(self, node):  # Verifica daca nodul este monstru, returnand 0 sau 1
        return self.monsters_arr[node]

    def check_treasure(self, node):  # Verifica daca nodul este comoara, returnand 0 sau 1
        return self.treasure_arr[node]

    def generate_monsters(self):
        """
        Genereaza MOB_NUMBER fara ca vreun monstru sa se suprapuna.
        """
        mobs_number = MOBS_NUMBER
        while mobs_number:
            # Genereaza un numar random intre 0 si rows*cols
            x = math.floor(random.random() * self.rows * self.cols)
            # Daca nodul curent nu este deja un monstru si nodul curent nu este cumva cel de start (0)
            if not self.monsters_arr[x] and x:
                # Genereaza un monstru pentru nodul X care se afla pe linia X % COLS si pe coloana X // COLS
                Mob(self, x % self.cols, x // self.cols)
                self.monsters_arr[x] = 1  # Marcheaza nodul ca fiind monstru
                mobs_number -= 1
                print(f'A fost generat un monstru pe nodul {x} pe pozitia {x % self.cols} {x // self.cols}')

    def generate_treasures(self):
        treasure_number = TREASURES_NUMBER
        while treasure_number:
            # Genereaza un numar random intre 0 si rows*cols
            x = math.floor(random.random() * self.rows * self.cols)
            # Daca nodul curent nu este deja un monstru si o comoara
            if not self.treasure_arr[x] and not self.monsters_arr[x]:
                # Genereaza o comoara pentru nodul X care se afla pe linia X % COLS si pe coloana X // COLS
                Treasure(self, x % self.cols, x // self.cols)
                self.treasure_arr[x] = 1  # Marcheaza nodul ca fiind comoara
                treasure_number -= 1
                print(f'A fost generata o comoara pe nodul {x} pe pozitia {x % self.cols} {x // self.cols}')

    def create_path(self, start, stop, parent):
        """
        Creaza drumul dintre doua noduri folosindu-se de lista de parinti.
        :param start: Nodul de start
        :param stop:  Nodul de stop
        :param parent:  Lista de parinti
        """
        solution = []
        current_node = stop

        solution.append(current_node)

        while current_node != start:
            current_node = parent[current_node]
            solution.append(current_node)

        print("\nPATH: ")
        for nod in solution:
            print(f'Nod: {nod} Pozitii: {nod // self.cols} si {nod % self.cols}', end='\n')
            # Pentru fiecare nod din lista de noduri care alcatuiesc drumul genereaza pe ecran pentru cate o patratica
            # in fiecare nod, alcatuind astfel drumul de la explorator la comoara.
            Path(self, nod % self.cols, nod // self.cols)
            self.score -= 1  # Actualizeaza scorul aferent

    def run(self):
        """
        Main loop-ul jocului.
        """
        while True:
            self.events()
            self.render()

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
        Afiseaza pe ecran, dupa stabilirea locatiilor, fiecare grup de sprite-uri.
        """
        self.wall_group.draw(self.screen)
        self.player_group.draw(self.screen)
        self.treasure_group.draw(self.screen)
        self.mob_group.draw(self.screen)

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


def create_grid_graph(matrix, rows, cols):
    """
    Genereaza matricea de adiacenta a unui graf grid in care fiecare nod se leaga de cel de sus, stanga, dreapta si jos
    depinzand de pozitionarea acestuia (in mijloc sau pe margine)
    Spre exemplu, matricea de adiacenta a unui graf cu 3x4 noduri (3 linii si 4 coloane de noduri) este:
        0  1  2  3  4  5  6  7  8  9  10  11
      0  .  1  .  .  1  .  .  .  .  .  .  .
      1  1  .  1  .  .  1  .  .  .  .  .  .
      2  .  1  .  1  .  .  1  .  .  .  .  .
      3  .  .  1  .  .  .  .  1  .  .  .  .
      4  1  .  .  .  .  1  .  .  1  .  .  .
      5  .  1  .  .  1  .  1  .  .  1  .  .
      6  .  .  1  .  .  1  .  1  .  .  1  .
      7  .  .  .  1  .  .  1  .  .  .  .  1
      8  .  .  .  .  1  .  .  .  .  1  .  .
      9  .  .  .  .  .  1  .  .  1  .  1  .
     10  .  .  .  .  .  .  1  .  .  1  .  1
     11  .  .  .  .  .  .  .  1  .  .  1  .
     Si graficul arata asa:
          0   1   2   3
          4   5   6   7
          8   9   10  11
    Unde putem observa ca nodul 0 se lega de 4 si de 1;
    nodul 1 se leaga de 0, 5 si 2
    nodul 5 se leaga de 1, 4, 9, 6
    ...
    :param matrix: Matricea de adiacenta
    :param rows: Numarul de linii
    :param cols: Numarul de coloane
    """
    for rowIdx in range(rows):
        for colIdx in range(cols):
            p = rowIdx * cols + colIdx

            if colIdx > 0:
                matrix[p - 1][p] = matrix[p][p - 1] = 1

            if rowIdx > 0:
                matrix[p - cols][p] = matrix[p][p - cols] = 1


def print_grid_graph(rows, cols):
    """
    Afiseaza g
    :param rows: Numarul de linii
    :param cols: Numarul de coloane
    """

    matrix = np.zeros([rows, cols], int)
    val = 0
    for i in range(rows):
        for j in range(cols):
            matrix[i][j] = val
            val += 1

    for i in range(rows):
        for j in range(cols):
            print('{:>4d}'.format(matrix[i][j]), end='')
        print('\n', end='')
