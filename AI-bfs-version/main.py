from src.game import *

# O scurta descriere
# Am implementat o cautare in adancime pe un graf de tip grid (o explicatie mai in detaliu in src/game.py la linia 195)
# avand totodata si o lista cu nodurile pe care le marchez ca fiind monstrii si o lista cu nodurile comori.
# Parcurgand graful in latime daca am intalnit un nod monstru il marcam ca nod final, daca gasim un nod comoara
# actualizam scorul, marcam nodul ca ne fiind comoara in continuare si continuam parcurgerea.

if __name__ == '__main__':
    g = Game()
    g.generate_monsters()
    g.generate_treasures()
    g.breadth_first_search(0)
    g.draw_grid()

    print(f'\nGraficul grid de {HEIGHT // SQUARE_SIZE}x{WIDTH // SQUARE_SIZE}:\n')
    print_grid_graph(HEIGHT // SQUARE_SIZE, WIDTH // SQUARE_SIZE)
    print('\n')

    g.run()
