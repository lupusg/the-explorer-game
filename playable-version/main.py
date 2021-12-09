import time

from src.game import *


# Controale
# E - Rotire spre stanga
# R - Rotire spre dreapta
# F - Foc
# Sageti - Miscare
# ESC - Iesire joc

if __name__ == '__main__':
    g = Game()

    start_time = int(time.time())
    while True:
        g.events()
        g.start_screen()
        if int(time.time()) - start_time > 3:
            break

    g.draw_walls()
    g.draw_mobs()
    g.draw_treasures()
    g.run()
