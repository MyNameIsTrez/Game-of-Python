import pygame.freetype
import pygame
import sys
import time

from grid import Grid


def setup():
    pygame.init()

    cols = 30
    rows = 16
    cell_size = 64  # the width and height of the cells' img

    size = (cols * cell_size, rows * cell_size)
    screen = pygame.display.set_mode(size)
    font = pygame.freetype.SysFont("comicsansms", 17)
    grid = Grid(cols, rows, cell_size, font, screen)  # create the grid
    grid.create_cells(cell_size)
    grid.create_cell_neighbors(cell_size)
    update_interval = 0.1

    return screen, grid, update_interval


def main():
    screen, grid, update_interval = setup()

    grid.create_update_list()

#     grid.draw_cell_updates()
    grid.draw_cells()
    grid.draw_neighbor_count()

    pygame.display.flip()
    time.sleep(update_interval)

    while (True):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                sys.exit()

        screen.fill((0, 0, 0))  # make the screen black

        grid.create_update_list()

        grid.update_from_update_list()
        # grid.draw_cell_updates()
        grid.draw_cells()
        grid.draw_neighbor_count()

        pygame.display.flip()  # display this frame
        time.sleep(update_interval)


main()
