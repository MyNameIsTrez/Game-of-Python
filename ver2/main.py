"""
Game of Python - Game of Life implementation written in Python by MyNameIsTrez.

Controls:
  escape - exits the program
  f - fullscreen
  d - draw the debug info
  n - draw the neighbor counts

You can temporarily get rid of most of the false alerts in your IDE
by adding this in your settings.json file, inside of the curly brackets:
  "python.linting.pylintArgs": [
    "--extension-pkg-whitelist=pygame",
  ]
"""

import sys
import time

import pygame.freetype
import pygame

from grid import Grid


def setup():
    """placeholder"""
    # CUSTOM VALUES
    fullscreen = False
    update_interval = 0
    draw_debug_info = True
    draw_neighbor_count = False
    font_type = "arial"
    debug_font_size = 30
    neighbor_font_size = 10

    cols = 100
    rows = 100
    cell_size = 10

    # INITIALIZATION
    pygame.init()

    info_object = pygame.display.Info()
    screen_width, screen_height = info_object.current_w, info_object.current_h
    size = (min(cols * cell_size, screen_width),
            min(rows * cell_size, screen_height))

    screen = pygame.display.set_mode(
        size, pygame.FULLSCREEN if fullscreen else 0)
    font_debug = pygame.freetype.SysFont(font_type, debug_font_size)
    font_neighbor = pygame.freetype.SysFont(font_type, neighbor_font_size)
    grid = Grid(cols, rows, cell_size, font_neighbor,
                screen)  # create the grid
    grid.create_cells()
    grid.create_cell_neighbors()

    return screen, grid, update_interval, draw_debug_info, draw_neighbor_count, size, font_debug


def main():
    """placeholder"""
    first_start_time = time.time()
    screen, grid, update_interval, draw_debug_info, draw_neighbor_count, size, font_debug = setup()

    grid.create_update_list()

    grid.draw_cells()

    draw_debug(draw_debug_info, draw_neighbor_count, first_start_time,
               update_interval, grid, font_debug, screen)

    pygame.display.flip()
    time.sleep(update_interval)

    grid.create_update_list()  # necessary for the while loop

    running = True
    while running:
        start_time = time.time()

        # check for keypresses and pressing the close button on the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # set running to False to exit the while loop,
                    # after which the program will quit.
                    # this is the recommended way of quitting a program,
                    # according to the Pygame documentation.
                    running = False
                elif event.key == pygame.K_f:
                    if screen.get_flags() & pygame.FULLSCREEN:
                        pygame.display.set_mode(size)
                    else:
                        pygame.display.set_mode(size, pygame.FULLSCREEN)
                elif event.key == pygame.K_d:
                    draw_debug_info = not draw_debug_info
                elif event.key == pygame.K_n:
                    draw_neighbor_count = not draw_neighbor_count

        screen.fill((0, 0, 0))  # make the screen black

        grid_stuff(grid)

        draw_debug(draw_debug_info, draw_neighbor_count, start_time,
                   update_interval, grid, font_debug, screen)

        pygame.display.flip()  # draw this frame
        time.sleep(update_interval)


def grid_stuff(grid):
    """functions that have to do with the grid"""
    grid.update_from_update_list()
    grid.draw_cells()
    grid.create_update_list()


def draw_debug(draw_debug_info, draw_neighbor_count,
               start_time, update_interval, grid, font_debug, screen):
    """code that has to do with drawing stats that can help with debugging"""
    if draw_neighbor_count:
        grid.draw_neighbor_count()

    if draw_debug_info:
        pos = (25, 25)
        time_elapsed = (time.time() - start_time)

        font_debug.render_to(screen, pos, str(round(time_elapsed, 3)) + " sec/" +
                             str(update_interval) + " sec to calculate this frame", (150, 150, 255))


main()
