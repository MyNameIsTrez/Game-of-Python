import pygame.freetype
import pygame
import sys
import time

from grid import Grid


def setup():
    pygame.init()

    cols = 10
    rows = 8
    cell_size = 64  # the width and height of the cells' img

    size = (cols * cell_size, rows * cell_size)
    screen = pygame.display.set_mode(size)
    font = pygame.freetype.SysFont("comicsansms", 17)
    grid = Grid(cols, rows, cell_size, screen)  # create the grid

    return screen, font, grid


def main():
    while (True):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                sys.exit()

        screen.fill((0, 0, 0))  # make the screen black

        grid.calc_neighbors()
        grid.draw_cells(screen, font)
        grid.update_cells()

        pygame.display.flip()  # display this frame
        time.sleep(0.2)


screen, font, grid = setup()
main()
