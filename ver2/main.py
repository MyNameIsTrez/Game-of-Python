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
  "--extension-pkg-whitelist=pygame"  // The extension is "lxml" not "1xml"
]
"""

import sys
import time
import math

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

    cols = 500
    rows = 500
    cell_size = 2

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

    return screen, grid, update_interval, draw_debug_info, draw_neighbor_count, size, font_debug, cols, rows


def main():
    """placeholder"""
    first_start_time = time.time()
    screen, grid, update_interval, draw_debug_info, draw_neighbor_count, size, font_debug, cols, rows = setup()

    grid.create_update_list()

    grid.draw_cells()

    draw_debug(draw_debug_info, draw_neighbor_count, first_start_time,
               update_interval, size, cols, rows, grid, font_debug, screen)

    pygame.display.flip()
    time.sleep(update_interval)

    grid.create_update_list()  # necessary for the while loop

    running = True
    while running:
        start_time = time.time()

        running, draw_debug_info, draw_neighbor_count = get_inputs(
            screen, size, running, draw_debug_info, draw_neighbor_count)

        screen.fill((50, 50, 50))  # make the screen gray

        grid_stuff(grid)

        draw_debug(draw_debug_info, draw_neighbor_count,
                   start_time, update_interval, size, cols, rows, grid, font_debug, screen)

        pygame.display.flip()  # draw this frame

        sleep(update_interval, start_time)

def get_inputs(screen, size, running, draw_debug_info, draw_neighbor_count):
    """placeholder"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed() # to register multiple keys held down
            # exit the program
            if event.key == pygame.K_ESCAPE:
                running = False # sets running to False to exit the while loop
            # toggle fullscreen
            if event.key == pygame.K_f:
                if screen.get_flags() & pygame.FULLSCREEN:
                    pygame.display.set_mode(size)
                else:
                    pygame.display.set_mode(size, pygame.FULLSCREEN)
            # what debug info to draw
            if keys[pygame.K_d]:
                if keys[pygame.K_1]:
                    draw_debug_info = not draw_debug_info
                if keys[pygame.K_2]:
                    draw_neighbor_count = not draw_neighbor_count
    return running, draw_debug_info, draw_neighbor_count


def grid_stuff(grid):
    """functions that have to do with the grid"""
    grid.update_from_update_list()
    grid.draw_cells()
    grid.create_update_list()


def draw_debug(draw_debug_info, draw_neighbor_count,
               start_time, update_interval, size, cols, rows, grid, font_debug, screen):
    """code that has to do with drawing stats that can help with debugging"""
    if draw_neighbor_count:
        grid.draw_neighbor_count()

    if draw_debug_info:
        text = []

        partial_time_elapsed = time.time() - start_time

        # ms taken from max ms
        string = str(math.floor(partial_time_elapsed * 1000))
        if (update_interval != 0):
            string += "/" + str(math.floor(update_interval * 1000)) + " ms"
        else:
            string += " ms"
        string += " to calculate this frame"
        text.append(string)

        # potential_speed_multiplier
        potential_speed_multiplier = round(update_interval / partial_time_elapsed, 1)
        if update_interval != 0:
            text.append("the program can run at " +
                        str(potential_speed_multiplier) + "x the current speed")
        else:
            text.append("the program is running as fast as it can!")
        
        # grid size
        text.append("grid size: " + str(cols) + "x" + str(rows))
        
        # resolution
        text.append("resolution: " + str(size[0]) + "x" + str(size[1]))

        for i, val in enumerate(text):
            pos = (25, 25 + 40 * i)
            font_debug.render_to(screen, pos, val, (150, 150, 255))


def sleep(update_interval, start_time):
    """placeholder"""
    final_time_elapsed = time.time() - start_time
    sleep_time = max(update_interval - final_time_elapsed, 0)
    time.sleep(sleep_time)


main()
