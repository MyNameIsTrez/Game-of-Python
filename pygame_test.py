import sys

import pygame
import pygame.freetype

from grid import Grid


def setup():
    pygame.init()
    cols = 15
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

        screen.fill((0, 0, 0))  # fill screen black

        grid.draw_cells()

        # font.render_to(  # display text
        #     screen,
        #     (30, 30),
        #     "Sample text",
        #     (255, 255, 255)
        # )

        pygame.display.flip()  # display this frame


size, screen, font, grid = setup()
main()
