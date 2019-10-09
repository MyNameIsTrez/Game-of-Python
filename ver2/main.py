"""Game of Python - Game of Life in Python

You can temporarily get rid of most of the false alerts in your IDE
by adding this in your settings.json file, inside of the curly brackets:

"python.linting.pylintArgs": [
  "--extension-pkg-whitelist=pygame",
  "--disable=C0111"
]
"""

import sys
import time
import math

import pygame.freetype
import pygame

from grid import Grid


def setup():
    # CUSTOM VALUES
    fullscreen = True
    update_interval = 0.3
    draw_debug_info = True
    font_type = "arial"
    font_size = 30

    cols = 10
    rows = 10
    cell_size = 50

    # INITIALIZATION
    pygame.init()

    info_object = pygame.display.Info()
    screen_width, screen_height = info_object.current_w, info_object.current_h
    size = (min(cols * cell_size, screen_width),
            min(rows * cell_size, screen_height))

    screen = pygame.display.set_mode(
        size, pygame.FULLSCREEN if fullscreen else 0)
    font = pygame.freetype.SysFont(font_type, font_size)
    grid = Grid(cols, rows, cell_size, font, screen)  # create the grid
    grid.create_cells(cell_size)
    grid.create_cell_neighbors(cell_size)

    return screen, grid, update_interval, draw_debug_info, size, font


def main():
    first_start_time = time.time()
    screen, grid, update_interval, draw_debug_info, size, font = setup()

    grid.create_update_list()

    grid.draw_cells()

    draw_debug(draw_debug_info, first_start_time,
               update_interval, grid, font, screen)

    pygame.display.flip()
    time.sleep(update_interval)

    grid.create_update_list()  # necessary for the while loop

    running = True
    while (running):
        start_time = time.time()

        # check for keypresses and pressing the close button on the program
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                sys.exit()
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    # set running to False to exit the while loop, after which the program will quit.
                    # this is the recommended way of quitting a program, according to the Pygame documentation.
                    running = False
                elif (event.key == pygame.K_f):
                    if screen.get_flags() & pygame.FULLSCREEN:
                        pygame.display.set_mode(size)
                    else:
                        pygame.display.set_mode(size, pygame.FULLSCREEN)
                elif(event.key == pygame.K_d):
                    draw_debug_info = not draw_debug_info

        screen.fill((0, 0, 0))  # make the screen black

        grid_stuff(grid)

        draw_debug(draw_debug_info, start_time,
                   update_interval, grid, font, screen)

        pygame.display.flip()  # draw this frame
        time.sleep(update_interval)


def grid_stuff(grid):
    grid.update_from_update_list()
    grid.draw_cells()
    grid.create_update_list()


def draw_debug(draw_debug_info, start_time, update_interval, grid, font, screen):
    if (draw_debug_info):
        grid.draw_neighbor_count()

        pos = (25, 25)
        time_elapsed = (time.time() - start_time)

        font.render_to(screen, pos, str(round(time_elapsed, 3)) + " sec/" +
                       str(update_interval) + " sec to calculate this frame", (150, 150, 255))


main()
