import pygame.freetype
import sys
from grid import Grid
import pygame
import time


def setup():
    pygame.init()

    cols = 10
    rows = 15
    cell_size = 64  # the width and height of the cells' img

    size = (cols * cell_size, rows * cell_size)
    screen = pygame.display.set_mode(size)
    font = pygame.freetype.SysFont("comicsansms", 17)
    grid = Grid(cols, rows, cell_size, screen)  # create the grid

    return size, screen, font, grid


def main():
    while (True):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                sys.exit()

        screen.fill((0, 0, 0))  # fill the screen black

        grid.calc_cells_neighbors()
        grid.draw_cells(screen, font)
        grid.update_cells()

        pygame.display.flip()  # display this frame
        time.sleep(0.2)


size, screen, font, grid = setup()
main()
